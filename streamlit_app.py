import streamlit as st
import pandas as p
import requests as r
import snowflake.connector
from urllib.error import URLError

def get_fruityvice_data(this_fruit_choise):
    st.write('The user entered ', fruit_choice)
    fruityvice_response = r.get("https://fruityvice.com/api/fruit/" + this_fruit_choise)
    fruityvice_normalized = p.json_normalize(fruityvice_response.json())
    return fruityvice_normalized


st.title("Breakfast Favourites")

st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado toast')

my_fruit_list = p.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index("Fruit")

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
st.dataframe(fruits_to_show)

st.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = st.text_input('What fruit would you like information about?','Kiwi')
    if not fruit_choice:
        st.error("Select a food to get information!")
    else:
        result_fruitvice = get_fruityvice_data(fruit_choice)
        st.dataframe(result_fruitvice)        
except URLError as e:
    st.error(e)

#st.stop()
if st.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    my_cur = my_cnx.cursor()
    my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
    my_data_row = my_cur.fetchone()
    st.text("Hello from Snowflake:")
    st.text(my_data_row)

    add_my_fruit = st.text_input("What fruit would you like to add?", 'Apple')
    st.write("The fruit " + add_my_fruit + " is added.")

    my_cur.execute("insert into fruit_load_list values('from streamlit " + add_my_fruit + "')")

    my_cur.execute("select * from FRUIT_LOAD_LIST")
    my_data_rows = my_cur.fetchall()
    st.text("The fruit list contains:")
    st.text(st.dataframe(my_data_rows))
