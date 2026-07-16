from dataclasses import dataclass
from datetime import datetime
from math import inf
from typing import Any

from app.models.ohlcv import OHLCV
from app.scanner.constants import (
    CUP_HANDLE_DEPTH_MAX,
    CUP_HANDLE_DEPTH_MIN,
    CUP_HANDLE_HANDLE_MAX_DEPTH,
    CUP_HANDLE_HANDLE_MAX_DURATION,
    CUP_HANDLE_HANDLE_MAX_RANGE,
    CUP_HANDLE_HANDLE_MIN_BARS,
    CUP_HANDLE_MIN_DURATION,
    CUP_HANDLE_MAX_DURATION,
    CUP_HANDLE_MIN_PRIOR_TREND_DAYS,
    CUP_HANDLE_MIN_PRIOR_TREND_GAIN,
    CUP_HANDLE_MAX_RIM_DIFF,
    CUP_HANDLE_PIVOT_LOOKBACK,
    CUP_HANDLE_BOTTOM_POSITION_MAX,
    CUP_HANDLE_BOTTOM_POSITION_MIN,
    CUP_HANDLE_NEAR_BOTTOM_THRESHOLD,
    CUP_HANDLE_MIN_NEAR_BOTTOM_BARS,
    CUP_HANDLE_RIGHT_RECOVERY_MIN,
    CUP_HANDLE_PIVOT_THRESHOLD,
)
from app.scanner.models.pattern_result import PatternResult, PatternType


@dataclass(slots=True)
class Pivot:
    index: int
    price: float
    type: str


@dataclass(slots=True)
class CupCandidate:
    left: Pivot
    bottom: Pivot
    right: Pivot


@dataclass(slots=True)
class HandleSegment:
    start_index: int
    end_index: int
    depth: float
    range_ratio: float
    max_high: float
    min_low: float


def _to_float(value: Any) -> float:
    return float(value)


def detect_pivots(
    candles: list[OHLCV],
    lookback: int = CUP_HANDLE_PIVOT_LOOKBACK,
) -> list[Pivot]:
    if len(candles) < lookback * 2 + 1:
        return []

    highs = [_to_float(c.high) for c in candles]
    lows = [_to_float(c.low) for c in candles]
    pivots: list[Pivot] = []

    for index in range(lookback, len(candles) - lookback):
        window_highs = highs[index - lookback: index + lookback + 1]
        window_lows = lows[index - lookback: index + lookback + 1]
        current_high = highs[index]
        current_low = lows[index]

        if (
            current_high == max(window_highs)
            and window_highs.count(current_high) == 1
            and current_high >= max(
                window_highs[:lookback] + window_highs[lookback + 1:],
                default=current_high,
            )
            * (1 + CUP_HANDLE_PIVOT_THRESHOLD)
        ):
            pivots.append(Pivot(index=index, price=current_high, type="high"))

        if (
            current_low == min(window_lows)
            and window_lows.count(current_low) == 1
            and current_low <= min(
                window_lows[:lookback] + window_lows[lookback + 1:],
                default=current_low,
            )
            * (1 - CUP_HANDLE_PIVOT_THRESHOLD)
        ):
            pivots.append(Pivot(index=index, price=current_low, type="low"))

    return sorted(pivots, key=lambda pivot: pivot.index)


def generate_cup_candidates(
    candles: list[OHLCV],
    pivots: list[Pivot],
) -> list[CupCandidate]:
    highs = [pivot for pivot in pivots if pivot.type == "high"]
    lows = [pivot for pivot in pivots if pivot.type == "low"]
    candidates: list[CupCandidate] = []

    for bottom in lows:
        left_rims = [pivot for pivot in highs if pivot.index < bottom.index]
        right_rims = [pivot for pivot in highs if pivot.index > bottom.index]

        if not left_rims or not right_rims:
            continue

        for left in left_rims[-3:]:
            for right in right_rims[:3]:
                duration = right.index - left.index

                if duration < CUP_HANDLE_MIN_DURATION:
                    continue

                if duration > CUP_HANDLE_MAX_DURATION:
                    continue

                if left.price <= bottom.price or right.price <= bottom.price:
                    continue

                rim_gap = abs(left.price - right.price) / left.price
                if rim_gap > 0.30:
                    continue

                candidates.append(
                    CupCandidate(
                        left=left,
                        bottom=bottom,
                        right=right,
                    )
                )

    return candidates


def _prior_trend_strength(
    candles: list[OHLCV],
    candidate: CupCandidate,
) -> float:
    left_index = candidate.left.index
    start_index = max(0, left_index - CUP_HANDLE_MIN_PRIOR_TREND_DAYS)
    prior_close = _to_float(candles[start_index].close)
    left_close = _to_float(candles[left_index].close)

    if prior_close <= 0:
        return 0.0

    return (left_close / prior_close) - 1.0


def _cup_depth(candidate: CupCandidate) -> float:
    return (candidate.left.price - candidate.bottom.price) / candidate.left.price


def _rim_similarity(candidate: CupCandidate) -> float:
    return abs(candidate.right.price - candidate.left.price) / candidate.left.price


def _bottom_position(candidate: CupCandidate) -> float:
    duration = candidate.right.index - candidate.left.index
    if duration <= 0:
        return 0.0
    return (candidate.bottom.index - candidate.left.index) / duration


def _roundness_score(
    candles: list[OHLCV],
    candidate: CupCandidate,
) -> float:
    left_index = candidate.left.index
    right_index = candidate.right.index
    bottom_price = candidate.bottom.price
    threshold = bottom_price * (1 + CUP_HANDLE_NEAR_BOTTOM_THRESHOLD)
    trough_count = 0

    for index in range(left_index, right_index + 1):
        if _to_float(candles[index].low) <= threshold:
            trough_count += 1

    width = right_index - left_index + 1
    if width <= 0:
        return 0.0

    return min(1.0, trough_count / max(width * 0.15, CUP_HANDLE_MIN_NEAR_BOTTOM_BARS))


def _is_v_shaped(
    candles: list[OHLCV],
    candidate: CupCandidate,
) -> bool:
    left_pressure = candidate.bottom.index - candidate.left.index
    right_pressure = candidate.right.index - candidate.bottom.index

    if left_pressure <= 0 or right_pressure <= 0:
        return True

    left_slope = (candidate.left.price - candidate.bottom.price) / left_pressure
    right_slope = (candidate.right.price - candidate.bottom.price) / right_pressure

    ratio = max(left_slope, right_slope) / min(left_slope, right_slope)
    return ratio > 3.0


def validate_cup(
    candles: list[OHLCV],
    candidate: CupCandidate,
) -> dict[str, float] | None:
    if len(candles) < candidate.right.index + 1:
        return None

    prior_strength = _prior_trend_strength(candles, candidate)
    if prior_strength < CUP_HANDLE_MIN_PRIOR_TREND_GAIN:
        return None

    depth = _cup_depth(candidate)
    if depth < CUP_HANDLE_DEPTH_MIN or depth > CUP_HANDLE_DEPTH_MAX:
        return None

    position = _bottom_position(candidate)
    if position < CUP_HANDLE_BOTTOM_POSITION_MIN or position > CUP_HANDLE_BOTTOM_POSITION_MAX:
        return None

    rim_similarity = _rim_similarity(candidate)
    if rim_similarity > CUP_HANDLE_MAX_RIM_DIFF:
        return None

    right_recovery = candidate.right.price / candidate.left.price
    if right_recovery < CUP_HANDLE_RIGHT_RECOVERY_MIN:
        return None

    if _is_v_shaped(candles, candidate):
        return None

    roundness = _roundness_score(candles, candidate)
    if roundness < 0.25:
        return None

    return {
        "prior_strength": prior_strength,
        "depth": depth,
        "duration": float(candidate.right.index - candidate.left.index),
        "rim_similarity": rim_similarity,
        "roundness": roundness,
        "right_recovery": right_recovery,
    }


def _handle_upper_half_threshold(
    candles: list[OHLCV],
    candidate: CupCandidate,
) -> float:
    cup_top = min(candidate.left.price, candidate.right.price)
    return candidate.bottom.price + (cup_top - candidate.bottom.price) * 0.5


def detect_handle(
    candles: list[OHLCV],
    candidate: CupCandidate,
) -> HandleSegment | None:
    start_index = candidate.right.index + 1
    if start_index + CUP_HANDLE_HANDLE_MIN_BARS >= len(candles):
        return None

    upper_half_threshold = _handle_upper_half_threshold(candles, candidate)
    best_segment: HandleSegment | None = None

    for end_index in range(
        start_index + CUP_HANDLE_HANDLE_MIN_BARS - 1,
        min(len(candles), start_index + CUP_HANDLE_HANDLE_MAX_DURATION),
    ):
        segment = candles[start_index:end_index + 1]
        highs = [_to_float(c.high) for c in segment]
        lows = [_to_float(c.low) for c in segment]
        closes = [_to_float(c.close) for c in segment]

        segment_high = max(highs)
        segment_low = min(lows)
        if segment_high <= 0:
            continue

        if segment_high >= candidate.right.price * 1.02:
            break

        if max(closes) < upper_half_threshold:
            continue

        depth = (segment_high - segment_low) / segment_high
        range_ratio = (segment_high - segment_low) / segment_high
        if depth > CUP_HANDLE_HANDLE_MAX_DEPTH:
            continue

        if range_ratio > CUP_HANDLE_HANDLE_MAX_RANGE:
            continue

        if best_segment is None or depth < best_segment.depth:
            best_segment = HandleSegment(
                start_index=start_index,
                end_index=end_index,
                depth=depth,
                range_ratio=range_ratio,
                max_high=segment_high,
                min_low=segment_low,
            )

    return best_segment


def _score_cup_handle(
    cup_metrics: dict[str, float],
    handle: HandleSegment,
) -> int:
    prior_score = min(max((cup_metrics["prior_strength"] - CUP_HANDLE_MIN_PRIOR_TREND_GAIN) / 0.20, 0.0), 1.0) * 20
    depth_score = min(max((cup_metrics["depth"] - CUP_HANDLE_DEPTH_MIN) / (CUP_HANDLE_DEPTH_MAX - CUP_HANDLE_DEPTH_MIN), 0.0), 1.0) * 15
    duration_mid = (CUP_HANDLE_MIN_DURATION + CUP_HANDLE_MAX_DURATION) / 2
    duration_score = max(0.0, 1.0 - abs(cup_metrics["duration"] - duration_mid) / duration_mid) * 10
    rim_score = max(0.0, 1.0 - cup_metrics["rim_similarity"] / CUP_HANDLE_MAX_RIM_DIFF) * 15
    roundness_score = min(max(cup_metrics["roundness"], 0.0), 1.0) * 15
    recovery_score = min(max((cup_metrics["right_recovery"] - CUP_HANDLE_RIGHT_RECOVERY_MIN) / (1.0 - CUP_HANDLE_RIGHT_RECOVERY_MIN), 0.0), 1.0) * 10
    handle_score = max(0.0, 1.0 - handle.depth / CUP_HANDLE_HANDLE_MAX_DEPTH) * 15

    total = prior_score + depth_score + duration_score + rim_score + roundness_score + recovery_score + handle_score
    return min(100, int(round(total)))


def detect_cup_handle(
    candles: list[OHLCV],
) -> PatternResult | None:
    pivots = detect_pivots(candles)
    if not pivots:
        return None

    candidates = generate_cup_candidates(candles, pivots)
    best_result: PatternResult | None = None
    best_score = -inf

    for candidate in candidates:
        metrics = validate_cup(candles, candidate)
        if metrics is None:
            continue

        handle = detect_handle(candles, candidate)
        if handle is None:
            continue

        confidence = _score_cup_handle(metrics, handle)
        if confidence <= 0:
            continue

        breakout_price = candidate.right.price
        duration_mid = (CUP_HANDLE_MIN_DURATION + CUP_HANDLE_MAX_DURATION) / 2
        prior_score = min(max((metrics["prior_strength"] - CUP_HANDLE_MIN_PRIOR_TREND_GAIN) / 0.20, 0.0), 1.0) * 20
        depth_score = min(max((metrics["depth"] - CUP_HANDLE_DEPTH_MIN) / (CUP_HANDLE_DEPTH_MAX - CUP_HANDLE_DEPTH_MIN), 0.0), 1.0) * 15
        duration_score = max(0.0, 1.0 - abs(metrics["duration"] - duration_mid) / duration_mid) * 10
        rim_score = max(0.0, 1.0 - metrics["rim_similarity"] / CUP_HANDLE_MAX_RIM_DIFF) * 15
        roundness_score = min(max(metrics["roundness"], 0.0), 1.0) * 15
        recovery_score = min(max((metrics["right_recovery"] - CUP_HANDLE_RIGHT_RECOVERY_MIN) / (1.0 - CUP_HANDLE_RIGHT_RECOVERY_MIN), 0.0), 1.0) * 10
        handle_score = max(0.0, 1.0 - handle.depth / CUP_HANDLE_HANDLE_MAX_DEPTH) * 15

        metadata = {
            "cup_depth": round(metrics["depth"], 4),
            "cup_duration": int(metrics["duration"]),
            "handle_duration": handle.end_index - handle.start_index + 1,
            "handle_depth": round(handle.depth, 4),
            "recovery_percentage": round((metrics["right_recovery"] - 1.0) * 100, 2),
            "score_breakdown": {
                "prior_trend": round(prior_score, 1),
                "depth": round(depth_score, 1),
                "duration": round(duration_score, 1),
                "rim_similarity": round(rim_score, 1),
                "roundness": round(roundness_score, 1),
                "recovery": round(recovery_score, 1),
                "handle": round(handle_score, 1),
            },
            "start_timestamp": candles[candidate.left.index].timestamp,
            "end_timestamp": candles[handle.end_index].timestamp,
        }

        result = PatternResult(
            pattern_type=PatternType.CUP_HANDLE,
            confidence=confidence,
            breakout_price=breakout_price,
            start_timestamp=candles[candidate.left.index].timestamp,
            end_timestamp=candles[handle.end_index].timestamp,
            metadata=metadata,
        )

        if confidence > best_score:
            best_score = confidence
            best_result = result

    return best_result
