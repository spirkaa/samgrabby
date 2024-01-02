"""Samlab parser."""

import logging
import re
from dataclasses import dataclass
from datetime import date, datetime

from bs4 import BeautifulSoup
from mechanicalsoup import StatefulBrowser
from tenacity import (
    before_sleep_log,
    retry,
    stop_after_attempt,
    wait_random_exponential,
)

logger = logging.getLogger(__name__)
logging.getLogger("urllib3").setLevel(logging.WARNING)

samlab_list = [
    "7zip",
    "aimp",
    "audacity",
    "fsviewer",
    "filezilla",
    "firefox",
    "googlechrome",
    "notepad",
    "reaper",
    "vlcplayer",
    "classicshell",
    "klite",
    "tcpp",
    "samdrivers",
]


@dataclass
class DownLink:
    """Download link."""

    dl_url_text: str
    dl_url: str


@dataclass
class Soft:
    """Soft entry."""

    name: str
    version: str
    upd_date: date
    url_key: str
    links: list[DownLink]


@retry(
    wait=wait_random_exponential(multiplier=1, max=10),
    stop=stop_after_attempt(10),
    before_sleep=before_sleep_log(logger, logging.DEBUG),
    reraise=True,
)
def get_page_soup(browser: StatefulBrowser, url_key: str) -> BeautifulSoup:
    """Get soup from samlab page."""
    logger.debug("Get page soup for %s", url_key)
    response = browser.get(f"https://samlab.ws/soft/{url_key}")
    response.raise_for_status()
    return response.soup  # type: ignore


def samlab_parser(browser: StatefulBrowser, url_key: str) -> Soft:
    """Parse samlab page."""
    soup = get_page_soup(browser, url_key)

    name_element = soup.select("div.description span")[0]
    name = name_element.get_text().split(" - ")[0]

    version_pattern = re.compile(r"\d[0-9a-zA-Z./\s]+")
    version_match = version_pattern.search(name)
    if version_match:
        version = version_match.group()
        name = name.replace(version, "").strip()
    else:
        version = ""

    date_element = soup.select('div[style^="text"]')[-1]
    upd_date = date_element.get_text()[-8:]
    upd_date = datetime.strptime(upd_date, "%d.%m.%y").date()

    links_element = soup.select("div.links a")
    links = [DownLink(a.get_text(), a.attrs.get("href", "")) for a in links_element]

    return Soft(name, version, upd_date, url_key, links)


def get_soft_data() -> list[Soft]:
    """Get soft data."""
    browser = StatefulBrowser(soup_config={"features": "html.parser"})
    return [samlab_parser(browser, url_key) for url_key in samlab_list]


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s  [%(name)s:%(lineno)s]  %(levelname)s - %(message)s",
        level=logging.DEBUG,
    )
    results = get_soft_data()
    for result in results:
        print(result)
