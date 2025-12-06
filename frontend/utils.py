import requests
from typing import Optional, Dict, Any

# Base API URL - updated for Docker environment
BASE_API = "http://127.0.0.1:8000"


def api_get(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Make GET request to backend API
    
    Args:
        endpoint: API endpoint (e.g., '/users/1')
        params: Query parameters
        
    Returns:
        JSON response as dictionary
        
    Raises:
        Exception with readable error message
    """
    url = f"{BASE_API}{endpoint}"
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        raise Exception(f"Cannot connect to backend at {BASE_API}. Is the server running?")
    except requests.exceptions.Timeout:
        raise Exception(f"Request timeout. Backend at {BASE_API} is not responding.")
    except requests.exceptions.HTTPError as e:
        try:
            error_detail = response.json().get('detail', str(e))
        except:
            error_detail = str(e)
        raise Exception(f"API Error ({response.status_code}): {error_detail}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")


def api_post(endpoint: str, json_data: Optional[Dict[str, Any]] = None, 
             params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Make POST request to backend API
    
    Args:
        endpoint: API endpoint (e.g., '/users/')
        json_data: Request body as dictionary
        params: Query parameters
        
    Returns:
        JSON response as dictionary
        
    Raises:
        Exception with readable error message
    """
    url = f"{BASE_API}{endpoint}"
    try:
        response = requests.post(url, json=json_data, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        raise Exception(f"Cannot connect to backend at {BASE_API}. Is the server running?")
    except requests.exceptions.Timeout:
        raise Exception(f"Request timeout. Backend at {BASE_API} is not responding.")
    except requests.exceptions.HTTPError as e:
        try:
            error_detail = response.json().get('detail', str(e))
        except:
            error_detail = str(e)
        raise Exception(f"API Error ({response.status_code}): {error_detail}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")


def api_patch(endpoint: str, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Make PATCH request to backend API
    
    Args:
        endpoint: API endpoint
        json_data: Request body as dictionary
        
    Returns:
        JSON response as dictionary
        
    Raises:
        Exception with readable error message
    """
    url = f"{BASE_API}{endpoint}"
    try:
        response = requests.patch(url, json=json_data, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        raise Exception(f"Cannot connect to backend at {BASE_API}. Is the server running?")
    except requests.exceptions.Timeout:
        raise Exception(f"Request timeout. Backend at {BASE_API} is not responding.")
    except requests.exceptions.HTTPError as e:
        try:
            error_detail = response.json().get('detail', str(e))
        except:
            error_detail = str(e)
        raise Exception(f"API Error ({response.status_code}): {error_detail}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")
