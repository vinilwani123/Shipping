"""
Test script to verify all API routes are registered correctly.
Lists all endpoints with their HTTP methods.
NO DATABASE CONNECTION REQUIRED.
"""
import sys
import os

# Temporarily set DATABASE_URL to SQLite in-memory to avoid MySQL connection
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

print("=" * 70)
print("BACKEND ROUTES VERIFICATION TEST")
print("=" * 70)

try:
    # Import the FastAPI app
    sys.path.insert(0, '.')
    from app.main import app
    
    print("\n✅ FastAPI app imported successfully!\n")
    print("-" * 70)
    print(f"{'ENDPOINT PATH':<45} {'METHODS':<25}")
    print("-" * 70)
    
    # Get all routes from the app
    routes = []
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            # Filter out HEAD and OPTIONS methods for cleaner output
            methods = [m for m in route.methods if m not in ['HEAD', 'OPTIONS']]
            if methods:
                routes.append({
                    'path': route.path,
                    'methods': ', '.join(sorted(methods)),
                    'name': getattr(route, 'name', 'N/A')
                })
    
    # Sort routes by path
    routes.sort(key=lambda x: x['path'])
    
    # Print all routes
    for route in routes:
        print(f"{route['path']:<45} {route['methods']:<25}")
    
    print("-" * 70)
    print(f"\n📊 Total Endpoints Registered: {len(routes)}")
    
    # Verify specific required endpoints
    print("\n" + "=" * 70)
    print("ENDPOINT VERIFICATION CHECKLIST")
    print("=" * 70)
    
    required_endpoints = [
        ("POST", "/users/", "User registration"),
        ("POST", "/users/login", "User login"),
        ("POST", "/countries/", "Create country"),
        ("GET", "/countries/", "List countries"),
        ("POST", "/countries/rules", "Create country rules"),
        ("POST", "/countries/banned", "Add banned item"),
        ("POST", "/shipping/estimate", "Get shipping estimate"),
        ("POST", "/shipping/confirm", "Confirm order"),
        ("GET", "/orders/{order_id}", "Get order details"),
        ("GET", "/orders/user/{user_id}", "List user orders"),
    ]
    
    all_found = True
    for method, path, description in required_endpoints:
        found = False
        for route in routes:
            if route['path'] == path and method in route['methods']:
                found = True
                break
        
        status = "✅" if found else "❌"
        print(f"{status} {method:<6} {path:<35} - {description}")
        if not found:
            all_found = False
    
    print("=" * 70)
    
    if all_found:
        print("\n🎉 SUCCESS! All required endpoints are registered!")
        print("\nThe backend API is ready with all specified routes.")
    else:
        print("\n⚠️  WARNING: Some required endpoints are missing!")
        sys.exit(1)
    
except Exception as e:
    print("\n" + "=" * 70)
    print("❌ ERROR: Route verification failed!")
    print("=" * 70)
    print(f"\nError: {str(e)}")
    import traceback
    print("\nFull traceback:")
    print(traceback.format_exc())
    sys.exit(1)
