# Admin Rules Page

import streamlit as st
import utils

st.title("Admin: Manage Shipping Rules")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["Add Country", "Add Shipping Rules", "Add Banned Item", "View All"])

# Tab 1: Create Country
with tab1:
    st.subheader("Create New Country")
    
    with st.form("create_country_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            country_name = st.text_input("Country Name", placeholder="e.g., United States")
        with col2:
            iso_code = st.text_input("ISO Code", placeholder="e.g., US", max_chars=10)
        
        create_country_btn = st.form_submit_button("Add Country", use_container_width=True, type="primary")
        
        if create_country_btn:
            if not country_name or not iso_code:
                st.error("Both fields are required")
            else:
                try:
                    with st.spinner("Creating country..."):
                        result = utils.api_post("/countries/", json_data={
                            "name": country_name,
                            "iso_code": iso_code
                        })
                    
                    st.success(f"Country created: {result['name']} (ID: {result['id']})")
                    
                except Exception as e:
                    st.error(str(e))

# Tab 2: Create Shipping Rules
with tab2:
    st.subheader("Add Shipping Rules for Country")
    
    try:
        countries = utils.api_get("/countries/")
        
        if countries:
            with st.form("create_rule_form"):
                country_options = {f"{c['name']} ({c['iso_code']})": c['id'] for c in countries}
                
                selected_country = st.selectbox("Select Country", options=list(country_options.keys()))
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    max_weight = st.number_input("Max Weight (kg)", min_value=0.1, value=50.0, step=0.1)
                with col2:
                    max_size = st.number_input("Max Size (cm)", min_value=1.0, value=200.0, step=1.0)
                with col3:
                    custom_duty = st.number_input("Custom Duty (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.1)
                
                create_rule_btn = st.form_submit_button("Add Rule", use_container_width=True, type="primary")
                
                if create_rule_btn:
                    try:
                        with st.spinner("Creating rule..."):
                            result = utils.api_post("/countries/rules", json_data={
                                "country_id": country_options[selected_country],
                                "max_weight_kg": max_weight,
                                "max_size_cm": max_size,
                                "custom_duty_percent": custom_duty
                            })
                        
                        st.success(f"Shipping rule created for {selected_country}")
                        with st.expander("View Rule Details"):
                            st.json(result)
                        
                    except Exception as e:
                        st.error(str(e))
        else:
            st.warning("No countries available. Create a country first.")
            
    except Exception as e:
        st.error(f"Failed to load countries: {str(e)}")

# Tab 3: Add Banned Items
with tab3:
    st.subheader("Add Banned Item")
    
    try:
        countries = utils.api_get("/countries/")
        
        if countries:
            with st.form("add_banned_item_form"):
                country_options = {f"{c['name']} ({c['iso_code']})": c['id'] for c in countries}
                
                selected_country = st.selectbox("Select Country", options=list(country_options.keys()))
                
                item_name = st.text_input(
                    "Banned Item Name",
                    placeholder="e.g., weapons, drugs, alcohol",
                    help="This will be matched against item descriptions (case-insensitive)"
                )
                
                add_banned_btn = st.form_submit_button("Ban Item", use_container_width=True, type="primary")
                
                if add_banned_btn:
                    if not item_name:
                        st.error("Item name is required")
                    else:
                        try:
                            with st.spinner("Adding banned item..."):
                                result = utils.api_post("/countries/banned", json_data={
                                    "country_id": country_options[selected_country],
                                    "item_name": item_name
                                })
                            
                            st.success(f"Banned item added: '{result['item_name']}' for {selected_country}")
                            
                        except Exception as e:
                            st.error(str(e))
        else:
            st.warning("No countries available. Create a country first.")
            
    except Exception as e:
        st.error(f"Failed to load countries: {str(e)}")

# Tab 4: View All
with tab4:
    st.subheader("View All Countries and Rules")
    
    if st.button("Refresh Data"):
        st.rerun()
    
    try:
        countries = utils.api_get("/countries/")
        
        if countries:
            st.success(f"Total Countries: {len(countries)}")
            
            for country in countries:
                with st.expander(f"{country['name']} ({country['iso_code']}) - ID: {country['id']}"):
                    try:
                        rule = utils.api_get(f"/countries/{country['id']}/rules")
                        
                        st.markdown("### Shipping Rules")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Max Weight", f"{rule['max_weight_kg']} kg")
                        with col2:
                            st.metric("Max Size", f"{rule['max_size_cm']} cm")
                        with col3:
                            st.metric("Custom Duty", f"{rule['custom_duty_percent']}%")
                        
                    except:
                        st.warning("No shipping rules configured yet")
        else:
            st.info("No countries found. Create your first country!")
            
    except Exception as e:
        st.error(f"Failed to load data: {str(e)}")
