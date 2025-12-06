import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import utils

st.set_page_config(
    page_title="Big Bag Shipping",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide sidebar and link icons
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        [data-testid="collapsedControl"] {
            display: none;
        }
        .stDeployButton {
            display: none;
        }
        #MainMenu {
            visibility: hidden;
        }
        footer {
            visibility: hidden;
        }
        header {
            visibility: hidden;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'email' not in st.session_state:
    st.session_state.email = None
if 'name' not in st.session_state:
    st.session_state.name = None
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def render_navbar():
    """Render top navigation bar"""
    st.markdown("""
        <style>
        .navbar {
            background-color: #2c3e50;
            padding: 1rem 2rem;
            margin: -1rem -1rem 2rem -1rem;
        }
        .navbar-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .navbar-brand {
            color: white;
            font-size: 1.5rem;
            font-weight: bold;
        }
        .navbar-user {
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 1, 1, 1, 1, 1, 1])
    
    with col1:
        st.markdown("### Big Bag Shipping")
    
    with col2:
        if st.button("Home", use_container_width=True, type="primary" if st.session_state.page == 'home' else "secondary"):
            st.session_state.page = 'home'
            st.rerun()
    
    with col3:
        if st.button("Create Order", use_container_width=True, type="primary" if st.session_state.page == 'create_order' else "secondary"):
            st.session_state.page = 'create_order'
            st.rerun()
    
    with col4:
        if st.button("Track Order", use_container_width=True, type="primary" if st.session_state.page == 'track_order' else "secondary"):
            st.session_state.page = 'track_order'
            st.rerun()
    
    with col5:
        if st.button("Admin Rules", use_container_width=True, type="primary" if st.session_state.page == 'admin_rules' else "secondary"):
            st.session_state.page = 'admin_rules'
            st.rerun()
    
    with col6:
        if st.button("Profile", use_container_width=True, type="primary" if st.session_state.page == 'profile' else "secondary"):
            st.session_state.page = 'profile'
            st.rerun()
    
    with col7:
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.email = None
            st.session_state.name = None
            st.session_state.page = 'home'
            st.rerun()
    
    st.markdown(f"<p style='text-align: right; color: #7f8c8d;'>Logged in as: {st.session_state.email}</p>", unsafe_allow_html=True)
    st.markdown("---")

# Check authentication
if not st.session_state.logged_in:
    # LOGIN PAGE
    st.markdown("<h1 style='text-align: center;'>Big Bag Shipping Management</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #7f8c8d;'>Login to your account</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            with st.form("login_form"):
                email = st.text_input("Email Address")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login", use_container_width=True, type="primary")
                
                if submit:
                    if not email or not password:
                        st.error("Please enter both email and password")
                    else:
                        try:
                            with st.spinner("Logging in..."):
                                response = utils.api_post("/users/login", params={
                                    "email": email,
                                    "password": password
                                })
                            
                            st.session_state.logged_in = True
                            st.session_state.user_id = response['id']
                            st.session_state.email = response['email']
                            st.session_state.name = response.get('name', email)
                            st.session_state.page = 'home'
                            
                            st.success("Login successful!")
                            st.rerun()
                            
                        except Exception as e:
                            error_msg = str(e)
                            if "401" in error_msg or "Invalid" in error_msg:
                                st.error("Invalid email or password")
                            else:
                                st.error(f"Login failed: {error_msg}")
        
        with tab2:
            with st.form("register_form"):
                reg_name = st.text_input("Full Name")
                reg_email = st.text_input("Email Address")
                reg_password = st.text_input("Password", type="password")
                reg_submit = st.form_submit_button("Register", use_container_width=True, type="primary")
                
                if reg_submit:
                    if not reg_name or not reg_email or not reg_password:
                        st.error("All fields are required")
                    elif len(reg_password) < 6:
                        st.error("Password must be at least 6 characters")
                    else:
                        try:
                            with st.spinner("Creating account..."):
                                response = utils.api_post("/users/", json_data={
                                    "name": reg_name,
                                    "email": reg_email,
                                    "password": reg_password
                                })
                            
                            st.success("Account created successfully! Please login.")
                            
                        except Exception as e:
                            st.error(f"Registration failed: {str(e)}")

else:
    # LOGGED IN - Show navbar and pages
    render_navbar()
    
    # Load appropriate page
    if st.session_state.page == 'home':
        exec(open('pages/home_page.py').read())
    elif st.session_state.page == 'create_order':
        exec(open('pages/2_Create_Order.py').read())
    elif st.session_state.page == 'track_order':
        exec(open('pages/3_Track_Order.py').read())
    elif st.session_state.page == 'admin_rules':
        exec(open('pages/4_Admin_Rules.py').read())
    elif st.session_state.page == 'profile':
        exec(open('pages/profile.py').read())
