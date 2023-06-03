import numpy as np
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go

import matplotlib.pyplot as plt

df = pd.read_csv('scrape_results/manual_cleaned_data.csv', header=None, names=['Webiste', 'Banner/Notice',  'Revocation Method', 'Landed Cookies', 'Acceptance Cookies', 'Revocation Cookies'])
df = df.reset_index(drop=True)
df.replace('NA', np.nan, inplace=True)
df['Landed Cookies'] = df['Landed Cookies'].astype(int)

print(df.describe())

#Create bins for different value ranges
bins = [0, 5, 10, 20, 30, 40, 50, float('inf')]
labels = ['0-5', '5-10','10-20', '20-30', '30-40', '40-50', 'Greater than 50']
df['Value Ranges'] = pd.cut(df['Landed Cookies'], bins=bins, labels=labels)

# Group by value ranges and get the count of values in each range
grouped_df = df.groupby('Value Ranges').count().reset_index()

# Create a bar chart using Plotly
fig = go.Figure([go.Bar(x=grouped_df['Value Ranges'], y=grouped_df['Landed Cookies'])])

# Set chart title and axis labels
fig.update_layout(title='Count of Cookies in Different Ranges',
                  xaxis_title='Value Ranges',
                  yaxis_title='No. of Websites')

# Show the plot
fig.show()

# Save the pie chart as a PNG file
# Add value labels on top of the bars
fig.update_traces(text=grouped_df['Landed Cookies'], textposition='auto')
fig.write_image('plots/cookie_landed.png')

# Calculate the change in values between 'Before' and 'After'
df['Changes'] = df['Revocation Cookies'] - df['Acceptance Cookies']

# # Count positive, negative, and zero values in the 'Changes' column
positive_count = (df['Changes'] > 0).sum()
negative_count = (df['Changes'] < 0).sum()
zero_count = (df['Changes'] == 0).sum()

df['Changes2'] = df['Revocation Cookies'] - df['Landed Cookies']

# # Count positive, negative, and zero values in the 'Changes' column
positive_count2 = (df['Changes2'] > 0).sum()
negative_count2 = (df['Changes2'] < 0).sum()
zero_count2 = (df['Changes2'] == 0).sum()

# # Create a bar chart using Plotly
fig = px.bar(x=['Positive', 'Negative', 'Zero'],
             y=[positive_count, negative_count, zero_count],
             labels={'x': 'Value', 'y': 'Count'},
             title='Count of Positive, Negative, and Zero Values in Changes Column')

# fig.show()
# fig.write_image('plots/cookie_landed_changes.png')

# Create subplots with 1 row and 2 columns
import plotly.subplots as sp
fig = sp.make_subplots(rows=1, cols=2)

# # Add first bar graph to the first subplot
fig.add_trace(go.Bar(x=['Increased', 'Decreased', 'Constant'],
             y=[positive_count, negative_count, zero_count], name='Revocation-Accepted Cookies'), row=1, col=1)

# # Add second bar graph to the second subplot
fig.add_trace(go.Bar(x=['Increased', 'Decreased', 'Constant'],
             y=[positive_count2, negative_count2, zero_count2], name='Revocation-Landed Cookies'), row=1, col=2)

# # Update subplot layout
fig.update_layout(title='Change in Number of Cookies')

# # Update x-axis and y-axis titles for all subplots
fig.update_yaxes(title_text='Number of Websites', row=1, col=1)
#fig.update_yaxes(title_text='Magnitude of Change', row=1, col=2)


# # Show the combined plot

fig.update_layout(legend=dict(yanchor="top", y=1.2, xanchor="left", x=0.6))
fig.write_image('plots/cookie_changes.png')