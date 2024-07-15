#!/usr/bin/env python
# coding: utf-8

# # Importing Libraries

# In[1]:


import os
from dotenv import load_dotenv
import spacy
import mysql.connector
import google.generativeai as genai
import re

# Load environment variables
load_dotenv()


# # Google API Configuration and Conversational Bot initialisation

# In[2]:


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])


# # Creating the Database Connection

# In[26]:


def create_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password=os.getenv("ROOT_PASSWORD"),
        database="26ideas",
        auth_plugin='mysql_native_password'
    )


# # Executing the SQL Query

# In[4]:


def execute_sql_query(sql):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
#     print("SQL Query Result:", result)  # Debug statement
    return result


# # Querying Gemini to generate the SQL Query from User Prompt

# In[5]:


def get_gemini_response(question, prompt):
    response = model.generate_content([prompt, question])
#     print("Gemini Response:", response)  # Debug statement
    return response.text.strip()


# # Cleaning the Returned SQL Query

# In[6]:


def clean_sql_query(sql_query):
    cleaned_query = re.sub(r'```', '', sql_query)
    cleaned_query = re.sub(r'^\s*sql\s*', '', cleaned_query, flags=re.IGNORECASE)
#     print("Cleaned SQL Query:", cleaned_query.strip())  # Debug statement
    return cleaned_query.strip()


# # Creation of The Context to be passed again to Gemini to return the final ans.

# In[7]:


def context_construction(data):
    context = ""
    for row in data:
        context += ", ".join(f"{key}: {value}" for key, value in row.items()) + "\n"
#     print("Constructed Context:", context)  # Debug statement
    return context


# # Passing the prompt to Gemini to generate the final response.

# In[8]:


def query_gemini(prompt, chat_session, stream=True):
    if stream:
        response = chat_session.send_message(prompt, stream=True)
        full_response = ''
        for chunk in response:
            full_response += chunk.text
#         print("Query Gemini Full Response:", full_response)  # Debug statement
        return full_response
    else:
        response = chat_session.send_message(prompt)
#         print("Query Gemini Response:", response.text)  # Debug statement
        return response.text


# # Main Function (Integrating everything)

# ### Adding the session_data, i.e history of the last mentioned, if no new mentions of the person or company, then the last mentioned is used. For example :- What is his designation?

# In[20]:


def handle_conversation(user_input, chat_session, session_data, stream=True):
    prompt = ogPrompt
    
    # Generating the SQL Query from the User Input
    
    sql_query = get_gemini_response(user_input, prompt)
    cleaned_query = clean_sql_query(sql_query)

    try:
        results = execute_sql_query(cleaned_query)
#         print(cleaned_query)
#         print(results)

# Construction of Context

        context = context_construction(results)
#         print(context)
        
        # Generating the FINAL Prompt
        enhanced_prompt = f"The user asked: {user_input}\n\This is the output of the User's Query from the database. This means that this is the answer to the question Uer has asked:\n{context}\nProvide a nice formatted answer to this question only based on this data to give it back to the User."
        response = query_gemini(enhanced_prompt, chat_session, stream)
        print("Gemini Enhanced Response:", response) 
        

    except Exception as e:
        print(f"Error executing SQL query: {e}")


# ### The prompt used to generate the SQL Query

# In[21]:


ogPrompt=''' 
    You are an expert in converting English questions to SQL queries!
    
        The SQL database has the following tables - newContacts and Company.
        See the Name of the columns and then give the query. Ensure that the SQL code does not include the word "sql" and does not have triple backticks (```).
        Where the schemas of both the table are are: newContacts (
            id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            designation VARCHAR(255),
            city VARCHAR(255),
            state VARCHAR(255),
            country VARCHAR(255),
            pincode VARCHAR(255),
            address TEXT,
            tags TEXT, /* can be investor, freelancer, developer, accountants, consultant */
            priority VARCHAR(255),
            companyId VARCHAR(255),
            FOREIGN KEY (companyId) REFERENCES Company(id)

        );
    
        Company (

            id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            domain VARCHAR(255) UNIQUE NOT NULL,
            domain_info TEXT,
            linkedin VARCHAR(255),
            type TEXT /*-- software, healthcare, venture studio, etc. */
        );
    
        Example questions:
    
        - How many entries of records are present in newContacts?
        - Give the list of all companies
        - List all companies in the software sector.

'''


# In[25]:


print("Chat session started. Type 'exit' to end the session.")
session_data = {}
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        print("Chat session ended.")
        break
    handle_conversation(user_input, chat, session_data)

