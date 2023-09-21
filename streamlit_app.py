import streamlit as st
import pandas as pd
import plotly_express as px
import plotly.graph_objects as go

def plotOER(dataframe):
    st.header("Oil Extraction Rate Performance")

    fig = px.line(df, x="date", y="%_OER", color="mill_code")
    #fig.update_traces(textposition="bottom right")
    st.plotly_chart(fig)

def data_header(dataframe):
    st.header("Data Header")
    st.write(dataframe.head())


def data_plot(dataframe):
    x_axis_val = st.selectbox('Select X-Axis Value', options = df.columns)
    y_axis_val = st.selectbox('Select Y-Axis Value', options = df.columns)
    millcode = st.selectbox('Select Mill Code', options = dataframe['mill_code'].unique())


    #col = st.color_picker('Select a plot color')
    mill_code = dataframe.loc[dataframe['mill_code']==millcode]

    plot = px.scatter(mill_code, x=x_axis_val, y = y_axis_val)
    #plot.update_traces(marker=(dict(color=col)))
    st.plotly_chart(plot)

def home_page():
    st.write('OER = (Quality of Crop) + (Quality of Ripeness) + (Efficiency of Mill)')

st.title("Oil Extraction Rate Data Explorer")
st.text("This is a POC for OER by SDPKS")


st.sidebar.title('Navigation')
uploaded_file = st.sidebar.file_uploader("Upload your file here")

options = st.sidebar.radio('Operations', options=['Home','OER Performance', 'Data Header', 'Exploratory Plot'])


if uploaded_file:

    df= pd.read_csv(uploaded_file)


    #df["date"] = df["date"].astype('datetime64')
    #df["mill_code"] = df["mill_code"].astype('string')



if options == "OER Performance":
    plotOER(df)
elif options =='Data Header':
    data_header(df)
elif options == 'Exploratory Plot':
    data_plot(df)
elif options =='Home':
    home_page()
