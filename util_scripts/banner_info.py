from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from multiprocessing import cpu_count
from datetime import datetime
from rule_list import get_rules
from nltk.util import ngrams

import csv
import re
import os
import time
import json
import nltk
import timeit
import argparse
nltk.download('punkt')

if not os.path.exists("results"):
    os.makedirs("results")

parser = argparse.ArgumentParser()
parser.add_argument('--results', type=str, required=True, help='Path to the banner_domain.csv generated from banner_scraper.py')
parser.add_argument('--websites', type=str, required=True, help='Path to the directory containing websites information')
args = parser.parse_args()

selector_dict = {}
with open(args.results, mode='r') as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        selector_dict[lines[0]] = lines[1:]
websites = selector_dict.keys()

# selector_num = {}
# with open('scrape_results/tag_accept_revocation.csv', mode='r') as file:
#     csvFile = csv.reader(file)
#     for lines in csvFile:
#         selector_num[lines[0]] = lines[1:]

generic_rules, domain_specific_rules = get_rules()

possible_revocation = ['cookie preferences', 'cookie settings', 'consent manager', 'privacy settings', 'manage cookies', 'cookies settings', 'cookies preferences']

# Define the list of strings
list_of_strings = [
    "we use cookies to personalize content and ads to provide social media features and to analyze our traffic",
    "by clicking accept or by continuing to browse the site you agree to our use of cookies",
    "this site uses cookies By continuing to browse the site you are agreeing to our use of cookies",
]

# Define the range of n-grams to generate
ngram_range = range(2, 6)  # 2-gram to 5-gram
ngrams_dict = {}

for i, string in enumerate(list_of_strings, start=1):
    string_ngrams = {}
    for n in ngram_range:
        # Generate n-grams for the current string
        ngrams_list = list(ngrams(nltk.word_tokenize(string), n))
        string_ngrams[f"{n}-gram"] = ngrams_list
    ngrams_dict[string] = string_ngrams

ngram_strs = []
for string, ngrams in ngrams_dict.items():
    for ngram, ngrams_list in ngrams.items():
        for gram in ngrams_list:
            ngram_str = ' '.join(gram)
            ngram_strs.append(ngram_str)

def scrape_url(url):
    domain = url #get domain name

    try:
        print("Scraping URL: " + url.strip())

        domain_dir = args.websites + "/" + str(domain) + "/"
        file_path = os.path.join(domain_dir, "source_code.txt")

        if os.path.exists(file_path):
        # open the file and read its contents
            with open(file_path, "r") as f:
                source_code = f.read()
  
                soup = BeautifulSoup(source_code, "lxml")

                generic_selectors = []
                domain_selectors = []

                # start = timeit.default_timer()
                # for css_selector in tqdm(generic_rules, desc=domain, total=len(generic_rules)):
                #     try:
                #         elements = soup.select(str(css_selector))
                #         if len(elements) > 0:
                #             generic_selectors.append(css_selector)
                #     except Exception as e:
                #         print('Issue with selector: ' + css_selector)
                #         print(e)

                # if domain in domain_specific_rules:
                #     for selector in domain_specific_rules[domain]:
                #         elements = soup.select(str(selector))
                #         if len(elements) > 0:
                #             domain_selectors.append(selector)
                # stop = timeit.default_timer()

                # selectors_list = generic_selectors + domain_selectors

                selectors_list = selector_dict[domain]

                # domain_dir = 'results/' + str(domain)
                # if not os.path.exists(domain_dir):
                #     os.mkdir(domain_dir)
                # with open(os.path.join(domain_dir, 'source_code-before.txt'), 'w') as f:
                #     f.write(soup.prettify())

                elements = []
                for selector in selectors_list:
                    elements += soup.select(str(selector))
                for element in elements:
                    element_text = element.get_text(strip=True)
                    element_text = re.sub(r'[^ \w]+', '', element_text)  # Remove all non-word characters excluding spaces
                    element_text = element_text.casefold()  # Convert to lowercase
                    for curr_str in ngram_strs:
                        if curr_str in element_text:
                            element.decompose()

                # with open(os.path.join(domain_dir, 'source_code-after.txt'), 'w') as f:
                #     f.write(soup.prettify())

                matched_strings = []
                for a_tag in soup.find_all('a'):
                    a_text = a_tag.get_text().casefold().strip()
                    for _str in possible_revocation:
                        if( _str in a_text ):
                            matched_strings.append(_str)

                for button_tag in soup.find_all('button'):
                    button_text = button_tag.get_text().casefold().strip()
                    for _str in possible_revocation:
                        if( _str in button_text ):
                            matched_strings.append(_str)

                output_str = f'{domain}'

                # temp_list = selector_num[domain]
                # output_str += f',{temp_list[0]}'
                # output_str += f',{temp_list[1]}'
                
                if(len(matched_strings) != 0):
                    for i, matched_string in enumerate(matched_strings):
                        output_str += f',{matched_string}'
                else:
                    output_str += f',None'

                selector_str = f'{domain}'
                for selector in selectors_list:
                    selector_str += f',{selector.strip()}'

                text_file = open("results/revocation_methods.csv", "a")
                text_file.write(output_str + "\n")
                text_file.close()

                # selector_file = open("results/selector_info.csv", "a")
                # selector_file.write(selector_str + "\n")
                # selector_file.close()

    except Exception as e:
        print("There was an error accessing url:" + url)
        print(e)
        not_accessed = open("results/not_accessed.csv", "a")
        not_accessed.write(domain + "\n")
        not_accessed.close()
        print('Facing error: ' + str(e))
    except KeyboardInterrupt:  
        print('Terminating Now...')  
        sys.exit(0)

for url in websites:
    scrape_url(url)
