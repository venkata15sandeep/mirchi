# 🌶️ Chilly Yard Manager

A Streamlit web application for managing your chilly (chili pepper) yard business. Track farmer purchases, export sales, and maintain comprehensive business analytics.

## Features

✅ **Purchase Management**
- Record purchases from farmers
- Track farmer details (name, phone number)
- Auto-calculate amounts based on quantity and price
- 2 decimal place precision

✅ **Export/Sales Management**
- Track sales to exporters/buyers
- Record buyer details
- Support custom pricing per transaction
- Amount calculation with precision

✅ **Daily Operations**
- Set daily chilly prices
- Real-time transaction tracking
- Edit and delete transactions
- View all transactions for the day

✅ **Daily Summary**
- Consolidated daily statistics
- Total quantity purchased and sold
- Total amounts paid and received
- Profit/loss calculation
- Quantity balance tracking

✅ **Balance Sheet & Reports**
- Overall business analytics
- Cumulative statistics across all dates
- Daily breakdown table
- Profit per kg calculations
- CSV export functionality

✅ **Data Storage**
- Day-wise JSON file storage
- Local data persistence
- Easy data retrieval and analysis

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or download the project**
```bash
cd d:\Mirchi
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application locally**
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## File Structure

```
Mirchi/
├── app.py                    # Main Streamlit application
├── utils.py                  # Helper functions for data operations
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── data/                     # Directory for day-wise JSON files (auto-created)
│   ├── 2024-01-15.json
│   ├── 2024-01-16.json
│   └── ...
└── README.md                # This file
```

## Data Format

Each day's data is stored in a JSON file with the following structure:

```json
{
    "chilly_price": 50.00,
    "purchase": [
        {
            "farmer_name": "John Farmer",
            "farmer_phone": "9876543210",
            "quantity": 100.50,
            "price_per_unit": 50.00,
            "amount": 5025.00,
            "timestamp": "10:30:45"
        }
    ],
    "export": [
        {
            "exporter_name": "Export Company ABC",
            "exporter_phone": "9123456789",
            "quantity": 80.00,
            "price_per_unit": 65.00,
            "amount": 5200.00,
            "timestamp": "14:25:10"
        }
    ]
}
```

## Deployment to Streamlit Cloud

### Step 1: Create a GitHub Repository

1. Create a new GitHub repository
2. Push your project files:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/Mirchi.git
git push -u origin main
```

### Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign up with your GitHub account
3. Click "New app" button
4. Select:
   - **Repository**: YOUR_USERNAME/Mirchi
   - **Branch**: main
   - **Main file path**: app.py
5. Click "Deploy!"

### Step 3: Access Your App

Once deployed, your app will be available at:
```
https://your-app-name.streamlit.app
```

## Usage Guide

### Today's Operations Tab

#### Set Chilly Price
1. Enter the price per unit for today's chilly
2. This price will be used for auto-calculation in transactions

#### Add Purchase Transaction
1. Fill in farmer name and phone number
2. Enter quantity purchased
3. Amount will auto-calculate (you can override if needed)
4. Click "Add Purchase"

#### Add Export/Sale Transaction
1. Fill in exporter/buyer name and phone number
2. Enter quantity sold
3. Enter price per unit (can be different from purchase price)
4. Amount will auto-calculate
5. Click "Add Export/Sale"

#### Delete Transactions
- Select a transaction from the dropdown
- Click "Delete" to remove it

### Daily Summary Tab

1. Select a date from the dropdown
2. View all metrics for that day:
   - Total purchased and amount paid
   - Total exported and amount received
   - Quantity balance
   - Profit/loss

### Balance Sheet Tab

1. View overall business statistics:
   - Total quantity purchased/exported
   - Total amounts
   - Overall profit/loss
   - Profit per kg
2. Detailed daily breakdown table
3. Download CSV report

## Important Notes

### Data Storage
- Data is stored locally on your machine (or cloud server if deployed to Streamlit Cloud)
- Each day has a separate JSON file in the `data/` folder
- Data persists between sessions

### Calculations
- All amounts are calculated to 2 decimal places
- Profit/Loss = Amount Received - Amount Paid
- Profit per kg = Total Profit/Loss ÷ Total Quantity Exported

### Constraints Implemented
✅ Price provided for each buyer and seller
✅ Buyer/seller name and phone number tracking
✅ Amount calculation with 2 decimal places
✅ Day-wise JSON file storage
✅ Consolidation button for daily summaries
✅ Balance sheet with purchases and sales

## Support

For issues or feature requests, please contact the developer.

## License

This project is provided as-is for personal business use.

---

**Made with ❤️ for your chilly yard business**
