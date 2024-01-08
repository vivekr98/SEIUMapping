import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go


zipcodes = pd.read_csv('zipcodes.csv')
zipcodes['Zipcodes'] = zipcodes['Zipcodes'].astype(str)
shapefile_path = 'California_Zip_Codes/California_Zip_Codes.shp'

schools = pd.read_csv('schools.csv')

# Read the shapefile into a GeoDataFrame
gdf = gpd.read_file(shapefile_path)

# Assuming your DataFrame 'df' has a column named 'zipcode' containing the zip codes you want to filter
zipcodes_to_filter = zipcodes['Zipcodes']

# Filter the GeoDataFrame based on the list of zip codes
filtered_gdf = gdf[gdf['ZIP_CODE'].astype(str).isin(zipcodes_to_filter)]


fig = px.scatter_mapbox(
    schools,
    lat='Latitude',
    lon='Longitude',
    color='SchoolType',
    hover_name='SchoolName',
    hover_data=['SchoolType'],
    mapbox_style="carto-positron",
    title='Schools in California by Type',
)

for feature in gdf.geometry.to_crs('EPSG:4326').__geo_interface__["features"]:
    fig.add_trace(go.Choroplethmapbox(
        geojson=feature,
        locations=[0],  # The location value doesn't matter, as we use geojson
        showscale=False,
        marker_opacity=0,
        hoverinfo='skip'
    ))

fig.show()