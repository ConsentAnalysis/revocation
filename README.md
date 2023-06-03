# Is Consent Absolute? An Analysis of Consent Modification on Websites

This repository contains the code used for the paper "Is Consent Absolute? An Analysis of Consent Modification on Websites".

## Pre-Requisites

To use the scraper, you need to have the `chromedriver` file on your system. The version of `chromedriver` that you use should always match the version of Google Chrome installed on your system. For our usage, we used Chrome version `111.0.5563.146`. You can download the appropriate version of `chromedriver` for your system from the following link: https://chromedriver.chromium.org/downloads. 

In addition to `chromedriver`, we use two Python packages for the scraper:

- `selenium` (version 4.7.2)
- `beautifulsoup4` (version 4.11.1)

Additionally, the project also contains a `requiremnts.txt` file containing all the packages and their version installed in our Conda environment.

```bash
pip install -r requirements.txt
```

## Usage

To run the project, execute the following command in your terminal:

```bash
python3 banner_scraper.py --chromedriver_path /path/to/chromedriver
```

This command will create a `results` directory with two files: `banner_domain.csv` and `not_accessed.csv`.

- The `banner_domain.csv` file contains a list of websites that have a banner and CSS elements matched.

- The `not_accessed.csv` file contains the websites that the scraper was unable to access.

**Note that the banner_domain.csv file contains all the code for searching for a CSS selector, which takes a lot of time. In case of a time constraint, we can use this script to just get all the data and then use the source code collected later for our analysis.**

**Also, the banner_domain.csv file takes a lot of time to run. For 1000 websites, it will take around 24 hours. We recommend using threading to optimize this. The most optimal solution would be to scrape all the source code first and then, using threading, search for the CSS selectors, because of threading issue with Selenium.**

In addition to the website list, for each website accessed, we create a folder with the website name inside the `results` directory. This folder contains the following three files:

- `cookies.txt`: a text file that lists the default cookies set by the website.
- `local_storage.txt`: a text file that lists the local storage objects set by the website.
- `source_code.txt`: a text file that contains the source code of the website.

For example, if we visit google.com, the `results` directory will have a folder named `google.com`, with the above mentioned three files.

The main usage of the `banner_scraper.py` file is to get a list of websites that have a banner and their source code. Once we have the source code of the accessed websites, we can use the scripts present in the `util_scripts` directory to obtain further results.

## Utility Scripts ( Please check paths of different CSV files and directories )

This directory contains additional scripts that may be helpful for further analysis of the data collected by the main scraper script.

### `banner_info.py`

This script assumes that you have a `websites` folder containing different directories, with the domain name as the name of the folder, each containing three files: `source_code.txt`, `cookies.txt`, and `local_storage.txt`. **Check the source code once to a get a better understanding.** The path of this `websites` directory is one argument to the program. The `results` arguments, takes the `banner_domain.csv` file generated from the `banner_scraper.py` program and uses the CSS Selectors found for further analysis.

```bash
python3 banner_info.py --results /path/to/banner_domain.csv --websites /path/to/scraped_webistes
```

The code in the script reads the source code of the domain, checks for the presence of a banner, removes the banner, and then checks for the presence of possible revocation methods in anchor or button tags. You may need to modify the path of CSV files to read. The output is saved to a CSV file named `revocation_methods.csv` in `results` directory. 

### `cookie_number.py`

This script assumes the same folder structure as `banner_info.py` and calculates the number of cookies set by default on each domain. The output is saved to a CSV file named `cookie_count.csv`.

### `reorganizer.py`

This script takes a list of websites and randomly shuffles them before rearranging the websites in the order of their ranking. The input file should be a CSV file with one domain per line, and the output is also saved as a CSV file.

### `rule_list.py`

This script reads the rules from `easylist.txt` and is used in `banner_scraper.py` to get the list of CSS rules to match against.
