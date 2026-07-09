from __future__ import annotations

import io

import pandas as pd
import requests


class NSESymbolProvider:
    """
    Downloads and parses the NSE equity symbol list.
    """

    SYMBOL_URL = (
        "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
    )

    TIMEOUT = 30

    def fetch_symbols(self) -> list[str]:
        """
        Download the complete NSE symbol list.

        Returns
        -------
        list[str]
        """

        response = requests.get(
            self.SYMBOL_URL,
            timeout=self.TIMEOUT,
        )

        response.raise_for_status()

        dataframe = pd.read_csv(
            io.StringIO(response.text)
        )

        dataframe = dataframe.dropna(subset=["SYMBOL"])

        symbols = (
            dataframe["SYMBOL"]
            .astype(str)
            .str.strip()
            .str.upper()
            + ".NS"
        )

        return sorted(symbols.unique().tolist())