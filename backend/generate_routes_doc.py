"""
Route verification and documentation generator
"""
import sys
import os

# Use SQLite to avoid MySQL connection
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

sys.path.insert(0, '.')
from app.main import app

# Collect all routes
routes_list = []
for route in app.routes:
    if hasattr(route, 'methods') and hasattr(route, 'path'):
        methods = [m for m in route.methods if m not in ['HEAD', 'OPTIONS']]
        if methods:
            routes_list.append({
                'path': route.path,
                'methods': sorted(methods)
            })

routes_list.sort(key=lambda x: x['path'])

# Generate markdown report
markdown = """# API Routes Report

## All Registered Endpoints

Total: {} endpoints

| PATH | HTTP METHODS |
|------|--------------|
""".format(len(routes_list))

for r in routes_list:
    markdown += f"| `{r['path']}` | {', '.join(r['methods'])} |\n"

# Required endpoints check
markdown += """
## Required Endpoints Verification

| Status | Method | Path | Description |
|--------|--------|------|-------------|
"""

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
    for route in routes_list:
        if route['path'] == path and method in route['methods']:
            found = True
            break
    
    status = "✅" if found else "❌"
    markdown += f"| {status} | {method} | `{path}` | {description} |\n"
    if not found:
        all_found = False

if all_found:
    markdown += "\n✅ **ALL REQUIRED ENDPOINTS ARE REGISTERED!**\n"
else:
    markdown += "\n❌ **SOME ENDPOINTS ARE MISSING!**\n"

# Write to file
with open('routes_documentation.md', 'w', encoding='utf-8') as f:
    f.write(markdown)

print("✅ Routes documentation generated: routes_documentation.md")
print(f"📊 Total endpoints: {len(routes_list)}")
if all_found:
    print("🎉 All required endpoints verified!")
