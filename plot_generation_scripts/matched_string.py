import os
import pandas as pd
import plotly.express as px

# Set the path to the CSV file
file_path = "/home/divyanshu/Documents/Academics/Sem8/Privacy Considerations of the Indian Web Ecosystem/scraper/scrape_results/tag_accept_revocation.csv"

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Print the first few rows of the DataFrame
# Select the columns that contain the matched strings
matched_strings_cols = df.columns[3:]

# Flatten the matched strings into a single Series
matched_strings = df[matched_strings_cols].values.flatten()

# Remove the NaN values from the Series
matched_strings = matched_strings[~pd.isnull(matched_strings)]
# matched_strings = matched_strings[matched_strings != "None"]

# Capitalize the matched strings
matched_strings = [s.capitalize() for s in matched_strings]

# Count the frequency of each matched string
matched_strings_counts = pd.Series(matched_strings).value_counts()


fig = px.bar(
    x=matched_strings_counts.index,
    y=matched_strings_counts.values,
    labels={"x": "Matched String", "y": "Frequency"},
    title="Frequency of Matched Strings"
)
# Add value labels on top of the bars
fig.update_traces(text=matched_strings_counts, textposition='auto')
# Set y-axis limit to 800
fig.update_yaxes(range=[0, 500])

# Create a directory named "plots" (if it doesn't already exist)
if not os.path.exists("plots"):
    os.mkdir("plots")

# Save the bar chart in the "plots" directory
fig.show()
fig.write_image("plots/matched_strings_accept_histogram.png")