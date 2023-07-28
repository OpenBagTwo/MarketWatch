"""Script to generate a new post"""
import datetime as dt
import json
import os
import random
from pathlib import Path
from typing import TypedDict

import pandas as pd
import requests
import yfinance as yf

AUTHOR = "MarketBot"

TICKERS: dict[str, str] = {
    # description, symbol
    "NASDAQ": "^IXIC",
    "Dow": "^DJI",
    "S&P 500": "^GSPC",
    "Nikkei": "^N225",
    "FTSE": "^FTSE",
    "Capital One Stock": "COF",
}

UPS: list[str] = [
    "soars",
    "skyrockets",
    "captapults",
    "zooms",
    "jumps",
    "shoots up",
]

DOWNS: list[str] = [
    "plummets",
    "tanks",
    "in free fall",
    "dives",
    "plunges",
    "scrambling",
]


EXCLUDED_SECTIONS: list[str] = [
    "About",
    "Better Business",
    "Business",
    "Business to business",
    "Opinion",
    "Community",
    "Crosswords",
    "Global development",
    "Help",
    "Inequality",
    "Info",
    "Jobs",
    "Membership",
    "Money",
    "News",
    "Politics",
    "Search",
    "From the Guardian",
    "From the Observer",
    "Guardian holiday offers",
    "World news",
]


def _clean_headline(headline: str) -> str:
    """Get to the relevant "sound byte" of a headline"""
    return headline.split("–")[0].split(":")[-1].split(";")[0].split("|")[0].strip()


def get_market_movement(ticker: str, date: dt.date) -> bool:
    """Ping Yahoo Finance and determine whether the
    given ticker closed higher or lower than it opened
    on the specified date.

    Parameters
    ----------
    ticker: str
        The symbol of the stock or index to query

    date : date
        The date to query

    Returns
    -------
    bool
        True if the stock closed higher than it opened, False otherwise.
    """
    stonk = (
        yf.Ticker(ticker)
        .history(period="1d", start=date, end=date + dt.timedelta(days=1))
        .reset_index()
    )
    return stonk.at[0, "Close"] > stonk.at[0, "Open"]


class _Article(TypedDict):
    """Everything important we're extracting from an article"""

    headline: str
    lede: str
    url: str
    tags: list[str]


def get_random_article(api_key: str, date: dt.date) -> _Article:
    """Grab a bunch of random articles from The Guardian
    from a given date and select one to use as the basis
    of this post

    Parameters
    ----------
    api_key : str
        An access key for The Guardian's API
    date : date
        The date to query

    Returns
    -------
    dict
        The relevant parts of the article
    """

    response = requests.get(
        "https://content.guardianapis.com/search",
        params={
            "api-key": api_key,
            "from-date": date.isoformat(),
            "to-date": (date + dt.timedelta(days=1)).isoformat(),
            "page-size": "50",
            "section": ",".join([f"-{section}" for section in EXCLUDED_SECTIONS]),
        },
    )
    if response.status_code != 200:
        raise RuntimeError(
            f"Couldn't hit The Guardian API. Recieved error code: {response.status_code}\n{response.text}"
        )

    articles = json.loads(response.text)["response"]["results"]

    response = requests.get(
        random.choice(articles)["apiUrl"],
        params={
            "api-key": api_key,
            "show-fields": ["body"],
        },
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Couldn't hit The Guardian API. Recieved error code: {response.status_code}\n{response.text}"
        )

    article = json.loads(response.text)["response"]["content"]
    return {
        "headline": _clean_headline(article["webTitle"]),
        "lede": article["fields"]["body"].split("</p>")[0].split("<p>")[-1],
        "url": article["webUrl"],
        "tags": [article["pillarName"]],
    }


def generate_post(guardian_api_key: str, date: dt.date | None = None) -> str:
    """Create a new post

    Parameters
    ----------
    guardian_api_key : str
        An access key for The Guardian's API
    date : date, optional
        The date to generate the post for. If None is given, yesterday will be used.

    Returns
    -------
    str
        Hugo-style markdown post
    """
    date = date or dt.date.today() - dt.timedelta(days=1)

    indicator, symbol = random.choice(list(TICKERS.items()))
    is_up = get_market_movement(symbol, date)

    status = random.choice(UPS if is_up else DOWNS)

    article = get_random_article(guardian_api_key, date)

    headline = " ".join([indicator, status, "as", article["headline"]])

    tags = ", ".join([f'"{tag}"' for tag in article["tags"] + [indicator, symbol]])

    return f"""---
author: {AUTHOR}
title: {headline}
summary: {article["lede"]}
image: {"up" if is_up else "down"}1.png
tags: [{tags}]
date: {date.isoformat()}
redirect_to: {article["url"]}
redirect_enabled: true
---
"""


if __name__ == "__main__":
    random.seed()

    date = dt.date.today() - dt.timedelta(days=1)
    Path(f"content/redirect/{date.isoformat()}.md").write_text(
        generate_post(os.environ["GUARDIAN_API_KEY"], date)
    )
