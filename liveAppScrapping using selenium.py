import re
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import math
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ExpectedConditions
import time

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
Football = []
finalfootball = []
MMA = []
finalMMA = []
Baseball = []
finalbaseball = []


def live_matches(sportNme):

    data = []

    if sportNme == "Tennis":
        data = Tennis

    elif sportNme == "Hockey":
        data = Hockey
    elif sportNme == "Cricket":
        data = Cricket
    elif sportNme == "Volleyball":
        data = Volleyball

    elif sportNme == "Basketball":
        data = Basketball

    elif sportNme == "Soccer":
        data = Soccer
    elif sportNme == "Football":
        data = Football
    elif sportNme == "MMA":
        data = MMA
    elif sportNme == "Baseball":
        data = Baseball

    for i in data:
        info_dict = dict()
        name = i.find("p", class_="game-line__banner").text
        if "LIVE BETTING" in name:
            split_values = re.split("\\| |-|:", name)
            info_dict["name"] = split_values[1]
        else:
            info_dict["name"] = ""

        info_dict["team1"] = (
            i.find("div", class_="game-line__visitor-team")
            .find("p", class_="game-line__visitor-team__name")
            .find("a")
            .text
        )

        info_dict["team2"] = (
            i.find("div", class_="game-line__home-team")
            .find("p", class_="game-line__home-team__name")
            .find("a")
            .text
        )

        info_dict["date_time"] = i.find("p", class_="game-line__time__date").text

        section = i.find_all(
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

        all_rows = i.find_all("div", class_="row")
        info = all_rows[0].text

        info_dict["liveinfo"] = info

        scores = all_rows[1].find_all("span", class_="score_live")

        n = 0
        for score in scores:
            n = n + 1
            itr = "score" + str(n)
            info_dict[itr] = score.text

        if sportNme == "Tennis":
            finalTennis.append(info_dict)
        elif sportNme == "Hockey":
            finalhockey.append(info_dict)
        elif sportNme == "Cricket":
            finalcricket.append(info_dict)
        elif sportNme == "Volleyball":
            finalvolleyball.append(info_dict)
        elif sportNme == "Basketball":
            finalBasketball.append(info_dict)
        elif sportNme == "Soccer":
            finalsoccer.append(info_dict)
        elif sportNme == "Football":
            finalfootball.append(info_dict)
        elif sportNme == "MMA":
            finalMMA.append(info_dict)
        elif sportNme == "Baseball":
            finalbaseball.append(info_dict)


def getLiveSports():

    baseUrl = "https://mybookie.ag"
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--log-level=3")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")

    browser = webdriver.Chrome(options=options)

    # browser.get("https://mybookie.ag/sportsbook/live/")

    url = "https://mybookie.ag/sportsbook/live/"

    # WebDriverWait(browser, 10).until(
    #     lambda browser: browser.execute_script("return document.readyState")
    #     == "complete"
    # )
    requested_data = requests.get(url)

    total_data_div = BeautifulSoup(requested_data.content, "html.parser").find_all(
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
                        print(url)
                        browser.get(url)
                        try:
                            WebDriverWait(browser, 4).until(
                                ExpectedConditions.presence_of_element_located(
                                    (By.CLASS_NAME, "live-current-period")
                                )
                            )
                        except Exception as inst:
                            print("not live")

                        all_div = BeautifulSoup(
                            browser.page_source, "html.parser"
                        ).find_all("div", class_="line-default")

                        for div in all_div:
                            container = div.find_all("div", class_="container-fluid")
                            for i in container:
                                if i not in Tennis:
                                    Tennis.append(i)
                    print("Tennis")
                    live_matches("Tennis")

                elif "Basketball" in left_menu_title:
                    list_of_baskets = sport_name.find_all(
                        "li", class_="nav-item sub-items-menu__body__item"
                    )
                    for basket_type in list_of_baskets:
                        url = baseUrl + basket_type.find("a").get("href")
                        print(url)
                        browser.get(url)
                        try:
                            WebDriverWait(browser, 4).until(
                                ExpectedConditions.presence_of_element_located(
                                    (By.CLASS_NAME, "live-current-period")
                                )
                            )
                        except Exception as inst:
                            print("not live")
                        all_div = BeautifulSoup(
                            browser.page_source, "html.parser"
                        ).find_all("div", class_="line-default")
                        for div in all_div:
                            container = div.find_all("div", class_="container-fluid")
                            for i in container:
                                if i not in Basketball:
                                    Basketball.append(i)
                    print("Basketball")
                    live_matches("Basketball")

                elif "Volleyball" in left_menu_title:
                    list_of_volleys = sport_name.find_all(
                        "li", class_="nav-item sub-items-menu__body__item"
                    )
                    for volley_type in list_of_volleys:
                        url = baseUrl + volley_type.find("a").get("href")
                        print(url)
                        browser.get(url)
                        try:
                            WebDriverWait(browser, 4).until(
                                ExpectedConditions.presence_of_element_located(
                                    (By.CLASS_NAME, "live-current-period")
                                )
                            )
                        except Exception as inst:
                            print("not live")
                        all_div = BeautifulSoup(
                            browser.page_source, "html.parser"
                        ).find_all("div", class_="line-default")

                        for div in all_div:
                            container = div.find_all("div", class_="container-fluid")
                            for i in container:
                                if i not in Volleyball:
                                    Volleyball.append(i)
                    print("Volleyball")
                    live_matches("Volleyball")

                elif "Soccer" in left_menu_title:
                    list_of_soccers = sport_name.find_all(
                        "li", class_="nav-item sub-items-menu__body__item"
                    )
                    for soccer_type in list_of_soccers:
                        url = baseUrl + soccer_type.find("a").get("href")
                        print(url)
                        browser.get(url)
                        try:
                            WebDriverWait(browser, 4).until(
                                ExpectedConditions.presence_of_element_located(
                                    (By.CLASS_NAME, "live-current-period")
                                )
                            )
                        except Exception as inst:
                            print("not live")
                        all_div = BeautifulSoup(
                            browser.page_source, "html.parser"
                        ).find_all("div", class_="line-default")

                        for div in all_div:
                            container = div.find_all("div", class_="container-fluid")
                            for i in container:
                                if i not in Soccer:
                                    Soccer.append(i)
                    print("Soccer")
                    live_matches("Soccer")

                elif "Hockey" in left_menu_title or "NHL" in left_menu_title:
                    list_of_hockey = sport_name.find_all(
                        "li", class_="nav-item sub-items-menu__body__item"
                    )

                    for hockey_type in list_of_hockey:
                        url = baseUrl + hockey_type.find("a").get("href")
                        print(url)
                        browser.get(url)
                        try:
                            WebDriverWait(browser, 4).until(
                                ExpectedConditions.presence_of_element_located(
                                    (By.CLASS_NAME, "live-current-period")
                                )
                            )
                        except Exception as inst:
                            print("not live")
                        all_div = BeautifulSoup(
                            browser.page_source, "html.parser"
                        ).find_all("div", class_="line-default")

                        for div in all_div:
                            container = div.find_all("div", class_="container-fluid")
                            for i in container:
                                if i not in Hockey:
                                    Hockey.append(i)
                    print("Hockey")
                    live_matches("Hockey")

                elif "Cricket" in left_menu_title:
                    list_of_cricket = sport_name.find_all(
                        "li", class_="nav-item sub-items-menu__body__item"
                    )

                    for cricket_type in list_of_crickets:
                        url = baseUrl + hockey_type.find("a").get("href")
                        print(url)
                        browser.get(url)
                        try:
                            WebDriverWait(browser, 4).until(
                                ExpectedConditions.presence_of_element_located(
                                    (By.CLASS_NAME, "live-current-period")
                                )
                            )
                        except Exception as inst:
                            print("not live")
                        all_div = BeautifulSoup(
                            browser.page_source, "html.parser"
                        ).find_all("div", class_="line-default")

                        for div in all_div:
                            container = div.find_all("div", class_="container-fluid")
                            for i in container:
                                if i not in Cricket:
                                    Cricket.append(i)
                    print("Cricket")
                    live_matches("Cricket")

                elif "Football" in left_menu_title:
                    list_of_footballs = sport_name.find_all(
                        "li", class_="nav-item sub-items-menu__body__item"
                    )

                    for football_type in list_of_footballs:
                        url = baseUrl + football_type.find("a").get("href")
                        print(url)
                        browser.get(url)
                        try:
                            WebDriverWait(browser, 4).until(
                                ExpectedConditions.presence_of_element_located(
                                    (By.CLASS_NAME, "live-current-period")
                                )
                            )
                        except Exception as inst:
                            print("not live")
                        all_div = BeautifulSoup(
                            browser.page_source, "html.parser"
                        ).find_all("div", class_="line-default")

                        for div in all_div:
                            container = div.find_all("div", class_="container-fluid")
                            for i in container:
                                if i not in Football:
                                    Football.append(i)
                    print("football")
                    live_matches("Football")

                elif "Baseball" in left_menu_title:
                    list_of_baseballs = sport_name.find_all(
                        "li", class_="nav-item sub-items-menu__body__item"
                    )

                    for baseball_type in list_of_baseballs:
                        url = baseUrl + baseball_type.find("a").get("href")
                        print(url)
                        browser.get(url)
                        try:
                            WebDriverWait(browser, 4).until(
                                ExpectedConditions.presence_of_element_located(
                                    (By.CLASS_NAME, "live-current-period")
                                )
                            )
                        except Exception as inst:
                            print("not live")
                        all_div = BeautifulSoup(
                            browser.page_source, "html.parser"
                        ).find_all("div", class_="line-default")

                        for div in all_div:
                            container = div.find_all("div", class_="container-fluid")
                            for i in container:
                                if i not in Baseball:
                                    Baseball.append(i)
                    print("baseball")
                    live_matches("Baseball")

                elif "MMA" in left_menu_title:
                    list_of_MMAs = sport_name.find_all(
                        "li", class_="nav-item sub-items-menu__body__item"
                    )
                    for mma_type in list_of_MMAs:
                        url = baseUrl + mma_type.find("a").get("href")
                        browser.get(url)
                        try:
                            WebDriverWait(browser, 4).until(
                                ExpectedConditions.presence_of_element_located(
                                    (By.CLASS_NAME, "live-current-period")
                                )
                            )
                        except Exception as inst:
                            print("not live")
                        all_div = BeautifulSoup(
                            browser.page_source, "html.parser"
                        ).find_all("div", class_="line-default")

                        for div in all_div:
                            container = div.find_all("div", class_="container-fluid")
                            for i in container:
                                if i not in MMA:
                                    MMA.append(i)
                    print("MMA")
                    live_matches("MMA")
    browser.close()


getLiveSports()

print(
    finalTennis,
    "\n\n",
    finalBasketball,
    "\n\n",
    finalvolleyball,
    "\n\n",
    finalsoccer,
    "\n\n",
    finalhockey,
    "\n\n",
    finalcricket,
    "\n\n",
    finalbaseball,
    "\n\n",
    finalMMA,
    "\n\n",
    finalfootball,
    "\n",
)
