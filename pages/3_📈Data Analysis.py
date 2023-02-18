import streamlit as st
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


#Page configurations
st.set_page_config(
    page_title="Data Analysis",
    page_icon="📈",
)

def plot_linear_regression(df, x, y, type):
    """
    Create linear regression model and graph area, beds, and baths against price for all properties of a given type
    :param df:
    :param x:
    :param y:
    :param type:
    :return:
    """
    df2 = df.loc[df['Type'] == type].dropna(how='any') #Remove all 0 and NA values and extract selected property data subset from dataframe
    X = df2[x] #Set x variable
    y = df2[y] #Set y variable
    X_train, X_test, y_train, y_test, = train_test_split(X, y, test_size=0.2, random_state=42) #Split data set into testing and training data for x and y
    lr = LinearRegression() #Linear regression
    lr.fit(X_train, y_train) #Fit training data
    predictions = lr.predict(X_test) #Predict prices from x test data
    plot = px.scatter(x=y_test, y=predictions, trendline='ols') #Plot x test predictions against y test data
    st.plotly_chart(plot) #Plot the data

def plot_specific(df, x, y):
    """
    Plots user selected information field against price for each property type
    :param df:
    :param x:
    :param y:
    :return:
    """
    df2 = df[[x, y, 'Type']].dropna(how='any') #Remove all NA values from dataframe
    plot = px.scatter(data_frame=df2, x=x, y=y, color='Type') #Plot user selected x variable against price
    st.plotly_chart(plot) #Plot data


st.title("Data Analysis")

df = st.session_state['df'] #Access dataframe from session state
st.dataframe(df) #Display dataframe

generate_csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Export as CSV", #Button to generate csv file
                   generate_csv,
                   file_name='properties_analysis.csv',
                   mime= 'text/csv')


user_x = st.sidebar.selectbox('X Variable', ['Area', 'Beds', 'Baths']) #Selection box for user to select x variable
user_type = st.sidebar.selectbox('Type', ['Land/Lot', 'House', 'Retail', 'Land/Lot', 'Townhouse']) #Selection box for user to select property type


col1, col2 = st.columns(2) #Create two columns
with col1: #Display linear regression graph
    st.subheader(f'Linear Regression of Area, Beds, and Baths for {str(user_type)} Properties')
    plot_linear_regression(df, ['Area', 'Beds', 'Baths'], 'Price', user_type)
with col2: #Display graph for specific information field
    st.subheader(f'Scatter plot of {str(user_x)} for Properties')
    plot_specific(df, user_x, 'Price', )












