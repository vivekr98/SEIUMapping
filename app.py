import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import geopandas as gpd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Read the California zip code shapefile
libraries_df = pd.read_csv('libraries.csv')

# Read the schools data into a DataFrame
schools_df = pd.read_csv('schools_new.csv')
#schools_df['Zip'] = schools_df['Zip'].astype(str)
#schools_df['Latitude'] = schools_df['Latitude'].astype(int)
#schools_df['Longitude'] = schools_df['Longitude'].astype(int)

print(schools_df['Latitude'])

# Merge schools data with zip code GeoDataFrame
school_zipcodes = schools_df['Zip'].unique()

# Filter libraries dataset based on school ZIP codes
filtered_libraries_df = libraries_df[libraries_df['Zip'].isin(school_zipcodes)]

# Append the filtered libraries dataset to the bottom of the school dataset
merged_df = pd.concat([schools_df, filtered_libraries_df], ignore_index=True)


# Create Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    # Dropdown for selecting regions
    dcc.Dropdown(
        id='city_dropdown',
        options=[
            {'label': city, 'value': city} for city in merged_df['County'].unique()
        ],
        value=merged_df['County'].unique()[0],  # Initial value
        style={'width': '50%'}
    ),
    # Map
    dcc.Graph(id='map', style={'height': '100vh'}),
])

# Define callback to update map based on dropdown selection
@app.callback(
    Output('map', 'figure'),
    [Input('city_dropdown', 'value')]
)
def update_map(selected_city):
    # Filter the DataFrame based on the selected region
    filtered_df = merged_df[merged_df['County'] == selected_city]

    print("Updating map for:", selected_city)
    #print("Filtered DataFrame:", filtered_df)


    # Create a scatter mapbox plot
    fig = px.scatter_mapbox(
        merged_df,
        lat='Latitude',
        lon='Longitude',
        color='Type',
        hover_name='Name',
        hover_data=['Type'],
        mapbox_style="carto-positron",
        title='Schools and Libaries in California by SEIU Zip Codes',
    )

    # Set map layout
    fig.update_layout(
        mapbox_zoom=10,  # Adjust as needed
        mapbox_center={"lat": filtered_df['Latitude'].mean(), "lon": filtered_df['Longitude'].mean()},
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)

server = app.server