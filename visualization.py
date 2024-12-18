import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output

# Load the datasets
demographics = pd.read_csv('north_Carolina_detailed_demographics.csv')
election = pd.read_csv('cleaned_election_results_summary.csv')

# Rename columns for clarity
rename_dict = {
    "K200101_001E": "pop",
    "K200103_001E": "med_age",
    "K201902_001E": "med_inc",
    "K202510_001E": "med_home_val",
    "K200201_002E": "white_pop",
    "K200201_003E": "black_pop",
    "K200201_004E": "native_pop",
    "K200201_005E": "asian_pop",
    "K200301_003E": "hispanic_pop",
    "K200301_001E": "hispanic_total",
    "K200101_002E": "male_pop",
    "K201501_008E": "masters_plus",
    "K201501_007E": "bachelors_plus",
    "K201803_002E": "stem_fields"
}
demographics.rename(columns=rename_dict, inplace=True)

# Clean and standardize county names
demographics['County_Name'] = demographics['County_Name'].str.upper().str.replace(' COUNTY, NORTH CAROLINA', '',
                                                                                  regex=True)
election['county'] = election['county'].str.upper()

# Merge both datasets on county name
merged_data = pd.merge(
    election,
    demographics,
    left_on='county',
    right_on='County_Name',
    how='outer'
)

# Load North Carolina FIPS codes
fips_data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/minoritymajority.csv')
nc_fips = fips_data[fips_data['STNAME'] == 'North Carolina'].copy()
nc_fips['County_Name'] = nc_fips['CTYNAME'].str.upper().str.replace(' COUNTY', '', regex=True)

# Merge to ensure proper FIPS matching
merged_data = pd.merge(
    nc_fips[['FIPS', 'County_Name']],
    merged_data,
    on='County_Name',
    how='left'
)

# Save the cleaned merged data to a CSV file
merged_data.to_csv('merged_nc_data.csv', index=False)

# Prepare data for plotting
merged_data['FIPS'] = merged_data['FIPS'].astype(str)  # Ensure FIPS codes are strings
geojson_url = "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"

# Initialize Dash App
app = dash.Dash(__name__)

# Data options for selection
data_options = {
    "Democratic Vote %": "pct_dem",
    "Population": "pop",
    "Median Age": "med_age",
    "Median Income": "med_inc",
    "Median Home Value": "med_home_val",
    "White Population": "white_pop",
    "Black Population": "black_pop",
    "Native Population": "native_pop",
    "Asian Population": "asian_pop",
    "Hispanic Population": "hispanic_pop",
    "Hispanic Total": "hispanic_total",
    "Male Population": "male_pop",
    "Masters Degree or Higher": "masters_plus",
    "Bachelors Degree or Higher": "bachelors_plus",
    "STEM Fields": "stem_fields"
}

# Layout for the app
app.layout = html.Div([
    html.H1("North Carolina County Demographics and Election Results", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Select Data to Display:"),
        dcc.Dropdown(
            id='data-selector',
            options=[{'label': key, 'value': value} for key, value in data_options.items()],
            value='pct_dem',  # Default value
            clearable=False
        )
    ], style={'width': '50%', 'margin': 'auto'}),

    dcc.Graph(id='choropleth-map', style={'height': '80vh'})
])


# Update the map based on selection
@app.callback(
    Output('choropleth-map', 'figure'),
    Input('data-selector', 'value')
)
def update_map(selected_metric):
    fig = px.choropleth(
        merged_data,
        geojson=geojson_url,
        locations='FIPS',
        color=selected_metric,
        hover_data=['County_Name', selected_metric],
        scope='usa',
        title=f'North Carolina County {selected_metric.replace("_", " ").title()}',
        color_continuous_scale='Viridis',
        labels={selected_metric: selected_metric.replace("_", " ").title()}
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        title_x=0.5,
        plot_bgcolor='rgb(229,229,229)',
        paper_bgcolor='rgb(229,229,229)'
    )
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
