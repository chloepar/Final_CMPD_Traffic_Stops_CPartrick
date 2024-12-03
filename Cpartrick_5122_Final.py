import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

cmpd_final = pd.read_csv("data/cmpd_final.csv")

# Set the page configuration
st.set_page_config(layout="wide")


values = cmpd_final.select_dtypes(include=['number']).columns.tolist()
values = [col for col in values if col not in ('Year')]

features = cmpd_final.select_dtypes(include=['object']).columns.tolist()

# Create three columns
col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 2, 1])

# Center the title
st.markdown("<h1 style='text-align: center;'>Charlotte Mecklenberg Police Department (CMPD) Traffic Stops</h1>", unsafe_allow_html=True)

# Place the image in the center column
with col3:
    st.image('CMPD Logo.jpeg', caption='CMPD Logo', width=200)

with st.expander('About this app'):
  st.write('This app shows the information related to historical CMPD traffic stops. There are options to analyze items based on your own selections, along with pre-built charts.')

# Aggregate the data
agg_df = cmpd_final.groupby('Race/Ethnicity').agg(
    average_stop_count=('Stop Count', 'mean'),
    average_search_count=('Search Count', 'mean'),
    average_search_stop_rate=('Search to Stop Rate', 'mean'),
    average_cntrbnd_rate=('Contraband Rate (of Searches)', 'mean'),
    average_uof_rate=('Use of Force Rate (of Searches)', 'mean'),
    average_pop=('Population', 'mean'),
    average_stop_rate=('Stop Rate', 'mean'),
    average_search_rate=('Search Rate', 'mean')
).reset_index()

# Calculate the average percent of population
total_population = agg_df['average_pop'].sum()
agg_df['average_percent_pop'] = (agg_df['average_pop'] / total_population) * 100

# Rename columns for better readability
agg_df.columns = ['Race/Ethnicity', 'Average Stop Count', 'Average Search Count', 'Average Search to Stop Rate', 
                  'Average Contraband to Search Rate', 'Average Use of Force to Search Rate', 
                  'Average Population', 'Average Stop Rate', 'Average Search Rate', 
                  'Average Percent of Population']

# Ensure the columns are numeric
agg_df['Average Stop Count'] = pd.to_numeric(agg_df['Average Stop Count'])
agg_df['Average Search Count'] = pd.to_numeric(agg_df['Average Search Count'])
agg_df['Average Search to Stop Rate'] = pd.to_numeric(agg_df['Average Search to Stop Rate'])
agg_df['Average Population'] = pd.to_numeric(agg_df['Average Population'])
agg_df['Average Percent of Population'] = pd.to_numeric(agg_df['Average Percent of Population'])
agg_df['Average Stop Rate'] = pd.to_numeric(agg_df['Average Stop Rate'])
agg_df['Average Search Rate'] = pd.to_numeric(agg_df['Average Search Rate'])

# Select specific columns to display
columns_to_display = ['Race/Ethnicity', 'Average Stop Count', 'Average Search Count', 
                      'Average Search to Stop Rate', 'Average Contraband to Search Rate',
                      'Average Use of Force to Search Rate']

# Apply formatting to force one decimal place
styled_df = agg_df[columns_to_display].style.format({
   'Average Stop Count': '{:,.1f}', 
   'Average Search Count': '{:,.1f}',
   'Average Search to Stop Rate': '{:,.1f}', 
   'Average Contraband to Search Rate': '{:,.1f}',
   'Average Use of Force to Search Rate': '{:,.1f}',
   'Average Stop Rate': '{:,.1f}',
   'Average Search Rate': '{:,.1f}'
   })

# Apply gradient color coding to each column
styled_df = styled_df.background_gradient(subset=['Average Stop Count'], cmap='Blues') \
                             .background_gradient(subset=['Average Search Count'], cmap='Blues') \
                             .background_gradient(subset=['Average Search to Stop Rate'], cmap='Blues') \
                             .background_gradient(subset=['Average Contraband to Search Rate'], cmap='Blues') \
                             .background_gradient(subset=['Average Use of Force to Search Rate'], cmap='Blues')

# Plot bar chart for number of stops by race/ethnicity and year
Stop_Trend = px.line(cmpd_final, x='Year', y='Stop Count', color='Race/Ethnicity', title='Number of Stops by Race/Ethnicity')

# Plot bar chart for number of stops by race/ethnicity and year
Search_Trend = px.line(cmpd_final, x='Year', y='Search Count', color='Race/Ethnicity', title='Number of Searches by Race/Ethnicity')
Search_Trend.update_layout(showlegend=False)  # Remove legend from Search_Trend

with st.expander("Who's Getting Pulled Over in Charlotte?"):
    st.write('This section of the analysis provides insight into traffic stop data for the Charlotte Mecklenberg Police Department (CMPD)')
    st.write('The analysis includes data pertinent to: traffic stops, traffic searches, use of force in these events, and the rate at which contraband was ultimately found (as a result of a traffic search).')
    st.write('Any citizen can be stopped, but those who are searched also have to have been stopped. Likewise, use of force can only happen if they have been stopped, and contraband can only be found if they are searched.')
    st.write('This data includes Charlotte gov information for the past 20 years and was pulled from: https://www.opendatapolicingnc.com/report?var=stateAbbreviation:NC&var=agencyTitle:Charlotte-Mecklenburg+Police+Department')
    
    # Display the styled DataFrame with selected columns
    st.dataframe(styled_df)
    
    # Create two columns for the trend lines
    col1, col2 = st.columns(2)
    
    # Display the first trend line in the first column
    with col1:
        st.plotly_chart(Stop_Trend, use_container_width=True)

    # Display the second trend line in the second column
    with col2:
        st.plotly_chart(Search_Trend, use_container_width=True)


# Create trend lines using Plotly Express

stop_rate_trend = px.line(cmpd_final, x='Year', y='Stop Rate', color='Race/Ethnicity', title='Stop Rate')
stop_rate_trend.update_layout(xaxis_title='Year', yaxis_title='Stop Rate (%)')

search_rate_trend = px.line(cmpd_final, x='Year', y='Search Rate', color='Race/Ethnicity', title='Search Rate')
search_rate_trend.update_layout(xaxis_title='Year', yaxis_title='Search Rate (%)')
search_rate_trend.update_layout(showlegend=False)  # Remove legend from Search_Trend

with st.expander("Who Lives in Charlotte?"):
    st.write('This section of the analysis dives into the overall population of Charlotte and looks at the rate of traffic stops and traffic searches based on the entire population.')
    st.write('The goal here is to highlight the differences between ethnicities, especially when accounting for the overarching % of population each ethnicity in Charlotte encompasses.')
    st.write('This data includes government census information for the past 10 years and was pulled from: https://datausa.io/profile/geo/charlotte-nc/')
    
    # Create side by side horizontal bar charts using Streamlit
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    agg_df.plot(kind='barh', x='Race/Ethnicity', y='Average Percent of Population', ax=axes[0], legend=False)
    axes[0].set_title('Average % Population')
    axes[0].set_xlabel('Population (%)')
    
    agg_df.plot(kind='barh', x='Race/Ethnicity', y='Average Stop Rate', ax=axes[1], legend=False)
    axes[1].set_title('Average Stop Rate')
    axes[1].set_xlabel('Stop Rate (%)')
    axes[1].yaxis.set_visible(False)  # Hide y-axis
    
    agg_df.plot(kind='barh', x='Race/Ethnicity', y='Average Search Rate', ax=axes[2], legend=False)
    axes[2].set_title('Average Search Rate')
    axes[2].set_xlabel('Search Rate (%)')
    axes[2].yaxis.set_visible(False)  # Hide y-axis
    
    st.pyplot(fig)

        # Create two columns for the trend lines
    col1, col2 = st.columns(2)
    
    # Display the first trend line in the first column
    with col1:
        st.plotly_chart(stop_rate_trend, use_container_width=True)

    # Display the second trend line in the second column
    with col2:
        st.plotly_chart(search_rate_trend, use_container_width=True)


selected_x_var = st.selectbox(
    "What do you want the x variable to be?",
    values,
)
selected_y_var = st.selectbox(
    "What about the y?",
    values,
)

alt_chart = (
    alt.Chart(cmpd_final, title="Scatterplot of CMPD Traffic Stops")
    .mark_circle()
    .encode(
        x=alt.X(selected_x_var, scale=alt.Scale(zero=False)),
        y=alt.Y(selected_y_var, scale=alt.Scale(zero=False)),
        color="Race/Ethnicity",
    )
    .interactive()
)
st.altair_chart(alt_chart, use_container_width=True)
