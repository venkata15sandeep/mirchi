# Quick Start Guide 🚀

## Getting Started in 5 Minutes

### 1. Install Dependencies (One Time)

Open PowerShell and navigate to the project:

```powershell
cd d:\Mirchi
pip install -r requirements.txt
```

### 2. Run the Application

```powershell
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

### 3. Start Using!

- **Tab 1: Today's Operations** - Enter purchases and sales
- **Tab 2: Daily Summary** - View today's consolidated data
- **Tab 3: Balance Sheet** - See all-time statistics and reports

---

## Application Features Overview

### 🛒 Purchase Flow
- Enter farmer name, phone, and quantity
- Price auto-calculates based on today's chilly price
- All data saved in JSON format

### 📦 Export/Sales Flow
- Record buyer name, phone, and quantity
- Set custom selling price
- Track all sales transactions

### 📊 Daily Summary
- View purchase and sale totals
- Check profit/loss for the day
- See quantity balance on hand

### 📈 Balance Sheet
- Overall statistics across all dates
- Daily breakdown table
- Download CSV reports

---

## File Locations & What They Do

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit application with all UI |
| `utils.py` | Helper functions for data storage/retrieval |
| `requirements.txt` | Python package list |
| `.streamlit/config.toml` | Streamlit theme & settings |
| `README.md` | Full documentation |
| `DEPLOYMENT.md` | Step-by-step cloud deployment |
| `data/` | Auto-created folder with day-wise JSON files |

---

## Data Storage

Your data is stored locally in:
```
d:\Mirchi\data\

2024-01-15.json   ← Today's file
2024-01-14.json   ← Yesterday
2024-01-13.json   ← And so on...
```

Each file contains:
- Today's chilly price
- All purchase transactions
- All export/sale transactions
- Amounts and timestamps

---

## Common Tasks

### Add a Purchase Transaction
1. Go to "Today's Operations" tab
2. Click "🛒 Purchase from Farmers" tab
3. Enter farmer details and quantity
4. Click "✅ Add Purchase"

### Add a Sale Transaction
1. Go to "Today's Operations" tab
2. Click "📦 Export/Sales" tab
3. Enter buyer details, quantity, and price
4. Click "✅ Add Export/Sale"

### View Daily Summary
1. Go to "Daily Summary" tab
2. Select a date
3. View consolidated statistics

### Export Data to CSV
1. Go to "Balance Sheet" tab
2. Click "📥 Download as CSV"
3. Save to your computer

---

## Troubleshooting

### App won't start
```
Error: Module not found
→ Solution: pip install -r requirements.txt
```

### Port already in use
```
streamlit run app.py --logger.level=debug --server.port=8502
```

### Data not showing up
- Check the `data/` folder exists
- Ensure JSON files are created
- Refresh the browser (F5)

---

## Next Steps

1. ✅ Run the app locally to test
2. ✅ Get familiar with the features
3. ✅ Create a GitHub repository
4. ✅ Deploy to Streamlit Cloud (see DEPLOYMENT.md)
5. ✅ Share the URL with stakeholders

---

## Need Help?

- **Full Documentation**: See `README.md`
- **Deployment Help**: See `DEPLOYMENT.md`
- **Questions**: Check Streamlit docs at https://docs.streamlit.io

---

**Happy farming! 🌶️**
