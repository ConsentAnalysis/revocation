from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from multiprocessing import cpu_count
from datetime import datetime

from rule_list import get_rules

import csv
import re
import os
import time
import json
import sys 

with open('scrape_results/banners_mult.csv', mode='r') as file:
    csvFile = csv.reader(file)
    websites = []
    for lines in csvFile:
        websites.append(lines[1])


for domain in websites:
    domain_dir = '../websites/' + str(domain) + "/"
    file_path = os.path.join(domain_dir, "cookies.txt")

    if os.path.exists(file_path):

        with open(file_path, 'r') as f:
            cookie_str = f.read()
            cookie_array = cookie_str.split("\n")
            print(str(domain)+','+ str(len(cookie_array) - 1))

