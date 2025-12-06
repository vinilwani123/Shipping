# Homepage - Landing page after login

import streamlit as st

# Hero Section
st.markdown("""
    <div style='text-align: center; padding: 3rem 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin-bottom: 2rem;'>
        <h1 style='font-size: 3rem; margin-bottom: 1rem;'>Shipping Management System</h1>
        <p style='font-size: 1.2rem;'>Efficient and reliable shipping solutions worldwide</p>
    </div>
""", unsafe_allow_html=True)

# Welcome message
st.markdown(f"## Welcome, {st.session_state.name}!")
st.markdown("---")

# Info Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div style='padding: 2rem; background-color: #f8f9fa; border-radius: 10px; border-left: 4px solid #3498db;'>
            <h3>Create New Order</h3>
            <p>Start shipping your items to any destination worldwide</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Create Order", key="home_create", use_container_width=True, type="primary"):
        st.session_state.page = 'create_order'
        st.rerun()

with col2:
    st.markdown("""
        <div style='padding: 2rem; background-color: #f8f9fa; border-radius: 10px; border-left: 4px solid #2ecc71;'>
            <h3>Track Your Orders</h3>
            <p>Monitor the status of your shipments in real-time</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Track Orders", key="home_track", use_container_width=True, type="primary"):
        st.session_state.page = 'track_order'
        st.rerun()

with col3:
    st.markdown("""
        <div style='padding: 2rem; background-color: #f8f9fa; border-radius: 10px; border-left: 4px solid #e74c3c;'>
            <h3>Admin Dashboard</h3>
            <p>Manage countries, rules, and banned items</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Admin Panel", key="home_admin", use_container_width=True, type="primary"):
        st.session_state.page = 'admin_rules'
        st.rerun()

st.markdown("---")

# Quick Stats
st.markdown("### Quick Overview")

try:
    import utils
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        try:
            orders = utils.api_get(f"/orders/user/{st.session_state.user_id}")
            st.metric("Your Orders", len(orders) if orders else 0)
        except:
            st.metric("Your Orders", "N/A")
    
    with col2:
        try:
            countries = utils.api_get("/countries/")
            st.metric("Available Countries", len(countries) if countries else 0)
        except:
            st.metric("Available Countries", "N/A")
    
    with col3:
        st.metric("Account Status", "Active")
        
except:
    pass

st.markdown("---")

# About section
with st.expander("About Big Bag Shipping"):
    st.markdown("""
    **Big Bag** is a global shipping company that provides reliable and efficient shipping solutions.
    
    Our services include:
    - International shipping to multiple countries
    - Real-time order tracking
    - Automated cost calculation
    - Country-specific rules and regulations compliance
    - Banned items verification
    
    For support, please contact: support@bigbag.com
    """)
