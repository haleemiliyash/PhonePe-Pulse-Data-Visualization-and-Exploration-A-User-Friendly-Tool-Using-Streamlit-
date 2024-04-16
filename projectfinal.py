import os
from PIL import Image
import pandas as pd
import json
import requests
import mysql.connector
import sqlalchemy
from sqlalchemy import create_engine
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="phone_pe_I"

)
mycursor=mydb.cursor(buffered=True)
engine = create_engine('mysql+mysqlconnector://root:@localhost/phone_pe_I', echo=False)

st.set_page_config(layout= "wide")
st.title(':white[ PhonePe Data Visualization of Year (2018-2023) ]')

with st.sidebar:
    select= option_menu("Main Menu",["Home", "Data Exploration","Charts visualization"],icons=["house", "gear"],menu_icon="cast", default_index=0)

if select == "Home":
    col1,col2= st.columns(2)
    with col1:
        st.image(Image.open(r"C:\Users\halee\OneDrive\Desktop\Guvi Project\phone pay\phone pe image.jpg"),width= 400)
    with col2:
        st.image(Image.open(r"C:\Users\halee\OneDrive\Desktop\Guvi Project\phone pay\phonepe logo.jpg"),width= 400)
    col3,col4= st.columns(2)
    with col3:
        st.header('About PhonePe')
        st.write('PhonePe is an Indian digital payments and financial services company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015,by Sameer Nigam, Rahul Chari and Burzin Engineer.The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016')
    with col4:
        st.header('PhonePe Services')
        st.subheader('Digital payment')
        st.write('Mobile payment')
        st.write('Payment system Financial service')
        st.subheader('Merchant payment')
        st.write('Mutual Fund')
        st.write('Insurance')
        st.write('Digital Gold')
        st.write('Payment Gateway')


if select == "Data Exploration":
    data=st.sidebar.selectbox("choose one",["Aggregated data", "Map Data", "Top Data"])
    if data=="Aggregated data":
        analysis=st.sidebar.selectbox("choose one",["Transaction Data", "User Data"])
        if analysis=="Transaction Data":
            trans_year = st.sidebar.selectbox('**Select Year**', ('None','2018','2019','2020','2021','2022','2023'),key='trans_year')
            trans_quater= st.sidebar.selectbox('**Select Quarter**', ('None','1','2','3','4'),key='trans_quarter')
            trans_type = st.sidebar.selectbox('**Select Transaction type**', ('Recharge & bill payments','Peer-to-peer payments',
            'Merchant payments','Financial Services','Others'),key='trans_type')
#agg trans amt bar chart
            col1,col2= st.columns(2)
            with col1:
                mycursor.execute(f"SELECT State, Trans_count, Trans_amt FROM agg_transaction WHERE Year = '{trans_year}' AND Quater = '{trans_quater}' AND Trans_Ty = '{trans_type}';")
                agg_trans_result=pd.DataFrame(mycursor.fetchall(),columns=['State','Trans_count','Trans_amt'])
                agg_trans_result_1=agg_trans_result.set_index(pd.Index(range(1, len(agg_trans_result) + 1)))

                #agg trans amt bar chart
                agg_trans_result_1['State'] = agg_trans_result_1['State'].astype(str)
                agg_trans_result_1['Transaction_amount'] = agg_trans_result_1['Trans_amt'].astype(float)
                agg_trans_bar_amt = px.bar(agg_trans_result_1, x='State', y='Trans_amt',
                                            color='Trans_amt', color_continuous_scale='tealrose',
                                            title=f'{trans_year}({trans_quater}) Agg.Trans_Amt Analysis Chart', height=500, )
                agg_trans_bar_amt.update_layout(title_font=dict(size=25), title_font_color='#3377FF')
                st.plotly_chart(agg_trans_bar_amt, use_container_width=True)
##agg trans count bar chart           
            with col2:
                agg_trans_result_1['State'] = agg_trans_result_1['State'].astype(str)
                agg_trans_result_1['Trans_count'] = agg_trans_result_1['Trans_count'].astype(float)
                agg_trans_bar_count = px.bar(agg_trans_result_1, x='State', y='Trans_count',
                                            color='Trans_count', color_continuous_scale='turbid',
                                            title=f'{trans_year}({trans_quater}) Agg.Trans_count Analysis Chart', height=500, )
                agg_trans_bar_count.update_layout(title_font=dict(size=25), title_font_color='#3377FF')
                st.plotly_chart(agg_trans_bar_count, use_container_width=True)

#Geo plot agg trans amt
            
            col3,col4= st.columns(2)
            with col3:
                url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                response= requests.get(url)
                data1= json.loads(response.content)
                states_Agg_trans= [feature["properties"]["ST_NM"] for feature in data1["features"]]
                states_Agg_trans.sort()

                fig_ind_1= px.choropleth(agg_trans_result_1, geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                                 color= "Trans_amt", color_continuous_scale= "thermal",
                                 range_color= (agg_trans_result_1["Trans_amt"].min(),agg_trans_result_1["Trans_amt"].max()),
                                 hover_name= "State",title = f"{trans_year} AGG.TRANSACTION AMOUNT",
                                 fitbounds= "locations",width =400, height= 600)
                fig_ind_1.update_geos(visible =False)
                fig_ind_1.update_layout(title_font=dict(size=25), title_font_color='#3377FF')

                #fig_ind_1.show()
                st.plotly_chart(fig_ind_1)
#Geo plot agg trans count
            with col4:
                url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                response= requests.get(url)
                data2= json.loads(response.content)
                states_name_trans= [feature["properties"]["ST_NM"] for feature in data2["features"]]
                states_name_trans.sort()

                fig_ind_2= px.choropleth(agg_trans_result_1, geojson= data2, locations= "State", featureidkey= "properties.ST_NM",
                                 color= "Trans_amt", color_continuous_scale= "thermal",
                                 range_color= (agg_trans_result_1["Trans_amt"].min(),agg_trans_result_1["Trans_amt"].max()),
                                 hover_name= "State",title = f"{trans_year} AGG.TRANSACTION COUNT",
                                 fitbounds= "locations",width =400, height= 600)
                fig_ind_2.update_geos(visible =False)
                fig_ind_2.update_layout(title_font=dict(size=25), title_font_color='#3377FF')

                #fig_ind_2.show()
        
                st.plotly_chart(fig_ind_2)
        if analysis=="User Data":
            user_year = st.sidebar.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023'),key='user_year')
            user_quarter= st.sidebar.selectbox('**Select Quarter**', ('1','2','3','4'),key='user_quarter')
        #agg user bar chart
            col1,col2= st.columns(2)

            with col1:
                mycursor.execute( f"SELECT State, Brand, Trans_count FROM agg_user WHERE Year = '{user_year}' AND Quater = '{user_quarter}'")
                agg_user_bar=pd.DataFrame(mycursor.fetchall(),columns=['State','Brand','Trans_count'])
                agg_user_bar_1 = agg_user_bar.set_index(pd.Index(range(1, len(agg_user_bar) + 1)))

                mycursor.execute( f"SELECT State, SUM(Trans_count) FROM agg_user WHERE Year = '{user_year}' AND Quater = '{user_quarter}' GROUP BY State")
                agg_user_count=pd.DataFrame(mycursor.fetchall(),columns=['State','Trans_count'])
                agg_user_count_1 = agg_user_count.set_index(pd.Index(range(1, len(agg_user_count) + 1)))

                mycursor.execute(f"SELECT State,percentage FROM agg_user WHERE Year = '{user_year}' AND Quater = '{user_quarter}' GROUP BY State")
                agg_user_percent=pd.DataFrame(mycursor.fetchall(),columns=['State','percentage',])
                agg_user_percent_1 = agg_user_percent.set_index(pd.Index(range(1, len(agg_user_percent) + 1)))

                ##agg user Bcount bar chart
                agg_user_bar_1['State'] = agg_user_bar_1['State'].astype(str)
                agg_user_bar_1['Trans_count'] = agg_user_bar_1['Trans_count'].astype(float)
                agg_user_bar_1['Brand'] = agg_user_bar_1['Brand'].astype(str)
                agg_user_bar_count = px.bar(agg_user_bar_1, x='State', y='Trans_count',
                                                color='Brand', color_continuous_scale='twilight',
                                                title=f'{user_year}({user_quarter}) Agg.user_Bcount Analysis Chart', height=700, )
                agg_user_bar_count.update_layout(title_font=dict(size=25), title_font_color='#3377FF')
                #agg_user_bar_count.show()
                st.plotly_chart(agg_user_bar_count, use_container_width=True)
            
            with col2:
                ##agg user Tcount bar chart
                agg_user_count_1['State'] = agg_user_count_1['State'].astype(str)
                agg_user_count_1['Trans_count'] = agg_user_count_1['Trans_count'].astype(float)
                agg_user_bar_tcount = px.bar(agg_user_count_1, x='State', y='Trans_count',
                                            color='Trans_count', color_continuous_scale='twilight',
                                            title=f'{user_year}({user_quarter}) Agg.user_Tcount Analysis Chart', height=700, )
                agg_user_bar_tcount.update_layout(title_font=dict(size=25), title_font_color='#3377FF')
                #agg_user_bar_tcount.show()
                st.plotly_chart(agg_user_bar_tcount, use_container_width=True)
            
            col3,col4= st.columns(2)
            with col3:
#GEO PLOT agg user Tcount
                url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                response= requests.get(url)
                data3= json.loads(response.content)
                states_name_user= [feature["properties"]["ST_NM"] for feature in data3["features"]]
                states_name_user.sort()

                fig_ind_3= px.choropleth(agg_user_bar_1, geojson= data3, locations= "State", featureidkey= "properties.ST_NM",
                                 color= "Trans_count", color_continuous_scale= "thermal",
                                 range_color= (agg_user_bar_1['Trans_count'].min(),agg_user_bar_1["Trans_count"].max()),
                                 hover_name= "State",title = f"{user_year} AGG_USER COUNT",
                                 fitbounds= "locations",width =500, height= 500)
                fig_ind_3.update_geos(visible =False)
                fig_ind_3.update_layout(title_font=dict(size=25), title_font_color='#3377FF')
                #fig_ind_3.show()
                st.plotly_chart(fig_ind_3)

            with col4:
                #GEO PLOT agg user Bcount
                url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                response= requests.get(url)
                data4= json.loads(response.content)
                states_name_user= [feature["properties"]["ST_NM"] for feature in data4["features"]]
                states_name_user.sort()

                fig_ind_4= px.choropleth(agg_user_percent_1, geojson= data4, locations= "State", featureidkey= "properties.ST_NM",
                                 color= "percentage", color_continuous_scale= "thermal",
                                 range_color= (agg_user_percent_1['percentage'].min(),agg_user_percent_1["percentage"].max()),
                                 hover_name= "State",title = f"{user_year} AGG_USER PCOUNT",
                                 fitbounds= "locations",width =500, height= 500)
                fig_ind_4.update_geos(visible =False)
                fig_ind_4.update_layout(title_font=dict(size=25), title_font_color='#3377FF')
                #fig_ind_4.show()
                st.plotly_chart(fig_ind_4)

    if data=="Map Data":
        analysis_1=st.sidebar.selectbox("choose one",["Transaction Data", "User Data"])
        if analysis_1=="Transaction Data":
            mapT_year = st.sidebar.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023'),key='mapT_year')
            mapT_quater= st.sidebar.selectbox('**Select Quarter**', ('1','2','3','4'),key='mapT_quarter')
        #map transaction bar chart
            col1,col2= st.columns(2)
            with col1:
                mycursor.execute( f"SELECT State, District, Trans_count,Trans_amount FROM map_transaction WHERE Year = '{mapT_year}' AND Quater = '{mapT_quater}'")
                map_trans_bar=pd.DataFrame(mycursor.fetchall(),columns=['State','District','Trans_count','Trans_amount'])
                map_trans_bar_1 = map_trans_bar.set_index(pd.Index(range(1, len(map_trans_bar) + 1)))

                mycursor.execute( f"SELECT District, Trans_count FROM map_transaction WHERE Year = '{mapT_year}' AND Quater = '{mapT_quater}'GROUP BY State")
                mtdtc=pd.DataFrame(mycursor.fetchall(),columns=['District','Trans_count'])
                mtdtc_1 = mtdtc.set_index(pd.Index(range(1, len(mtdtc) + 1)))

                mycursor.execute( f"SELECT State, Trans_count FROM map_transaction WHERE Year = '{mapT_year}' AND Quater = '{mapT_quater}'GROUP BY State")
                mtstc=pd.DataFrame(mycursor.fetchall(),columns=['State','Trans_count'])
                mtstc_1 = mtstc.set_index(pd.Index(range(1, len(mtstc) + 1)))

                mycursor.execute( f"SELECT State, Trans_amount FROM map_transaction WHERE Year = '{mapT_year}' AND Quater = '{mapT_quater}'GROUP BY State")
                mtsta=pd.DataFrame(mycursor.fetchall(),columns=['State','Trans_amount'])
                mtsta_1 = mtsta.set_index(pd.Index(range(1, len(mtsta) + 1)))

                mycursor.execute( f"SELECT District, Trans_amount FROM map_transaction WHERE Year = '{mapT_year}' AND Quater = '{mapT_quater}'GROUP BY State")
                mtdta=pd.DataFrame(mycursor.fetchall(),columns=['District','Trans_amount'])
                mtdta_1 = mtdta.set_index(pd.Index(range(1, len(mtdta) + 1)))

                #map Trans Dist Tcount bar chart
                mtdtc_1['District'] = mtdtc_1['District'].astype(str)
                mtdtc_1['Trans_count'] = mtdtc_1['Trans_count'].astype(float)
                map_trans_bar_dcount = px.bar(mtdtc_1, x='Trans_count', y='District',
                                                color='Trans_count', color_continuous_scale='thermal',
                                                title=f'{mapT_year}({mapT_quater}) Map.Trans_Dist_Tcount Analysis Chart', height=900, )
                map_trans_bar_dcount.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
                #map_trans_bar_dcount.show()
                st.plotly_chart(map_trans_bar_dcount, use_container_width=True)

                #map Trans State Tcount bar chart
            with col2:
                    mtstc_1['State'] = mtstc_1['State'].astype(str)
                    mtstc_1['Trans_count'] = mtstc_1['Trans_count'].astype(float)
                    map_trans_bar_scount = px.bar(mtstc_1, x='Trans_count', y='State',
                                                color='Trans_count', color_continuous_scale='twilight',
                                                title=f'{mapT_year}({mapT_quater}) Map.Trans_State_Tcount Analysis Chart', height=700, )
                    map_trans_bar_scount.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
                    #map_trans_bar_scount.show()
                    st.plotly_chart(map_trans_bar_scount, use_container_width=True)

                #map Trans State Tamt bar chart
            col3,col4= st.columns(2)
            with col3:
                    mtsta_1['State'] =mtsta_1['State'].astype(str)
                    mtsta_1['Trans_amount'] = mtsta_1['Trans_amount'].astype(float)
                    map_trans_bar_samt = px.bar(mtsta_1, x='Trans_amount', y='State',
                                                color='Trans_amount', color_continuous_scale='rainbow',
                                                title=f'{mapT_year}({mapT_quater}) Map.Trans_State_Tamt Analysis Chart', height=700, )
                    map_trans_bar_samt.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
                    #map_trans_bar_samt.show()
                    st.plotly_chart(map_trans_bar_samt, use_container_width=True)

                #map Trans Dist Tamt bar chart
            with col4:
                    mtdta_1['District'] = mtdta_1['District'].astype(str)
                    mtdta_1['Trans_amount'] = mtdta_1['Trans_amount'].astype(float)
                    map_trans_bar_damt = px.bar(mtdta_1, x='Trans_amount', y='District',
                                                color='Trans_amount', color_continuous_scale='thermal',
                                                title=f'{mapT_year}({mapT_quater}) Map.Trans_Dist_Tamt Analysis Chart', height=900, )
                    map_trans_bar_damt.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
                    #map_trans_bar_damt.show()
                    st.plotly_chart(map_trans_bar_damt, use_container_width=True)

            col5,col6= st.columns(2)
            with col5:
                 #GEO PLOT map Trans State Tcount
                url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                response= requests.get(url)
                data5= json.loads(response.content)
                states_name_user= [feature["properties"]["ST_NM"] for feature in data5["features"]]
                states_name_user.sort()

                fig_ind_5= px.choropleth(mtstc_1, geojson= data5, locations= "State", featureidkey= "properties.ST_NM",
                                 color= "Trans_count", color_continuous_scale= "tropic",
                                 range_color= (mtstc_1['Trans_count'].min(),mtstc_1["Trans_count"].max()),
                                 hover_name= "State",title = f"{mapT_year} MAP_TRANS TCOUNT",
                                 fitbounds= "locations",width =500, height= 500)
                fig_ind_5.update_geos(visible =False)
                fig_ind_5.update_layout(title_font=dict(size=25), title_font_color='#3377FF')
                #fig_ind_5.show()
                st.plotly_chart(fig_ind_5)
            with col6:
                 #GEO PLOT map Trans State TAMT
                url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                response= requests.get(url)
                data6= json.loads(response.content)
                states_name_user= [feature["properties"]["ST_NM"] for feature in data6["features"]]
                states_name_user.sort()

                fig_ind_6= px.choropleth(mtsta_1, geojson= data6, locations= "State", featureidkey= "properties.ST_NM",
                                 color= "Trans_amount", color_continuous_scale= "tropic",
                                 range_color= (mtsta_1['Trans_amount'].min(),mtsta_1["Trans_amount"].max()),
                                 hover_name= "State",title = f"{mapT_year} MAP_TRANS TAMOUNT",
                                 fitbounds= "locations",width =500, height= 500)
                fig_ind_6.update_geos(visible =False)
                fig_ind_6.update_layout(title_font=dict(size=25), title_font_color='#3377FF')
                #fig_ind_6.show()
                st.plotly_chart(fig_ind_6)

        if analysis_1=="User Data":
            mapU_year = st.sidebar.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023'),key='mapU_year')
            mapU_quater= st.sidebar.selectbox('**Select Quarter**', ('1','2','3','4'),key='mapU_quarter')

            #MAP USER bar chart
            col1,col2= st.columns(2)
            with col1:
                mycursor.execute( f"SELECT State, District,Regis_user FROM map_user WHERE Year = '{mapU_year}' AND Quater = '{mapU_quater}'")
                map_user_bar=pd.DataFrame(mycursor.fetchall(),columns=['State','District','Regis_user'])
                map_user_bar_1 = map_user_bar.set_index(pd.Index(range(1, len(map_user_bar) + 1)))

                mycursor.execute( f"SELECT State,Regis_user FROM map_user WHERE Year = '{mapU_year}' AND Quater = '{mapU_quater}'GROUP BY State")
                musru=pd.DataFrame(mycursor.fetchall(),columns=['State','Regis_user'])
                musru_1 = musru.set_index(pd.Index(range(1, len(musru) + 1)))

                mycursor.execute( f"SELECT District,Regis_user FROM map_user WHERE Year = '{mapU_year}' AND Quater = '{mapU_quater}'GROUP BY District")
                mudru=pd.DataFrame(mycursor.fetchall(),columns=['District','Regis_user'])
                mudru_1 = mudru.set_index(pd.Index(range(1, len(mudru) + 1)))

                mycursor.execute( f"SELECT State,App_open FROM map_user WHERE Year = '{mapU_year}' AND Quater = '{mapU_quater}'GROUP BY State")
                musao=pd.DataFrame(mycursor.fetchall(),columns=['State','App_open'])
                musao_1 = musao.set_index(pd.Index(range(1, len(musao) + 1)))

                mycursor.execute( f"SELECT District ,App_open FROM map_user WHERE Year = '{mapU_year}' AND Quater = '{mapU_quater}'GROUP BY District ")
                mudao=pd.DataFrame(mycursor.fetchall(),columns=['District','App_open'])
                mudao_1 = mudao.set_index(pd.Index(range(1, len(mudao) + 1)))

                #map user State Ruser bar chart
                musru_1['State'] = musru_1['State'].astype(str)
                musru_1['Regis_user'] = musru_1['Regis_user'].astype(int)
                map_user_bar_sRuser= px.bar(musru_1, x='Regis_user', y='State',
                                            color='Regis_user', color_continuous_scale='turbo',
                                            title=f'{mapU_year}({mapU_quater}) Map.User_State_Ruser Analysis Chart', height=700, )
                map_user_bar_sRuser.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
                #map_user_bar_sRuser.show()
                st.plotly_chart(map_user_bar_sRuser, use_container_width=True)
            with col2:
                #map user District Ruser bar chart
                mudru_1['District'] = mudru_1['District'].astype(str)
                mudru_1['Regis_user'] =mudru_1['Regis_user'].astype(int)
                map_user_bar_dRuser= px.bar(mudru_1, x='Regis_user', y='District',
                                            color='Regis_user', color_continuous_scale='rainbow',
                                            title=f'{mapU_year}({mapU_quater}) Map.User_Dist_Ruser Analysis Chart', height=1000, )
                map_user_bar_dRuser.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
                #map_user_bar_dRuser.show()
                st.plotly_chart(map_user_bar_dRuser, use_container_width=True)

            col3,col4= st.columns(2)
            with col3:
                #map user state appopen bar chart
                musao_1['State'] = musao_1['State'].astype(str)
                musao_1['App_open'] =musao_1['App_open'].astype(int)
                map_user_bar_saopen= px.bar(musao_1, x='App_open', y='State',
                                                            color='App_open', color_continuous_scale='thermal',
                                                            title=f'{mapU_year}({mapU_quater}) Map.User_state_Appopen Analysis Chart', height=700, )
                map_user_bar_saopen.update_layout(title_font=dict(size=25), title_font_color='#3377FF')
                #map_user_bar_saopen.show()
                st.plotly_chart(map_user_bar_saopen, use_container_width=True)

            with col4:
                #map user District dappopoen bar chart
                mudao_1['District'] = mudao_1['District'].astype(str)
                mudao_1['App_open'] =mudao_1['App_open'].astype(int)
                map_user_bar_daopen= px.bar(mudao_1, x='App_open', y='District',
                                                            color='App_open', color_continuous_scale='thermal',
                                                            title=f'{mapU_year}({mapU_quater}) Map.User_state_Appopen Analysis Chart', height=700, )
                map_user_bar_daopen.update_layout(title_font=dict(size=25), title_font_color='#3377FF')
                #map_user_bar_daopen.show()
                st.plotly_chart(map_user_bar_daopen, use_container_width=True)


            col5,col6= st.columns(2)
            with col5:
                #Geo plot map user  
                url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                response= requests.get(url)
                data7= json.loads(response.content)
                states_name_user= [feature["properties"]["ST_NM"] for feature in data7["features"]]
                states_name_user.sort()

                fig_ind_7= px.choropleth(musru_1, geojson= data7, locations= "State", featureidkey= "properties.ST_NM",
                                 color= "Regis_user", color_continuous_scale= "tropic",
                                 range_color= (musru_1['Regis_user'].min(),musru_1["Regis_user"].max()),
                                 hover_name= "State",title = f"{mapU_year} MAP_USER RIG_USER",
                                 fitbounds= "locations",width =500, height= 500)
                fig_ind_7.update_geos(visible =False)
                fig_ind_7.update_layout(title_font=dict(size=25), title_font_color='#3377FF')
                #fig_ind_7.show()
                st.plotly_chart(fig_ind_7)
            with col6:
                #Geo plot map user app open  
                url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                response= requests.get(url)
                data11= json.loads(response.content)
                states_name_user= [feature["properties"]["ST_NM"] for feature in data11["features"]]
                states_name_user.sort()

                fig_ind_11= px.choropleth(musao_1, geojson= data11, locations= "State", featureidkey= "properties.ST_NM",
                                 color= "App_open", color_continuous_scale= "tropic",
                                 range_color= (musao_1['App_open'].min(),musao_1["App_open"].max()),
                                 hover_name= "State",title = f"{mapU_year} MAP_USER APP_OPEN",
                                 fitbounds= "locations",width =500, height= 500)
                fig_ind_11.update_geos(visible =False)
                fig_ind_11.update_layout(title_font=dict(size=25), title_font_color='#3377FF')
                #fig_ind_11.show()
                st.plotly_chart(fig_ind_11)


    if data=="Top Data":
        analysis_2=st.sidebar.selectbox("choose one",["Transaction Data", "User Data"])
        if analysis_2=="Transaction Data":
            topT_year = st.sidebar.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023'),key='topT_year')
            topT_quater= st.sidebar.selectbox('**Select Quarter**', ('1','2','3','4'),key=' topT_quarter')

            col1,col2= st.columns(2)
            with col1:
            #top transaction
                mycursor.execute( f"SELECT State, pincode,P_count,P_amount FROM top_trans WHERE Year = '{topT_year}' AND Quater = '{topT_quater}'")
                top_trans_bar=pd.DataFrame(mycursor.fetchall(),columns=['State','pincode','P_count','P_amount'])
                top_trans_bar_1 = top_trans_bar.set_index(pd.Index(range(1, len(top_trans_bar) + 1)))

                mycursor.execute( f"SELECT State,P_count FROM top_trans WHERE Year = '{topT_year}' AND Quater = '{topT_quater}'GROUP BY State")
                Ttsc=pd.DataFrame(mycursor.fetchall(),columns=['State','P_count'])
                Ttsc_1 = Ttsc.set_index(pd.Index(range(1, len(Ttsc) + 1)))

                mycursor.execute( f"SELECT State,P_amount FROM top_trans WHERE Year = '{topT_year}' AND Quater = '{topT_quater}'GROUP BY State")
                Ttsa=pd.DataFrame(mycursor.fetchall(),columns=['State','P_amount'])
                Ttsa_1 = Ttsa.set_index(pd.Index(range(1, len(Ttsa) + 1)))

                #top trans State Pcount bar chart
                Ttsc_1['State'] = Ttsc_1['State'].astype(str)
                Ttsc_1['P_count'] = Ttsc_1['P_count'].astype(float)
                top_trans_bar_scount= px.bar(Ttsc_1, x='P_count', y='State',
                                                color='P_count', color_continuous_scale='turbo',
                                                title=f'{topT_year}({topT_quater}) Map.Trans_State_count Analysis Chart', height=700, )
                top_trans_bar_scount.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
                #top_trans_bar_scount.show()
                st.plotly_chart(top_trans_bar_scount, use_container_width=True)

            with col2:
                #top trans State Pamt bar chart
                Ttsa_1['State'] = Ttsa_1['State'].astype(str)
                Ttsa_1['P_amount'] = Ttsa_1['P_amount'].astype(float)
                top_trans_bar_sAMT= px.bar(Ttsa_1, x='P_amount', y='State',
                                                color='P_amount', color_continuous_scale='turbo',
                                                title=f'{topT_year}({topT_quater}) Map.Trans_State_amount Analysis Chart', height=700, )
                top_trans_bar_sAMT.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
                #top_trans_bar_sAMT.show()
                st.plotly_chart(top_trans_bar_sAMT, use_container_width=True)

            col3,col4= st.columns(2)
            with col3:
                    #GEO PLOT TOP TRANS STATE COUNT
                url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                response= requests.get(url)
                data8= json.loads(response.content)
                states_name_user= [feature["properties"]["ST_NM"] for feature in data8["features"]]
                states_name_user.sort()

                fig_ind_8= px.choropleth(Ttsc_1, geojson= data8, locations= "State", featureidkey= "properties.ST_NM",
                                                    color= "P_count", color_continuous_scale= "tropic",
                                                    range_color= (Ttsc_1['P_count'].min(),Ttsc_1["P_count"].max()),
                                                    hover_name= "State",title = f"{topT_year} TOP_TRANS STATE COUNT",
                                                    fitbounds= "locations",width =500, height= 500)
                fig_ind_8.update_geos(visible =False)
                fig_ind_8.update_layout(title_font=dict(size=25), title_font_color='#3377FF')
                #fig_ind_8.show()
                st.plotly_chart(fig_ind_8)

            with col4:
                #GEO PLOT TOP TRANS STATE AMOUNT
    
                url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                response= requests.get(url)
                data9= json.loads(response.content)
                states_name_user= [feature["properties"]["ST_NM"] for feature in data9["features"]]
                states_name_user.sort()

                fig_ind_9= px.choropleth(Ttsa_1, geojson= data9, locations= "State", featureidkey= "properties.ST_NM",
                                                    color= "P_amount", color_continuous_scale= "tropic",
                                                    range_color= (Ttsa_1['P_amount'].min(),Ttsa_1["P_amount"].max()),
                                                    hover_name= "State",title = f"{topT_year} TOP_TRANS STATE AMOUNT",
                                                    fitbounds= "locations",width =500, height= 500)
                fig_ind_9.update_geos(visible =False)
                fig_ind_9.update_layout(title_font=dict(size=25), title_font_color='#3377FF')
                #fig_ind_9.show()
                st.plotly_chart(fig_ind_9)

        if analysis_2=="User Data":
            topU_year = st.sidebar.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023'),key='topU_year')
            topU_quater= st.sidebar.selectbox('**Select Quarter**', ('1','2','3','4'),key='topU_quarter')

            col1,col2= st.columns(2)
            with col1:
            #top USER
                mycursor.execute(f"SELECT State, pincode,register_user FROM top_user WHERE Year ='{topU_year}' AND Quater = '{topU_quater}'")
                map_user_bar=pd.DataFrame(mycursor.fetchall(),columns=['State','pincode','register_user'])
                map_user_bar_1 = map_user_bar.set_index(pd.Index(range(1, len(map_user_bar) + 1)))

                mycursor.execute( f"SELECT State,register_user FROM top_user WHERE Year = '{topU_year}' AND Quater = '{topU_quater}'GROUP BY State")
                musru=pd.DataFrame(mycursor.fetchall(),columns=['State','register_user'])
                musru_1 = musru.set_index(pd.Index(range(1, len(musru) + 1)))


                mycursor.execute( f"SELECT pincode,register_user FROM top_user WHERE Year = '{topU_year}' AND Quater = '{topU_quater}'GROUP BY pincode")
                mupru=pd.DataFrame(mycursor.fetchall(),columns=['pincode','register_user'])
                mupru_1 = mupru.set_index(pd.Index(range(1, len(mupru) + 1)))

                #top user State Reg user bar chart
                musru_1['State'] = musru_1['State'].astype(str)
                musru_1['register_user'] = musru_1['register_user'].astype(float)
                top_user_bar_scount= px.bar(musru_1, x='register_user', y='State',
                                                            color='register_user', color_continuous_scale='turbo',
                                                            title=f'{topU_year}({topU_quater}) Top.user_State_Regis.User Analysis Chart', height=700, )
                top_user_bar_scount.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
                #top_user_bar_scount.show()
                st.plotly_chart(top_user_bar_scount, use_container_width=True)
            with col2:
                #GEO PLOT TOP USER STATE AMOUNT
    
                url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                response= requests.get(url)
                data10= json.loads(response.content)
                states_name_user= [feature["properties"]["ST_NM"] for feature in data10["features"]]
                states_name_user.sort()

                fig_ind_10= px.choropleth(musru_1, geojson= data10, locations= "State", featureidkey= "properties.ST_NM",
                                                color= "register_user", color_continuous_scale= "tropic",
                                                range_color= (musru_1['register_user'].min(),musru_1["register_user"].max()),
                                                hover_name= "State",title = f"{topU_year} TOP_USER REG USER",
                                                fitbounds= "locations",width =500, height= 500)
                fig_ind_10.update_geos(visible =False)
                fig_ind_10.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
                #fig_ind_10.show()
                st.plotly_chart(fig_ind_10)

if select =="Charts visualization":
    query=st.sidebar.selectbox("choose one Query",['Query 1','Query 2','Query 3','Query 4','Query 5'])
    if query=='Query 1':
        st.subheader('State wise Aggregated transaction counts and Amounts data visualization')
        #agg transaction
        mycursor.execute(f"SELECT State,SUM(Trans_amt) AS Trans_amt FROM agg_transaction GROUP BY State ORDER BY Trans_amt LIMIT 10;")
        atamta=pd.DataFrame(mycursor.fetchall(),columns=['State','Trans_amt'])
        atamta_1=atamta.set_index(pd.Index(range(1, len(atamta) + 1)))

        mycursor.execute(f"SELECT State,SUM(Trans_amt) AS Trans_amt FROM agg_transaction GROUP BY State ORDER BY Trans_amt DESC LIMIT 10;")
        atamtd=pd.DataFrame(mycursor.fetchall(),columns=['State','Trans_amt'])
        atamtd_1=atamtd.set_index(pd.Index(range(1, len(atamtd) + 1)))

        mycursor.execute(f"SELECT State,AVG(Trans_amt) AS Trans_amt FROM agg_transaction GROUP BY State ORDER BY Trans_amt;")
        atamtA=pd.DataFrame(mycursor.fetchall(),columns=['State','Trans_amt'])
        atamtA_1=atamtA.set_index(pd.Index(range(1, len(atamtA) + 1)))

        mycursor.execute(f"SELECT State,SUM(Trans_count) AS Trans_count  FROM agg_transaction GROUP BY State ORDER BY Trans_count LIMIT 10;")
        atCOUa=pd.DataFrame(mycursor.fetchall(),columns=['State','Trans_count'])
        atCOUa_1=atCOUa.set_index(pd.Index(range(1, len(atCOUa) + 1)))

        mycursor.execute(f"SELECT State,SUM(Trans_count) AS Trans_count FROM agg_transaction GROUP BY State ORDER BY Trans_count DESC LIMIT 10;")
        atCOUd=pd.DataFrame(mycursor.fetchall(),columns=['State','Trans_count'])
        atCOUd_1=atCOUd.set_index(pd.Index(range(1, len(atCOUd) + 1)))

        mycursor.execute(f"SELECT State,AVG(Trans_count) AS Trans_count FROM agg_transaction GROUP BY State ORDER BY Trans_count;")
        atCOUA=pd.DataFrame(mycursor.fetchall(),columns=['State','Trans_count'])
        atCOUA_1=atCOUA.set_index(pd.Index(range(1, len(atCOUA) + 1)))

        col1,col2= st.columns(2)
        with col1:
            #AGG.TRANS_State_AMT_ASEC Analysis Chart
            atamta_1['State'] = atamta_1['State'].astype(str)
            atamta_1['Trans_amt'] =atamta_1['Trans_amt'].astype(float)
            AGG_TAMT_ASEC= px.bar(atamta_1, x='Trans_amt', y='State',
                                            color='Trans_amt', color_continuous_scale='turbo',
                                            title=f'AGG.TRANS_State_AMT_ASEC Analysis Chart', height=400, )
            AGG_TAMT_ASEC.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
            #AGG_TAMT_ASEC.show()
            st.plotly_chart(AGG_TAMT_ASEC, use_container_width=True)

        with col2:
            #AGG.TRANS_State_AMT_ASEC Analysis Chart
            atamtd_1['State'] = atamtd_1['State'].astype(str)
            atamtd_1['Trans_amt'] =atamtd_1['Trans_amt'].astype(float)
            AGG_TAMT_DSEC= px.bar(atamtd_1, x='Trans_amt', y='State',
                                            color='Trans_amt', color_continuous_scale='turbo',
                                            title=f'AGG.TRANS_State_AMT_DSEC Analysis Chart', height=400, )
            AGG_TAMT_DSEC.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
            #AGG_TAMT_DSEC.show()
            st.plotly_chart(AGG_TAMT_DSEC, use_container_width=True)
        
        col3,col4= st.columns(2)
        with col3:
            #AGG.TRANS_State_AMT_AVG Analysis Chart
            atamtA_1['State'] = atamtA_1['State'].astype(str)
            atamtA_1['Trans_amt'] =atamtA_1['Trans_amt'].astype(float)
            AGG_TAMT_AVG= px.bar(atamtA_1, x='Trans_amt', y='State',
                                            color='Trans_amt', color_continuous_scale='turbo',
                                            title=f'AGG.TRANS_State_AMT_AVG Analysis Chart', height=400, )
            AGG_TAMT_AVG.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
            #AGG_TAMT_AVG.show()
            st.plotly_chart(AGG_TAMT_AVG, use_container_width=True)

        with col4:
            #AGG.TRANS_State_COUNT_ASEC Analysis Chart
            atCOUa_1['State'] = atCOUa_1['State'].astype(str)
            atCOUa_1['Trans_count'] =atCOUa_1['Trans_count'].astype(float)
            AGG_TCOUNT_ASEC= px.bar(atCOUa_1, x='Trans_count', y='State',
                                            color='Trans_count', color_continuous_scale='turbo',
                                            title=f'AGG.TRANS_State_COUNT_ASEC Analysis Chart', height=400, )
            AGG_TCOUNT_ASEC.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
            #AGG_TCOUNT_ASEC.show()
            st.plotly_chart(AGG_TCOUNT_ASEC, use_container_width=True)

        col5,col6= st.columns(2)
        with col5:
            #AGG.TRANS_State_COUNT_DSEC Analysis Chart
            atCOUd_1['State'] = atCOUd_1['State'].astype(str)
            atCOUd_1['Trans_count'] =atCOUd_1['Trans_count'].astype(float)
            AGG_TCOUNT_DSEC= px.bar(atCOUd_1, x='Trans_count', y='State',
                                            color='Trans_count', color_continuous_scale='turbo',
                                            title=f'AGG.TRANS_State_COUNT_DSEC Analysis Chart', height=700, )
            AGG_TCOUNT_DSEC.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
            #AGG_TCOUNT_DSEC.show()
            st.plotly_chart(AGG_TCOUNT_DSEC, use_container_width=True)
        
        with col6:
            #AGG.TRANS_State_COUNT_AVG Analysis Chart
            atCOUA_1['State'] = atCOUA_1['State'].astype(str)
            atCOUA_1['Trans_count'] =atCOUA_1['Trans_count'].astype(float)
            AGG_TCOUNT_AVG= px.bar(atCOUA_1, x='Trans_count', y='State',
                                            color='Trans_count', color_continuous_scale='turbo',
                                            title=f'AGG.TRANS_State_COUNT_AVG Analysis Chart', height=700, )
            AGG_TCOUNT_AVG.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
            #AGG_TCOUNT_AVG.show()
            st.plotly_chart(AGG_TCOUNT_AVG, use_container_width=True)

    if query=='Query 2':
        st.subheader('State wise Map transaction counts and Amounts data visualization')
        #map transaction
        mycursor.execute(f"SELECT State,SUM(Trans_amount) AS Trans_amount FROM map_transaction GROUP BY State ORDER BY Trans_amount LIMIT 10;")
        mtamta=pd.DataFrame(mycursor.fetchall(),columns=['State','Trans_amount'])
        mtamta_1=mtamta.set_index(pd.Index(range(1, len(mtamta) + 1)))

        mycursor.execute(f"SELECT State,SUM(Trans_amount) AS Trans_amount FROM map_transaction GROUP BY State ORDER BY Trans_amount DESC LIMIT 10;")
        mtamtd=pd.DataFrame(mycursor.fetchall(),columns=['State','Trans_amount'])
        mtamtd_1=mtamtd.set_index(pd.Index(range(1, len(mtamtd) + 1)))

        mycursor.execute(f"SELECT State,AVG(Trans_amount) AS Trans_amount FROM map_transaction GROUP BY State ORDER BY Trans_amount;")
        mtamtA=pd.DataFrame(mycursor.fetchall(),columns=['State','Trans_amount'])
        mtamtA_1=mtamtA.set_index(pd.Index(range(1, len(mtamtA) + 1)))

        mycursor.execute(f"SELECT State,SUM(Trans_count) AS Trans_count  FROM map_transaction GROUP BY State ORDER BY Trans_count LIMIT 10;")
        mtCOUNa=pd.DataFrame(mycursor.fetchall(),columns=['State','Trans_count'])
        mtCOUNa_1=mtCOUNa.set_index(pd.Index(range(1, len(mtCOUNa) + 1)))

        mycursor.execute(f"SELECT State,SUM(Trans_count) AS Trans_count  FROM map_transaction GROUP BY State ORDER BY Trans_count DESC  LIMIT 10;")
        mtCOUNd=pd.DataFrame(mycursor.fetchall(),columns=['State','Trans_count'])
        mtCOUNd_1=mtCOUNd.set_index(pd.Index(range(1, len(mtCOUNd) + 1)))

        mycursor.execute(f"SELECT State,AVG(Trans_count) AS Trans_count  FROM map_transaction GROUP BY State ORDER BY Trans_count;")
        mtCOUNA=pd.DataFrame(mycursor.fetchall(),columns=['State','Trans_count'])
        mtCOUNA_1=mtCOUNA.set_index(pd.Index(range(1, len(mtCOUNA) + 1)))

        col1,col2= st.columns(2)
        with col1:
            #MAP.TRANS_State_AMT_ASEC Analysis Chart
            mtamta_1['State'] = mtamta_1['State'].astype(str)
            mtamta_1['Trans_amount'] =mtamta_1['Trans_amount'].astype(float)
            MAP_TAMT_ASEC= px.bar(mtamta_1, x='Trans_amount', y='State',
                                            color='Trans_amount', color_continuous_scale='turbo',
                                            title=f'MAP.TRANS_State_AMT_ASEC Analysis Chart', height=500, )
            MAP_TAMT_ASEC.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
            #MAP_TAMT_ASEC.show()
            st.plotly_chart(MAP_TAMT_ASEC, use_container_width=True)

        with col2:
            #MAP.TRANS_State_AMT_DSEC Analysis Chart
            mtamtd_1['State'] = mtamtd_1['State'].astype(str)
            mtamtd_1['Trans_amount'] =mtamtd_1['Trans_amount'].astype(float)
            MAP_TAMT_DSEC= px.bar(mtamtd_1, x='Trans_amount', y='State',
                                            color='Trans_amount', color_continuous_scale='turbo',
                                            title=f'MAP.TRANS_State_AMT_DSEC Analysis Chart', height=500, )
            MAP_TAMT_DSEC.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
            #MAP_TAMT_DSEC.show()
            st.plotly_chart(MAP_TAMT_DSEC, use_container_width=True)

        col3,col4= st.columns(2)
        with col3:
            #MAP.TRANS_State_AMT_AVG Analysis Chart
            mtamtA_1['State'] = mtamtA_1['State'].astype(str)
            mtamtA_1['Trans_amount'] =mtamtA_1['Trans_amount'].astype(float)
            MAP_TAMT_AVG= px.bar(mtamtA_1, x='Trans_amount', y='State',
                                            color='Trans_amount', color_continuous_scale='turbo',
                                            title=f'MAP.TRANS_State_AMT_AVG Analysis Chart', height=500, )
            MAP_TAMT_AVG.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
            #MAP_TAMT_AVG.show()
            st.plotly_chart(MAP_TAMT_AVG, use_container_width=True)

        with col4:
            #MAP.TRANS_State_count_ASEC Analysis Chart
            mtCOUNa_1['State'] = mtCOUNa_1['State'].astype(str)
            mtCOUNa_1['Trans_count'] =mtCOUNa_1['Trans_count'].astype(float)
            MAP_TCOUNT_ASEC= px.bar(mtCOUNa_1, x='Trans_count', y='State',
                                            color='Trans_count', color_continuous_scale='turbo',
                                            title=f'MAP.TRANS_State_count_ASEC Analysis Chart', height=500, )
            MAP_TCOUNT_ASEC.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
            #MAP_TCOUNT_ASEC.show()
            st.plotly_chart(MAP_TCOUNT_ASEC, use_container_width=True)

        col5,col6= st.columns(2)
        with col5:
            #MAP.TRANS_State_count_DSEC Analysis Chart
            mtCOUNd_1['State'] = mtCOUNd_1['State'].astype(str)
            mtCOUNd_1['Trans_count'] =mtCOUNd_1['Trans_count'].astype(float)
            MAP_TCOUNT_DSEC= px.bar(mtCOUNd_1, x='Trans_count', y='State',
                                            color='Trans_count', color_continuous_scale='turbo',
                                            title=f'MAP.TRANS_State_count_DSEC Analysis Chart', height=500, )
            MAP_TCOUNT_DSEC.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
            #MAP_TCOUNT_DSEC.show()
            st.plotly_chart(MAP_TCOUNT_DSEC, use_container_width=True)
        with col6:
            #MAP.TRANS_State_count_AVG Analysis Chart
            mtCOUNA_1['State'] =mtCOUNA_1['State'].astype(str)
            mtCOUNA_1['Trans_count'] =mtCOUNA_1['Trans_count'].astype(float)
            MAP_TCOUNT_AVG= px.bar(mtCOUNA_1, x='Trans_count', y='State',
                                            color='Trans_count', color_continuous_scale='turbo',
                                            title=f'MAP.TRANS_State_count_AVG Analysis Chart', height=500, )
            MAP_TCOUNT_AVG.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
            #MAP_TCOUNT_AVG.show()
            st.plotly_chart(MAP_TCOUNT_AVG, use_container_width=True)

    if query=='Query 3':
        st.subheader('State wise top transaction counts and Amounts data visualization')
        mycursor.execute(f"SELECT State,SUM(P_count) AS P_count FROM top_trans GROUP BY State ORDER BY P_count LIMIT 10;")
        TtCOUNa=pd.DataFrame(mycursor.fetchall(),columns=['State','P_count'])
        TtCOUNa_1=TtCOUNa.set_index(pd.Index(range(1, len(TtCOUNa) + 1)))

        mycursor.execute(f"SELECT State,SUM(P_count) AS P_count  FROM top_trans GROUP BY State ORDER BY P_count DESC LIMIT 10;")
        TtCOUNd=pd.DataFrame(mycursor.fetchall(),columns=['State','P_count'])
        TtCOUNd_1=TtCOUNd.set_index(pd.Index(range(1, len(TtCOUNd) + 1)))

        mycursor.execute(f"SELECT State,AVG(P_count) AS P_count FROM top_trans GROUP BY State ORDER BY P_count;")
        TtCOUNA=pd.DataFrame(mycursor.fetchall(),columns=['State','P_count'])
        TtCOUNA_1=TtCOUNA.set_index(pd.Index(range(1, len(TtCOUNA) + 1)))

        mycursor.execute(f"SELECT State,SUM(P_amount) AS P_amount FROM top_trans GROUP BY State ORDER BY P_amount LIMIT 10;")
        TtAMTa=pd.DataFrame(mycursor.fetchall(),columns=['State','P_amount'])
        TtAMTa_1=TtAMTa.set_index(pd.Index(range(1, len(TtAMTa) + 1)))

        mycursor.execute(f"SELECT State,SUM(P_amount) AS P_amount FROM top_trans GROUP BY State ORDER BY P_amount DESC LIMIT 10;")
        TtAMTd=pd.DataFrame(mycursor.fetchall(),columns=['State','P_amount'])
        TtAMTd_1=TtAMTd.set_index(pd.Index(range(1, len(TtAMTd) + 1)))


        mycursor.execute(f"SELECT State,AVG(P_amount) AS P_amount FROM top_trans GROUP BY State ORDER BY P_amount;")
        TtAMTA=pd.DataFrame(mycursor.fetchall(),columns=['State','P_amount'])
        TtAMTA_1=TtAMTA.set_index(pd.Index(range(1, len(TtAMTA) + 1)))

        col1,col2= st.columns(2)
        with col1:
            #TOP.TRANS_State_COUNT_ASEC Analysis Chart
            TtCOUNa_1['State'] = TtCOUNa_1['State'].astype(str)
            TtCOUNa_1['P_count'] =TtCOUNa_1['P_count'].astype(float)
            TOP_TCOUNT_ASEC= px.bar(TtCOUNa_1, x='P_count', y='State',
                                            color='P_count', color_continuous_scale='turbo',
                                            title=f'TOP.TRANS_State_COUNT_ASEC Analysis Chart', height=500, )
            TOP_TCOUNT_ASEC.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
            #TOP_TCOUNT_ASEC.show()
            st.plotly_chart(TOP_TCOUNT_ASEC, use_container_width=True)
        with col2:
            #TOP.TRANS_State_COUNT_DSEC Analysis Chart
            TtCOUNd_1['State'] = TtCOUNd_1['State'].astype(str)
            TtCOUNd_1['P_count'] =TtCOUNd_1['P_count'].astype(float)
            TOP_TCOUNT_DSEC= px.bar(TtCOUNd_1, x='P_count', y='State',
                                            color='P_count', color_continuous_scale='turbo',
                                            title=f'TOP.TRANS_State_COUNT_DSEC Analysis Chart', height=500, )
            TOP_TCOUNT_DSEC.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
            #TOP_TCOUNT_DSEC.show()
            st.plotly_chart(TOP_TCOUNT_DSEC, use_container_width=True)
        col3,col4= st.columns(2)
        with col3:
            #TOP.TRANS_State_COUNT_AVG Analysis Chart
            TtCOUNA_1['State'] =TtCOUNA_1['State'].astype(str)
            TtCOUNA_1['P_count'] =TtCOUNA_1['P_count'].astype(float)
            TOP_TCOUNT_AVG= px.bar(TtCOUNA_1, x='P_count', y='State',
                                            color='P_count', color_continuous_scale='turbo',
                                            title=f'TOP.TRANS_State_COUNT_AVG Analysis Chart', height=500, )
            TOP_TCOUNT_AVG.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
            #TOP_TCOUNT_AVG.show()
            st.plotly_chart(TOP_TCOUNT_AVG, use_container_width=True)
        with col4:
            #TOP.TRANS_State_AMT_ASEC Analysis Chart
            TtAMTa_1['State'] = TtAMTa_1['State'].astype(str)
            TtAMTa_1['P_amount'] =TtAMTa_1['P_amount'].astype(float)
            TOP_TAMT_ASEC= px.bar(TtAMTa_1, x='P_amount', y='State',
                                                        color='P_amount', color_continuous_scale='turbo',
                                                        title=f'TOP.TRANS_State_AMT_ASEC Analysis Chart', height=500, )
            TOP_TAMT_ASEC.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
            #TOP_TAMT_ASEC.show()
            st.plotly_chart(TOP_TAMT_ASEC, use_container_width=True)
        col5,col6= st.columns(2)
        with col5:
            #TOP.TRANS_State_AMT_DSEC Analysis Chart
            TtAMTd_1['State'] = TtAMTd_1['State'].astype(str)
            TtAMTd_1['P_amount'] =TtAMTd_1['P_amount'].astype(float)
            TOP_TAMT_DSEC= px.bar(TtAMTd_1, x='P_amount', y='State',
                                            color='P_amount', color_continuous_scale='turbo',
                                            title=f'TOP.TRANS_State_AMT_DSEC Analysis Chart', height=500, )
            TOP_TAMT_DSEC.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
            #TOP_TAMT_DSEC.show()
            st.plotly_chart(TOP_TAMT_DSEC, use_container_width=True)
        with col6:
            #TOP.TRANS_State_AMT_AVG Analysis Chart
            TtAMTA_1['State'] = TtAMTA_1['State'].astype(str)
            TtAMTA_1['P_amount'] =TtAMTA_1['P_amount'].astype(float)
            TOP_TAMT_AVG= px.bar(TtAMTA_1, x='P_amount', y='State',
                                                        color='P_amount', color_continuous_scale='turbo',
                                                        title=f'TOP.TRANS_State_AMT_AVG Analysis Chart', height=500, )
            TOP_TAMT_AVG.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
            #TOP_TAMT_AVG.show()
            st.plotly_chart(TOP_TAMT_AVG, use_container_width=True)
    if query=='Query 4':
        st.subheader('State and District wise Registered user in Map User')
        mycursor.execute(f"SELECT State,SUM(Regis_user) AS Regis_user FROM map_user GROUP BY State ORDER BY Regis_user LIMIT 10;")
        MUSRUa=pd.DataFrame(mycursor.fetchall(),columns=['State','Regis_user'])
        MUSRUa_1=MUSRUa.set_index(pd.Index(range(1, len(MUSRUa) + 1)))

        mycursor.execute(f"SELECT State,SUM(Regis_user) AS Regis_user FROM map_user GROUP BY State ORDER BY Regis_user DESC LIMIT 10;")
        MUSRUd=pd.DataFrame(mycursor.fetchall(),columns=['State','Regis_user'])
        MUSRUd_1=MUSRUd.set_index(pd.Index(range(1, len(MUSRUd) + 1)))

        mycursor.execute(f"SELECT State,AVG(Regis_user) AS Regis_user FROM map_user GROUP BY State ORDER BY Regis_user;")
        MUSRUA=pd.DataFrame(mycursor.fetchall(),columns=['State','Regis_user'])
        MUSRUA_1=MUSRUA.set_index(pd.Index(range(1, len(MUSRUA) + 1)))

        mycursor.execute(f"SELECT District,SUM(Regis_user) AS Regis_user FROM map_user GROUP BY District ORDER BY Regis_user LIMIT 10;")
        MUDRUa=pd.DataFrame(mycursor.fetchall(),columns=['District','Regis_user'])
        MUDRUa_1=MUDRUa.set_index(pd.Index(range(1, len(MUDRUa) + 1)))

        mycursor.execute(f"SELECT District,SUM(Regis_user) AS Regis_user FROM map_user GROUP BY District ORDER BY Regis_user DESC LIMIT 10;")
        MUDRUd=pd.DataFrame(mycursor.fetchall(),columns=['District','Regis_user'])
        MUDRUd_1=MUDRUd.set_index(pd.Index(range(1, len(MUDRUd) + 1)))

        col1,col2= st.columns(2)
        with col1:
        #MAP.USER_State_REGIS USER_ASEC Analysis Chart
            MUSRUa_1['State'] = MUSRUa_1['State'].astype(str)
            MUSRUa_1['Regis_user'] =MUSRUa_1['Regis_user'].astype(float)
            MAP_RUSER_ASEC= px.bar(MUSRUa_1, x='Regis_user', y='State',
                                                        color='Regis_user', color_continuous_scale='turbo',
                                                        title=f'MAP.USER_REGISUR_ASEC Analysis Chart', height=500, )
            MAP_RUSER_ASEC.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
            #MAP_RUSER_ASEC.show()
            st.plotly_chart(MAP_RUSER_ASEC, use_container_width=True)
        with col2:
            #MAP.USER_State_REGIS USER_DSEC Analysis Chart
            MUSRUd_1['State'] =MUSRUd_1['State'].astype(str)
            MUSRUd_1['Regis_user'] =MUSRUd_1['Regis_user'].astype(float)
            MAP_RUSER_DSEC= px.bar(MUSRUd_1, x='Regis_user', y='State',
                                                        color='Regis_user', color_continuous_scale='turbo',
                                                        title=f'MAP.USER_REGISUR_DSEC Analysis Chart', height=500, )
            MAP_RUSER_DSEC.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
            #MAP_RUSER_DSEC.show()
            st.plotly_chart(MAP_RUSER_DSEC, use_container_width=True)
        col3,col4= st.columns(2)
        with col3:
            #MAP.USER_State_REGIS USER_AVG Analysis Chart
            MUSRUA_1['State'] =MUSRUA_1['State'].astype(str)
            MUSRUA_1['Regis_user'] =MUSRUA_1['Regis_user'].astype(float)
            MAP_RUSER_AVG= px.bar(MUSRUA_1, x='Regis_user', y='State',
                                                        color='Regis_user', color_continuous_scale='turbo',
                                                        title=f'MAP.USER_REGISUR_AVG Analysis Chart', height=500, )
            MAP_RUSER_AVG.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
            #MAP_RUSER_AVG.show()
            st.plotly_chart(MAP_RUSER_AVG, use_container_width=True)
        with col4:
            #MAP.USER_DIST_REGIS USER_ASEC Analysis Chart
            MUDRUa_1['District'] =MUDRUa_1['District'].astype(str)
            MUDRUa_1['Regis_user'] =MUDRUa_1['Regis_user'].astype(float)
            MAP_DRUSER_ASEC= px.bar(MUDRUa_1, x='Regis_user', y='District',
                                                        color='Regis_user', color_continuous_scale='turbo',
                                                        title=f'MAP.USER_DREGISUR_ASEC Analysis Chart', height=500, )
            MAP_DRUSER_ASEC.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
            #MAP_DRUSER_ASEC.show()
            st.plotly_chart(MAP_DRUSER_ASEC, use_container_width=True)
        col5,col6= st.columns(2)
        with col5:#MAP.USER_DIST_REGIS USER_DSEC Analysis Chart
            MUDRUd_1['District'] =MUDRUd_1['District'].astype(str)
            MUDRUd_1['Regis_user'] =MUDRUd_1['Regis_user'].astype(float)
            MAP_DRUSER_DSEC= px.bar(MUDRUd_1, x='Regis_user', y='District',
                                                        color='Regis_user', color_continuous_scale='turbo',
                                                        title=f'MAP.USER_DREGISUR_DSEC Analysis Chart', height=700, )
            MAP_DRUSER_DSEC.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
            #MAP_DRUSER_DSEC.show()
            st.plotly_chart(MAP_DRUSER_DSEC, use_container_width=True)
    if query=='Query 5':
        st.subheader('State and District wise App opened  in Map User')
        mycursor.execute(f"SELECT State,SUM(App_open) AS App_open FROM map_user GROUP BY State ORDER BY App_open  LIMIT 10;")
        MUSAOa=pd.DataFrame(mycursor.fetchall(),columns=['State','App_open'])
        MUSAOa_1=MUSAOa.set_index(pd.Index(range(1, len(MUSAOa) + 1)))

        mycursor.execute(f"SELECT State,SUM(App_open) AS App_open FROM map_user GROUP BY State ORDER BY App_open DESC LIMIT 10;")
        MUSAOd=pd.DataFrame(mycursor.fetchall(),columns=['State','App_open'])
        MUSAOd_1=MUSAOd.set_index(pd.Index(range(1, len(MUSAOd) + 1)))

        mycursor.execute(f"SELECT State,AVG(App_open) AS App_open FROM map_user GROUP BY State ORDER BY App_open;")
        MUSAOA=pd.DataFrame(mycursor.fetchall(),columns=['State','App_open'])
        MUSAOA_1=MUSAOA.set_index(pd.Index(range(1, len(MUSAOA) + 1)))

        mycursor.execute(f"SELECT District ,SUM(App_open) AS App_open FROM map_user GROUP BY District  ORDER BY App_open  LIMIT 10;")
        MUDAOa=pd.DataFrame(mycursor.fetchall(),columns=['District','App_open'])
        MUDAOa_1=MUDAOa.set_index(pd.Index(range(1, len(MUDAOa) + 1)))

        mycursor.execute(f"SELECT District ,SUM(App_open) AS App_open FROM map_user GROUP BY District  ORDER BY App_open DESC LIMIT 10;")
        MUDAOd=pd.DataFrame(mycursor.fetchall(),columns=['District','App_open'])
        MUDAOd_1=MUDAOd.set_index(pd.Index(range(1, len(MUDAOd) + 1)))
        col1,col2= st.columns(2)
        with col1:
            #MAP.USER_State_APP OPEN_ASEC Analysis Chart
            MUSAOa_1['State'] = MUSAOa_1['State'].astype(str)
            MUSAOa_1['App_open'] =MUSAOa_1['App_open'].astype(float)
            MAP_APPO_ASEC= px.bar(MUSAOa_1, x='App_open', y='State',
                                                        color='App_open', color_continuous_scale='turbo',
                                                        title=f'MAP.USER_APPOPEN_ASEC Analysis Chart', height=700, )
            MAP_APPO_ASEC.update_layout(title_font=dict(size=25), title_font_color='#3377FF')
            #MAP_APPO_ASEC.show()
            st.plotly_chart(MAP_APPO_ASEC, use_container_width=True)
        with col2:
            #MAP.USER_State_APP OPEN_DSEC Analysis Chart
            MUSAOd_1['State'] = MUSAOd_1['State'].astype(str)
            MUSAOd_1['App_open'] =MUSAOd_1['App_open'].astype(float)
            MAP_APPO_DSEC= px.bar(MUSAOd_1, x='App_open', y='State',
                                                        color='App_open', color_continuous_scale='turbo',
                                                        title=f'MAP.USER_APPOPEN_DSEC Analysis Chart', height=700, )
            MAP_APPO_DSEC.update_layout(title_font=dict(size=25), title_font_color='#3377FF')
            #MAP_APPO_DSEC.show()
            st.plotly_chart(MAP_APPO_DSEC, use_container_width=True)

        col3,col4= st.columns(2)
        with col3:
            #MAP.USER_State_APP OPEN_DSEC Analysis Chart
            MUSAOA_1['State'] = MUSAOA_1['State'].astype(str)
            MUSAOA_1['App_open'] =MUSAOA_1['App_open'].astype(float)
            MAP_APPO_AVG= px.bar(MUSAOA_1, x='App_open', y='State',
                                                        color='App_open', color_continuous_scale='turbo',
                                                        title=f'MAP.USER_APPOPEN_AVG Analysis Chart', height=700, )
            MAP_APPO_AVG.update_layout(title_font=dict(size=25), title_font_color='#3377FF')
            #MAP_APPO_AVG.show()
            st.plotly_chart(MAP_APPO_AVG, use_container_width=True)
        with col4:
             #MAP.USER_district_APP OPEN_ASEC Analysis Chart
            MUDAOa_1['District'] = MUDAOa_1['District'].astype(str)
            MUDAOa_1['App_open'] =MUDAOa_1['App_open'].astype(float)
            MAP_DIST_APPO_ASEC= px.bar(MUDAOa_1, x='App_open', y='District',
                                                        color='App_open', color_continuous_scale='turbo',
                                                        title=f'MAP.USER_DIST_APPOPEN_ASEC Analysis Chart', height=500, )
            MAP_DIST_APPO_ASEC.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
            #MAP_DIST_APPO_ASEC.show()
            st.plotly_chart(MAP_DIST_APPO_ASEC, use_container_width=True)
        
        col5,col6= st.columns(2)
        with col5:
            #MAP.USER_district_APP OPEN_ASEC Analysis Chart
            MUDAOd_1['District'] = MUDAOd_1['District'].astype(str)
            MUDAOd_1['App_open'] =MUDAOd_1['App_open'].astype(float)
            MAP_DIST_APPO_DSEC= px.bar(MUDAOd_1, x='App_open', y='District',
                                                        color='App_open', color_continuous_scale='turbo',
                                                        title=f'MAP.USER_DIST_APPOPEN_DSEC Analysis Chart', height=500, )
            MAP_DIST_APPO_DSEC.update_layout(title_font=dict(size=20), title_font_color='#3377FF')
            #MAP_DIST_APPO_DSEC.show()
            st.plotly_chart(MAP_DIST_APPO_DSEC, use_container_width=True)





































                         
            






    


