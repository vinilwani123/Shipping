"""
End-to-end flow simulation test
"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 70)
print("END-TO-END FLOW SIMULATION")
print("=" * 70)

# Step 1: Register/Login
print("\n1. USER REGISTRATION/LOGIN")
print("-" * 70)
try:
    # Try to register a new test user
    register_data = {
        "email": "flowtest@example.com",
        "password": "test123",
        "name": "Flow Test User"
    }
    
    response = requests.post(f"{BASE_URL}/users/", json=register_data)
    if response.status_code == 201:
        user_data = response.json()
        print(f"✅ User registered successfully")
    elif response.status_code == 400:
        # User exists, try to login
        login_response = requests.post(
            f"{BASE_URL}/users/login",
            params={"email": "flowtest@example.com", "password": "test123"}
        )
        user_data = login_response.json()
        print(f"✅ User logged in successfully")
    
    print(json.dumps(user_data, indent=2))
    user_id = user_data['id']
    
except Exception as e:
    print(f"❌ Registration/Login failed: {e}")
    exit(1)

# Step 2: Get countries
print("\n2. GET COUNTRIES")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/countries/")
    countries = response.json()
    print(f"✅ Retrieved {len(countries)} countries")
    print(json.dumps(countries, indent=2))
    
    if countries:
        country_id = countries[0]['id']
    else:
        print("⚠️ No countries available")
        exit(1)
        
except Exception as e:
    print(f"❌ Failed to get countries: {e}")
    exit(1)

# Step 3: Shipping Estimate
print("\n3. SHIPPING ESTIMATE")
print("-" * 70)
try:
    estimate_data = {
        "country_id": country_id,
        "weight_kg": 10.0,
        "size_cm": 50.0,
        "item_description": "Books and documents"
    }
    
    response = requests.post(f"{BASE_URL}/shipping/estimate", json=estimate_data)
    estimate_result = response.json()
    print(f"✅ Shipping estimate calculated")
    print(json.dumps(estimate_result, indent=2))
    
    if not estimate_result.get('valid'):
        print(f"⚠️ Estimate not valid: {estimate_result.get('rejection_reason')}")
        
except Exception as e:
    print(f"❌ Shipping estimate failed: {e}")
    exit(1)

# Step 4: Confirm Order
print("\n4. CONFIRM ORDER")
print("-" * 70)
try:
    confirm_data = {
        "country_id": country_id,
        "weight_kg": 10.0,
        "size_cm": 50.0,
        "item_description": "Books and documents",
        "accept_charge": True
    }
    
    response = requests.post(
        f"{BASE_URL}/shipping/confirm",
        json=confirm_data,
        params={"user_id": user_id}
    )
    order_result = response.json()
    print(f"✅ Order created successfully")
    print(json.dumps(order_result, indent=2))
    
    order_id = order_result['id']
    
except Exception as e:
    print(f"❌ Order confirmation failed: {e}")
    exit(1)

# Step 5: Track Order
print("\n5. TRACK ORDER")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/orders/{order_id}")
    order_details = response.json()
    print(f"✅ Order retrieved successfully")
    print(json.dumps(order_details, indent=2))
    
except Exception as e:
    print(f"❌ Order tracking failed: {e}")
    exit(1)

print("\n" + "=" * 70)
print("✅ END-TO-END FLOW COMPLETED SUCCESSFULLY!")
print("=" * 70)
