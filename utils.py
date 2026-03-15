import json
import os
from datetime import datetime

DATA_DIR = "data"

# Grade definitions
GRADES = {
    "Grade 1": "Grade 1 - Premium",
    "Grade 2": "Grade 2 - High Quality",
    "Grade 3": "Grade 3 - Medium Quality",
    "Grade 4": "Grade 4 - Standard",
    "Grade 5": "Grade 5 - Economy"
}

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
            data = json.load(f)
            
        # Migrate old data format to new format
        if 'chilly_price' in data and 'grade_prices' not in data:
            # Old format - convert to new format
            old_price = data.pop('chilly_price', 0.0)
            data['grade_prices'] = {
                "Grade 1": old_price,
                "Grade 2": old_price,
                "Grade 3": old_price,
                "Grade 4": old_price,
                "Grade 5": old_price
            }
        
        # Ensure grade_prices exists
        if 'grade_prices' not in data:
            data['grade_prices'] = {
                "Grade 1": 0.0,
                "Grade 2": 0.0,
                "Grade 3": 0.0,
                "Grade 4": 0.0,
                "Grade 5": 0.0
            }
        
        # Ensure purchase and export lists exist
        if 'purchase' not in data:
            data['purchase'] = []
        if 'export' not in data:
            data['export'] = []
            
        return data
    
    return {
        "grade_prices": {
            "Grade 1": 0.0,
            "Grade 2": 0.0,
            "Grade 3": 0.0,
            "Grade 4": 0.0,
            "Grade 5": 0.0
        },
        "purchase": [],
        "export": []
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
    files = [f for f in os.listdir(DATA_DIR) if f.endswith('.json') and f != 'SAMPLE_DATA_STRUCTURE.json']
    dates = [f.replace('.json', '') for f in sorted(files, reverse=True)]
    return dates

def load_data_for_date(date_str):
    """Load data for a specific date."""
    filename = os.path.join(DATA_DIR, f"{date_str}.json")
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        
        # Migrate old data format to new format
        if 'chilly_price' in data and 'grade_prices' not in data:
            # Old format - convert to new format
            old_price = data.pop('chilly_price', 0.0)
            data['grade_prices'] = {
                "Grade 1": old_price,
                "Grade 2": old_price,
                "Grade 3": old_price,
                "Grade 4": old_price,
                "Grade 5": old_price
            }
        
        # Ensure grade_prices exists
        if 'grade_prices' not in data:
            data['grade_prices'] = {
                "Grade 1": 0.0,
                "Grade 2": 0.0,
                "Grade 3": 0.0,
                "Grade 4": 0.0,
                "Grade 5": 0.0
            }
        
        return data
    return None

def calculate_amount(total_weight, price_per_kg):
    """Calculate amount with 2 decimal places."""
    return round(total_weight * price_per_kg, 2)

def get_farmer_transactions(data, farmer_phone):
    """Get all transactions for a specific farmer by phone number."""
    transactions = [t for t in data['purchase'] if t['farmer_phone'] == farmer_phone]
    return transactions

def get_exporter_transactions(data, exporter_phone):
    """Get all transactions for a specific exporter by phone number."""
    transactions = [t for t in data['export'] if t['exporter_phone'] == exporter_phone]
    return transactions

def get_consolidated_summary(date_str):
    """Get daily consolidated summary for a specific date."""
    data = load_data_for_date(date_str)
    if not data:
        return None
    
    # Calculate purchase totals (handle both old and new formats)
    total_quantity_purchased = 0
    for item in data['purchase']:
        # Handle both old format (quantity) and new format (total_weight)
        total_quantity_purchased += item.get('total_weight', item.get('quantity', 0))
    
    total_amount_paid = sum(item.get('amount', 0) for item in data['purchase'])
    
    # Calculate export totals (handle both old and new formats)
    total_quantity_exported = 0
    for item in data['export']:
        # Handle both old format (quantity) and new format (total_weight)
        total_quantity_exported += item.get('total_weight', item.get('quantity', 0))
    
    total_amount_received = sum(item.get('amount', 0) for item in data['export'])
    
    return {
        "date": date_str,
        "grade_prices": data.get('grade_prices', {}),
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
