"""
Simple route verification - lists all registered endpoints
"""
import sys
import os

# Use SQLite to avoid MySQL connection
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

sys.path.insert(0, '.')
from app.main import app

print("\n" + "=" * 70)
print("ALL REGISTERED ROUTES")
print("=" * 70)

routes_list = []
for route in app.routes:
    if hasattr(route, 'methods') and hasattr(route, 'path'):
        methods = [m for m in route.methods if m not in ['HEAD', 'OPTIONS']]
        if methods:
            routes_list.append({
                'path': route.path,
                'methods': ', '.join(sorted(methods))
            })

routes_list.sort(key=lambda x: x['path'])

print(f"\n{'PATH':<45} {'METHODS':<25}")
print("-" * 70)
for r in routes_list:
    print(f"{r['path']:<45} {r['methods']:<25}")

print("-" * 70)
print(f"Total: {len(routes_list)} endpoints")
print("=" * 70)
