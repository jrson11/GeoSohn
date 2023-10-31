import numpy as np
import pandas as pd

def mudmat_disp():
  
  # Display two columns
  col1, col2 = st.columns(2)

  with col1:
    st.text('Plots')
    #plot_topview()
    #plot_fontview()
  
  with col2:
    st.text('Data')
    #tab0,tab1,tab2,tab3,tab4 = st.tabs(['1-Structural_Coordinates','2-Structural_Loads','3-','4-','5-'])

