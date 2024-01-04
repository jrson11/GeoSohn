import pandas as pd

Soil_Su = {'Depth_Top_ft':[0.0, 1.6, 4.9, 9.8, 16.4, 32.8, 49.2, 114.8],
           'SuDSS_LE_psf':[4.2, 52.2, 35.5, 44.4, 79.9, 159.7, 230.7, 656.7],
           'SuDSS_BE_psf':[4.2, 87.7, 41.8, 52.2, 94.0, 187.9, 271.4, 772.6],
           'SuDSS_HE_psf':[4.2, 125.3, 48.0, 60.0, 108.1, 216.1, 312.2, 888.4],
           'Depth_Top_m':[0.0, 0.5, 1.5, 3.0, 5.0, 10.0, 15.0, 35.0],
           'SuDSS_LE_kPa':[0.2, 2.5, 1.7, 2.1, 3.8, 7.7, 11.1, 31.5],
           'SuDSS_BE_kPa':[0.2, 4.2, 2.0, 2.5, 4.5, 9.0, 13.0, 37.0],
           'SuDSS_HE_kPa':[0.2, 6.0, 2.3, 2.9, 5.2, 10.4, 15.0, 42.6],
          }
df_Soil_Su = pd.DataFrame(Soil_Su)

Soil_SUW = {'Depth_Top_ft':[0.0, 1.5, 6.0, 19.0, 19.0, 60.0],
            'SUW_LE_pcf':[],
            'SUW_BE_pcf':[],
            'SUW_HE_pcf':[],
            'Depth_Top_m':[],
            'SUW_LE_kN/m3':[],
            'SUW_BE_kN/m3':[],
            'SUW_HE_kN/m3':[],
          }
df_Soil_Su = pd.DataFrame(Soil_Su)
