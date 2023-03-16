import geopandas as gpd
import plotly.express as px
import streamlit as st

victoria_data = gpd.read_file("filtered_DATA/v_data_small.shp")
fire_data = gpd.read_file("filtered_FIRE/v_fire_small.shp")


st.markdown('## People and Fires in Victoria ')
st.markdown("""
The red shapes on the map indicate areas of actual (not percentage) population increase between the 2016 and 2021 census.
The black shapes are areas of high bushfire activity.


Data was gathered from the abs and datashare.maps.vic.gov.au

Note: The 2021 census occured in unique circumstances which may impact data reliability.""")


fig = px.choropleth_mapbox(victoria_data, 
                           geojson=victoria_data.geometry, 
                           locations= victoria_data.index, 
                           color=victoria_data.pop_change,
                           color_continuous_scale=["white", "red"],
                           range_color=(0, 50),
                           mapbox_style="open-street-map",
                           zoom=6.8, 
                           center = {"lat": -37.8136, "lon": 144.9631},
                           opacity=0.5,
                           custom_data = ['SA2_NAME21','Tot_P_P_21','pop_change']
                          )


fig.update_geos(fitbounds="locations", visible=False).update_layout(
    margin={"l": 0, "r": 0, "t": 0, "b": 0}
)

fig.update_traces(hovertemplate = 'Greater Region: %{customdata[0]}<br>%{customdata[1]} people in 2021<br>%{customdata[2]} more than in 2016',marker_line_width=0)


fig2 = px.choropleth_mapbox(fire_data, 
                           geojson=fire_data.geometry, 
                           locations= fire_data.index, 
                           color_discrete_sequence=['black'],
                           mapbox_style="open-street-map",
                           zoom=6, 
                           center = {"lat": -37.8136, "lon": 144.9631},
                           opacity=1,
                           hover_name = 'FIRETYPE',
                           hover_data = ['AREA_HA','CR_DATE']
                          )


fig2.update_geos(fitbounds="locations", visible=False).update_layout(
    margin={"l": 0, "r": 0, "t": 0, "b": 0}
)

trace0 = fig2 # the second map from the previous code

fig.add_trace(trace0.data[0])

fig.layout.update(showlegend=False)


st.plotly_chart(fig, use_container_width=False, sharing="streamlit", theme="streamlit")
