import requests
import pandas as pd


def format_flow_status(flow_cfs, optimal_min, optimal_max):
    """Classify flow conditions"""
    if flow_cfs < optimal_min:
        return {"status": "Too Low", "emoji": "🟡"}
    elif flow_cfs > optimal_max:
        return {"status": "Too High", "emoji": "🔴"}
    else:
        return {"status": "Good", "emoji": "🟢"}


def fetch_with_retry(url, retries=3, timeout=5):
    """Fetch data with retry logic"""
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            if attempt == retries - 1:
                raise
            continue
    return None


def format_timestamp(ts):
    """Format timestamp for display"""
    if isinstance(ts, str):
        return ts.split('T')[0] + ' ' + ts.split('T')[1].split('.')[0]
    return str(ts)
