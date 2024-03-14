from pymongo import MongoClient
import streamlit as st
import pandas as pd
import uuid

# Define functions to interact with MongoDB
def display_mongodb_data(collection):
    cursor = collection.find()
    documents = list(cursor)
    df = pd.DataFrame(documents)
    return df

def update_by_kg(KG, col, price, collection):
    query = {"KG": KG}
    new_values = {"$set": {col: price}}
    collection.update_one(query, new_values)

def update_by_machine_size(machine_size, col, price, collection):
    query = {"Machine_size": machine_size}
    new_values = {"$set": {col: price}}
    collection.update_one(query, new_values)

def update_all(col, price, collection):
    query = {}
    new_values = {"$set": {col: price}}
    collection.update_many(query, new_values)

# Connect to MongoDB
client = MongoClient("mongodb+srv://muhammadammarmalik1:cOLtj3dW7KVvfXZJ@cluster0.sri1w80.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['Estimation']
st.session_state['rate']= db['Material_Labour_rates']
st.session_state['shipping_rate']= db['Shipping_rates']
# email_db = db['email_password']
# login_session = db['login_session']  # Collection to store login state

# Get or generate a unique session ID for the current user
# session_id = str(uuid.uuid4())

# Retrieve the session state
# if 'login' not in st.session_state:
#     st.session_state['login'] = False
#     st.session_state['rate']= db['Material_Labour_rates']
#     st.session_state['shipping_rate']= db['Shipping_rates']
#     st.session_state["result"]=0

# # Display login form
# if not st.session_state['login']:
#     placeholder = st.empty()
#     with placeholder.container():
#         email = st.text_input("Username or Email")
#         pwd = st.text_input("Password", type="password")
#         submit = st.button("Submit")

#         if submit:
#             query = {"email": email, "password": pwd}
#             result = email_db.find_one(query)
#             st.session_state["result"]=result

#             if result:
#                 # Set login state to True
#                 st.session_state['login'] = True
#                 placeholder.empty()
#                 # st.success("Welcome!")  # Display a success message
#             else:
#                 st.error("Incorrect email or password. Please try again.")  # Display an error message

# Display main content if logged in
if (st.session_state['login']) and (st.session_state["result"].get("role")=="admin"):
    # rate = db['Material_Labour_rates']
    # shipping_rate = db['Shipping_rates']

    df = display_mongodb_data(st.session_state['rate'])
    df.drop("_id", axis=1, inplace=True)
    df_ship = display_mongodb_data(st.session_state['shipping_rate'])
    df_ship.drop("_id", axis=1, inplace=True)

    form = st.sidebar.form("Rate Update")
    m_size = form.selectbox("Machine Size", ["12x17", "23x17", "25x36", "28x40", "35x45", "40x56"])
    Col = form.selectbox("Feature", df.columns[1:10])
    price = form.number_input("Rate")
    submitted = form.form_submit_button("Submit")
    if submitted:
        try:
            update_by_machine_size(m_size, Col, price, st.session_state['rate'])
        except Exception as e:
            print(e)

    form1 = st.sidebar.form("Rate_Update")
    Col = form1.selectbox("Feature", df.columns[10:])
    price = form1.number_input("Rate")
    submit = form1.form_submit_button("Submit")
    if submit:
        try:
            update_all(Col, price, st.session_state['rate'])
        except Exception as e:
            print(e)

    form2 = st.sidebar.form("Rate_Update_ship")
    Col = form2.selectbox("Feature", df_ship.columns[4:])
    price = form2.number_input("Rate")
    submit = form2.form_submit_button("Submit_ship")
    if submit:
        try:
            update_all(Col, price, st.session_state['shipping_rate'])
        except Exception as e:
            print(e)

    form3 = st.sidebar.form("Shiping_Rate Update")
    kg = form3.selectbox("Kg", [1, 2, 5, 10, 15, 20, 25])
    Col = form3.selectbox("Feature", df_ship.columns[1:4])
    price = form3.number_input("Rate")
    submitted = form3.form_submit_button("Submit")
    if submitted:
        try:
            update_by_kg(kg, Col, price, st.session_state['shipping_rate'])
        except Exception as e:
            print(e)


    df = display_mongodb_data(st.session_state['rate'])
    df.drop("_id", axis=1, inplace=True)
    df_ship = display_mongodb_data(st.session_state['shipping_rate'])
    df_ship.drop("_id", axis=1, inplace=True)
    st.dataframe(df.iloc[:, :10], hide_index=True)
    st.dataframe(df.iloc[:1, 10:17], hide_index=True)
    st.dataframe(df.iloc[:1, 17:26], hide_index=True)
    st.dataframe(df.iloc[:1, 26:34], hide_index=True)
    st.dataframe(df.iloc[:1, 34:], hide_index=True)
    st.dataframe(df_ship, hide_index=True)