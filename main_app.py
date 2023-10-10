import streamlit as st 
import mysql.connector
import pandas as pd

import pandas as pd
import plotly.express  as px
from PIL import Image
import csv

cnx = mysql.connector.connect(
    user="root",
    password="Krishna@9011",
    host="localhost",
    database="movies"
)
cursor = cnx.cursor()

add_selectbox = st.sidebar.selectbox(
    "What would you like to know ?",
    ("Main","All Info about a movie", "Top 10 earners from 2017-2020", "Highest Earner 2017-2020",
     "Total number of movies released in each year from 2017-20","Movie Recommendation", "Movies with your favourite actor/actress", "Highest Runtime Movies"
     ,"Highest Openings","Movie Summary")
)

st.title('Bollywood MetaData 2017 - 2020 :sunglasses:')
st.divider()
if add_selectbox == "Main":
    st.image("1.png",width=1000)
elif add_selectbox == "All Info about a movie":
    st.subheader('Seach for your Movie Data')
    
    movie_name = st.text_input("Enter Movie Name")
    get_movie_details = pd.read_sql_query("select * from bollywood_box_clean WHERE movie_name = '%s'" % movie_name,cnx)
    
    if movie_name != "":
        st.caption('Note : All monetary values are in Cr')
        st.write(get_movie_details)

elif add_selectbox == "Top 10 earners from 2017-2020":
    st.title('Top 10 earners from 2017-2020')
    get_top10_movies = ("select movie_name,concat(movie_total_worldwide,' ','cr') as Total from bollywood_box_clean order by movie_total_worldwide desc limit 10")
    cursor.execute(get_top10_movies)

    results = cursor.fetchall()
    st.table(results)
    sheet_name = 'data'
    excel_file1="top101.xlsx"
    sheet_name1='top'
    df_top=pd.read_excel(excel_file1,
               sheet_name==sheet_name1,
                 usecols="A:B",
                 header=0)
    
    pie_chart = px.pie(df_top,
                   title='Top 10 Box-Office Collector',
                   values='collections',
                   names='movies')
    st.plotly_chart(pie_chart)

elif add_selectbox == "Highest Earner 2017-2020":
    st.title('Highest Earner 2017-2020')
    get_top = ("select movie_name from bollywood_box_clean order by movie_total_worldwide desc limit 1")
    get_top1 = pd.read_sql_query("select movie_total_worldwide from bollywood_box_clean order by movie_total_worldwide desc limit 1",cnx)
    cursor.execute(get_top)

    res = cursor.fetchall()
    for row in res:
        st.title(row[0])
        
        st.image("padmavat.jpg",width=300)

elif add_selectbox == "Total number of movies released in each year from 2017-20":
    st.title("Total number of movies released in each year from 2017-20")
    total_movie_releases = pd.read_sql_query("select release_year,count(movie_name) as Number_Of_Movies from bollywood_box_clean group by release_year",cnx)
    
    st.table(total_movie_releases)
    # for row in res:
    #     st.title(row)

elif add_selectbox == "Movie Recommendation":
    genre = st.radio("Whats your mood",('Comedy','Romance','Action','Drama','Thriller','Horror','Period','Biographical','Crime','Musical','Social'),horizontal=True)
    search = f'%{genre}%'
    cursor.execute(("select movie_name from bollywood_box_clean WHERE movie_genre like '%s'" % search))
    res1 = cursor.fetchall()
    for k in res1:
        st.subheader(f"{k[0]}")

elif add_selectbox == "Movies with your favourite actor/actress":
    actor_name = st.text_input("Enter Actor's Name")
    search_term = f'%{actor_name}%'
    cursor.execute(("select movie_name,actors from bollywood_box_clean WHERE actors like '%s'" % search_term))
    if actor_name != "":
        res = cursor.fetchall()
        for r in res:
            st.dataframe(r,width=1000)

elif add_selectbox == "Highest Runtime Movies":
    st.subheader("Highest Runtime Movies")
    runtime = pd.read_sql_query("select movie_name,runtime from bollywood_box_clean order by runtime desc limit 3",cnx)
    st.dataframe(runtime)

elif add_selectbox == "Highest Openings":
    st.subheader("Highest Openings")
    openings = pd.read_sql_query("select movie_name,movie_opening from bollywood_box_clean order by movie_opening desc limit 5",cnx)
    st.dataframe(openings)

elif add_selectbox == "Movie Summary":
    st.subheader('Movie Summary')
    
    mov_name = st.text_input("Enter Movie Name")
    cursor.execute("select movie_details from bollywood_box_clean WHERE movie_name = '%s'" % mov_name)
    get_dets = cursor.fetchall()

    if mov_name != "":
        for i in get_dets:
            st.header(mov_name)
            st.subheader(i[0])
