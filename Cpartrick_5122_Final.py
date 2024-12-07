import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt


# Data Cleaning

traffic_stop_cnt = pd.read_excel("data/NC_TRAFFIC_STOP_DATA.xlsx", sheet_name="TRAFFIC_STOP_CNT")
stop_purpose = pd.read_excel("data/NC_TRAFFIC_STOP_DATA.xlsx", sheet_name="STOP_PURPOSE")
search_type = pd.read_excel("data/NC_TRAFFIC_STOP_DATA.xlsx", sheet_name="SEARCH_BY_STOP_TYPE")
srch_cnt = pd.read_excel("data/NC_TRAFFIC_STOP_DATA.xlsx", sheet_name="SEARCH_CNT")
srch_rte = pd.read_excel("data/NC_TRAFFIC_STOP_DATA.xlsx", sheet_name="SEARCH_RATE")
stop_cause_rte = pd.read_excel("data/NC_TRAFFIC_STOP_DATA.xlsx", sheet_name="STOP_CAUSE_RATE")
cntrbnd_rte = pd.read_excel("data/NC_TRAFFIC_STOP_DATA.xlsx", sheet_name="CONTRABAND_RATE")
use_force = pd.read_excel("data/NC_TRAFFIC_STOP_DATA.xlsx", sheet_name="USE_OF_FORCE")
clt_pop = pd.read_csv("data/Race and Ethnicity.csv")



# %% Unpivot the Traffic Stop Count DataFrame
traffic_stop_cnt_final = pd.melt(traffic_stop_cnt, id_vars=['Year'], value_vars=['Black', 'White', 'Latinx', 'Asian', 'Other', 'Indigenous'],
                     var_name='Race/Ethnicity', value_name='Count')

traffic_stop_cnt_final['Year'] = traffic_stop_cnt_final['Year'].astype(object)
traffic_stop_cnt_final["Count"] = traffic_stop_cnt_final["Count"].astype(int)

# %% Unpivot the Stop Purpose DataFrame
stop_purpose_final = pd.melt(stop_purpose, id_vars=['Year', 'Stop Purpose'], value_vars=['Black', 'White', 'Latinx', 'Asian', 'Other', 'Indigenous'],
                     var_name='Race/Ethnicity', value_name='Count')

stop_purpose_final["Count"] = stop_purpose_final["Count"].astype(int)
stop_purpose_final['Year'] = stop_purpose_final['Year'].astype(object)
# %% Unpivot the Search Type DataFrame
search_type_final = pd.melt(search_type, id_vars=['Year', 'Stop Purpose'], value_vars=['Black', 'White', 'Latinx', 'Asian', 'Other', 'Indigenous'],
                     var_name='Race/Ethnicity', value_name='Count')

search_type_final["Count"] = search_type_final["Count"].astype(int)
search_type_final['Year'] = search_type_final['Year'].astype(object)
# %% Unpivot the Search Count DataFrame
srch_cnt_final = pd.melt(srch_cnt, id_vars=['Year'], value_vars=['Black', 'White', 'Latinx', 'Asian', 'Other', 'Indigenous'],
                     var_name='Race/Ethnicity', value_name='Count')

srch_cnt_final["Count"] = srch_cnt_final["Count"].astype(int)
srch_cnt_final['Year'] = srch_cnt_final['Year'].astype(object)

# %% Unpivot the Search Rate DataFrame
srch_rte_unpivot = pd.melt(srch_rte, id_vars=['Year'], value_vars=['Black', 'White', 'Latinx', 'Asian', 'Other', 'Indigenous', 'Total'],
                     var_name='Race/Ethnicity', value_name='Count/Total')

srch_rte_unpivot[['Search Count', 'Stop Count']] = srch_rte_unpivot['Count/Total'].str.split('/', expand=True)

srch_rte_final = srch_rte_unpivot.drop('Count/Total', axis=1)

srch_rte_final["Search Count"] = srch_rte_final["Search Count"].str.replace(",", "").astype(int)
srch_rte_final["Stop Count"] = srch_rte_final["Stop Count"].str.replace(",", "").astype(int)
srch_rte_final['Year'] = srch_rte_final['Year'].astype(object)

srch_rte_final.head(5)

# %% Unpivot the Stop Cause Rate DataFrame
stop_cause_rte_unpivot = pd.melt(stop_cause_rte, id_vars=['Year', 'Stop Purpose'], value_vars=['Black', 'White', 'Latinx', 'Asian', 'Other', 'Indigenous'],
                     var_name='Race/Ethnicity', value_name='Count/Total')

# Split column to have search count and stop count

stop_cause_rte_unpivot[['Search Count', 'Stop Count']] = stop_cause_rte_unpivot['Count/Total'].str.split('/', expand=True)

stop_cause_rte_final = stop_cause_rte_unpivot.drop('Count/Total', axis=1)

stop_cause_rte_final["Search Count"] = stop_cause_rte_final["Search Count"].str.replace(",", "").astype(int)
stop_cause_rte_final["Stop Count"] = stop_cause_rte_final["Stop Count"].str.replace(",", "").astype(int)
stop_cause_rte_final['Year'] = stop_cause_rte_final['Year'].astype(object)

stop_cause_rte_final = stop_cause_rte_final.groupby(['Year', 'Race/Ethnicity'])[['Stop Count', 'Search Count']].sum().reset_index()

# %% Unpivot the Contraband Rate DataFrame
cntrbnd_rte_unpivot = pd.melt(cntrbnd_rte, id_vars=['Year'], value_vars=['Black', 'White', 'Latinx', 'Asian', 'Other', 'Indigenous'],
                     var_name='Race/Ethnicity', value_name='Contraband Count/Search Count')

# Split column to have contraband count and search count

cntrbnd_rte_unpivot[['Contraband Count', 'Search Count']] = cntrbnd_rte_unpivot['Contraband Count/Search Count'].str.split('/', expand=True)

cntrbnd_rte_final = cntrbnd_rte_unpivot.drop('Contraband Count/Search Count', axis=1)

cntrbnd_rte_final["Contraband Count"] = cntrbnd_rte_final["Contraband Count"].str.replace(",", "").astype(int)
cntrbnd_rte_final["Search Count"] = cntrbnd_rte_final["Search Count"].str.replace(",", "").astype(int)
cntrbnd_rte_final['Year'] = cntrbnd_rte_final['Year'].astype(object)

# %% Unpivot the Use of Force DataFrame
use_force_2 = pd.melt(use_force, id_vars=['Year', 'Stop Purpose'], value_vars=['Black', 'White', 'Latinx', 'Asian', 'Other', 'Indigenous'],
                     var_name='Race/Ethnicity', value_name='Use of Force Count')

use_force_2["Use of Force Count"] = use_force_2["Use of Force Count"].astype(int)

use_force_final = use_force_2.groupby(['Year', 'Race/Ethnicity'])[['Use of Force Count']].sum().reset_index()
use_force_final['Year'] = use_force_final['Year'].astype(object)

# %% Identify all unique values from the Race column in cmpd dataframes
unique_races = use_force_final['Race/Ethnicity'].unique()

# Identify all unique values from the Race column in charlotte population dataframe
unique_races_pop = clt_pop['Race'].unique()

# %% Define a mapping function to convert race values
def map_race(row):
    if row['Ethnicity'] == 'Hispanic or Latino':
        return 'Latinx'
    race_mapping = {
        'White Alone': 'White',
        'Black or African American Alone': 'Black',
        'American Indian & Alaska Native Alone': 'Indigenous',
        'Asian Alone': 'Asian',
        'Native Hawaiian & Other Pacific Islander Alone': 'Indigenous',
        'Some Other Race Alone': 'Other',
        'Two or More Races': 'Other'
    }
    return race_mapping.get(row['Race'], row['Race'])

# Apply the mapping function to the Race column
clt_pop['Race'] = clt_pop.apply(map_race, axis=1)
clt_pop["Population"] = clt_pop["Population"].astype(int)

clt_pop_final = clt_pop.groupby(['Year', 'Race'])[['Population']].sum().reset_index()

# Renaming the variable
clt_pop_final['Race/Ethnicity'] = clt_pop_final['Race']

# delete the old variable
del clt_pop_final['Race']

# %%  Merge dataframes
stp_cause_rte_clt_pop_merge = pd.merge(stop_cause_rte_final, clt_pop_final, on=['Year', 'Race/Ethnicity'])

cntrbnd_stp_cause_rte_merge = pd.merge(stp_cause_rte_clt_pop_merge, cntrbnd_rte_final, on=['Year', 'Race/Ethnicity'])

cntrbnd_stp_cause_rte_merge = cntrbnd_stp_cause_rte_merge.drop('Search Count_y', axis=1)

final_merge = pd.merge(cntrbnd_stp_cause_rte_merge, use_force_final, on=['Year', 'Race/Ethnicity'])

final_merge['Search Count'] = final_merge['Search Count_x'] 

final_merge = final_merge.drop('Search Count_x', axis=1)

# %% Calculate rates
final_merge["Stop Rate"] = ((final_merge["Stop Count"] / final_merge["Population"]) * 100).round(2)
final_merge["Search Rate"] = ((final_merge["Search Count"] / final_merge["Population"]) * 100).round(2)
final_merge["Search to Stop Rate"] = ((final_merge["Search Count"] / final_merge["Stop Count"]) * 100).round(2)
final_merge["Contraband Rate (of Searches)"] = ((final_merge["Contraband Count"] / final_merge["Search Count"]) * 100).round(2)
final_merge["Use of Force Rate (of Searches)"] = ((final_merge["Use of Force Count"] / final_merge["Search Count"]) * 100).round(2)
final_merge["Use of Force Rate (of Stops)"] = ((final_merge["Use of Force Count"] / final_merge["Stop Count"]) * 100).round(2)

# %% Specify the new order of columns
new_order = ["Year", "Race/Ethnicity", "Population", "Stop Count", "Search Count", "Contraband Count", "Use of Force Count", "Search Rate", "Stop Rate", "Search to Stop Rate", "Contraband Rate (of Searches)", "Use of Force Rate (of Searches)", "Use of Force Rate (of Stops)"]

# Reorder the DataFrame columns
cmpd_final = final_merge[new_order]

# %% Export DataFrame to CSV
cmpd_final.to_csv('data/cmpd_final.csv', index=False)

# %% Start App

# Set the page configuration
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# Switch Page

def switch_page(page: str):
    st.session_state.current_page = page

# Sidebar
summary_button = st.sidebar.button(
    "About this app".upper(), on_click=switch_page, args=["About this app"]
)

stops_button = st.sidebar.button(
    "CMPD Traffic Stops".upper(), on_click=switch_page, args=["stops"]
)

population_button = st.sidebar.button(
    "Charlotte Population".upper(), on_click=switch_page, args=["population"]
)

population_button = st.sidebar.button(
    "Explore on your own".upper(), on_click=switch_page, args=["self_explore"]
)

values = cmpd_final.select_dtypes(include=['number']).columns.tolist()
values = [col for col in values if col not in ('Year')]

features = cmpd_final.select_dtypes(include=['object']).columns.tolist()

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

stop_rate_trend = px.line(cmpd_final, x='Year', y='Stop Rate', color='Race/Ethnicity', title='Stop Rate')
stop_rate_trend.update_layout(xaxis_title='Year', yaxis_title='Stop Rate (%)')

search_rate_trend = px.line(cmpd_final, x='Year', y='Search Rate', color='Race/Ethnicity', title='Search Rate')
search_rate_trend.update_layout(xaxis_title='Year', yaxis_title='Search Rate (%)')
search_rate_trend.update_layout(showlegend=False)  # Remove legend from Search_Trend

@st.cache_resource

def summary():
        # Create three columns
    col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 2, 1])

    # Center the title
    st.markdown("<h1 style='text-align: center;'>Charlotte Mecklenberg Police Department (CMPD) Traffic Stops</h1>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center;">
            This app shows data related to historical CMPD traffic stops. There are options to analyze items based on your own selections, along with pre-built charts.
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Place the image in the center column
    with col3:
        st.image('data/CMPD Logo.jpeg', caption='CMPD Logo', width=200)
    

    st.subheader('CMPD Traffic Stops')
    st.write('The first section of the analysis provides insight into traffic stop data for the Charlotte Mecklenberg Police Department (CMPD). The analysis includes data pertinent to: traffic stops, traffic searches, use of force in these events, and the rate at which contraband was ultimately found (as a result of a traffic search).')
    st.write('Any citizen can be stopped, but those who are searched also have to have been stopped. Likewise, use of force can only happen if they have been stopped, and contraband can only be found if they are searched.')
    st.write('This data includes Charlotte gov information for the past 20 years and was pulled from: https://www.opendatapolicingnc.com/report?var=stateAbbreviation:NC&var=agencyTitle:Charlotte-Mecklenburg+Police+Department')
    
    st.subheader('Charlotte Population')
    st.write('The second section of the analysis dives into the overall population of Charlotte and looks at the rate of traffic stops and traffic searches based on the entire population.')
    st.write('The goal here is to highlight the differences between ethnicities, especially when accounting for the overarching % of population each ethnicity in Charlotte encompasses.')
    st.write('This data includes government census information for the past 10 years and was pulled from: https://datausa.io/profile/geo/charlotte-nc/')
        

def stops():

    st.title("Who's Getting Pulled Over in Charlotte?")
        
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

def population():

    st.title("Who Lives in Charlotte?")
        
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



def self_explore():
    
    #Initializing selected filters in session state
    if "selected_x_var" not in st.session_state:
        st.session_state.selected_x_var = None
    if "selected_y_var" not in st.session_state:
        st.session_state.selected_y_var = None
    
    selected_x_var = st.selectbox(
        "What do you want the x variable to be?",
        values,
        index=values.index(st.session_state.selected_x_var) if st.session_state.selected_x_var else 0
    )
    selected_y_var = st.selectbox(
        "What about the y?",
        values,
        index=values.index(st.session_state.selected_y_var) if st.session_state.selected_y_var else 0
    )

    st.session_state.selected_x_var = selected_x_var
    st.session_state.selected_y_var = selected_y_var


    alt_scatter = (
        alt.Chart(cmpd_final, title="Scatterplot")
        .mark_circle()
        .encode(
            x=alt.X(selected_x_var, scale=alt.Scale(zero=False)),
            y=alt.Y(selected_y_var, scale=alt.Scale(zero=False)),
            color="Race/Ethnicity",
        )
        .interactive()
    )
    st.altair_chart(alt_scatter, use_container_width=True)

    alt_trend = (
        alt.Chart(cmpd_final, title="Trend Line")
        .mark_line()
        .encode(
            x=alt.X('Year', scale=alt.Scale(zero=False), axis=alt.Axis(format='d')),
            y=alt.Y(selected_y_var, scale=alt.Scale(zero=False)),
            color="Race/Ethnicity",
        )
        .interactive()
    )
    
    st.altair_chart(alt_trend, use_container_width=True)


fn_map = {
    "summary": summary, 
    "stops": stops,
    "population": population,
    "self_explore": self_explore,
}

main_window  =st.container()
main_workflow = fn_map.get(st.session_state.current_page, summary)

main_workflow()

# %%
