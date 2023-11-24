import streamlit as st

def main():

    # Sidebar
    password = st.sidebar.text_input('Password?', '******')
    
    # Main Page
    st.title("Main Page")
    st.markdown("## Welcome to the Main Page")

    # Link to App 1
    if st.button("Go to App 1"):
        st.markdown("[Click here](http://localhost:8501/app1) to go to App 1")

    # Link to App 2
    if st.button("Go to App 2"):
        st.markdown("[Click here](http://localhost:8501/app2) to go to App 2")

if __name__ == "__main__":
    main()
