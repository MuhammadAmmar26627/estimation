from pymongo import MongoClient
import streamlit as st
import pandas as pd
import uuid
from function_file import *


# Define functions to interact with MongoDB
def display_mongodb_data(collection):
    cursor = collection.find()
    documents = list(cursor)
    df = pd.DataFrame(documents)
    df.drop("_id", axis=1, inplace=True)
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
email_db = db['email_password']
# login_session = db['login_session']  # Collection to store login state

# Get or generate a unique session ID for the current user
# session_id = str(uuid.uuid4())

# Retrieve the session state
if 'login' not in st.session_state:
    st.session_state['login'] = False
    st.session_state['rate']= db['Material_Labour_rates']
    st.session_state['shipping_rate']= db['Shipping_rates']
    st.session_state["material_df_db"]=db['material']
    st.session_state["lab_df"]=db['labour']
    st.session_state["shiping_df"]=db['shipping']
    st.session_state["result"]=0

# Display login form
if not st.session_state['login']:
    placeholder = st.empty()
    with placeholder.container():
        email = st.text_input("Username or Email")
        pwd = st.text_input("Password", type="password")
        submit = st.button("Login")

        if submit:
            query = {"email": email, "password": pwd}
            result = email_db.find_one(query)
            st.session_state["result"]=result
            if result:
                # Set login state to True
                st.session_state['login'] = True
                placeholder.empty()
                # st.success("Welcome!")  # Display a success message
            else:
                st.error("Incorrect email or password. Please try again.")  # Display an error message

# Display main content if logged in
if st.session_state['login']:
    df=display_mongodb_data(st.session_state['rate'])
    # df.drop("_id", axis=1, inplace=True)
    lab_df=display_mongodb_data(st.session_state["lab_df"])
    # lab_df.drop("_id", axis=1, inplace=True)
    shiping_df=display_mongodb_data(st.session_state["shiping_df"])
    # shiping_df.drop("_id", axis=1, inplace=True)
    df_ship=display_mongodb_data(st.session_state['shipping_rate'])
    # df_ship.drop("_id", axis=1, inplace=True)
    st.session_state["material_df"]=display_mongodb_data(st.session_state["material_df_db"])
    # st.session_state["material_df"].drop("_id", axis=1, inplace=True)
    ################################

    ######## Client Data ###########
    # form=st.sidebar.form("Calculate Material and Labour")

    # Input fields
    st.sidebar.header("Packaging Estimation Sheet")
    st.sidebar.header("Client Bio")
    col1,col2=st.sidebar.columns(2)
    client_name=col1._text_input("Client Name")
    CSR=col2._text_input("CSR Name")
    col1,col2=st.sidebar.columns(2)
    client_email=col1._text_input("Client Email")
    Phone=col2._text_input("Phone Number")


    #####################################
    # col1,col2,col3=st.sidebar.columns(3)
    
    # rigid=col1.checkbox("Rigid")

    # custom=col2.checkbox("Sheet")
    # custom_p = st.sidebar.checkbox('Custom Print Size')



    ########### Sheet Data (Size) #############

    st.sidebar.header("Sheet Size")
    # if rigid:
    #     col1, col2 = st.sidebar.columns(2)
    #     Material_Rigid = col1.selectbox(
    #     "Material_Rigid",
    #     ["Grey Board",
    # "Bux Board",]
    # )
    #     gsm_rigid = col2.selectbox("GSM_Rigid",[900,1000,1200,1400,1600,1800,])
    #     col1, col2 = st.sidebar.columns(2)
    #     W_B=col1.number_input("Board_W", min_value=0.0)
    #     L_B=col2.number_input("Board_L", min_value=0.0)
    #     Board_size = st.sidebar.selectbox(
    #     "Board Size",
    #     [
    #     "5x5","8x8",'9x9','Custom']
    #     )
    #     if Board_size=="Custom":
    #         Custom_Labour_Rigid=st.sidebar.number_input("Custom Rate", min_value=0.0)
    #     col1, col2 = st.sidebar.columns(2)
    #     Material = col1.selectbox(
    #         "Material",
    #         [
    #         "Art Paper",]
    #         )
    #     gsm_list=[128,150,]
    #     gsm = col2.selectbox("GSM",gsm_list)
    #     col1, col2 = st.sidebar.columns(2)
    #     W_paper=col1.number_input("Paper_W", min_value=0.0)
    #     L_paper=col2.number_input("Paper_L", min_value=0.0)
    #     W_P=W_S=W_paper
    #     L_P=L_S=L_paper
    # else:
        # pass
    col1, col2 = st.sidebar.columns(2)
    Material = col1.selectbox(
        "Material",
        ["Bleached Card",
        "Bleached Card Pasted",
        "Bux Board",
        "Bux Board Pasted",
        "Art Card",
        "Grey Board",
        "Bux Board",
        "Kraft Local",
        "Kraft Imported",
        "Morocco",
        "Art Paper",
        "Rigid Box",]
        )
    # gsm_list=[210,230,250,270,300,350,420,460,500,540,600,700,]
    # if Material=="Art Paper":
    #     gsm_list=[128,150,]
    gsm = col2.number_input("GSM", min_value=0.0)
    # if custom:
    col1, col2 = st.sidebar.columns(2)
    W_S=col1.number_input("W_Sheet", min_value=0.0)
    L_S=col2.number_input("L_Sheet", min_value=0.0)
    # else:
        # col1, col2 = st.sidebar.columns(2)
        # Packets_size=["23x36","25x36","22x28",'20x30','25x30',"27x34"]
        # Packet = col1.selectbox( 
        #     "Sheet Size",
        #     Packets_size)
        # Sheet_size=[("9x7.66","11.5x7.2","12x7.66","9x11.5","11.5x12","12x23","18x23"),
        # ("9x8.33","12.5x7.5","12x8.33","9x12.5","12.5x12","12x25","18x25"),
        # ('9.33x7.33',"11x14","14x22"),("10x7.5","10x15",'10x20','15x20'),
        # ("10x8.33","10x12.5",'12.5x15','15x25'),('9x11.33','13.5x17','17x27')]

        # sheet_index=Packets_size.index(Packet)
        # # print(sheet_index)
        # sheet = col2.selectbox(
        #     "Sheet Size",
        #     Sheet_size[sheet_index])
        # pack=sheet.split("x")
        # # print(sheet)
        # W_S,L_S=float(pack[0]),float(pack[1])

    col1, col2 = st.sidebar.columns(2)
    W_P=col1.number_input("W_Print", min_value=0.0)
    L_P=col2.number_input("L_Print", min_value=0.0)


    col1, col2 = st.sidebar.columns(2)
    machine_selection=col1.selectbox("Machine_selection",["Sheet Size","Print Size",])
    up = col2.number_input("Box Uping", min_value=1)
    col1, col2 = st.sidebar.columns(2)
    Req_Q = col1.number_input("Required Quantity", min_value=1)
    Rigid_making = col2.number_input("Rigid Making", min_value=0)








    # submitted = st.sidebar.form_submit_button("Submit")
    ################################################
    # if not rigid:
    st.sidebar.header("Corrugation")
    col1, col2 = st.sidebar.columns(2)
    pasting = col1.selectbox(
        "Corrugation Pasting",
        ["None","Single Side", "Double Side",]
    )
    stock = col2.selectbox(
        "Corrugation Material",
        ["L1", "E Flute", "B Flute"]
    )
    # else:
    #     pasting="None"
    #     stock="L1"


    st.sidebar.header("Printing Colors")
    col1, col2, col3 = st.sidebar.columns(3)
    process_color = col1.selectbox(
        "Process Color",
        [0,1,2,3,4,5,6,7,8,]
    )
    pantone_color=col2.number_input("Pantone Color", min_value=0)
    matallic_color=col3.number_input("Matallic Color", min_value=0)


    st.sidebar.header("Add-Ons")
    col1, col2 = st.sidebar.columns(2)
    # Foil = col1.selectbox(
    #     "Foiling",
    #     ["None","Copper","Brass","Zinc"],
    #      index=0
    # )
    f_l=col1.number_input("Foiling_L", min_value=0.0)

    # st.write(W_S)

    f_w=col2.number_input("Foiling_W", min_value=0.0)
    col1, col2 = st.sidebar.columns(2)

    d_l=col1.number_input("Deboss_L", min_value=0.0)

    # st.write(W_S)

    d_w=col2.number_input("Deboss_W", min_value=0.0)
    col1, col2 = st.sidebar.columns(2)

    E_l=col1.number_input("Emboss_L", min_value=0.0)

    # st.write(W_S)

    E_w=col2.number_input("Emboss_W", min_value=0.0)
    col1, col2 = st.sidebar.columns(2)

    Uv_l=col1.number_input("UV_L", min_value=0.0)

    # st.write(W_S)

    Uv_w=col2.number_input("UV_W", min_value=0.0)
    col1, col2,col3 = st.sidebar.columns(3)
    window_die_cut=col1.selectbox(
        "Window Diecut",

        ["None","With PVC",])
    win_l=col2.number_input("Window_L", min_value=0.0)

    # st.write(W_S)

    win_w=col3.number_input("Window_W", min_value=0.0)
    ############ Lamination ##########
    st.sidebar.header("Lamination")
    col1,col2=st.sidebar.columns(2)
    inside=col1.selectbox(
        "Inside Lamination",
        ["None","Matte","Gloss","Soft Touch","Aqueous Coating",])
    outside=col2.selectbox(
        "Outside Lamination",
        ["None","Matte","Gloss","Soft Touch","Aqueous Coating",])

    ############ Additional Expense ##########

    st.sidebar.header("Additional Expense")
    col1, col2 = st.sidebar.columns(2)
    Mics = col1.number_input("Micsellneus", min_value=0)
    Profit_margin = col2.number_input("Profit Margin", min_value=0)
    col1, col2 = st.sidebar.columns(2)
    taping=col1.number_input("Taping", min_value=0.0)
    packing=col2.number_input("Packing", min_value=0.0)
    ################# Shipping ########################
    # st.sidebar.header("Shipping")
    # col1,col2=st.sidebar.columns(2)
    # Company=col1.selectbox(
    #     "Shipping company",
    #     ["FED EX","SKY Net","DHL",])
    # custom_weight=col2.number_input("Shipping box weight", min_value=0.0)
    # col1,col2,col3=st.sidebar.columns(3)
    # height=col3.number_input("height", min_value=0.0)
    # length=col1.number_input("length", min_value=0.0)
    # width=col2.number_input("width", min_value=0.0)
    ###################### Shipping ######################
    submitted = st.sidebar.button("Submit")


    ############ Calculation  #####################
    if submitted:
        if machine_selection=="Print Size":
            machine_rate=find_machine_size(W_P,L_P,st.session_state["df"])
        else:
            machine_rate=find_machine_size(W_S,L_S,st.session_state["df"])
        Sheets=Req_Q/up
        print_sheet=Print_Sheet_calculator(Sheets)
        laminate_sheet=Lamination_sheets_calculator(Sheets)
        process_color_rate,pantone_color_rate,matallic_color_rate=Printing_Calculator(machine_rate,process_color,pantone_color,matallic_color,print_sheet)
        lamination_price=Lamination_price_calculator(W_P,L_P,laminate_sheet,inside,outside,machine_rate)
        die_cut_price=Die_cut_price(print_sheet,machine_rate)
        pasting_material=Pasting_Calculator(machine_rate,Req_Q)
        UV_coating=UV_price(Uv_l,Uv_w,print_sheet,machine_rate)
        foiling=foil_price(f_l,f_w,laminate_sheet,machine_rate)
        Debosing=debosing_price(d_l,d_w,machine_rate,print_sheet)
        Embosing=embosing_price(E_l,E_w,machine_rate,print_sheet)
        carrug_lab=corgation_price(W_S,L_S,pasting,laminate_sheet,machine_rate)
        st.dataframe(machine_rate,hide_index=True)
        Custom_Labour_Rigid=Rigid_making*Req_Q
        ################### Table Update ################
        # print(st.session_state["lab_df"].columns)
        lab_df.set_index('index',inplace=True)
        # st.write(st.session_state["lab_df"].loc["Lam"])
        lab_df.loc["Printing"]=(process_color_rate,pantone_color_rate,matallic_color_rate,process_color_rate+pantone_color_rate+matallic_color_rate)
        lab_df.loc["Lam"]=(lamination_price[0],lamination_price[1],0,lamination_price[0]+lamination_price[1])
        lab_df.loc["Die cut"]=(die_cut_price,0,0,die_cut_price)
        lab_df.loc["Pasting"]=(pasting_material,0,0,pasting_material)
        lab_df.loc["Uv Coating"]=(UV_coating,0,0,UV_coating)
        lab_df.loc["Foiling"]=(foiling,0,0,foiling)
        lab_df.loc["Debossing"]=(Debosing,0,0,Debosing)
        lab_df.loc["Embossing"]=(Embosing,0,0,Embosing)
        lab_df.loc["Carrug Lab"]=(carrug_lab,0,0,carrug_lab)
        lab_df.loc["Packing"]=(0,0,0,packing)
        try:
            lab_df.loc["Rigid_making_labour"]=(Custom_Labour_Rigid,0,0,Custom_Labour_Rigid)
        except:
            lab_df.loc["Rigid_making_labour"]=(0,0,0,0)
        lab_df.loc["Lab Total"]=(0,0,0,lab_df.iloc[:-1,3].sum())
        lab_df.reset_index(inplace=True)

        # ##################### Shipping ###############################
        # # shipping_rate,weight=shipping_cost(W_P,L_P,gsm,Req_Q,df_ship,Company,custom_weight)
        # if (height!=0) or (width!=0) or (length!=0):
        #     shipping_rate,weight=shipping_cost_vol(length,width,height,Req_Q,df_ship,Company,custom_weight)
        #     shiping_df["Vol_Price"]=shipping_rate
        # else:
        #     shipping_rate,weight=shipping_cost(W_P,L_P,gsm,Req_Q,df_ship,Company,custom_weight)         
        #     shiping_df["Price"]=shipping_rate
        # shiping_df["Total weight"]=weight
        
        # #######################################################
        ctp=CTP_Plates_price(machine_rate,process_color,pantone_color,matallic_color)
        paper_price=paper_material(W_S,L_S,gsm,print_sheet,Material,machine_rate)
        die_making_price=Die_making_price(machine_rate)
        foil_block=foil_block_price(f_l,f_w,machine_rate)
        deboss_price_Material=DebossBlock_price(d_l,d_w,machine_rate)   ###############  Function should be updated
        emboss_price_Material=EmbossBlock_price(E_l,E_w,machine_rate)   ###############  Function should be updated
        Carrugation_price_Material=carrugation_price_Material(stock,W_S,L_S,laminate_sheet,machine_rate,pasting) ### Editing
        if window_die_cut=="None":
            pvc_total=0
        else:
            pvc_total=PVC(win_l,win_w,laminate_sheet,machine_rate)
        #########################################################
        st.session_state["material_df"].set_index('index',inplace=True)
        st.session_state["material_df"].loc["CTP Plates"]=(0,0,0,ctp)
        st.session_state["material_df"].loc["Paper"]=(0,paper_price,0,paper_price)
        st.session_state["material_df"].loc["Die Making"]=(0,die_making_price,0,die_making_price)
        st.session_state["material_df"].loc["Foil Block"]=(0,0,0,foil_block)
        st.session_state["material_df"].loc["DebossBlock"]=(0,0,0,deboss_price_Material)
        st.session_state["material_df"].loc["EmbossBlock"]=(0,0,0,emboss_price_Material)
        st.session_state["material_df"].loc["Carrugation"]=(0,0,0,Carrugation_price_Material)
        st.session_state["material_df"].loc["PVC Window"]=(0,0,0,pvc_total)
        st.session_state["material_df"].loc["D Tapes"]=(0,0,0,taping)
        st.session_state["material_df"].loc["Material"]=(0,0,0,st.session_state["material_df"].iloc[:-1,3].sum())

        st.session_state["material_df"].reset_index(inplace=True)
        # print(st.session_state["material_df"].iloc[:-1,4].sum())
        total=st.session_state["material_df"].iloc[:-1,4].sum()+lab_df.iloc[:-1,4].sum()
        # print(total)
        Profit_margin=1+Profit_margin/100
        total=total*Profit_margin
        cost_per_piece=total/Req_Q
        cost_per_piece=round(cost_per_piece, 2)
        #############################################
    else:
        print_sheet=laminate_sheet=total=cost_per_piece=0
    # total=st.session_state["material_df"].iloc[:-1,3].sum()+lab_df.iloc[:-1,3].sum()
    # Profit_margin=1+Profit_margin/100
    # total=total*Profit_margin
    # cost_per_piece=total/Req_Q
    ##########################################################
    col1, col2, col3, = st.columns(3)
    col1.metric("Sheet",print_sheet, laminate_sheet)
    col2.metric("Total",total, "")
    col3.metric("cost per Unit", cost_per_piece, "")
    # try:
        # col4.metric("shipping",shipping_rate,weight)
    # except:
        # col4.metric("shipping",0,0)
    col1, col2, col3 = st.columns(3)
    col1.metric("Material Cost",st.session_state["material_df"].iloc[:-1,4].sum(), "")
    col2.metric("Labour Cost",lab_df.iloc[:-1,4].sum(), "")
    col3.metric("Mics", Mics, "")
    # print(Mics)


    if st.session_state["result"].get("role")=="admin":
        col1,col2=st.columns(2)
        n_rows=13
        height = int(35.2*(n_rows+1))
        col1.header("Material Cost")
        col1.dataframe(st.session_state["material_df"], width=700, height=410,hide_index=True)
        # col1.dataframe(shiping_df, width=700,hide_index=True,)
        col2.header("Labour Cost")
        col2.dataframe(lab_df, width=700, height=height,hide_index=True)