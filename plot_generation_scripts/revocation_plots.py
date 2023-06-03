###
#All possible bins = ['None', 'Option On Website', '']
###

import os
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Set the path to the CSV file
file_path = "/home/divyanshu/Documents/Academics/Sem8/Privacy Considerations of the Indian Web Ecosystem/scraper/scrape_results/manual_scrape.csv"


# Read the CSV file into a DataFrame
df = pd.read_csv(file_path, names=["Rank", "Domain", "Cookie Notice", "Revocation Method"])

all_possible_methods = df["Revocation Method"].unique()

counts = df['Revocation Method'].value_counts()

print(counts)

print(all_possible_methods)

print(len(df["Revocation Method"].unique()))

possibles_bins = ['No Consent', 'No Way To Revoke after Initial Accpetance', 'Modification by directing to Policy Page', 'Options Avaiaable on Landing Page', 'Persistent Icon/Notification to CMP'] #No Consent, None


bin1 = ['None']
bin2 = ['No way after accepting']
bin3 = ['Cookie Policy', 'Your Privacy Choice', 'Cookies', 'Your Privacy Choices', 'Cookies', 'cookies', 'Cookie Information', 'Privacy', 'Cookie Policy ', 'Cookies',  'Cookie', 'Use of cookies', 'Privacy Policy', 'Privacy Policy ']
bin5 = ['Hovering Cookie Policy Banner', 'Hovering Icon', 'Hovering Privacy Policy']

bin4 = ['Cookie Preferences',
 'manage cookies', 'Cookie Settings', 'Consent Manager',
 'Privacy Settings', 'Cookie Notice', 'Cookies Settings',
 'cookie preferences', 'consent manager', 'cookie settings',
  'cookies preferences', 'cookies settings',
 'Privacy Preferences',  'cookie consent',
  'privacy settings',  
  'Privacy Center', 
 'Preference Center', 
 'Cookie Consent Tool', 'Manage Preferences', 'Cookie Details',
 'My cookie settings', 'Manage Cookie Preferences',
  'Manage my cookies', 'review cookie settings', 'My cookie settings']

print(len(bin1) + len(bin2) + len(bin3) + len(bin4) + len(bin5))

assigned_bin = []
for index, row in df.iterrows():
    # Do something with the row data
    if row['Revocation Method'].strip() in bin1:
        assigned_bin.append('No Way to Modify Tracking Choices')
    elif row['Revocation Method'].strip() in bin2:
        assigned_bin.append('No Way To Revoke after Initial Accpetance')
    elif row['Revocation Method'].strip() in bin3:
        assigned_bin.append('Modification by directing to Policy Page')
    elif row['Revocation Method'].strip() in bin4:
        assigned_bin.append('Options Available on Landing Page')   
    elif row['Revocation Method'].strip() in bin5:
        assigned_bin.append('Persistent Icon/Notification redirecting to CMP') 
    else:
        print(row['Revocation Method'])

df['Assigned Bin'] = assigned_bin

import plotly.express as px

# Get the count of each unique value in the 'Assigned Bin' column
bin_counts = df['Assigned Bin'].value_counts()

print(bin_counts)

# fig = px.bar(
#     x=bin_counts.index,
#     y=bin_counts.values,
#     labels={"x": "Revocation Method", "y": "Frequency"},
#     title="Ways to Revoke Consent for Manually Scraped Webites"
# )

fig = px.pie(
    values=bin_counts.values,
    names=bin_counts.index,
    title='Ways to Revoke Consent for Manually Scraped Websites',
)

fig.update_layout(
    title={'font': {'size': 24}},
    font={'size': 14}
)

# create a directory if it does not exist
if not os.path.exists('plots'):
    os.makedirs('plots')

# save the pie chart as an HTML file
fig.write_image('plots/revocation_method_pie_chart.png')

# Show the histogram
fig.show()