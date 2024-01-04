import pandas as pd

Soil_HUB = {'Depth_Top_m':[0.0, 2.0, 7.9],
            'SUW_LE_kNm3':[3.7, 3.9, 4.2],
            'SUW_BE_kNm3':[4.3, 4.7, 6.0],
            'SUW_HE_kNm3':[6.3, 6.8, 8.3],
            'Su_LE_kPa':[0.3, 3.7, 13.7],
            'Su_BE_kPa':[3.1, 6.5, 16.5],
            'Su_HE_kPa':[5.8, 9.2, 19.2],
            }

df_Soil_HUB = pd.DataFrame(Soil_Hub)
