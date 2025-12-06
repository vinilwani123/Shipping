# User Profile Page

import streamlit as st

st.title("User Profile")
st.markdown("---")

# Profile Information
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("""
        <div style='padding: 2rem; background-color: #f8f9fa; border-radius: 10px; text-align: center;'>
            <div style='width: 100px; height: 100px; background-color: #3498db; border-radius: 50%; margin: 0 auto 1rem; display: flex; align-items: center; justify-content: center; color: white; font-size: 3rem;'>
                {initial}
            </div>
            <h3>{name}</h3>
        </div>
    """.format(
        initial=st.session_state.name[0].upper() if st.session_state.name else "U",
        name=st.session_state.name
    ), unsafe_allow_html=True)

with col2:
    st.subheader("Account Details")
    
    st.text_input("Full Name", value=st.session_state.name, disabled=True)
    st.text_input("Email Address", value=st.session_state.email, disabled=True)
    st.text_input("User ID", value=str(st.session_state.user_id), disabled=True)

st.markdown("---")

# Order History
st.subheader("Order Statistics")

try:
    import utils
    
    orders = utils.api_get(f"/orders/user/{st.session_state.user_id}")
    
    if orders:
        col1, col2, col3, col4 = st.columns(4)
        
        total_orders = len(orders)
        confirmed_orders = len([o for o in orders if o['status'] == 'CONFIRMED'])
        pending_orders = len([o for o in orders if o['status'] == 'PENDING'])
        rejected_orders = len([o for o in orders if o['status'] == 'REJECTED'])
        
        with col1:
            st.metric("Total Orders", total_orders)
        with col2:
            st.metric("Confirmed", confirmed_orders)
        with col3:
            st.metric("Pending", pending_orders)
        with col4:
            st.metric("Rejected", rejected_orders)
    else:
        st.info("No orders found")
        
except Exception as e:
    st.error(f"Failed to load order statistics: {str(e)}")

st.markdown("---")

# Change Password Section
st.subheader("Security")

with st.form("change_password_form"):
    st.info("Password change functionality will be available in the next update")
    current_password = st.text_input("Current Password", type="password", disabled=True)
    new_password = st.text_input("New Password", type="password", disabled=True)
    confirm_password = st.text_input("Confirm New Password", type="password", disabled=True)
    
    change_button = st.form_submit_button("Change Password", disabled=True)
