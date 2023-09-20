import streamlit as st
import pandas as pd
import plotly_express as px

def stats(dataframe):
    st.header("Data Statistics")
    st.write(dataframe.describe())

def data_header(dataframe):
    st.header("Data Header")
    st.write(dataframe.head())


def data_plot(dataframe):
    x_axis_val = st.selectbox('Select X-Axis Value', options = df.columns)
    y_axis_val = st.selectbox('Select Y-Axis Value', options = df.columns)
    millcode = st.selectbox('Select Mill Code', options = dataframe['mill_code'].unique())


    #col = st.color_picker('Select a plot color')
    mill_042 = dataframe.loc[dataframe['mill_code']==millcode]

    plot = px.scatter(mill_042, x=x_axis_val, y = y_axis_val)
    #plot.update_traces(marker=(dict(color=col)))
    st.plotly_chart(plot)

st.title("Oil Extraction Rate Data Explorer")
st.text("This is a POC for OER by SDPKS")


st.sidebar.title('Navigation')
uploaded_file = st.sidebar.file_uploader("Upload your file here")

options = st.sidebar.radio('Operations', options=['Home','Data Statistics', 'Data Header', 'Plot'])


if uploaded_file:

    df= pd.read_csv(uploaded_file)


    df["date"] = df["date"].astype('datetime64')
    df["mill_code"] = df["mill_code"].astype('string')



if options == "Data Statistics":
    stats(df)
elif options =='Data Header':
    data_header(df)
elif options == 'Plot':
    data_plot(df)
