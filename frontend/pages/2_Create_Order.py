# Create Order Page

import streamlit as st
import utils

st.title("Create Shipping Order")
st.markdown("---")

if 'estimate_result' not in st.session_state:
    st.session_state.estimate_result = None
if 'order_data' not in st.session_state:
    st.session_state.order_data = None

# Fetch countries
try:
    countries = utils.api_get("/countries/")
    
    if not countries:
        st.warning("No countries available. Please contact admin to add countries.")
        st.stop()
    
    st.subheader("Step 1: Enter Shipment Details")
    
    with st.form("order_form"):
        country_options = {f"{c['name']} ({c['iso_code']})": c['id'] for c in countries}
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_country = st.selectbox("Destination Country", options=list(country_options.keys()))
            weight_kg = st.number_input("Weight (kg)", min_value=0.1, max_value=1000.0, value=5.0, step=0.1)
        
        with col2:
            size_cm = st.number_input("Size (cm)", min_value=1.0, max_value=1000.0, value=50.0, step=1.0)
        
        item_description = st.text_area(
            "Item Description",
            placeholder="Describe the items you are shipping",
            help="This will be checked against banned items list"
        )
        
        estimate_button = st.form_submit_button("Estimate Shipping Cost", use_container_width=True, type="primary")
        
        if estimate_button:
            if not item_description:
                st.error("Item description is required")
            else:
                try:
                    with st.spinner("Calculating shipping cost..."):
                        estimate_data = {
                            "country_id": country_options[selected_country],
                            "weight_kg": weight_kg,
                            "size_cm": size_cm,
                            "item_description": item_description
                        }
                        
                        result = utils.api_post("/shipping/estimate", json_data=estimate_data)
                        
                        st.session_state.estimate_result = result
                        st.session_state.order_data = {
                            "country_id": country_options[selected_country],
                            "country_name": selected_country,
                            "weight_kg": weight_kg,
                            "size_cm": size_cm,
                            "item_description": item_description
                        }
                        st.rerun()
                        
                except Exception as e:
                    st.error(str(e))
    
    # Show estimate result
    if st.session_state.estimate_result:
        st.markdown("---")
        st.subheader("Step 2: Review and Confirm")
        
        result = st.session_state.estimate_result
        order_data = st.session_state.order_data
        
        if result['valid']:
            st.success("Shipment is valid and ready to process")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Destination", order_data['country_name'])
            with col2:
                st.metric("Weight", f"{order_data['weight_kg']} kg")
            with col3:
                st.metric("Size", f"{order_data['size_cm']} cm")
            
            st.info(f"Item: {order_data['item_description']}")
            
            st.markdown("### Total Shipping Cost")
            st.markdown(f"# ${result['shipping_charge']:.2f}")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.info("Click 'Confirm Order' to proceed with shipment")
            with col2:
                if st.button("Confirm Order", use_container_width=True, type="primary"):
                    try:
                        with st.spinner("Processing order..."):
                            confirm_data = {
                                "country_id": order_data["country_id"],
                                "weight_kg": order_data["weight_kg"],
                                "size_cm": order_data["size_cm"],
                                "item_description": order_data["item_description"],
                                "accept_charge": True
                            }
                            
                            confirmed_order = utils.api_post(
                                "/shipping/confirm",
                                json_data=confirm_data,
                                params={"user_id": st.session_state.user_id}
                            )
                        
                        st.success(f"Order #{confirmed_order['id']} confirmed successfully!")
                        
                        st.session_state.last_order_id = confirmed_order['id']
                        
                        with st.expander("View Order Details"):
                            st.json(confirmed_order)
                        
                        if st.button("View in Track Order"):
                            st.session_state.page = 'track_order'
                            st.session_state.track_order_id = confirmed_order['id']
                            st.rerun()
                        
                        st.session_state.estimate_result = None
                        st.session_state.order_data = None
                        
                    except Exception as e:
                        st.error(f"Failed to confirm order: {str(e)}")
            
            if st.button("Cancel and Start Over"):
                st.session_state.estimate_result = None
                st.session_state.order_data = None
                st.rerun()
        
        else:
            st.error("Shipment cannot be processed")
            st.warning(f"Reason: {result['rejection_reason']}")
            
            if st.button("Try Again"):
                st.session_state.estimate_result = None
                st.session_state.order_data = None
                st.rerun()

except Exception as e:
    st.error(f"Failed to load countries: {str(e)}")
