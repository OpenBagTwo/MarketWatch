# SMBC Market Watch

[![Generate Post](https://github.com/OpenBagTwo/MarketWatch/actions/workflows/generate_content.yaml/badge.svg)](https://github.com/OpenBagTwo/MarketWatch/actions/workflows/generate_content.yaml)

***A Meme Financial Headline Generator***


## What Is This?

I woke up one morning, and as am I am wont to do, was randomly wandering through the [SMBC](https://www.smbc-comics.com) archive
when I came across [this webcomic](https://www.smbc-comics.com/comic/markets) from 2020:

![SMBC Markets](https://www.smbc-comics.com/comics/1592665375-20200620.png)

and I thought to myself, "Hey, I bet I could code that pretty easily!"

[which is exactly what I did.](https://openbagtwo.github.io/MarketWatch/)


## How does it work?

The two components going into generating the headlines were:

- getting market data (is the market up or down on any given day?)
- getting news headlines

I figured the first would be easy and the second would be hard, but the reverse ended up being true,
as most Finance APIs I could find were either decommissioned (Google), paid (NASDAQ DataLink) or
didn't contain composite indices (Alpha Vantage). Luckily, not only is [Yahoo Finance](https://finance.yahoo.com)
still around, but there's even a well-maintained Python package called [`yfinance`](https://aroussi.com/post/python-yahoo-finance)
that I could use without even creating a developer account!

On the news side, I found [this handy list of news media APIs](https://en.wikipedia.org/wiki/List_of_news_media_APIs) and decided to go with
[The Guardian](https://open-platform.theguardian.com/). Their documentation was excellent and their API was extremely easy
to use.

If you'd like to get a deeper look at how I combined the two halves, have a look at the
[the development notebook](Development%20Notebook.ipynb)
or just jump straight into [the script that generates the posts](post_generator.py). To run
the code, you'll need an [environment](https://docs.conda.io/en/latest/) with:
- Python 3.11 or newer (if your system doesn't ship with one, I highly recommend [mambaforge](https://github.com/conda-forge/miniforge#mambaforge) across any system.
- [`yfinance`](https://pypi.org/project/yfinance/)
- [`requests`](https://pypi.org/project/requests/)
- [JupyterLab](https://jupyterlab.readthedocs.io/en/latest/) is optional but highly recommended.
- You'll also need to register with [The Guardian's Open Platform](https://open-platform.theguardian.com/access/)
  and snag an API key.

If you're interested in learning about the website side of things, take a read through the
[Hugo quickstart guide](https://gohugo.io/getting-started/quick-start/). This project uses
the [Blonde theme](https://github.com/opera7133/Blonde), so have a look at their documentation
as well.

If you're interested in the automation portion (new content is updated daily), it's all done
via [GitHub Actions](.github/workflows)

## Contribution and Licensing

The project is licensed under the [Affero GPL](LICENSE) and all contributions, uses and modifications
must be done under those terms (read: if you spin up your own site, you must make the source code
publicly available under the AGPL).
