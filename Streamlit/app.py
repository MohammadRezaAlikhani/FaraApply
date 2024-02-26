# Import packages
import streamlit as st
import pandas as pd
import folium
import streamlit_folium as st_folium


st.title("""
Welcome to my web app, In this app, we analyze the price of houses in 'Newyork city'   
""")

st.divider()
st.header("First, Install library using `pip`")

st.divider()
st.header("Second, Import library")

st.divider()
st.header("Information table")

df = pd.read_csv("NY-House-Dataset.csv")
st.dataframe(df)
st.map(data=df, latitude="LATITUDE", longitude="LONGITUDE")
st.divider()

st.header("Aggregation")
expander = st.expander(label="Aggregation", expanded=False)
house_type = expander.multiselect(label="House type", options=df["TYPE"].unique())
agg_func = expander.radio("Select aggregation function", ["Mean","Max","Min"])

if len(house_type) > 0:
    if agg_func == "Mean":
        sample = df[df["TYPE"].isin(house_type)].groupby(by="TYPE")["PRICE"].mean()
    if agg_func == "Max":
        sample = df[df["TYPE"].isin(house_type)].groupby(by="TYPE")["PRICE"].max()
    if agg_func == "Min":
        sample = df[df["TYPE"].isin(house_type)].groupby(by="TYPE")["PRICE"].min()

    expander.bar_chart(sample)

st.divider()

st.header("Correlation")
expander = st.expander(label="Correlation plot", expanded=False)
x_axis = expander.selectbox(label="Select value for X axis", options=["PRICE","BEDS","BATH","PROPERTYSQFT"])
y_axis = expander.selectbox(label="Select value for Y axis", options=["PRICE","BEDS","BATH","PROPERTYSQFT"])

if len(x_axis) > 0 and len(y_axis) > 0:
    expander.scatter_chart(data=df, x=x_axis, y=y_axis)

st.divider()
st.header("Filter properties on map")
expander = st.expander(label="Select filter", expanded= False)

# create filter
sub_loc = expander.selectbox(label="Sub locality", options=df["SUBLOCALITY"].unique())

# filter dataframe
df_filtered = df[(df["SUBLOCALITY"] == sub_loc)]
expander.map(data=df_filtered, latitude="LATITUDE", longitude="LONGITUDE", color=[1.0, 0.5, 0, 0.2])


st.divider()
st.header("Folium in Streamlit")

# Folium in Streamlit
center_map = folium.Map(location=[40.761255,-73.974483])

for index, row in df_filtered.iterrows():
    folium.Marker(location=[row["LATITUDE"], row["LONGITUDE"]],
                popup=f'Lat: {row["LATITUDE"]}, Lon: {row["LONGITUDE"]}',
                tooltip=f'Lat: {row["LATITUDE"]}, Lon: {row["LONGITUDE"]}').add_to(center_map)

    st_folium.st_folium(center_map)