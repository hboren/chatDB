import streamlit as st
import pandas as pd
import sqlite3
from pymongo import MongoClient
import json
import os

# Initialize MongoDB and SQLite configurations
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["your_database"]
mongodb_list = []
sqldb_list = []

# Helper function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv', 'json'}

# Function to store data in MongoDB
def store_in_mongodb(data, json_name):
    collection = mongo_db["data_collection"]
    collection.drop()  # Clear old data before inserting new
    collection.insert_many(data.to_dict(orient='records'))
    collectionName = json_name[:-5]
    mongodb_list.append(collectionName)

def make_sql_db(df, csv_name):
    conn = sqlite3.connect("sql")
    tableName = csv_name[:-4]
    print(tableName)
    df.to_sql(tableName, conn, if_exists='replace', index=False)
    sqldb_list.append()


# ------------------------------------------------------------------------------------------------------------------------------------



# Set up the main Streamlit app
st.title("ChatDB: Interactive Query Assistant")
st.write("Ask me anything about your database!\n\nFirst, upload a database \
         below, or choose from one of our default databases, Furniture (SQLite) or *** (MongoDB).\
         \n\nTo select a database, please type \"use\" and the name of your database. \
         ie. \"Use Furniture\"\n\nIf you are using a database of your own, the name \
         should be the name of your file including the extension.")

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Chat interface input box
user_input = st.text_input("Type your query here...")

# Process the user's input and add to chat history
if st.button("Submit"):
    if user_input:
        # Append user message to chat history
        st.session_state['chat_history'].append({"user": user_input})

        # Placeholder for handling user queries with the database
        response = "This is a placeholder response for your query."
        st.session_state['chat_history'].append({"bot": response})

# Display chat history
for chat in st.session_state['chat_history']:
    if "user" in chat:
        st.write(f"**You:** {chat['user']}")
    if "bot" in chat:
        st.write(f"**ChatDB:** {chat['bot']}")

# File upload section
st.write("----")
st.write("**Upload a CSV or JSON file to populate your database:**")
file = st.file_uploader("Choose a CSV or JSON file", type=["csv", "json"])

# Process the file upload
if file:
    filename = file.name
    if allowed_file(filename):
        if filename.endswith('.csv'):
            data = pd.read_csv(file)
        else:
            data = pd.read_json(file)

        # Button to store file data in the selected database
        if filename.endswith('.csv'):
            make_sql_db(data, filename)
            st.write("File successfully uploaded and stored in SQLite.")
        elif filename.endswith('.json'):
            store_in_mongodb(data, filename)
            st.write("File successfully uploaded and stored in MongoDB.")
    else:
        st.write("**BAD FILE TYPE** - Only CSV or JSON files are allowed.")
