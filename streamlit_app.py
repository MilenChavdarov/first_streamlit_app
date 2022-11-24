import streamlit as st
import pandas as p

st.title("Breakfast Favourites")

st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado toast')

my_fruit_list = p.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
st.dataframe(my_fruit_list)