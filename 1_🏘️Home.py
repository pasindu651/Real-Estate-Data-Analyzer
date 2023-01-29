import streamlit as st

st.set_page_config(
    page_title="Real Estate App",
    page_icon = "🏘️",
)
st.sidebar.success("Select a page above.")

st.title("Web Scraper + AI Real Estate App")
st.header("Introduction")
st.markdown(
    """
    A small project I created in January of 2023 for scraping, analyzing, and visualizing housing prices in Canada. The program consists of three parts, which are the following:
    \n🚩**Part 1:** Scrape housing prices and information based on user location (beds, baths, square footage).
    \n🚩**Part 2:** Filter the data for null values and parse it into a data frame.
    \n🚩**Part 3:** Conduct linear regression for specific property types, using the square footage, number of bedrooms and bathrooms as the x variable, and the price as the dependent variable.
    \n🚩**Part 4:** Graph specific information fields as a scatter plot sorted by different property types.
    """
)
st.image("https://i.ibb.co/z6TssC2/web-scraping-about.png")

st.header("Tools Used")
st.markdown(
    """
    The following tools were used in the development of this application:
    \n🚩Streamlit was used for the front-end.
    \n🚩Selenium was used to handle dynamic web elements and passed to a Beautiful Soup object.
    \n🚩Beautiful soup was used to scrape listing information from Selenium HTML.
    \n🚩Pandas was used for data analysis and manipulation.
    \n🚩Plotly, in combination with Streamlit was used for graphing and interactive data visualization.
    \n🚩Sklearn was used for linear regression and data testing and training.
    """
)

st.image("https://i.ibb.co/WPsPm4R/newplot-2.png")
st.caption("Scatter plot output for **area vs price** of **land** in **Toronto, Ontario**.")
st.image("https://i.ibb.co/z5pxfQh/newplot.png")
st.caption("Linear regression output for **houses** in **Toronto, Ontario**.")


