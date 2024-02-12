import streamlit as st
import pandas as pd

st.title("""
Welcome to my web app, In this app, we analyze the price of houses in 'Newyork city'   
""")

st.write("---")
st.header("First, Install library using `pip`")

st.markdown("---")
st.header("Second, Import library")

st.markdown("---")
st.header("Import dataframe")
df = pd.read_csv("NY-House-Dataset.csv")
st.dataframe(df)
st.markdown("---")

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

st.markdown("---")

st.header("Correlation")
expander = st.expander(label="Correlation plot", expanded=False)
x_axis = expander.selectbox(label="Select value for X axis", options=["PRICE","BEDS","BATH","PROPERTYSQFT"])
y_axis = expander.selectbox(label="Select value for Y axis", options=["PRICE","BEDS","BATH","PROPERTYSQFT"])

if len(x_axis) > 0 and len(y_axis) > 0:
    expander.scatter_chart(data=df, x=x_axis, y=y_axis)
