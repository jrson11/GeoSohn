import streamlit as st

def main():

    # Sidebar
    password = st.sidebar.text_input('Password?', '******')
    
    # Main Page
    st.title("Main Page")
    st.markdown("## Welcome to the Main Page")



if __name__ == "__main__":
    main()
