# Track Order Page

import streamlit as st
import utils

st.title("Track Your Orders")
st.markdown("---")

if 'track_order_id' not in st.session_state:
    st.session_state.track_order_id = None

tab1, tab2 = st.tabs(["Track by Order ID", "My Orders"])

# Tab 1: Track by Order ID
with tab1:
    st.subheader("Track Order by ID")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        order_id_input = st.number_input(
            "Enter Order ID",
            min_value=1,
            step=1,
            value=st.session_state.track_order_id if st.session_state.track_order_id else 1
        )
    
    with col2:
        st.write("")
        track_button = st.button("Get Order", use_container_width=True, type="primary")
    
    if track_button:
        try:
            with st.spinner(f"Loading order #{order_id_input}..."):
                order = utils.api_get(f"/orders/{order_id_input}")
            
            st.success(f"Order #{order['id']} Found")
            
            status = order['status']
            if status == "CONFIRMED":
                st.success(f"Status: {status}")
            elif status == "PENDING":
                st.warning(f"Status: {status}")
            elif status == "REJECTED":
                st.error(f"Status: {status}")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Order ID", order['id'])
            with col2:
                st.metric("User ID", order['user_id'])
            with col3:
                st.metric("Country ID", order['country_id'])
            with col4:
                st.metric("Status", order['status'])
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"Weight: {order['weight_kg']} kg")
                st.info(f"Size: {order['size_cm']} cm")
            with col2:
                if order['shipping_charge']:
                    st.info(f"Shipping Charge: ${order['shipping_charge']:.2f}")
                else:
                    st.warning("Shipping Charge: Not calculated")
                st.info(f"Created: {order['created_at']}")
            
            st.text_area("Item Description", value=order['item_description'], height=100, disabled=True)
            
            if order['rejection_reason']:
                st.error(f"Rejection Reason: {order['rejection_reason']}")
            
            with st.expander("View Full Order JSON"):
                st.json(order)
            
            st.session_state.track_order_id = None
            
        except Exception as e:
            st.error(str(e))

# Tab 2: My Orders
with tab2:
    st.subheader("Your Order History")
    
    if st.button("Refresh Orders"):
        st.rerun()
    
    try:
        with st.spinner("Loading your orders..."):
            orders = utils.api_get(f"/orders/user/{st.session_state.user_id}")
        
        if orders:
            st.success(f"Found {len(orders)} orders")
            
            for order in orders:
                with st.container():
                    col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 1])
                    
                    with col1:
                        st.write(f"**#{order['id']}**")
                    
                    with col2:
                        if order['status'] == "CONFIRMED":
                            st.success(order['status'])
                        elif order['status'] == "PENDING":
                            st.warning(order['status'])
                        else:
                            st.error(order['status'])
                    
                    with col3:
                        st.write(f"{order['weight_kg']} kg, {order['size_cm']} cm")
                    
                    with col4:
                        if order['shipping_charge']:
                            st.write(f"${order['shipping_charge']:.2f}")
                        else:
                            st.write("N/A")
                    
                    with col5:
                        if st.button("View", key=f"view_{order['id']}"):
                            st.session_state.track_order_id = order['id']
                            st.rerun()
                    
                    st.caption(f"{order['item_description'][:60]}..." if len(order['item_description']) > 60 else order['item_description'])
                    st.caption(f"{order['created_at']}")
                    st.divider()
        else:
            st.info("No orders found. Create your first order!")
            
    except Exception as e:
        st.error(f"Failed to load orders: {str(e)}")
