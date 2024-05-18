import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import os
from PIL import Image
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="AirBnb-Analysis by Uma!!!", page_icon=":bar_chart:", layout="wide")

st.title(":bar_chart: AirBnb-Analysis")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Sidebar menu
SELECT = option_menu(
    menu_title=None,
    options=["Home", "Explore Data", "Contact"],
    icons=["house", "bar-chart", "at"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "white"},
        "icon": {"color": "black", "font-size": "20px"},
        "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
        "nav-link-selected": {"background-color": "#6F36AD"}
    }
)

# Home section
if SELECT == "Home":
    st.header('Airbnb Analysis')
    st.subheader("Airbnb is an American San Francisco-based company operating an online marketplace for short- and long-term homestays and experiences. The company acts as a broker and charges a commission from each booking. The company was founded in 2008 by Brian Chesky, Nathan Blecharczyk, and Joe Gebbia. Airbnb is a shortened version of its original name, AirBedandBreakfast.com. The company is credited with revolutionizing the tourism industry, while also having been the subject of intense criticism by residents of tourism hotspot cities like Barcelona and Venice for enabling an unaffordable increase in home rents, and for a lack of regulation.")
    st.subheader('Skills take away From This Project:')
    st.subheader('Python Scripting, Data Preprocessing, Visualization, EDA, Streamlit, MongoDb, PowerBI or Tableau')
    st.subheader('Domain:')
    st.subheader('Travel Industry, Property management and Tourism')

# Explore Data section
if SELECT == "Explore Data":
    fl = st.file_uploader(":file_folder: Upload a file", type=["csv", "txt", "xlsx", "xls"])
    if fl is not None:
        if fl.name.endswith('.csv'):
            df = pd.read_csv(fl)
        elif fl.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(fl)
        else:
            st.error("Unsupported file format.")
    else:
        try:
            df = pd.read_csv(r"C:\Users\Administrator\Desktop\uma\sample_airbnb.csv", encoding="ISO-8859-1")
        except FileNotFoundError:
            st.error("File not found. Please upload a file.")

    if fl is not None or df is not None:
        st.sidebar.header("Choose your filter:")

        neighbourhood_group = st.sidebar.multiselect("Pick your neighbourhood_group", df["neighbourhood_group"].unique())
        neighbourhood = st.sidebar.multiselect("Pick the neighbourhood", df[df["neighbourhood_group"].isin(neighbourhood_group) if neighbourhood_group else df["neighbourhood_group"].unique()]["neighbourhood"].unique())

        filtered_df = df[(df["neighbourhood_group"].isin(neighbourhood_group) if neighbourhood_group else df.index) &
                         (df["neighbourhood"].isin(neighbourhood) if neighbourhood else df.index)]

        room_type_df = filtered_df.groupby(by=["room_type"], as_index=False)["price"].sum()

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("room_type_ViewData")
            fig = px.bar(room_type_df, x="room_type", y="price", text=['${:,.2f}'.format(x) for x in room_type_df["price"]],
                         template="seaborn")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("neighbourhood_group_ViewData")
            fig = px.pie(filtered_df, values="price", names="neighbourhood_group", hole=0.5)
            fig.update_traces(text=filtered_df["neighbourhood_group"], textposition="outside")
            st.plotly_chart(fig, use_container_width=True)

        cl1, cl2 = st.columns((2))
        with cl1:
            with st.expander("room_type wise price"):
                st.write(room_type_df.style.background_gradient(cmap="Blues"))
                csv = room_type_df.to_csv(index=False).encode('utf-8')
                st.download_button("Download Data", data=csv, file_name="room_type.csv", mime="text/csv", help='Click here to download the data as a CSV file')

        with cl2:
            with st.expander("neighbourhood_group wise price"):
                neighbourhood_group_df = filtered_df.groupby(by="neighbourhood_group", as_index=False)["price"].sum()
                st.write(neighbourhood_group_df.style.background_gradient(cmap="Oranges"))
                csv = neighbourhood_group_df.to_csv(index=False).encode('utf-8')
                st.download_button("Download Data", data=csv, file_name="neighbourhood_group.csv", mime="text/csv", help='Click here to download the data as a CSV file')

        # Create a scatter plot
        data1 = px.scatter(filtered_df, x="neighbourhood_group", y="neighbourhood", color="room_type")
        data1.update_layout(title="Room_type in the Neighbourhood and Neighbourhood_Group wise data using Scatter Plot.",
                            titlefont=dict(size=20), xaxis=dict(title="Neighbourhood_Group", titlefont=dict(size=20)),
                            yaxis=dict(title="Neighbourhood", titlefont=dict(size=20)))
        st.plotly_chart(data1, use_container_width=True)

        with st.expander("Detailed Room Availability and Price View Data in the Neighbourhood"):
            st.write(filtered_df.iloc[:500, 1:20:2].style.background_gradient(cmap="Oranges"))

        # Download original DataSet
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button('Download Data', data=csv, file_name="Data.csv", mime="text/csv")

        import plotly.figure_factory as ff

        st.subheader(":point_right: Neighbourhood_group wise Room_type and Minimum stay nights")
        with st.expander("Summary_Table"):
            df_sample = df[0:5][["neighbourhood_group", "neighbourhood", "reviews_per_month", "room_type", "price", "minimum_nights", "host_name"]]
            fig = ff.create_table(df_sample, colorscale="Cividis")
            st.plotly_chart(fig, use_container_width=True)

        # Map function for room_type
        st.subheader("Airbnb Analysis in Map view")
        df = df.rename(columns={"Latitude": "lat", "Longitude": "lon"})
        st.map(df)

# Contact section
if SELECT == "Contact":
    Name = "Name : UMAMAGESHWARI.S"
    mail = "Mail : seenuma2506@gmail.com"
    description = "An Aspiring DATA-SCIENTIST..!"

    col1, col2 = st.columns(2)
    col1.image(Image.open(r"C:\Users\Administrator\Desktop\uma\452.jpg"), width=300)

    with col2:
        st.header('Airbnb Analysis')
        st.subheader("This project aims to analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive geospatial visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends.")
        st.write("---")
        st.subheader(Name)
        st.subheader(mail)

    st.write("#")
    social_media = {
        "LinkedIn": "https://www.linkedin.com/",
        "GitHub": "https://github.com/",
        "Twitter": "https://twitter.com/"
    }
    cols = st.columns(len(social_media))
    for index, (platform, link) in enumerate(social_media.items()):
        cols[index].write(f"[{platform}]({link})")
