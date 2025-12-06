# API Routes Report

## All Registered Endpoints

Total: 19 endpoints

| PATH | HTTP METHODS |
|------|--------------|
| `/` | GET |
| `/countries/` | POST |
| `/countries/` | GET |
| `/countries/banned` | POST |
| `/countries/rules` | POST |
| `/countries/{country_id}/rules` | GET |
| `/docs` | GET |
| `/docs/oauth2-redirect` | GET |
| `/health` | GET |
| `/openapi.json` | GET |
| `/orders/` | POST |
| `/orders/user/{user_id}` | GET |
| `/orders/{order_id}` | GET |
| `/orders/{order_id}/accept` | PATCH |
| `/redoc` | GET |
| `/shipping/confirm` | POST |
| `/shipping/estimate` | POST |
| `/users/` | POST |
| `/users/login` | POST |

## Required Endpoints Verification

| Status | Method | Path | Description |
|--------|--------|------|-------------|
| ✅ | POST | `/users/` | User registration |
| ✅ | POST | `/users/login` | User login |
| ✅ | POST | `/countries/` | Create country |
| ✅ | GET | `/countries/` | List countries |
| ✅ | POST | `/countries/rules` | Create country rules |
| ✅ | POST | `/countries/banned` | Add banned item |
| ✅ | POST | `/shipping/estimate` | Get shipping estimate |
| ✅ | POST | `/shipping/confirm` | Confirm order |
| ✅ | GET | `/orders/{order_id}` | Get order details |
| ✅ | GET | `/orders/user/{user_id}` | List user orders |

✅ **ALL REQUIRED ENDPOINTS ARE REGISTERED!**
