import streamlit as st
import pandas as pd
import math
import os
st.set_page_config(layout="wide")
# if "df" not in st.session_state:
#   if os.path.exists("Rate.csv"):
#       st.session_state["df"]=pd.read_csv("Rate.csv")
#   else:
#       st.session_state["df"]=pd.read_csv("rate_.csv")
#       st.session_state["df"].to_csv("Rate.csv",index=False)


####################### Shipping ###################
@st.cache_data
def shipping_cost_vol(w_s,l_s,height,Qty,shiping_df,company_name,custom_weight_add):
    try:
        weight= ((w_s*l_s*height*2.54*2.54*2.54)/5000*Qty)+custom_weight_add
        # print(w_s,(w_s*2.54))
#         (shiping_df[material].iloc[0]))
        # if "material"!="Art Paper":
        #     weight= int(w_s*l_s*height/15500*Qty/100)+custom_weight_add
        # else:
        #     weight= int(w_s*l_s*height/3100*Qty/500)+custom_weight_add
        # name=f'{company_name}_Vol'
        # print(name)
        # print("##################################",shiping_df[name])
        if weight<=1:
            price=(shiping_df[company_name].iloc[0])*weight
        elif weight<=2:
            price=(shiping_df[company_name].iloc[1])*weight
        elif weight<=5:
            price=(shiping_df[company_name].iloc[2])*weight
        elif weight<=10:
            price=(shiping_df[company_name].iloc[3])*weight
        elif weight<=15:
            price=(shiping_df[company_name].iloc[4])*weight
        elif weight<=20:
            price=(shiping_df[company_name].iloc[5])*weight
        elif weight<=25:
            price=(shiping_df[company_name].iloc[6])*weight
        else:
            price=(shiping_df[company_name+"_Vol"].iloc[0])*weight
        return int(price),weight
    except Exception as e:
        print(e)
        return 0,0

@st.cache_data
def shipping_cost(w_s,l_s,gms,Qty,shiping_df,company_name,custom_weight_add):
    try:
#         (shiping_df[material].iloc[0]))
        if "material"!="Art Paper":
            weight= (w_s*l_s*gms/15500*Qty/100)+custom_weight_add
        else:
            weight= (w_s*l_s*gms/3100*Qty/500)+custom_weight_add
        # name=f'{company_name}_Vol'
        # print(name)
        # print("##################################",shiping_df[name])
        if weight<=1:
            price=(shiping_df[company_name].iloc[0])*weight
        elif weight<=2:
            price=(shiping_df[company_name].iloc[1])*weight
        elif weight<=5:
            price=(shiping_df[company_name].iloc[2])*weight
        elif weight<=10:
            price=(shiping_df[company_name].iloc[3])*weight
        elif weight<=15:
            price=(shiping_df[company_name].iloc[4])*weight
        elif weight<=20:
            price=(shiping_df[company_name].iloc[5])*weight
        elif weight<=25:
            price=(shiping_df[company_name].iloc[6])*weight
        else:
            price=(shiping_df[company_name+"_Vol"].iloc[0])*weight
        return int(price),weight
    except Exception as e:
        # print(e)
        return 0,0
# @st.cache_data
# def carrugation_price_Material(stock,w_s,l_s,laminate_sheet,machine_rate,pasting):
#     if pasting=="None":
#         return 0
#     else:
#         return int(machine_rate[stock].iloc[0]*laminate_sheet*w_s*l_s/2400)
####################################################
@st.cache_data
def carrugation_price_Material(stock,w_s,l_s,laminate_sheet,machine_rate,pasting):
    if pasting=="None":
        return 0
    else:
        return int(machine_rate[stock].iloc[0]*laminate_sheet*w_s*l_s/2400)
    # if stock=="L1":
    #     return int(w_s*l_s*laminate_sheet/2400*70)
    # elif stock=="E Flute":
    #     return int(w_s*l_s*laminate_sheet/2400*120)
    # elif stock=="B Flute":
    #     return int(w_s*l_s*laminate_sheet/2400*120)
    # else:
    #     return 0
@st.cache_data
def EmbossBlock_price(w_p,l_p,machine_rate):
    if (w_p>=1) and (l_p>=1):
        return int(w_p*l_p*machine_rate["Block_making"].iloc[0])
    else:
        return 0
@st.cache_data
def DebossBlock_price(w_p,l_p,machine_rate):
    if (w_p>=1) and (l_p>=1):
        return int(w_p*l_p*machine_rate["Block_making"].iloc[0])
    else:
        return 0
@st.cache_data
def foil_block_price(w_p,l_p,machine_rate,):
    # print(w_p)
    if ((w_p>=1) and (l_p>=1)):
        return int(w_p*l_p*machine_rate["Block_making"].iloc[0])
    else:
        return 0
@st.cache_data
def Die_making_price(machine):
    try:
        return machine["Die Making"].iloc[0]
    except Exception as e:
        print(e)
        return 0

@st.cache_data
def paper_material(w_s,l_s,gms,print_sheet,material,machine,):
    # print(material=="Bleached Card")
    # print(machine.columns)
    try:
        if "material"!="Art Paper":
            return int(w_s*l_s*gms/15500*print_sheet/100*(machine[material].iloc[0]))
        else:
            return int(w_s*l_s*gms/3100*print_sheet/500*(machine[material].iloc[0]))
    except:
        return 0
    # if gms<=350 and material=="Bleach Card":
    #     return int(w_s*l_s*gms/15500*print_sheet/100*(400))
    # elif gms>350 and material=="Bleach Card":
    #     return int(w_s*l_s*gms/15500*print_sheet/100*(450))
    # elif gms<=350 and material=="Bux Board":
    #     return int(w_s*l_s*gms/15500*print_sheet/100*(350))
    # elif gms>350 and material=="Bux Board":
    #     return int(w_s*l_s*gms/15500*print_sheet/100*(425))
    # elif gms<=350 and material=="Kraft":
    #     return int(w_s*l_s*gms/15500*print_sheet/100*(350))
    # elif gms>350 and material=="Kraft":
    #     return int(w_s*l_s*gms/15500*print_sheet/100*(425))
    # elif gms<=350 and material=="Art Card":
    #     return int(w_s*l_s*gms/15500*print_sheet/100*(350))
    # elif gms>350 and material=="Art Card":
    #     return int(w_s*l_s*gms/15500*print_sheet/100*(425))
    # else:
    #     return 0

@st.cache_data
def CTP_Plates_price(Machine,process_color,pantone_color,matallic_color):
    try:
        # print(process_color,pantone_color,matallic_color)
        return Machine["CTP"].iloc[0]*(process_color+pantone_color+matallic_color)
    except Exception as e:
        # print(e)
        return 0

@st.cache_data
def corgation_price(w_s,l_s,pasting,Lamination_sheet,machine_rate):
    try:
        if pasting=="Single Side":
            # print(w_s*l_s*machine_rate["carugation_pasting_rate"].iloc[0]*Lamination_sheet/2400)
            return int(w_s*l_s*machine_rate["carugation_pasting_rate"].iloc[0]*Lamination_sheet/2400)
        elif pasting=="Double Side":
            # print(machine_rate["carugation_pasting_rate"].iloc[0]*2)
            return int(2*w_s*l_s*machine_rate["carugation_pasting_rate"].iloc[0]*Lamination_sheet/2400)
        else:
            # print(machine_rate["carugation_pasting_rate"].iloc[0]*0)
            return 0
    except Exception as e:
        return 0
@st.cache_data
def embosing_price(E_l,E_w,Machine,print_sheet):
    try:
        if (E_l>=1) and (E_w>=1):
        # as printing rate is per 1170 and below list show us that if printing rate is 1400 and we have sheets 3350 it is below 4387 so we multply its index+1 to rate
            sheet_list =[1170, 2310, 3300, 4387, 5360, 6405, 7500, 8500, 9532, 10529, 11500, 12500, 13553, 14595, 15742, 16680, 17723, 18765, 19808, 20850, 21893, 22935, 23978, 25020, 26167, 27105, 28252, 29294, 30233, 31275, 32318, 33360, 34403, 35485, 36488, 37634, 38677, 39719]
            for i in sheet_list:
                if print_sheet<=i:
                    factor=sheet_list.index(i)+1
                    break
            return Machine["Embos"].iloc[0]*factor
        else:
            return 0
    except:
        return 0
@st.cache_data
def debosing_price(d_w,d_l,Machine,print_sheet):
    try:
        if (d_w>=1) and (d_l>=1):
        # as printing rate is per 1170 and below list show us that if printing rate is 1400 and we have sheets 3350 it is below 4387 so we multply its index+1 to rate
            sheet_list =[1170, 2310, 3300, 4387, 5360, 6405, 7500, 8500, 9532, 10529, 11500, 12500, 13553, 14595, 15742, 16680, 17723, 18765, 19808, 20850, 21893, 22935, 23978, 25020, 26167, 27105, 28252, 29294, 30233, 31275, 32318, 33360, 34403, 35485, 36488, 37634, 38677, 39719]
            for i in sheet_list:
                if print_sheet<=i:
                    factor=sheet_list.index(i)+1
                    break
            return Machine["Debos"].iloc[0]*factor
        else:
            return 0
    except:
        return 0
@st.cache_data
def foil_price(f_l,f_w,laminate_sheet,machine_rate):
    if ((f_l>=1) and (f_w>=1)):
        return int(f_l*f_w*laminate_sheet*machine_rate["Foil_A"].iloc[0])
    else:
        return 0
    
def UV_price(UV_L,UV_W,print_sheet,machine_rate):
    try:
        if (UV_L>=1) and (UV_W>=1):
            # print(int(UV_L*UV_W*printable_quantity*machine_rate["UV_price"][0]))
            return int(UV_L*UV_W*print_sheet*machine_rate["UV / Spot UV"].iloc[0])
        else:
            return 0
    except:
        return 0
@st.cache_data   
def Pasting_Calculator(Machine,Req_Q):
    try:
        thresholds = [
            1050, 2100, 3150, 4200, 5250, 6300, 7350, 8400, 9450, 10500,
            11500, 12500, 13500, 14500, 15500, 16500, 17500, 18500, 19600,
            20700, 21700, 22700, 23978, 25020, 26167, 27105, 28252, 29294,
            30233, 31275, 32318, 33360, 34403, 35485, 36488, 37634, 38677, 39719
        ]
        for i, threshold in enumerate(thresholds, start=1):
            if Req_Q <= threshold:
                factor=i
                break
        return Machine["Pasting"].iloc[0]*i
    except:
        return 0
@st.cache_data
def Die_cut_price(print_sheet,Machine):
    try:
        # as printing rate is per 1170 and below list show us that if printing rate is 1400 and we have sheets 3350 it is below 4387 so we multply its index+1 to rate
        sheet_list =[1170, 2310, 3300, 4387, 5360, 6405, 7500, 8500, 9532, 10529, 11500, 12500, 13553, 14595, 15742, 16680, 17723, 18765, 19808, 20850, 21893, 22935, 23978, 25020, 26167, 27105, 28252, 29294, 30233, 31275, 32318, 33360, 34403, 35485, 36488, 37634, 38677, 39719]
        for i in sheet_list:
            if print_sheet<=i:
                factor=sheet_list.index(i)+1
                break
        return Machine["Die Cut"].iloc[0]*factor
    except:
        return 0
@st.cache_data
def Lamination_sheets_calculator(sheet):
    try:
        if sheet <= 100:
            return math.ceil(sheet * 0.5 + sheet)
        elif sheet <= 200:
            return math.ceil(sheet * 0.5 + sheet)
        elif sheet <= 300:
            return math.ceil(sheet * 0.4 + sheet)
        elif sheet <= 400:
            return math.ceil(sheet * 0.2 + sheet)
        elif sheet <= 500:
            return math.ceil(sheet * 0.2 + sheet)
        elif sheet <= 600:
            return math.ceil(sheet * 0.18 + sheet)
        elif sheet >= 650 and sheet <= 1000:
            return math.ceil(sheet * 0.15 + sheet)
        elif sheet >= 1000 and sheet <= 1500:
            return math.ceil(sheet * 0.1 + sheet)
        elif sheet >= 1500 and sheet <= 2000:
            return math.ceil(sheet * 0.12 + sheet)
        elif sheet >= 2000 and sheet <= 3000:
            return math.ceil(sheet * 0.08 + sheet)
        elif sheet >= 3000 and sheet <= 4000:
            return math.ceil(sheet * 0.04 + sheet)
        elif sheet >= 4000 and sheet <= 7000:
            return math.ceil(sheet * 0.04 + sheet)
        elif sheet > 7000:
            return math.ceil(sheet * 0.025 + sheet)
        else:
            return sheet
    except:
        return 0
@st.cache_data
def Print_Sheet_calculator(sheet):
    try:
        if sheet <= 100:
            return math.ceil(sheet * 1.5 + sheet)
        elif sheet <= 200:
            return math.ceil(sheet * 1.0 + sheet)
        elif sheet <= 300:
            return math.ceil(sheet * 0.65 + sheet)
        elif sheet <= 400:
            return math.ceil(sheet * 0.45 + sheet)
        elif sheet <= 500:
            return math.ceil(sheet * 0.35 + sheet)
        elif sheet <= 600:
            return math.ceil(sheet * 0.3 + sheet)
        elif sheet >= 700 and sheet <= 1000:
            return math.ceil(sheet * 0.17 + sheet)
        elif sheet >= 1000 and sheet <= 1500:
            return math.ceil(sheet * 0.15 + sheet)
        elif sheet >= 1500 and sheet <= 2000:
            return math.ceil(sheet * 0.15 + sheet)
        elif sheet >= 2000 and sheet <= 3000:
            return math.ceil(sheet * 0.1 + sheet)
        elif sheet >= 3000 and sheet <= 4000:
            return math.ceil(sheet * 0.08 + sheet)
        elif sheet >= 4000 and sheet <= 5000:
            return math.ceil(sheet * 0.07 + sheet)
        elif sheet <= 6000:
            return math.ceil(sheet * 0.05 + sheet)
        elif sheet <= 7000:
            return math.ceil(sheet * 0.05 + sheet)
        elif sheet <= 8000:
            return math.ceil(sheet * 0.05 + sheet)
        elif sheet <= 9000:
            return math.ceil(sheet * 0.045 + sheet)
        elif sheet <= 10000:
            return math.ceil(sheet * 0.0475 + sheet)
        elif sheet > 10000:
            return math.ceil(sheet * 0.0425 + sheet)
    except:
        return 0

@st.cache_data
def find_machine_size(w, l,rate_df):
    
    if (w <= 12.5 and l <= 18) or (l <= 12.5 and w <= 18):
        machine = rate_df[rate_df.Machine_size == "12x17"]
        # print("12x17")
    elif (w <= 25 and l <= 18) or (l <= 25 and w <= 18):
        machine = rate_df[rate_df.Machine_size == "23x17"]
        # print("23x17")
    elif (w <= 25 and l <= 36) or (l <= 25 and w <= 36):
        machine = rate_df[rate_df.Machine_size == "25x36"]
        # print("25x36")
    elif (w <= 28 and l <= 40) or (l <= 28 and w <= 40):
        machine = rate_df[rate_df.Machine_size == "28x40"]
        # print("28x40")
    elif (w <= 35 and l <= 45) or (l <= 35 and w <= 45):
        machine = rate_df[rate_df.Machine_size == "35x45"]
        # print("35x45")
    elif (w <= 40 and l <= 60) or (l <= 40 and w <= 60):
        machine = rate_df[rate_df.Machine_size == "40x56"]
        # print("40x56")
    else:
        # print("No matching machine size found.")
        machine = None
    return machine
    # st.dataframe(machine, hide_index=True)
@st.cache_data
def Printing_Calculator(Machine,cmyk,pms,met,print_sheet):
    try:
        # as printing rate is per 1170 and below list show us that if printing rate is 1400 and we have sheets 3350 it is below 4387 so we multply its index+1 to rate
        sheet_list =[1170, 2310, 3300, 4387, 5360, 6405, 7500, 8500, 9532, 10529, 11500, 12500, 13553, 14595, 15742, 16680, 17723, 18765, 19808, 20850, 21893, 22935, 23978, 25020, 26167, 27105, 28252, 29294, 30233, 31275, 32318, 33360, 34403, 35485, 36488, 37634, 38677, 39719]
        for i in sheet_list:
            if print_sheet<=i:
                factor=sheet_list.index(i)+1
                break
            # CMYK=Machine["CMYK"].iloc[0, 0]
        return Machine["CMYK"].iloc[0]*cmyk*factor,Machine["PMS"].iloc[0]*pms*factor,Machine["Met"].iloc[0]*met*factor
    except:
        return 0,0,0
@st.cache_data
def Lamination_price_calculator(w_p,l_p,Sheet_printable,inside_rate,outside_rate,rate_df):
    # Outside_rate=Inside_rate=0
    # print("#########################################")
    print(w_p,l_p,Sheet_printable,inside_rate,outside_rate,)
    try:
        # print(rate_df[outside_rate][0])
        Outside_rate=rate_df[outside_rate].iloc[0]
    except Exception as e:
        # print(e,"apple")
        Outside_rate=0
    try:
        Inside_rate=rate_df[inside_rate].iloc[0]
    except:
        # print("#########################################2")
        # print(inside_rate)
        Inside_rate=0
    # if Inside_rate!="None":
        # Inside_rate=rate_df[inside_rate][0]
    
    outside_lamination= int((w_p*l_p/144)*Outside_rate*Sheet_printable)
    inside_lamination= int((w_p*l_p/144)*Inside_rate*Sheet_printable)
    return outside_lamination,inside_lamination

@st.cache_data
def load_data(file,sheet_name):
    # Load your data into a DataFrame (replace 'your_data.csv' with your actual data source)
    data = pd.read_excel(file,sheet_name=sheet_name)
    data.fillna(0,inplace=True)
    return data

@st.cache_data
def PVC(w,l,qty,machine_rate):
    try:
        ans=(54//w)*(24//l)
        total_sheet=qty/ans
        total_sheet=math.ceil(total_sheet)
        sheet_price=total_sheet*machine_rate["PVC_Sheet_price"].iloc[0]
        if qty<=1000:
            factor=1
        else:
            factor=math.ceil(qty/1000)
        return sheet_price+machine_rate["PVC_pasting"].iloc[0]*factor
    except Exception as e:
        print(e)
        return 0
def Rigid_making_labour(Board_size,machine_rate):
    print(machine_rate[Board_size].iloc[0])
    return machine_rate[Board_size].iloc[0]