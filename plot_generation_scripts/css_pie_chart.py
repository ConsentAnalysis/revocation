import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# read the csv file into a pandas dataframe
df = pd.read_csv('scrape_results/tag_accept_revocation.csv', header=None)


print(df.head())
# convert the 'General CSS' and 'Domain-specific CSS' columns to integer type
df['General CSS'] = df[1].astype(int)
df['Domain-specific CSS'] = df[2].astype(int)

# count the number of domains with non-zero values in 'General CSS' and 'Domain-specific CSS' columns
general_css_count = len(df[df['General CSS'] > 0])
domain_specific_css_count = len(df[df['Domain-specific CSS'] > 0])

print(f"Number of domains with non-zero 'General CSS' value: {general_css_count}")
print(f"Number of domains with non-zero 'Domain-specific CSS' value: {domain_specific_css_count}")

# Create a dataframe to hold the CSS selector counts
css_counts = pd.DataFrame({
    'Selector Type': ['General CSS', 'Domain Specific CSS'],
    'Count': [general_css_count, domain_specific_css_count]
})

# Create the pie chart using Plotly
colors = ['#0084b4', '#4cae4c']
fig = px.pie(
    css_counts, 
    values='Count', 
    names='Selector Type', 
    title='CSS Selector Types', 
    color='Selector Type',
    color_discrete_sequence=colors
)

fig.update_layout(
     title={
        'text': 'CSS Selector Types',
        'font': {
            'size': 20  # set the title font size to 20
        }
    },
    font=dict(
        size=20  # set the label font size to 16
    )
)

# Save the pie chart as a PNG file
fig.write_image('plots/css_pie_chart.png')
