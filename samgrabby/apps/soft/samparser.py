import datetime
import logging
import re
from multiprocessing.pool import ThreadPool

import mechanicalsoup

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
    "skype",
    "vlcplayer",
    "teamviewer",
    "classicshell",
    "java",
    "klite",
    "potplayer",
    "tcpp",
    "samdrivers",
]

nnmclub_minstall_id = "1532753"
nnmclub_jinnsliveusb_id = "1530947"
nnmclub_list = [nnmclub_minstall_id, nnmclub_jinnsliveusb_id]


def samlab_parser(url_key):
    root_url = "https://samlab.ws/soft/"
    browser = mechanicalsoup.Browser(soup_config={"features": "html.parser"})
    response = browser.get(root_url + url_key)
    name = (
        response.soup.select('div[class="description"] span')[0]
        .get_text()
        .split(" - ")[0]
    )
    try:
        version = re.search(r"\d[0-9a-zA-Z./\s]+", name).group()
        name = name.replace(version, "").strip()
    except AttributeError:
        version = ""
    upd_date = response.soup.select('div[style^="text"]')[-1].get_text()[-8:]
    upd_date = datetime.datetime.strptime(upd_date, "%d.%m.%y").date()
    links = response.soup.select('div[class="links"] a')
    links = [[a.get_text(), a.attrs.get("href")] for a in links]

    res = {
        "name": name,
        "version": version,
        "upd_date": upd_date,
        "url_key": url_key,
        "links": links,
    }
    return res


def nnmclub_parser(url_key):
    root_url = "https://nnmclub.to/forum/viewtopic.php?t="
    browser = mechanicalsoup.Browser(soup_config={"features": "html.parser"})
    response = browser.get(root_url + url_key)

    maintitle = response.soup.select('a[class="maintitle"]')[0].text.split(" ")
    name = maintitle[0]
    version = maintitle[1]

    upd_date = response.soup.select('td[class="genmed"]')[3].text.strip()
    months = {
        "Янв": "Jan",
        "Фев": "Feb",
        "Мар": "Mar",
        "Апр": "Apr",
        "Май": "May",
        "Июн": "Jun",
        "Июл": "Jul",
        "Авг": "Aug",
        "Сен": "Sep",
        "Окт": "Oct",
        "Ноя": "Nov",
        "Дек": "Dec",
    }

    pattern = re.compile(r"\b(" + "|".join(months.keys()) + r")\b")
    upd_date = pattern.sub(lambda x: months[x.group()], upd_date)
    upd_date = datetime.datetime.strptime(upd_date, "%d %b %Y %H:%M:%S").date()

    links = [
        ["magnet", response.soup.select('td[class="gensmall"] a')[1].attrs.get("href")]
    ]

    res = {
        "name": name,
        "version": version,
        "upd_date": upd_date,
        "url_key": url_key,
        "links": links,
    }
    return res


def parser():
    with ThreadPool(8) as pool:
        list_one = pool.map(samlab_parser, samlab_list)
        list_two = pool.map(nnmclub_parser, nnmclub_list)
        return list_one + list_two


if __name__ == "__main__":
    results = parser()
    for result in results:
        print(result)
