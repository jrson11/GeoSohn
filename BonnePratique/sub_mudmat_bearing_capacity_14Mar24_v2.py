import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# log
#    03/13/2024: 첫번째 버전 완성
#    03/14/2024: 진진 박사님께 처음으로 시연
#    03/14/2024: 클래스를 사용한 객체화 시도

# ================================================================================
## 클래스

class Mudmat_Geometry:
    def __init__(self,B,L,D):
        self.B = B
        self.L = L
        self.D = D

class Mudmat_Load:
    def __init__(self,Vext):
        self.Vext = Vext

class Mudmat_Soil:
    Nc = 5.14
    def __init__(self,k):
        self.Su0 = Su0
        self.k = k

class Mudmat_Factor:
    def __init__(self,g):
        self.g = g


# ================================================================================
## 서브펑션

def inputs_for_mudmat(project):

    if project == '10inchFTA_Tortue':
        B = 6
        L = 12
        D = 0.2
    else:
        pass

    Mudmat_inputs = Mudmat_Geometry(B,L,D)
    Mudmat_loads = Mudmat_Load(1)
    Mudmat_soils = Mudmat_Soil(1,1)
    Mudmat_factorss = Mudmat_Factor(1)

    return Mudmat_inputs, Mudmat_soils




def sidebar():
    st.sidebar.subheader('Special thanks to the my Advisor Philippe Jeanjean, Ph.D., P.E., F.ASCE')
    st.sidebar.write(':blue[Purpose]: To estimate Factor of Safety from offshore mudmat bearing capacity analysis with CLAY soils.')
    st.sidebar.write(':blue[How to use]: Left columns has three tabs. Please fill out input data in the 1st tab.')
    st.sidebar.write(':blue[Last update]: 03/14/2024')
    
def comment(toggle, symbol, note):
    if toggle:
        st.write(':blue['+symbol+']: '+note)


# ================================================================================
## 메인
def main(project):
    sidebar()
    col1, col2 = st.columns([1,2])

    # --------------------------------------------------------------------
    with col1:

        tab1,tab2,tab3 = st.tabs(['Input','Deduced','Output'])
        
        with tab1:
            st.header(':blue[Input Properties]')
            onComments = st.toggle('Comments On')
            Mudmat_inputs, Mudmat_soils = inputs_for_mudmat(project)
            
            st.subheader('Foundation Geometry')
            st.write('B (m) ='+str(Mudmat_inputs.B))
            st.write('L (m) ='+str(Mudmat_inputs.L))
            st.write('D (m) ='+str(Mudmat_inputs.D))

            st.subheader('Loads')
            st.subheader('Soil')
            st.subheader('Factors')

        with tab2:
            st.header(':green[Deduced Values]')   
            st.write('Nc ='+str(Mudmat_soils.Nc))
            
        with tab3:
            st.header(':red[Output Results]')        


def eg_clay_bearing_capacity():
    sidebar()
    
    col1, col2 = st.columns([1,2])

    # --------------------------------------------------------------------
    with col1:

        tab1,tab2,tab3 = st.tabs(['Input','Deduced','Output'])

        with tab1:
            st.header(':blue[Input Properties]')
            onComments = st.toggle('Comments On')

            ## Foundation Geometry
            st.subheader('Foundation Geometry')
            col_g1,col_g2,col_g3 = st.columns(3)
            with col_g1:
                B = st.number_input('B (m)', value = 10)
                comment(onComments, 'B', 'Width')
            with col_g2:
                L = st.number_input('L (m)', value = 10)      # Length (m)
                comment(onComments, 'L', 'Length')
            with col_g3:
                D = st.number_input('D (m)', value = 2)       # Embedment (m)
                comment(onComments, 'D', 'Embedment')

            ## Loads
            st.subheader('Loads')
            col_l1,col_l2,col_l3 = st.columns(3)
            with col_l1:
                SW = st.number_input('SW (kN)', value = 0)         # Self weight (kN)
                comment(onComments, 'SW', 'Self weight')
                Vext = st.number_input('Vext (kN)', value = 2000)  # External Vertical load (kN)
                comment(onComments, 'Vext', 'External Vertical load')
            with col_l2:
                Hext = st.number_input('Hext (kN)', value = 500)   # External Horizontal load (kN)
                comment(onComments, 'Hext', 'External Horizontal load')
                θ = st.number_input('θ (deg)', value = 0)           # angle between Hext and long axis (deg)
                comment(onComments, 'θ', 'angle between Hext and long axis')
            with col_l3:
                Mext_B = st.number_input('Mext_B (kNm)', value = 0) # Moment in B direction (kNm)
                comment(onComments, 'Mext_B', 'Moment in B direction')
                Mext_L = st.number_input('Mext_L (kNm)', value = 0) # Moment in L direction (kNm)
                comment(onComments, 'Mext_B', 'Moment in L direction')

            ## Soil
            st.subheader('Soil')
            col_s1,col_s2,col_s3 = st.columns(3)
            with col_s1:
                Su0 = st.number_input('Su0 (kPa)', value = 10)        # Shear strength at mudline (kPa)
                comment(onComments, 'Su0', 'Shear strength at mudline')
                k = st.number_input('k (kPa/m)', value = 1)           # rate of increasment with depth (kPa/m)
                comment(onComments, 'k', 'rate of increasment with depth')
            with col_s2:
                SUW = st.number_input('SUW (kN/m3)', value = 4)         # Average submerged unit weight (kN/m3)
                comment(onComments, 'SUW', 'Average submerged unit weight')
                UWw = st.number_input('UWw (kN/m3)', value = 10)        # Water unit weight (kN/m3)
                comment(onComments, 'UWw', 'Water unit weight')
                phi = st.number_input('phi (deg)', value = 0)         # Triaxial drained friction angle (deg)
                comment(onComments, 'phi', 'Triaxial drained friction angle')
                flagGap = st.number_input('Gap in soil?' , value = 0)     
                st.write('1 = yes, 0 = no')
            with col_s3:
                α1 = st.number_input('α1 (-) ', value = 0.1)        # Horizontal friction factor along skirt (-)
                comment(onComments, 'α1', 'Horizontal friction factor along skirt')
                Kru = st.number_input('Kru (-) ', value = 1)         # Earth pressure coefficient (no gap) (-)
                comment(onComments, 'Kru', 'Earth pressure coefficient (no gap)')
                Kru_gap = st.number_input('Kru_gap (-) ', value = 2)     # Earth pressure coefficient (with gap) (-)
                comment(onComments, 'Kru_gap', 'Earth pressure coefficient (with gap)')
                flagRough = st.number_input('Rough surface?', value = 1)   # Is footing rough? 1 for yes, 0 for no
                st.write('1 = yes, 0 = no')

            ## Factors
            st.subheader('Factors')
            col_f1,col_f2,col_f3 = st.columns(3)
            with col_f1:
                FSbear_API = st.number_input('FSbear_API', value = 2)
                FSslid_API = st.number_input('FSslid_API', value = 1.5)
            with col_f2:
                γ_load_LRFD = st.number_input('γ_load_LRFD', value = 1.35)
                γ_bear_LRFD = st.number_input('γ_bear_LRFD', value = 0.67)
                γ_slid_LRFD = st.number_input('γ_slid_LRFD', value = 0.8)
            with col_f3:
                γ_loadV_ISO = st.number_input('γ_loadV_ISO', value = 1.35)
                γ_loadH_ISO = st.number_input('γ_loadH_ISO', value = 1.35)
                γ_ISO_mat = st.number_input('γ_ISO_mat', value = 1.25)

        with tab2:
            st.header(':green[Deduced Values]')   

            # ============================================================================
            # Calculation

            ## Effective area
            eB = Mext_B/(Vext+SW)   # Ecentricity in B (m)
            eL = Mext_L/(Vext+SW)   # Ecentricity in L (m)
            Beff = B-2*eB           # Effective width (m)
            Leff = L-2*eL           # Effective length (m)
            Aeff = Beff*Leff        # Effective area (m2)

            ## Vertical load transfer
            Wplug = SUW*D*Aeff                  # Weight of soil plug (kN)
            Vext_base = round(SW+Vext+Wplug)    # Vertical load at base (kN)

            ## Horizontal load transfer
            Su1 = Su0+(k*D)/2       # average Su over skirt (kPa)
            Hf = α1*Su1*2*B*D       # soil friction on skirt (kN)
            Hep = Kru*Su1*L*D       # Act and Pass earth pressure (kN)
            if flagGap == 1:
                Wwedge = SUW*L*D**2/(2*np.tan((np.pi/180)*(45-phi/2)))  # Weight of passive wedge (kN)
                Hep_c = min(Kru_gap*Su1*L*D + Wwedge,Hep)
                Hep_tot = Hep_c
            else:
                Hep_tot = Hep
            H_B_base = max(round(Hext-((Hf+Hep_tot)/FSslid_API)),0.00001)
            # Note: transfered H load at the base cannot be negative value. 
            # When H_B_base become zero, then next equations will be in error.
            # Thus, I put very small number 0.00001 to prevent this error.


            # ----------------------------------------------------------------------------
            ## API 2A 21st
            Cu0 = Su0 + k*D             # Su at base
            Su_bear = Su0+k*(D+B/4)     # Su at failure depth
            Nc = 5.14
            Nq = 1
            Sc = 1+(Beff/Leff)*(Nq/Nc)  # Note: p243 (C6.13.1-7)
            mL = (2+Leff/Beff)/(1+Leff/Beff)
            mB = (2+Beff/Leff)/(1+Beff/Leff)
            m = mL*(np.cos(θ*np.pi/180))**2 + mB*(np.sin(θ*np.pi/180))**2 

            ## Ultimate
            Qv_APIult = Aeff*(Su_bear*Nc*Sc+(SUW+UWw)*D)
            Qh_APIult = Cu0*Aeff

            ## Envelope
            ns = 201 # Number of samples to descretize H
            def make_envelope_conatant(X):
                last_value = X[-1]
                dummy = np.linspace(last_value,last_value,ns)
                Y = np.concatenate((X,dummy), axis=0)
                return Y

            def make_envelope_decrease(X):
                last_value = X[-1]
                dummy = np.linspace(last_value,0,ns)
                Y = np.concatenate((X,dummy), axis=0)
                return Y

            api_H = np.linspace(0,Qh_APIult,ns)
            api_ic = 1-m*api_H/(Beff*Leff*Su_bear*Nc)   # Note: p243, (C6.13.1-6)
            api_Kc = api_ic*Sc                          # Note: p243 (C6.13.1-3)
            api_Qv = Aeff*(Su_bear*Nc*api_Kc+(SUW+UWw)*D)
            #
            API_Qh = make_envelope_conatant(api_H)
            API_Qv = make_envelope_decrease(api_Qv)

            ## API_WSD
            WSD_Hall = API_Qh.copy()
            ii = WSD_Hall > Qh_APIult/FSslid_API
            WSD_Hall[ii] = Qh_APIult/FSslid_API
            WSD_Vall = API_Qv/FSbear_API

            ## API_LRFD
            LRFD_Hall = API_Qh.copy()
            ii = WSD_Hall > Qh_APIult*γ_slid_LRFD/γ_load_LRFD
            LRFD_Hall[ii] = Qh_APIult*γ_slid_LRFD/γ_load_LRFD
            LRFD_Vall = API_Qv * γ_bear_LRFD/γ_load_LRFD


            # ----------------------------------------------------------------------------
            ## API 2GEO

            ## new parameters: F & Scv
            f = lambda a,b,c,d,x: a + b*x - ((c + b*x)**2 + d**2)**0.5 # Note: (A.17)
            #
            if flagRough == 1:
                a = 2.56; b = 0.457; c = 0.713; d = 1.38
            else:
                a = 1.372; b = 0.07; c = -0.128; d = 0.342
            #
            x = k*Beff/Su0
            F = f(a,b,c,d,x)
            #
            lilst_kBeff_over_Su0 = [0,2,4,6,8,10]
            list_Scv =[0.18, 0.00, -0.05, -0.07, -0.09, -0.10]
            Scv = np.interp(x,lilst_kBeff_over_Su0,list_Scv)    # Note: p78, Table A.2

            ## Correction factors
            # Ic_geo = 0.5 - 0.5[1 - H′/(Α′suo)]0.5         (A.21)
            # Sc_geo = Scv*Beff/L scv (1−2ic) (Β′/L′)       (A.18)
            # Dc_geo = 0.3 (su ave / su2) arctan(D/B′)      (A.20)
            # su2 = F(Nc suo+ κΒ′/4) / Nc.
            # Kc_iso = 1 + sc + dc − ic− bc− gc             (A.16)
            Su2 = F*(Nc*Cu0 + k*Beff/4)/Nc

            ## Ultimate
            Qh_ISOult = Cu0*Aeff
            # Note: Qc_ISOult will be calculated in df_GEO

            ## Ultimate
            geo_H = np.linspace(0,Qh_ISOult,ns)
            geo_ic = 0.5 - 0.5*(1 - geo_H/(Aeff*Su0))**0.5  # Note: 2GEO uses unfactored H
            geo_sc = Scv*(1-2*geo_ic)*(Beff/Leff)           # Note: 2GEO uses Leff
            geo_dc = 0.3*(Su1/Su2)*np.arctan(D/Beff)        # Note: 2GEO uses Su1/Su2
            geo_Kc = 1 + geo_sc + geo_dc - geo_ic
            geo_Qv = Aeff*(SUW*D + F*(Nc*Cu0 + k*Beff/4)*geo_Kc)
            #
            GEO_Qh = make_envelope_conatant(geo_H)
            GEO_Qv = make_envelope_decrease(geo_Qv)
            #
            geo_Hall = geo_H/FSslid_API
            geo_Vall = geo_Qv/FSbear_API
            #
            GEO_Hall = make_envelope_conatant(geo_Hall)
            GEO_Vall = make_envelope_decrease(geo_Vall)


            # ----------------------------------------------------------------------------
            ## ISO 19901-4
            iso_H = geo_H.copy()
            ii = iso_H > Qh_ISOult/(γ_loadH_ISO*γ_ISO_mat)
            iso_H[ii] = Qh_ISOult/(γ_loadH_ISO*γ_ISO_mat)

            ## Correction factors
            # Ic_iso = 0,5 − 0,5 1−[Hb /(Α′cu /γ m)]        (A.17) 
            # Sc_iso = 0,2(1− 2ic )(Β′ / L)                 (A.15)
            # Dc_iso = 0,3 arctan(Db / Β′)                  (A.16)
            # Kc = 1 + sc + dc − ic                         (A.14)

            iso_Hb = iso_H*γ_loadH_ISO                        # Note: ISO uses factored H
            iso_ic = 0.5 - 0.5*(1 - iso_Hb/(Aeff*Su0/γ_ISO_mat))**0.5 
            iso_sc = 0.2*(1-2*iso_ic)*(Beff/L)              # Note: ISO uses L
            iso_dc = 0.3*np.arctan(D/Beff)
            iso_Kc = 1 + iso_sc + iso_dc - iso_ic
            iso_Qv = (1/γ_loadV_ISO)*Aeff*(SUW*D + F*(Nc*Cu0 + k*Beff/4)*iso_Kc/γ_ISO_mat)
            #
            ISO_Qh = make_envelope_conatant(iso_H)
            ISO_Qv = make_envelope_decrease(iso_Qv)
            ISO_Qv[-1] = 0 # Note: Because the last value has N/A, replace it to zero.

        
        with tab3:
            st.header(':red[Output Results]')        

            # ============================================================================
            # Output
    
            ## API
            df_API = pd.DataFrame()
            df_API['API_Hult'] = API_Qh
            df_API['API_Vult'] = API_Qv
            df_API['WSD_Hall'] = WSD_Hall
            df_API['WSD_Vall'] = WSD_Vall
            df_API['LRFD_Hall'] = LRFD_Hall
            df_API['LRFD_Vall'] = LRFD_Vall

            ## GEO
            df_GEO = pd.DataFrame()
            df_GEO['GEO_Hult'] = GEO_Qh
            df_GEO['GEO_Vult'] = GEO_Qv
            df_GEO['GEO_Vult'].fillna(0, inplace=True)
            df_GEO['GEO_Hall'] = GEO_Hall
            df_GEO['GEO_Vall'] = GEO_Vall
            df_GEO['GEO_Vall'].fillna(0, inplace=True)
            df_GEO['GEO_Hult*slope'] = GEO_Qh*Vext_base/H_B_base
            df_GEO['GEO_Hult*slope-GEO_Vult'] = df_GEO['GEO_Hult*slope'] - df_GEO['GEO_Vult']
            idx_min_geo_ult_direction = df_GEO['GEO_Hult*slope-GEO_Vult'].abs().idxmin(0)
            max_Qh_geo_ult = round(df_GEO.loc[idx_min_geo_ult_direction,'GEO_Hult'])
            max_Qv_geo_ult = round(df_GEO.loc[idx_min_geo_ult_direction,'GEO_Hult*slope'])
            max_Qd_geo_ult = round(np.sqrt(max_Qh_geo_ult**2 + max_Qv_geo_ult**2))

            ## ISO
            df_ISO = pd.DataFrame()
            df_ISO['ISO_Hall'] = ISO_Qh
            df_ISO['ISO_Vall'] = ISO_Qv
            df_ISO['ISO_Vall'].fillna(0, inplace=True)
            #
            interp_H = np.interp(iso_H,geo_Hall,geo_Vall)
            INTERP_H = make_envelope_conatant(interp_H)
            df_ISO['GEO_Vall'] = INTERP_H
            df_ISO['min_Vall'] = df_ISO[['GEO_Vall','ISO_Vall']].min(axis=1)
            #
            max_Qv_api = round(np.interp(H_B_base,api_H,api_Qv))
            max_Qv_geo = round(np.interp(H_B_base,geo_H,geo_Qv))
            max_Qh_api = round(np.interp(Vext_base,API_Qv,API_Qh))
            max_Qd_api = round(max_Qh_api*Vext_base/H_B_base)
            resultant_QhQv = round(np.sqrt(H_B_base**2 + Vext_base**2))
            #
            FS_bear_2A_ult = round(max_Qv_api/Vext_base,2)
            FS_bear_2GEO_ult = round(max_Qv_geo/Vext_base,2)
            FS_slid_2GEO_ult = round(max_Qh_api/H_B_base,2)
            FS_api_ult = round(max_Qd_geo_ult/resultant_QhQv,2)

    
    
    # --------------------------------------------------------------------
    with col2:

        ## Plot
        fig,ax = plt.subplots(2,1, figsize=(6,7), dpi=200, height_ratios=[3,1])
        #
        ax[0].plot(H_B_base,Vext_base, 'ro', label='Load at the base')
        ax[0].text(H_B_base*0.7,Vext_base-500, '('+str(H_B_base)+','+str(Vext_base)+')')
        if D == 0:
            pass
        else:
            ax[0].plot(Hext,Vext, 'bx', label='Load at the seafloor')
            ax[0].text(Hext*0.7,Vext-500, '('+str(Hext)+','+str(Vext)+')',color='b')
        #
        ax[0].plot(df_API['API_Hult'],df_API['API_Vult'],'-',c='C0', label='API 2A ultimate')
        ax[0].plot(df_API['WSD_Hall'],df_API['WSD_Vall'],'--',c='C1', label='API WSD allowable')
        ax[0].plot(df_API['LRFD_Hall'],df_API['LRFD_Vall'],'-.',c='purple', label='API LRFD allowable')
        #
        ax[0].plot(df_GEO['GEO_Hult'],df_GEO['GEO_Vult'],'g-', label='API 2GEO ultimate')
        ax[0].plot(df_GEO['GEO_Hall'],df_GEO['GEO_Vall'],'g--', label='API 2GEO allowable')
        ax[0].plot(df_ISO['ISO_Hall'],df_ISO['ISO_Vall'],'k--', label='ISO 19901-4 allowable')
        #
        ax[0].fill_between(df_ISO['ISO_Hall'],df_ISO['min_Vall'],y2=0, color='C0', alpha=0.3)
        ax[0].plot([H_B_base,H_B_base],[Vext_base,max_Qv_api],'k--',linewidth=0.5)
        ax[0].text(H_B_base,max_Qv_geo+100, 'Bearing \n(2A: FS='+str(FS_bear_2A_ult)+')\n(2GEO: FS='+str(FS_bear_2GEO_ult)+')')
        ax[0].plot([H_B_base,max_Qh_api],[Vext_base,Vext_base],'k--',linewidth=0.5)
        ax[0].text(max_Qh_api*0.85,Vext_base*1.0, 'Sliding \n(FS='+str(FS_slid_2GEO_ult)+')')
        ax[0].plot([0,max_Qh_geo_ult],[0,max_Qv_geo_ult],'r--',linewidth=0.5)
        ax[0].text(max_Qh_geo_ult*0.85,max_Qv_geo_ult*0.85,'(FS='+str(FS_api_ult)+')', color='r',bbox=dict(edgecolor='None',facecolor='yellow', alpha=0.5))
        #
        ax[1].plot(0,0,'ro', label='Load at the base')
        ax[1].plot(0,0,'-',c='C0', label='API 2A ultimate')
        ax[1].plot(0,0,'--',c='C1', label='API WSD allowable')
        ax[1].plot(0,0,'-.',c='purple', label='API LRFD allowable')
        if D == 0:
            pass
        else:
            ax[1].plot(0,0,'bx', label='Load at the mudline')
        ax[1].plot(0,0,'g-', label='API 2GEO ultimate')
        ax[1].plot(0,0,'g--', label='API 2GEO allowable')
        ax[1].plot(0,0,'k--', label='ISO 19901-4 allowable')
        ax[1].axis('off')
        #
        ax[0].set_xlabel('Unfactored H (kN)')
        ax[0].set_ylabel('Unfactored V (kN)')
        ax[0].set_xlim([0,Qh_APIult*1.1])
        ax[0].set_ylim([0,Qv_APIult*1.1])
        ax[0].grid(linestyle='dotted')
        ax[0].minorticks_on()
        ax[1].legend(loc='upper center', fancybox=True, shadow=True, fontsize=10, ncol=2)
        ax[0].set_title('$B$='+str(B)+'(m), $L$='+str(L)+'(m), $D$='+str(D)+'(m), $s_u$='+str(Su0)+'(kPa), κ='+str(k)+'(kPa/m)', fontsize=10)
        #ax.axis('equal')
        fig.suptitle('Undrained Load Interaction Envelopes', y=0.95)

        st.pyplot(fig)
