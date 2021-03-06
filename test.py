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

url = "https://academic.microsoft.com/api/search"

data = {
    "query": "machine learning",
    "queryExpression": "",
    "filters": [],
    "orderBy": None,
    "skip": 0,
    "sortAscending": True,
    "take": 10,
}

r = requests.post(url=url, json=data)

result = r.json()

print(result)