import re
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import math
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

College_Basketball = []
BasketballNBA = []
Basketball = []
finalBasketball = []
Hockey = []
finalhockey = []
Soccer = []
finalsoccer = []
Tennis = []
finalTennis = []
Cricket = []
finalcricket = []
Volleyball = []
finalvolleyball = []


def tennislive_matches():
    for i in Tennis:
        info_dict = dict()
        name = i.find("p", class_="game-line__banner").text
        if "LIVE BETTING" in name:
            split_values = re.split("\\| |-|:", name)
            info_dict["name"] = split_values[1]
        else:
            info_dict["name"] = ""

        info_dict["team1"] = (
            i.find("div", class_="col-5")
            .find("p", class_="game-line__visitor-team__name")
            .find("a")
            .text
        )

        info_dict["team2"] = (
            i.find("div", class_="col-5")
            .find("p", class_="game-line__home-team__name")
            .find("a")
            .text
        )

        info_dict["date_time"] = i.find("p", class_="game-line__time__date").text

        data = []
        section = i.find("div", class_="col-7").find_all(
            "div",
            {
                "class": [
                    "game-line__visitor-line",
                    "game-line__home-line",
                ]
            },
        )

        m = 0
        for info in section:
            buttons = info.find_all("button", class_="lines-odds")
            for button in buttons:
                m = m + 1
                m = str(m)
                info_dict["point" + m] = button.text
                m = int(m)
        finalTennis.append(info_dict)

        print(i.find("div", class_="col-5").find("span", class_="score_live"))

        print(i.find("p", class_="game-line__time__date").find("span"))


def getLiveSports():

    baseUrl = "https://mybookie.ag/"
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    browser = webdriver.Chrome(chrome_options=chrome_options)

    browser.get("https://mybookie.ag/sportsbook/live/")

    WebDriverWait(browser, 10).until(
        lambda browser: browser.execute_script("return document.readyState")
        == "complete"
    )

    total_data_div = BeautifulSoup(browser.page_source, "html.parser").find_all(
        "div", class_="desktop-parent-group"
    )

    for data in total_data_div:
        if "Live Betting" in data.find("h3", class_="parent-league-menu").text:
            live_sport_names = data.find_all("div", class_="desktop-parent-group")
            for sport_name in live_sport_names:
                left_menu_title = sport_name.find(
                    "h3", class_="left-menu-group__header__title"
                ).text

                if "Tennis" in left_menu_title:

                    list_of_tennis = sport_name.find_all(
                        "li", class_="nav-item sub-items-menu__body__item"
                    )

                    for tennis_type in list_of_tennis:
                        url = baseUrl + tennis_type.find("a").get("href")
                        browser.get(url)
                        WebDriverWait(browser, 10).until(
                            lambda browser: browser.execute_script(
                                "return document.readyState"
                            )
                            == "complete"
                        )
                        all_div = BeautifulSoup(
                            requested_data.content, "html.parser"
                        ).find_all("div", class_="line-default")
                        for div in all_div:
                            container = div.find_all("div", class_="container-fluid")
                            for i in container:
                                if i not in Tennis:
                                    Tennis.append(i)
                    tennislive_matches()

                elif "Basketball" in left_menu_title:
                    list_of_basketball = sport_name.find_all(
                        "li", class_="nav-item sub-items-menu__body__item"
                    )

                    for basketball_type in list_of_basketball:
                        url = baseUrl + basketball_type.find("a").get("href")
                        requested_data = requests.get(url)
                        all_div = BeautifulSoup(
                            browser.page_source, "html.parser"
                        ).find_all("div", class_="line-default")
                        for div in all_div:
                            container = div.find_all("div", class_="container-fluid")
                            for i in container:
                                if i not in Tennis:
                                    Tennis.append(i)
                    tennislive_matches()

                # elif "Volleyball" in left_menu_title:
                #     print(left_menu_title)

                # elif "Soccer" in left_menu_title:
                #     print(left_menu_title)

                # elif "Hockey" in left_menu_title or "NHL" in left_menu_title:
                #     print(left_menu_title)

                # elif "Cricket" in left_menu_title:
                #     print(left_menu_title)


getLiveSports()
print(finalTennis)