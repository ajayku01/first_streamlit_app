import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Bluberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# The picker works, but the numbers don't make any sense! We want the customer to be able to choose the fruits by name!!
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
#We want to filter the table data based on the fruits a customer will choose, so we'll pre-populate the list to set an example for the customer. 
#We'll ask our app to put the list of selected fruits into a variable called fruits_selected. Then, we'll ask our app to use the fruits in our fruits_selected list to pull rows from the full data set (and assign that data to a variable called fruits_to_show). Finally, we'll ask the app to use the data in fruits_to_show in the dataframe it displays on the page. 

fruits_selected = streamlit.multiselect("Pick Some Fruits: ", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#Display the table on the page
streamlit.dataframe(fruits_to_show)


#New section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')

#Add a Text Entry Box and Send the Input to Fruityvice as Part of the API Call
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('the user entered',fruit_choice)


#import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
# streamlit.text(fruityvice_response.json())

#take json resonse and normalise it to look more like table and less like code
fruitvice_normalized = pandas.json_normalize(fruityvice_response.json())
#output of the above is a dataframe (table) not just text
streamlit.dataframe(fruitvice_normalized)

#dont run anything past here while we troubleshoot
streamlit.stop()

#import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.text("The fruit load list contains")
streamlit.dataframe(my_data_rows)

add_my_fruit = streamlit.text_input('What fruit you would like to add?','Jackfruit')
streamlit.write('Thanks for adding ',add_my_fruit)
#Add the new fruit into snowflake table

my_cur.execute("INSERT INTO FRUIT_LOAD_LIST VALUES('from streamlit')")
