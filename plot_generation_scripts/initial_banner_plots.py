import os
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Set the path to the CSV file
file_path = "/home/divyanshu/Documents/Academics/Sem8/Privacy Considerations of the Indian Web Ecosystem/scraper/scrape_results/manual_scrape.csv"


# Read the CSV file into a DataFrame
df = pd.read_csv(file_path, names=["Rank", "Domain", "Cookie Notice", "Revocation Method"],  index_col=None)

# Get the existing ranks in the DataFrame
existing_ranks = df["Rank"].unique()

# Generate a range of ranks from 1 to 1000
# all_ranks = range(1, 1001)

# # Get the missing ranks that are not in the DataFrame
# missing_ranks = set(all_ranks) - set(existing_ranks)


# missing_ranks = pd.DataFrame(sorted(missing_ranks))
# missing_ranks.columns = ["Rank"]
# urls = []
# for i in range(len(missing_ranks)):
#     urls.append('url.com')

# missing_ranks['Domain'] = urls

# init_banner = []
# for i in range(len(missing_ranks)):
#     init_banner.append('No')

# missing_ranks['Cookie Notice'] = init_banner

# #print(missing_ranks)
# # Create a DataFrame for the missing ranks with "No" for the "Cookie Notice" column
# #missing_df = pd.DataFrame({"Rank": sorted(missing_ranks), "Domain": "url.com", "Cookie Notice": "No"}, dtype={"Rank": int, "Domain": str, "Cookie Notice": str})

# # Concatenate the existing and missing DataFrames
# df = pd.concat([df, missing_ranks], ignore_index=True)

# Sort the DataFrame by rank
df = df.sort_values("Rank")

# Reset the index of the DataFrame
df = df.reset_index(drop=True)
df['Cookie Notice'] = df['Cookie Notice'].apply(lambda x: x.strip())
df['Cookie Notice'] = df['Cookie Notice'].replace('None', 'No')

print(df['Cookie Notice'].unique())

# group the dataframe into chunks of 200 rows
#groups = df.groupby(df.index // 100)
df['group'] = pd.cut(df['Rank'], bins=[0, 200, 400, 600, 800, 1000], labels=['1-200', '201-400', '401-600', '601-800', '801-1000'])


# group the dataframe by the new 'group' column
groups = df.groupby('group')

# create a list of colors for each of the three values in the third column
# create a list of colors for each of the three values in the third column
colors = {'No': 'indianred', 'Cookie Notice': 'cornflowerblue', 'Cookie Banner': 'mediumseagreen'}

# loop through each group and create a stacked bar chart
for i, group in groups:
    # group the data by the third column and count the number of occurrences
    counts = group.groupby('Cookie Notice')['Cookie Notice'].count()
    print(counts)
    # create a bar chart with the counts for each value in the third column
    plt.bar(i, counts['No'], color=colors['No'], linewidth=2)
    plt.bar(i, counts['Cookie Notice'], bottom=counts['No'], linewidth=2, color=colors['Cookie Notice'])
    plt.bar(i, counts['Cookie Banner'], bottom=counts['No']+counts['Cookie Notice'], color=colors['Cookie Banner'],  linewidth=2)

# set the x-axis tick labels and title
plt.xticks(range(len(groups)), [f'Top {i*200}-{(i+1)*200-1}' for i in range(len(groups))])
plt.xlabel('Rank')
plt.ylabel('Count')
plt.title('Website Cookie Notices')

# create a legend for the colors
plt.legend(labels=['No Notice or Banner', 'Cookie Notice', 'Cookie Banner'], loc='upper left', fontsize=14)

# display the chart
plt.show()