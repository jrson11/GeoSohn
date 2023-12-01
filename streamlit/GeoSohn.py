# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# Purpose: To develop python script to manage geotechnical engineering skills
# Author: J.S.
# Date: 12/1/2023
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# Contents
#    1. Data (AGS format digitized)
#    2. Site Investigation (CPT + MV + TV)
#    3. Lab Testing
#    4. Shallow Foundation
#    5. Deep Foundation
#    6. Risk Assessment
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# Structure
#    A. Functions
#    B. Setup
#    C. Sidebar (pw + project)
#    D. Main (Engineering Analysis + Control Panel + Plot)
# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

## Setup main streamlit options
st.set_page_config(layout="wide") # wide / centered 


# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# A. Functions
class ImportData:
    def __init__(self, file):
        self.df_PROJ = pd.read_excel(file, sheet_name="PROJ", header=2)
        self.df_LOCA = pd.read_excel(file, sheet_name="LOCA", header=2)
        self.df_GEOL = pd.read_excel(file, sheet_name="GEOL", header=2)
        self.df_SCPT = pd.read_excel(file, sheet_name="SCPT", header=2)
        self.df_IVAN = pd.read_excel(file, sheet_name="IVAN", header=2)
        
               
class SiteInvestigation:
    def __init__(self, DB):
        self.DB = DB
        
    def MAP(self, df_LOCA):
        # Engineering Analysis
        min_NATN = min(df_LOCA['LOCA_NATN_ft'])
        max_NATN = max(df_LOCA['LOCA_NATN_ft'])
        min_NATE = min(df_LOCA['LOCA_NATE_ft'])
        max_NATE = max(df_LOCA['LOCA_NATE_ft'])  

        # Control Panel
        
        
        # Plotting with Altair   
        base = alt.Chart(df_LOCA).mark_point(opacity=0.9).encode(
                x=alt.X('LOCA_NATE_ft', scale=alt.Scale(domain=(min_NATE-1e3,max_NATE+1e3))), 
                y=alt.Y('LOCA_NATN_ft', scale=alt.Scale(domain=(min_NATN-1e3,max_NATN+1e3))), 
                color=('LOCA_TYPE_x'),
                shape=('LOCA_TYPE_x'),
                tooltip=['LOCA_ID_x','LOCA_FDEO_ft']
                ).properties(width=900, height=600).interactive()
        #
        text = base.mark_text(align='left',baseline='middle',color=('black')
                                  ).encode(text='LOCA_ID_x')

        # Display the chart using Streamlit
        st.altair_chart(base, use_container_width=True)
        
    def CPT(self, df_SCPT):
        col1, col2 = st.columns(2)
        
        with col1:
            # Enngineering Analysis
            list_SCPT_LOCA_ID = list(pd.unique(df_SCPT['LOCA_ID_x']))
            n_SCPT_LOCA_ID = len(list_SCPT_LOCA_ID)
                
            # Control Panel
            st.text('Control Panel')
            selected_cpt_loca_id = st.selectbox('Location of CPT',list(['ALL'])+list_SCPT_LOCA_ID)
            selected_cpt_zmax = int(st.text_input('Max depth of CPT (m) =', 40))
            selected_qcmax = int(st.text_input('Max qc (MPa) =', 2))      
            
            # Note
            st.text('Note')
            
        with col2:
            # Plot
            fig,ax = plt.subplots(1,2,figsize=(7,7), dpi=100)
            #
            if selected_cpt_loca_id == 'ALL':
                for i in range(n_SCPT_LOCA_ID):
                    loca_id = list_SCPT_LOCA_ID[i]
                    ii = loca_id == df_SCPT['LOCA_ID_x']
                    ax[0].plot(df_SCPT.loc[ii,'SCPT_RES_MPa'],df_SCPT.loc[ii,'SCPT_DPTH_m'],'.',alpha=0.1)
                    ax[1].plot(df_SCPT.loc[ii,'SCPT_QNET_kPa'],df_SCPT.loc[ii,'SCPT_DPTH_m'],'.',alpha=0.1,label=loca_id)
            else:
                ii = selected_cpt_loca_id == df_SCPT['LOCA_ID_x']
                ax[0].plot(df_SCPT.loc[ii,'SCPT_RES_MPa'],df_SCPT.loc[ii,'SCPT_DPTH_m'],'.',alpha=0.1)
                ax[1].plot(df_SCPT.loc[ii,'SCPT_QNET_kPa'],df_SCPT.loc[ii,'SCPT_DPTH_m'],'.',alpha=0.1,label=selected_cpt_loca_id)            
            #
            ax[0].set_ylabel("Depth (m)")
            ax[0].set_xlabel("qc (MPa)")
            ax[0].set_xlim([0,selected_qcmax])
            ax[1].set_ylabel("Depth (m)")
            ax[1].set_xlabel("qnet (kPa)")
            ax[1].set_xlim([0,selected_qcmax*1000])
            #
            for j in range(2):
                ax[j].set_ylim([selected_cpt_zmax,0])
                ax[j].grid(linestyle='dotted')
                ax[j].minorticks_on()
            ax[1].legend(loc=0, fancybox=True, shadow=True, fontsize=10, ncol=1)
            #
            plt.tight_layout()
            st.pyplot(fig)
            
    def Su(self, df_SCPT, df_IVAN, df_GEOL):
        col1, col2 = st.columns(2)
        
        with col1:
            # Enngineering Analysis        
            list_SCPT_LOCA_ID = list(pd.unique(df_SCPT['LOCA_ID_x']))
            list_IVAN_LOCA_ID = list(pd.unique(df_IVAN['LOCA_ID_x']))
            list_GEOL_PROJ_ID = list(pd.unique(df_GEOL['PROJ_ID_x']))
            #st.write(list_GEOL_PROJ_ID)
            MV = df_IVAN['IVAN_TYPE_x'] == 'MV'
            list_MV_LOCA_ID = list(pd.unique(df_IVAN.loc[MV,'LOCA_ID_x']))
            #st.write(list_MV_LOCA_ID)
            n_MV_LOCA_ID = len(list_MV_LOCA_ID)
            TV = df_IVAN['IVAN_TYPE_x'] == 'TV'
            list_TV_LOCA_ID = list(pd.unique(df_IVAN.loc[TV,'LOCA_ID_x']))
            #st.write(list_TV_LOCA_ID)
            n_TV_LOCA_ID = len(list_TV_LOCA_ID)
                
            # Control Panel
            st.text('Control Panel')
            selected_su_loca_id = st.selectbox('Location of Su',list(['ALL'])+list_IVAN_LOCA_ID)
            selected_su_zmax = int(st.text_input('Max depth of Su (m) =', 35))
            selected_sumax = int(st.text_input('Max su (kPa) =', 50))    
            
            # Note
            st.text('Note')
            st.text('No. of MV = '+str(n_MV_LOCA_ID)+' , No. of TV = '+str(n_TV_LOCA_ID))
            
            # CPT
            onCPT = st.toggle('Activate CPT profiles with Nkt')
            if onCPT:
                selected_Nkt = int(st.text_input('Nkt (-) =', 25))
                selected_su_cpt_id = st.selectbox('Location of CPT for Su',list(['ALL'])+list_SCPT_LOCA_ID)
                
            # Recommended profiles
            onBP = st.toggle('Activate recomended profiles')
            if onBP:
                selected_su_proj_id = st.selectbox('Recommended Su',list_GEOL_PROJ_ID)
                kk = selected_su_proj_id == df_GEOL['PROJ_ID_x']
                st.dataframe(df_GEOL.loc[kk,['GEOL_TOP_m','GEOL_SU_kPa']])
            
        with col2:
            # Plot
            fig,ax = plt.subplots(1,2,figsize=(7,7), dpi=100)
            #
            if selected_su_loca_id == 'ALL':
                # MV
                for i in range(n_MV_LOCA_ID):
                    loca_id = list_MV_LOCA_ID[i]
                    color_idx = list_IVAN_LOCA_ID.index(loca_id)
                    ii = loca_id == df_IVAN['LOCA_ID_x']
                    ax[0].plot(df_IVAN.loc[ii&MV,'IVAN_IVAN_kPa'],df_IVAN.loc[ii&MV,'IVAN_DPTH_m'],'o',color='C'+str(color_idx),alpha=0.5)
                    ax[1].plot(df_IVAN.loc[ii&MV,'IVAN_IVAN_ksf'],df_IVAN.loc[ii&MV,'IVAN_DPTH_ft'],'o',color='C'+str(color_idx),alpha=0.5,label=loca_id)
                
                # TV
                for i in range(n_TV_LOCA_ID):
                    loca_id = list_TV_LOCA_ID[i]
                    color_idx = list_IVAN_LOCA_ID.index(loca_id)
                    ii = loca_id == df_IVAN['LOCA_ID_x']
                    ax[0].plot(df_IVAN.loc[ii&TV,'IVAN_IVAN_kPa'],df_IVAN.loc[ii&TV,'IVAN_DPTH_m'],'x',color='C'+str(color_idx),alpha=0.5,label=loca_id)
                    ax[1].plot(df_IVAN.loc[ii&TV,'IVAN_IVAN_ksf'],df_IVAN.loc[ii&TV,'IVAN_DPTH_ft'],'x',color='C'+str(color_idx),alpha=0.5)
                    
                # CPT
                if onCPT:
                    if selected_su_cpt_id == 'ALL':
                        ax[0].plot(df_SCPT['SCPT_QNET_kPa']/selected_Nkt,df_SCPT['SCPT_DPTH_m'],'.',c='grey',alpha=0.1)
                    else:
                        jj = selected_su_cpt_id == df_SCPT['LOCA_ID_x']
                        ax[0].plot(df_SCPT.loc[jj,'SCPT_QNET_kPa']/selected_Nkt,df_SCPT.loc[jj,'SCPT_DPTH_m'],'.',c='grey',alpha=0.1)
                
                # Recommended Su
                if onBP:
                    kk = selected_su_proj_id == df_GEOL['PROJ_ID_x']
                    #st.dataframe(df_GEOL.loc[kk,'GEOL_SU_kPa'])
                    #st.dataframe(df_GEOL.loc[kk,'GEOL_TOP_m'])
                    ax[0].plot(df_GEOL.loc[kk,'GEOL_SU_kPa'],df_GEOL.loc[kk,'GEOL_TOP_m'],'r--')
                    
            else:
                ii = selected_su_loca_id == df_IVAN['LOCA_ID_x']
                color_idx = list_IVAN_LOCA_ID.index(selected_su_loca_id)
                # MV
                ax[0].plot(df_IVAN.loc[ii&MV,'IVAN_IVAN_kPa'],df_IVAN.loc[ii&MV,'IVAN_DPTH_m'],'o',color='C'+str(color_idx),alpha=0.5)
                ax[1].plot(df_IVAN.loc[ii&MV,'IVAN_IVAN_ksf'],df_IVAN.loc[ii&MV,'IVAN_DPTH_ft'],'o',color='C'+str(color_idx),alpha=0.5,label=selected_su_loca_id)
                # TV
                ax[0].plot(df_IVAN.loc[ii&TV,'IVAN_IVAN_kPa'],df_IVAN.loc[ii&TV,'IVAN_DPTH_m'],'x',color='C'+str(color_idx),alpha=0.5,label=selected_su_loca_id)
                ax[1].plot(df_IVAN.loc[ii&TV,'IVAN_IVAN_ksf'],df_IVAN.loc[ii&TV,'IVAN_DPTH_ft'],'x',color='C'+str(color_idx),alpha=0.5)                         
            #
            ax[0].set_ylabel("Depth (m)")
            ax[0].set_xlabel("Su (kPa)")
            ax[0].set_xlim([0,selected_sumax])
            ax[0].set_ylim([selected_su_zmax,0])
            ax[1].set_ylabel("Depth (ft)")
            ax[1].set_xlabel("Su (ksf)")
            ax[1].set_xlim([0,selected_sumax/47.880])
            ax[1].set_ylim([selected_su_zmax*3.280,0])
            ax[0].text(selected_sumax*0.7,selected_su_zmax*0.9,'o MV \n x TV', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=1'))
            #
            for j in range(2):
                ax[j].grid(linestyle='dotted')
                ax[j].minorticks_on()
                ax[j].legend(loc=0, fancybox=True, shadow=True, fontsize=10, ncol=1)
            #
            plt.tight_layout()
            st.pyplot(fig)

    def SUW(self, df_SCPT, df_IVAN):
        col1, col2 = st.columns(2)

            
    def run(self):
        st.dataframe(self.DB.df_PROJ)
        
        tab0, tab1, tab2, tab3 = st.tabs(['0.Map', '1.CPT', '2.Su', '3.SUW'])
            
        with tab0:
            #st.text('Map')
            self.MAP(self.DB.df_LOCA)
                
        with tab1:
            #st.text('CPT')
            self.CPT(self.DB.df_SCPT)
                
        with tab2:
            #st.text('Su')
            self.Su(self.DB.df_SCPT, self.DB.df_IVAN, self.DB.df_GEOL)

        with tab3:
            #st.text('Su')
            self.SUW(self.DB.df_SCPT, self.DB.df_IVAN)
                
# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# B. Setup

# Note: Use the raw file URL on GitHub to get the correct file content
#url_Kaskida = "https://github.com/jrson11/GeoSohn/raw/main/streamlit/src_AGS/AGS_Kaskida(24Nov23).xlsx"
#url_Argos = "https://github.com/jrson11/GeoSohn/raw/main/streamlit/src_AGS/AGS_Argos(24Nov23).xlsx"
#url_NaKika = "https://github.com/jrson11/GeoSohn/raw/main/streamlit/src_AGS/AGS_NaKika(24Nov23).xlsx"
url_Kaskida = "./src_AGS/AGS_Kaskida(01Dec23).xlsx"
url_Argos = "./src_AGS/AGS_Argos(01Dec23).xlsx"
url_NaKika = "./src_AGS/AGS_NaKika(01Dec23).xlsx"
df_Kaskida = ImportData(url_Kaskida)
df_Argos = ImportData(url_Argos)
df_NaKika = ImportData(url_NaKika)

# Create a dictionary to store data frames based on project names
project_data = {
    'All': None,
    'Kaskida': df_Kaskida,
    'Argos': df_Argos,
    'NaKika': df_NaKika
}


# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# C. Sidebar
selected_project = st.sidebar.selectbox("Select Project", ["All", "Kaskida", "Argos", "NaKika"])

#pw_input = st.sidebar.text_input('Password = ', '?')
#if pw_input == st.secrets['DB_pw']:
#  selected_project = st.sidebar.selectbox("Select Project", ["All", "Kaskida", "Argos", "NaKika"])
#else:
#  selected_project = st.sidebar.selectbox("Select Project", ["None"])

# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# D. Main

## Intro
selected_analysis = st.selectbox("Select Analysis", ["AGS Data", "Site Investigation", "Lab Testing", "Shallow Foundation", "Deep Foundation", "Risk Assessment"])

# Display the image for 'All' projects
if selected_project == 'All':
    st.image("https://raw.githubusercontent.com/jrson11/GeoSohn/main/docs/images/Canvas_of_Offshore_Geotech(Sep2023).png")
    

# Check if the selected project is in the dictionary
elif selected_project in project_data:
    
    # Setup
    DB = project_data[selected_project]
    n_LOCA = len(DB.df_LOCA)
    n_BC = len(DB.df_LOCA[DB.df_LOCA['LOCA_TYPE_x'] == 'BC'])
    n_PC = len(DB.df_LOCA[DB.df_LOCA['LOCA_TYPE_x'] == 'PC'])
    n_JPC = len(DB.df_LOCA[DB.df_LOCA['LOCA_TYPE_x'] == 'JPC'])
    n_CPT = len(DB.df_LOCA[DB.df_LOCA['LOCA_TYPE_x'] == 'CPT'])

    # Sidebar
    st.sidebar.text('No. of LOCA = '+str(n_LOCA))
    st.sidebar.text('No. of BC = '+str(n_BC))
    st.sidebar.text('No. of PC = '+str(n_PC))
    st.sidebar.text('No. of JPC = '+str(n_JPC))
    st.sidebar.text('No. of CPT = '+str(n_CPT))

    # Main
    if DB:
        if selected_analysis == 'AGS Data':
            st.dataframe(DB.df_PROJ)
            st.dataframe(DB.df_LOCA)
            
        elif selected_analysis == 'Site Investigation':
            SI = SiteInvestigation(DB)
            SI.run()
