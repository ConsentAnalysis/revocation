import csv
import sys

with open('top-10k.csv', mode='r') as file:
    csvFile = csv.reader(file)
    website_order = {}
    for line in csvFile:
        if line[1] in website_order.keys():
            print('something wrong')
            sys.exit()
        else:
            website_order[line[1]] = line[0]

with open('scrape_results/not_accessed.csv', mode='r') as file:
    csvFile = csv.reader(file)
    websites = []
    for line in csvFile:
        websites.append(line)

for website_info in websites:
    if( website_info[0] in website_order.keys() ): #For websites, www.gov.uk, www.nhs.uk, www.gov.pl
        website_info.append(int(website_order[website_info[0]]))
    else:
        #print( 'www.' + str(website_info[0]))
        website_info.append(int(website_order['www.' + str(website_info[0])]))

from operator import itemgetter
websites.sort(key=itemgetter(2))

with open("scrape_results/out.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(websites)