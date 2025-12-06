"""
Test user registration endpoint directly
"""
import requests
import json

url = "http://localhost:8000/users/"
data = {
    "email": "test@example.com",
    "password": "test123",
    "name": "Test User"
}

print("Testing user registration endpoint...")
print(f"POST {url}")
print(f"Data: {json.dumps(data, indent=2)}")
print("\nResponse:")

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200 or response.status_code == 201:
        print("\n✅ Registration successful!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"\n❌ Registration failed!")
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            pass
            
except Exception as e:
    print(f"❌ Error: {e}")
