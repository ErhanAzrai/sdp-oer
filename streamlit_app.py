import streamlit as st
import pandas as pd
import plotly_express as px
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title= 'OER Rocks!',
    page_icon = "tada"
)

def plotOER(dataframe):
    st.header("Oil Extraction Rate Performance")
    st.write('Oil extraction rate (OER) and kernel extraction rate (KER) are two indicators of efficiency which can indirectly influence the profitability of any plantation enterprise. Being an integrated oil palm venture, this is of prime importance, because the final arbiter of commercial success is the oil yield per ha and not just FFB yield per ha alone.')

    fig = px.line(df, x="date", y="%_OER", color="mill_code")
    st.plotly_chart(fig)
    st.write("OER hovers around 17-22 handle")


    df['date'] = pd.to_datetime(df['date'])
    #df.set_index('date', inplace =True)
    #df_monthly = df.resample('M').mean()
    

    df_monthly = df.groupby(pd.PeriodIndex(df['date'], freq="M")).mean()
    st.write(df_monthly.head())

    #fig = px.line(df_monthly, y="%_OER")
    #st.plotly_chart(fig)



def keyStats(dataframe):
    st.header("Key Operation Indicators")
    st.write("These are important indicators in a palm oil mills")

    st.subheader('Quality of the Crop')



    dt = df[['date','A_Crop%', 'mill_code']]
    dt['Crop_A%'] = dt.groupby('mill_code')['A_Crop%'].rolling(window=28).mean().reset_index(level=0, drop=True)
    figCropA = px.line(dt, x="date", y = "Crop_A%", color = "mill_code", title="Crop A as Percentage of Total (28-day moving average)")
    st.plotly_chart(figCropA)
    st.write('For a each mill, Crop A has a positive correlation with Oil Extraction Rate. One percentage point increase in Crop A, increases OER by between 0.2 and 0.4 point')

    st.subheader('Quality of Ripeness')

    dt = df[['date','Pct_Ripe', 'mill_code']]
    dt['Ripe%'] = dt.groupby('mill_code')['Pct_Ripe'].rolling(window=28).mean().reset_index(level=0, drop=True)
    figRipe = px.line(dt, x="date", y = "Ripe%", color = "mill_code", title="Ripe as Percentage of Total (28-day moving average)")
    st.plotly_chart(figRipe)

    dt = df[['date','Pct_OverRipe', 'mill_code']]
    dt['moving_ave'] = dt.groupby('mill_code')['Pct_OverRipe'].rolling(window=28).mean().reset_index(level=0, drop=True)
    figOverripe = px.line(dt, x="date", y = "moving_ave", color = "mill_code", title="Overripe A as Percentage of Total (28-day moving average)")
    st.plotly_chart(figOverripe)

    st.subheader('Mill Operation')

    dt = df[['date','Average_mill_press_throughput', 'mill_code']]
    dt['moving_ave'] = dt.groupby('mill_code')['Average_mill_press_throughput'].rolling(window=28).mean().reset_index(level=0, drop=True)
    figOverripe = px.line(dt, x="date", y = "moving_ave", color = "mill_code", title="Average mill press throughput (28-day moving average)")
    st.plotly_chart(figOverripe)


    st.metric(
        label = 'OER',
        value = 70,
        delta = 1.2,
        help="Oil Extraction Rate changes month over month"
    )
    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", "70 °F", "1.2 °F")
    col2.metric("Wind", "9 mph", "-8%")
    col3.metric("Humidity", "86%", "4%")

    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write("Hello")


def data_plot(dataframe):
    x_axis_val = st.selectbox('Select X-Axis Value', options = df.columns)
    y_axis_val = st.selectbox('Select Y-Axis Value', options = df.columns)
    millcode = st.selectbox('Select Mill Code', options = dataframe['mill_code'].unique())


    #col = st.color_picker('Select a plot color')
    mill_code = dataframe.loc[dataframe['mill_code']==millcode]

    plot = px.scatter(mill_code, x=x_axis_val, y = y_axis_val)
    #plot.update_traces(marker=(dict(color=col)))
    st.plotly_chart(plot)

def home_page(dataframe):
    st.write('OER = (Quality of Crop) + (Quality of Ripeness) + (Efficiency of Mill)')
    
    homecol1, homecol2 = st.columns([3,1])
    with homecol2:
       millcode = option_menu('Select Mill Code', options = dataframe['mill_code'].unique().tolist())

    

st.title("Mill Statistics Data Explorer")
st.text("This is a POC for OER by SDPKS")



st.sidebar.title('Navigate')
uploaded_file = st.sidebar.file_uploader("Upload your file here")

with st.sidebar:
    options = option_menu(None, options=['Home','OER Performance', 'Key Stats', 'Exploratory Plot'])


if uploaded_file:

    df= pd.read_csv(uploaded_file)


    #df["date"] = df["date"].astype('datetime64')
    #df["mill_code"] = df["mill_code"].astype('string')

    if options == "OER Performance":
        plotOER(df)
    elif options =='Key Stats':
        keyStats(df)
    elif options == 'Exploratory Plot':
        data_plot(df)
    elif options =='Home':
        home_page(df)

else: 
    st.write("<--- Please upload the input file")