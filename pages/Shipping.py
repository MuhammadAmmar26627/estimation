from pymongo import MongoClient
import streamlit as st
import pandas as pd
from function_file import shipping_cost,shipping_cost_vol
from estimator import display_mongodb_data

if (st.session_state['login']) and (st.session_state["result"].get("role")=="admin"):
    shiping_df=display_mongodb_data(st.session_state["shiping_df"])
    df_ship=display_mongodb_data(st.session_state['shipping_rate'])
    ################# Shipping ########################
    form = st.sidebar.form("my_form")
    form.header("Shipping")
    col1,col2=form.columns(2)
    gsm=col1.number_input("GSM", min_value=0.0)
    Req_Q=col2.number_input("Req Quantity", min_value=0.0)
    col1,col2=form.columns(2)
    Company=col1.selectbox(
        "Shipping company",
        ["FED EX","SKY Net","DHL",])
    custom_weight=col2.number_input("Shipping box weight", min_value=0.0)
    col1,col2,col3=form.columns(3)
    height=col3.number_input("height", min_value=0.0)
    length=col1.number_input("length", min_value=0.0)
    width=col2.number_input("width", min_value=0.0)
    # Every form must have a submit button.
    submitted = form.form_submit_button("Submit")
    if submitted:
            ##################### Shipping ###############################
        # shipping_rate,weight=shipping_cost(W_P,L_P,gsm,Req_Q,df_ship,Company,custom_weight)
            if (height!=0):
                shipping_rate,weight=shipping_cost_vol(length,width,height,Req_Q,df_ship,Company,custom_weight)
                shiping_df["Vol_Price"]=shipping_rate
            else:
                shipping_rate,weight=shipping_cost(length,width,gsm,Req_Q,df_ship,Company,custom_weight)         
                shiping_df["Price"].iloc[0]=shipping_rate
            shiping_df["Total weight"].iloc[0]=weight
            # st.dataframe(shiping_df, width=700,hide_index=True,)  
            st.write(weight)         
            #######################################################
    try:
        st.metric("shipping",shipping_rate,weight)
    except:
        st.metric("shipping",0,0)
    st.dataframe(shiping_df,hide_index=True,)
    ###################### Shipping ######################