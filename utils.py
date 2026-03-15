import json
import os
from datetime import datetime

DATA_DIR = "data"

def ensure_data_directory():
    """Create data directory if it doesn't exist."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def get_today_filename():
    """Get the filename for today's date."""
    today = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(DATA_DIR, f"{today}.json")

def load_today_data():
    """Load today's data from JSON file."""
    ensure_data_directory()
    filename = get_today_filename()
    
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {
        "purchase": [],
        "export": [],
        "chilly_price": 0.0
    }

def save_today_data(data):
    """Save today's data to JSON file."""
    ensure_data_directory()
    filename = get_today_filename()
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def get_all_dates():
    """Get all available dates with data."""
    ensure_data_directory()
    files = [f for f in os.listdir(DATA_DIR) if f.endswith('.json')]
    dates = [f.replace('.json', '') for f in sorted(files, reverse=True)]
    return dates

def load_data_for_date(date_str):
    """Load data for a specific date."""
    filename = os.path.join(DATA_DIR, f"{date_str}.json")
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return None

def calculate_amount(quantity, price):
    """Calculate amount with 2 decimal places."""
    return round(quantity * price, 2)

def get_consolidated_summary(date_str):
    """Get daily consolidated summary for a specific date."""
    data = load_data_for_date(date_str)
    if not data:
        return None
    
    # Calculate purchase totals
    total_quantity_purchased = sum(item['quantity'] for item in data['purchase'])
    total_amount_paid = sum(item['amount'] for item in data['purchase'])
    
    # Calculate export totals
    total_quantity_exported = sum(item['quantity'] for item in data['export'])
    total_amount_received = sum(item['amount'] for item in data['export'])
    
    return {
        "date": date_str,
        "chilly_price": data.get('chilly_price', 0.0),
        "purchase": {
            "total_quantity": total_quantity_purchased,
            "total_amount": total_amount_paid,
            "transaction_count": len(data['purchase'])
        },
        "export": {
            "total_quantity": total_quantity_exported,
            "total_amount": total_amount_received,
            "transaction_count": len(data['export'])
        },
        "balance": {
            "quantity_on_hand": total_quantity_purchased - total_quantity_exported,
            "profit_loss": total_amount_received - total_amount_paid
        }
    }
