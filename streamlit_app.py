import streamlit
import pandas
import requests 
import snowflake.connector
from urllib.error import URLError 

streamlit.title("My Parents New healthy Diner")
##Comment new update
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list=pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

#Let's put a pick list here so they can pick the fruit they want to include
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.Fruit),["Avocado", "Strawberries"])

#similar if set:
#my_fruit_list=my_fruit_list.set_index('Fruit')
#streamlit.multiselect("Pick some fruits:", list(my_fruit.index))
fruits_to_show=my_fruit_list.loc[my_fruit_list['Fruit'].apply(lambda x: x in fruits_selected)]
#similar approach if index set: fruits_to_show=my_fruit_list.loc[fruits_selected]
#display the table on the page
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
    #streamlit.write("The user entered: ", fruit_choice)
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
    #streamlit.text(fruityvice_response.json()) #just writes the data to the screen
    fruityvice_normalized=pandas.json_normalize(fruityvice_response.json())
    #output it the screen as a table
    return fruityvice_normalized

streamlit.header('Fruityvice Fruit Advice!')
try:
    fruit_choice=streamlit.text_input("What fruit would you like information about?")
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
        streamlit.dataframe(get_fruityvice_data(fruit_choice))

except URLError as e:
    streamlit.error()


#when using streamlit secrets then snowflake.connector.connect(**streamlit.secrets["snowflake"])


streamlit.header("View Our Fruit List - Add Your Favorites!")
def get_fruit_load_list(snowflake_connection):
    my_cur=snowflake_connection.cursor()
    my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
    my_data_row=my_cur.fetchone()
    my_data_rows=my_cur.fetchall()
    return my_data_rows

if streamlit.button("Get Fruit Load List"):
    try:
        my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
        streamlit.dataframe(get_fruit_load_list(my_cnx))
    except:
        streamlit.error()

def insert_row_snowflake(snowflake_connection,new_fruit):
    my_cur=snowflake_connection.cursor()
    my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('"+new_fruit+"')")
    return "Thanks for adding: " + new_fruit

add_my_fruit=streamlit.text_input("What fruit would you like to add?", "jackfruit")
if streamlit.button("Add Fruit to Load List"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    streamlit.write(insert_row_snowflake(my_cnx,add_my_fruit))
#