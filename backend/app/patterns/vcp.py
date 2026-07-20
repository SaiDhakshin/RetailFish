from datetime import datetime
from typing import Any
from dataclasses import dataclass

from app.models.ohlcv import OHLCV
from app.patterns.pivot import detect_pivots
from app.scanner.constants import (
    MIN_SEQUENCE_LENGTH,
    VCP_BREAKOUT_PROXIMITY,
    VCP_CONTRACTION_DECREASE_RATIO,
    VCP_HIGH_TIGHTENING_TOLERANCE,
    VCP_LOW_TIGHTENING_TOLERANCE,
    VCP_MAX_BREAKOUT_AGE,
    VCP_MAX_LEG_PERCENT,
    VCP_MAX_PATTERN_AGE,
    VCP_MIN_CONTRACTION_LEGS,
    VCP_MIN_LEG_PERCENT,
    VCP_MIN_PIVOT_COUNT,
    MAX_RECENT_PIVOTS,
    VCP_SEARCH_WINDOW,
    VCP_VOLUME_CONTRACTION_TOLERANCE,
)
from app.scanner.models.pattern_result import PatternResult, PatternType

@dataclass(slots=True)
class VCPCandidate:

    sequence: list

    confidence: int

    breakout_price: float

    breakout_status: str

    breakout_proximity: float

    tightening_score: float

    volume_valid: bool

    volume_ratios: list[float]

    legs: list[dict[str, Any]]

    breakout_index: int | None

    last_high: Any


def _to_float(value: Any) -> float:
    return float(value)


def _average_volume(candles: list[OHLCV], start_index: int, end_index: int) -> float:
    segment = candles[start_index:end_index + 1]
    volume_sum = sum(float(c.volume) for c in segment)
    return volume_sum / max(len(segment), 1)

def _is_alternating(sequence: list) -> bool:
    for previous, current in zip(sequence, sequence[1:]):
        if previous.type == current.type:
            return False

    return True

def _generate_vcp_candidates(
    pivots: list,
) -> list[list]:

    if len(pivots) < MIN_SEQUENCE_LENGTH:
        return []

    recent = pivots[-MAX_RECENT_PIVOTS:]

    candidates: list[list] = []

    for start in range(len(recent)):

        if recent[start].type != "high":
            continue

        sequence = [recent[start]]

        expected = "low"

        for pivot in recent[start + 1:]:

            if pivot.type != expected:
                continue

            sequence.append(pivot)

            expected = (
                "high"
                if expected == "low"
                else "low"
            )

            if (
                len(sequence) >= MIN_SEQUENCE_LENGTH
                and sequence[-1].type == "high"
            ):
                candidates.append(sequence.copy())

    return candidates



def _build_contraction_legs(selected: list) -> list[dict[str, Any]]:
    legs: list[dict[str, Any]] = []

    for index in range(len(selected) - 1):
        first = selected[index]
        second = selected[index + 1]

        if first.type == "high" and second.type == "low":
            if first.price <= 0:
                continue

            contraction = (first.price - second.price) / first.price
            legs.append(
                {
                    "high": first,
                    "low": second,
                    "contraction_pct": contraction,
                    "start_index": first.index,
                    "end_index": second.index,
                }
            )

    return legs


def _is_decreasing_contractions(legs: list[dict[str, Any]]) -> bool:
    for previous, current in zip(legs, legs[1:]):
        if current["contraction_pct"] >= previous["contraction_pct"] * VCP_CONTRACTION_DECREASE_RATIO:
            return False
    return True


def _validate_tightening(selected: list) -> tuple[bool, float]:
    highs = [pivot.price for pivot in selected if pivot.type == "high"]
    lows = [pivot.price for pivot in selected if pivot.type == "low"]

    if len(highs) < 2 or len(lows) < 2:
        return False, 0.0

    high_scores: list[float] = []
    low_scores: list[float] = []

    for previous, current in zip(highs, highs[1:]):
        if current > previous * (1.0 + VCP_HIGH_TIGHTENING_TOLERANCE):
            return False, 0.0
        deviation = max(0.0, (current / previous - 1.0))
        high_scores.append(max(0.0, 1.0 - deviation / VCP_HIGH_TIGHTENING_TOLERANCE))

    for previous, current in zip(lows, lows[1:]):
        if current < previous * (1.0 - VCP_LOW_TIGHTENING_TOLERANCE):
            return False, 0.0
        deviation = max(0.0, (previous / current - 1.0))
        low_scores.append(max(0.0, 1.0 - deviation / VCP_LOW_TIGHTENING_TOLERANCE))

    score = (sum(high_scores) + sum(low_scores)) / max(len(high_scores) + len(low_scores), 1)
    return True, score


def _volume_contraction(candles: list[OHLCV], legs: list[dict[str, Any]]) -> tuple[bool, list[float]]:
    leg_volumes = [
        _average_volume(candles, leg["start_index"], leg["end_index"])
        for leg in legs
    ]

    contraction_ratios: list[float] = []
    for previous, current in zip(leg_volumes, leg_volumes[1:]):
        contraction_ratios.append(current / previous if previous > 0 else 1.0)

    valid = all(ratio <= 1.0 + VCP_VOLUME_CONTRACTION_TOLERANCE for ratio in contraction_ratios)
    return valid, contraction_ratios


def _find_breakout_index(
    candles: list[OHLCV],
    breakout_price: float,
    start_index: int,
) -> int | None:
    for index in range(start_index, len(candles)):
        if _to_float(candles[index].close) >= breakout_price:
            return index
    return None


def _score_vcp(
    legs: list[dict[str, Any]],
    tightening_score: float,
    volume_contraction: bool,
    breakout_proximity: float,
    is_breakout: bool,
) -> int:
    leg_count_score = min(20, 10 + 5 * (len(legs) - VCP_MIN_CONTRACTION_LEGS))
    contraction_improvement = 0.0

    for previous, current in zip(legs, legs[1:]):
        if previous["contraction_pct"] > 0:
            contraction_improvement += (previous["contraction_pct"] - current["contraction_pct"]) / previous["contraction_pct"]

    contraction_score = min(20, int(round((contraction_improvement / max(len(legs) - 1, 1)) * 20)))
    tightening_score_value = min(20, int(round(tightening_score * 20)))
    volume_score = 10 if volume_contraction else 0
    breakout_score = 10 if breakout_proximity <= VCP_BREAKOUT_PROXIMITY or is_breakout else 0

    confidence = 40 + leg_count_score + contraction_score + tightening_score_value + volume_score + breakout_score
    return min(100, max(0, confidence))


def detect_vcp(candles: list[OHLCV]) -> PatternResult | None:
    if len(candles) > VCP_SEARCH_WINDOW:
        candles = candles[-VCP_SEARCH_WINDOW:]

    pivots = detect_pivots(candles)

    candidates = _generate_vcp_candidates(pivots)
    if not candidates:
        return None

    best: VCPCandidate | None = None

    for sequence in candidates:
        candidate = _evaluate_candidate(sequence, candles)

        if candidate is None:
            continue

        if best is None or candidate.confidence > best.confidence:
            best = candidate

    if best is None:
        return None

    overlay_points = [
        {
            "time": candles[pivot.index].timestamp.timestamp(),
            "value": pivot.price,
        }
        for pivot in best.sequence
    ]

    metadata = {
        "pivot_count": len(best.sequence),
        "candidate_count": len(candidates),
        "selected_candidate_length": len(best.sequence),
        "contraction_legs": len(best.legs),
        "contraction_percentages": [
            round(leg["contraction_pct"], 4)
            for leg in best.legs
        ],
        "tightening_score": round(best.tightening_score, 3),
        "volume_contraction": best.volume_valid,
        "volume_ratios": [
            round(ratio, 4)
            for ratio in best.volume_ratios
        ],
        "breakout_proximity": round(best.breakout_proximity, 4),
    }

    return PatternResult(
        pattern_type=PatternType.VCP,
        confidence=best.confidence,
        score=best.confidence,
        breakout_price=best.breakout_price,
        breakout_status=best.breakout_status,
        start_timestamp=candles[best.sequence[0].index].timestamp,
        end_timestamp=candles[-1].timestamp,
        metadata=metadata,
        overlay={
            "type": "vcp",
            "points": overlay_points,
        },
    )

def _evaluate_candidate(
    sequence: list,
    candles: list[OHLCV],
) -> VCPCandidate | None:
    print("Evaluating candidate", len(sequence))

    legs = _build_contraction_legs(sequence)

    if len(legs) < VCP_MIN_CONTRACTION_LEGS:
        print("Rejected: insufficient contraction legs")
        return None

    if any(
        leg["contraction_pct"] < VCP_MIN_LEG_PERCENT
        or leg["contraction_pct"] > VCP_MAX_LEG_PERCENT
        for leg in legs
    ):
        print(
            "Rejected: contraction %",
            [round(leg["contraction_pct"], 3) for leg in legs],
        )
        return None

    if not _is_decreasing_contractions(legs):
        print(
            "Rejected: contractions not decreasing",
            [round(leg["contraction_pct"], 3) for leg in legs],
        )
        return None

    tightening_valid, tightening_score = _validate_tightening(sequence)

    if not tightening_valid:
        print("Rejected: tightening")
        return None

    volume_valid, volume_ratios = _volume_contraction(
        candles,
        legs,
    )

    last_high = sequence[-1]

    breakout_price = last_high.price

    breakout_index = _find_breakout_index(
        candles,
        breakout_price,
        last_high.index + 1,
    )

    bars_since_breakout = None
    is_breakout = False

    if breakout_index is not None:
        bars_since_breakout = len(candles) - 1 - breakout_index

        if bars_since_breakout > VCP_MAX_BREAKOUT_AGE:
            print("Rejected: breakout too old", bars_since_breakout)
            return None

        is_breakout = True

    bars_since_completion = len(candles) - 1 - last_high.index

    if (
        not is_breakout
        and bars_since_completion > VCP_MAX_PATTERN_AGE
    ):
        print("Rejected: pattern too old", bars_since_completion)
        return None

    last_close = _to_float(candles[-1].close)

    breakout_proximity = (
        abs(last_close - breakout_price) / breakout_price
        if breakout_price > 0
        else 1.0
    )

    if is_breakout:
        breakout_status = (
            f"Breakout ({bars_since_breakout} bars ago)"
            if bars_since_breakout is not None
            else "Breakout"
        )
    elif breakout_proximity <= VCP_BREAKOUT_PROXIMITY:
        breakout_status = "Near Breakout"
    else:
        breakout_status = "Forming"

    confidence = _score_vcp(
        legs=legs,
        tightening_score=tightening_score,
        volume_contraction=volume_valid,
        breakout_proximity=breakout_proximity,
        is_breakout=is_breakout,
    )

    return VCPCandidate(
        sequence=sequence,
        confidence=confidence,
        breakout_price=breakout_price,
        breakout_status=breakout_status,
        breakout_proximity=breakout_proximity,
        tightening_score=tightening_score,
        volume_valid=volume_valid,
        volume_ratios=volume_ratios,
        legs=legs,
        breakout_index=breakout_index,
        last_high=last_high,
    )
