import plotly as plt
import streamlit as st
import pandas as pd
import functools
from locale import D_FMT
from plotly.subplots import make_subplots





from pickletools import float8
from sqlite3 import DatabaseError
from statistics import multimode
import plotly.express as px
import plotly.figure_factory as ff
from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objs as go
from plotly.graph_objs import *
from plotly.offline import init_notebook_mode, iplot
import altair as alt
from PIL import Image
from typing import List, Tuple
import requests
from streamlit_searchbox import st_searchbox


#Hash
import hashlib

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
        return False

#DB management 
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()

def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def add_userdata(username,password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
    conn.commit()

def login_user(username,password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
    data = c.fetchall()
    return data

def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data  


st.set_page_config(
    page_title="Self-medication",
    page_icon="🤳🏻",
    layout="wide",
)




def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv().encode('utf-8')

def main():

    st.title("Self-medication in Lebanon")


    menu = ["Home","Login","SignUp"]
    
    choice = st.sidebar.selectbox("Menu",menu)
    
    if choice == "Home":
        st.subheader("Home Page")
        st.write( "How Many times have you heard : Eh Bassita, sar maei nafs l shi akhadet hal dawa meshi hali!" )
        st.write("Which translates to: It's fine, I have been through the same thing and took this medication which I recommend ")
        st.write(" Knowing the circumstances and the habits that the Lebanese population have picked up over the year, Unicef has decided to do a survey to collect data about self-medication and raise the correct awarness to solve this issue. In this Web Application you will be able to deep dive into the analysis of this survey as well as a deep dive into the health facilies Available in Lebanon.  ")
        a1, a2, a3 = st.columns(3)
        a1.image(Image.open('download.png'))
        a2.image(Image.open('sign.png'))
        a3.image(Image.open('flag.png'))

        

    elif choice == "Login":
        st.subheader("Login Section")
        st.write("To access the Self-Medication Web App please Login")
        
        username = st.sidebar.text_input("User Name")
        
        password = st.sidebar.text_input("Password",type='password')

        if st.sidebar.checkbox("Login"):
            #if password == '12345':
            create_usertable()
            hashed_pswd = make_hashes(password)
            result = login_user(username,check_hashes(password,hashed_pswd))
            if result:



                st.success("Logged In as {}".format(username))
                task = st.selectbox("Task",['Explore the Dataset','Demographics Dashboard', 'Hazem Pharmacy Dashboard', 'Pharmacy Dashboard', 'Predictive model','Profiles'])
                
                if task == "Profiles":
                    st.subheader("User Profiles")
                    user_result = view_all_users()
                    clean_db= pd.DataFrame(user_result, columns=["Username","Password"])
                    st.dataframe(clean_db)
                elif task == "Explore the Dataset":
                    st.subheader("Self-medication Dataset")
                    dataframe = pd.read_csv("medication.csv")
                    dataframe2 = pd.read_csv("health.csv")
                    dataframe3= pd.read_csv("SalesClientsList.csv")
                    df=pd.DataFrame(dataframe)
                    df2=pd.DataFrame(dataframe2)
                    df3=pd.DataFrame(dataframe3)
                    st.subheader(' Raw data')  
                    if st.checkbox('Show raw data'):
                        st.subheader('Self Medication Raw data')
                        st.write(df)
                        st.subheader ('Health Facilities In Lebanon Raw Data')
                        st.write(df2)
                        st.subheader('Hazem Pharmacy Raw Data')
                        st.write(df3)
                    
                elif task == "Demographics Dashboard":
                    dataframe = pd.read_csv("medication.csv")
                    df=pd.DataFrame(dataframe)
                    st.subheader("Demographics Analysis")
                    income_filter,age_filter,education_filter = st.columns(3)
                    income_range = list(df.income.unique())
                    with income_filter:
                        income_filter = st.selectbox("Select the Income range", income_range)
                    df = df[df["income"] == income_filter]
                    age_range = list(df.age.unique())
                    with age_filter:
                        age_filter = st.selectbox("Select the age range", age_range)
                    df = df[df["age"] == age_filter]
                    education_level = list(df.Education.unique())
                    with education_filter:
                        education_filter = st.selectbox("Select the education level", education_level)
                    df = df[df["Education"] == education_filter]
                    
                    # create three columns
                    kpi1, kpi2, kpi3 = st.columns(3)
                    
                    Unique_residents=df.ID.nunique()
                    Number=df.insurance.value_counts().yes
                    chronic=df.chronic_disease.value_counts().yes
                    
                    kpi1.metric(
                        label="Unique Residents",
                        value= Unique_residents,
                         )
                    kpi2.metric(
                        label="Residents with Insurance",
                        value= Number,
                         )
                    kpi3.metric(
                        label="Residents with Chronic Disease",
                        value= chronic,
                         ) 
                    
                    #Column two
                    
                    fig_col1, fig_col2 = st.columns((5,5))
                    with fig_col1:
                        fig_col1= px.histogram(data_frame=df, x="sex", title="Gender")
                        st.write(fig_col1)
                    with fig_col2:
                      fig_col2= px.histogram(data_frame=df, x="self-medication", title="self-medication" )
                      st.write(fig_col2)
                    
                    #col 3

                    fig_col6, fig_col7 = st.columns(2)
                    with fig_col6:
                        fig_col6=px.histogram(
                            data_frame=df, x="accebility", title="accebility"
                        )
                        st.write(fig_col6)
                    with fig_col7:
                        fig_col7=px.histogram(
                            data_frame=df, x="prescription_to_others", title="prescription to others"
                        )
                        st.write(fig_col7)

                    value=df.groupby(['prescription_to_others']).size().reset_index(name='prescribe')

                    fig_col8, fig_col9, fig_col1 = st.columns(3)
                    with fig_col8:
                        fig_col8=px.histogram(
                            data_frame=df, x="residence", title="residence"
                        )
                        st.write(fig_col8)
                    with fig_col9:
                        fig_col9=px.histogram(
                            data_frame=df, x="reason", title="reason"
                        )
                        st.write(fig_col9)
                    with fig_col1:
                        fig_col1=px.histogram(
                            data_frame=df, x="drugs_used", title="drugs_used"
                        )
                        st.write(fig_col1)
                    
                    

                    
                    
                    

                    

                    

                elif task == "Pharmacy Dashboard":
                     dataframe2 = pd.read_csv("health.csv")
                     df2=pd.DataFrame(dataframe2)
                     df_new=df2[['Longitud_E','Latitude_N','Village','Short_Name']]
                     st.subheader('Number of Health Facilities per Governorate')
                     
                     df=df2[['Governorate','Name of Health Facility','Short_Name']]
                     
                     df_new2=df2.groupby(['Governorate']).size().reset_index(name='Number of Health Facilities')

                     data = pd.read_csv('pop.csv')
                     data2 = pd.read_csv('Pharmacy.csv')
                     fig2, fig3 = st.columns(2)
                     with fig2:
                        fig2 = px.histogram(
                            data_frame=df_new2, x='Governorate', y='Number of Health Facilities', title='Number of Health Facilities per Governorate'
                        )
                        st.write(fig2)
                    
                        
                     with fig3:
                        fig3 = px.bar(
                            data, x="Governorate", y="Population", color="Governorate",animation_frame="Year", animation_group="Governorate", range_y=[25,75]
                        )
                        st.write(fig3)



   


                     mapbox_access_token = 'pk.eyJ1IjoiYW1pcmJhenppIiwiYSI6ImNremIydG9ocTBocmwyd3M2NWY4amR5N2MifQ._mUJN0M6kAAzEYhAuLAwmQ'
                     site_lat = df2.Latitude_N
                     site_lon = df2.Longitud_E
                     table = ff.create_table(df2)
                     locations_name = df2.Village
                     location_short=df2.Short_Name

                     data = [
                        go.Scattermapbox(
                            lat=site_lat,
                            lon=site_lon,
                            mode='markers',
                            marker=dict(
                                size=17,
                                color='rgb(255, 0, 0)',
                                opacity=0.7
                            ),
                            text=locations_name,
                            hoverinfo='text'
                        ),
                        go.Scattermapbox(
                            lat=site_lat,
                            lon=site_lon,
                            mode='markers',
                            marker=dict(
                                size=8,color='rgb(242, 177, 172)',
                                opacity=0.7
                            ),
                            hoverinfo='none'
                        )]
                     layout = go.Layout(
                        title='Health facilities in Lebanon',
                        autosize=True,
                        hovermode='closest',
                        showlegend=False,
                        mapbox=dict(
                         accesstoken=mapbox_access_token,
                         bearing=0,
                         center=dict(
                             lat=33.8547,
                             lon=-35.8623
                            ),
                         pitch=0,
                         zoom=3,
                         style='light'
                        ),
                     )
                     fig = dict(data=data, layout=layout)
                     st.plotly_chart(fig)
                
                elif task == "Hazem Pharmacy Dashboard":
                    # function with list of tuples (label:str, value:any)
                    def search_wikipedia_ids(searchterm: str) -> List[Tuple[str, any]]:
                        # search that returns a list of wiki articles in dict form with information on title, id, etc.
                        response = requests.get(
                            "http://en.wikipedia.org/w/api.php",
                            params={
                                "list": "search",
                                "format": "json",
                                "action": "query",
                                "srlimit": 10,
                                "limit": 10,
                                "srsearch": searchterm,
                            },
                        ).json()["query"]["search"]

                     # first element will be shown in search, second is returned from component
                        return [
                            (
                                str(article["title"]),
                                article["pageid"],
                            )
                            for article in response
                        ]


                     # pass search function to searchbox
                    selected_value = st_searchbox(
                        search_wikipedia_ids,
                        key="wiki_searchbox",
                    )
                    st.markdown("You've selected: %s" % selected_value)

                    dataframe3= pd.read_csv("SalesClientsList.csv")

                    fig98 = px.histogram(
                            data_frame=dataframe3, x='Description', y='Quantity', title='Number of Health Facilities per Governorate'
                    )
                    st.write(fig98)
                    data2 = pd.read_csv('/Users/celine/Desktop/Pharmacy.csv')
                    governorate_option=data2['Location'].unique().tolist()
                    governorate= st.selectbox('Select Location', governorate_option, 0)
                    health=data2[data2['Location']==governorate]
                    st.write(data2)

                    
                    
                    


            
                     
                     
                    

                     
                    

            else:
                st.warning("Incorrect Username/Password")

            

    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username",key='1')
        new_password = st.text_input("Password",type='password',key='2')
        
        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user,make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")

        



if __name__ == "__main__":

    main()