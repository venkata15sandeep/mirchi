import streamlit as st
import pandas as pd
from datetime import datetime
from utils import (
    load_today_data, save_today_data, calculate_amount,
    get_all_dates, load_data_for_date, get_consolidated_summary
)

# Page configuration
st.set_page_config(
    page_title="Chilly Yard Manager",
    page_icon="🌶️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #c41e3a;
        font-size: 2.5em;
        margin-bottom: 0.5em;
    }
    .section-header {
        color: #c41e3a;
        border-bottom: 3px solid #c41e3a;
        padding-bottom: 0.5em;
        margin-top: 1em;
        margin-bottom: 1em;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🌶️ Chilly Yard Manager</h1>", unsafe_allow_html=True)

# Initialize session state
if 'today_data' not in st.session_state:
    st.session_state.today_data = load_today_data()

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Option", ["Today's Operations", "Daily Summary", "Balance Sheet"])

if page == "Today's Operations":
    # ========== TODAY'S OPERATIONS PAGE ==========
    st.markdown("<h2 class='section-header'>📊 Today's Operations</h2>", unsafe_allow_html=True)
    
    today_date = datetime.now().strftime("%Y-%m-%d")
    st.write(f"**Date:** {today_date}")
    
    # Set chilly price for the day
    st.markdown("### 💰 Set Today's Chilly Price")
    col1, col2 = st.columns([1, 1])
    with col1:
        chilly_price = st.number_input(
            "Price per unit (₹):",
            value=st.session_state.today_data.get('chilly_price', 0.0),
            min_value=0.0,
            step=0.01,
            format="%.2f"
        )
        st.session_state.today_data['chilly_price'] = chilly_price
    
    with col2:
        st.info(f"✓ Current price: ₹{chilly_price:.2f} per unit")
    
    # Create tabs for Purchase and Export flows
    tab1, tab2 = st.tabs(["🛒 Purchase from Farmers", "📦 Export/Sales"])
    
    # ========== PURCHASE TAB ==========
    with tab1:
        st.markdown("### Add Purchase Transaction")
        
        purchase_col1, purchase_col2 = st.columns(2)
        with purchase_col1:
            farmer_name = st.text_input("Farmer Name", key="farmer_name")
            quantity = st.number_input(
                "Quantity (kg):",
                value=0.0,
                min_value=0.0,
                step=0.01,
                key="purchase_qty"
            )
        
        with purchase_col2:
            farmer_phone = st.text_input("Farmer Phone Number", key="farmer_phone")
            # Auto-calculate amount based on quantity and chilly price
            amount = calculate_amount(quantity, chilly_price)
            st.number_input(
                "Amount to Pay (₹):",
                value=amount,
                disabled=True,
                format="%.2f",
                key="purchase_amount_display"
            )
        
        # Add manual override for amount if needed
        st.info("💡 Amount is automatically calculated based on quantity × today's price. Edit quantity to adjust amount.")
        
        if st.button("✅ Add Purchase", key="btn_add_purchase"):
            if farmer_name and farmer_phone and quantity > 0:
                new_purchase = {
                    "farmer_name": farmer_name,
                    "farmer_phone": farmer_phone,
                    "quantity": quantity,
                    "price_per_unit": chilly_price,
                    "amount": amount,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                }
                st.session_state.today_data['purchase'].append(new_purchase)
                save_today_data(st.session_state.today_data)
                st.success(f"✓ Added purchase from {farmer_name} - {quantity} kg")
                st.rerun()
            else:
                st.error("⚠️ Please fill all fields and ensure quantity > 0")
        
        # Display purchase transactions
        if st.session_state.today_data['purchase']:
            st.markdown("### 📋 Today's Purchases")
            purchase_df = pd.DataFrame(st.session_state.today_data['purchase'])
            
            # Reorder columns for better display
            display_cols = ['farmer_name', 'farmer_phone', 'quantity', 'price_per_unit', 'amount', 'timestamp']
            display_df = purchase_df[display_cols].copy()
            display_df.columns = ['Farmer Name', 'Phone', 'Quantity (kg)', 'Price/Unit (₹)', 'Amount (₹)', 'Time']
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Delete transaction option
            st.write("**Delete Transaction:**")
            if len(st.session_state.today_data['purchase']) > 0:
                delete_idx = st.selectbox(
                    "Select a transaction to delete:",
                    range(len(st.session_state.today_data['purchase'])),
                    format_func=lambda x: f"{st.session_state.today_data['purchase'][x]['farmer_name']} - {st.session_state.today_data['purchase'][x]['quantity']} kg",
                    key="delete_purchase_idx"
                )
                if st.button("🗑️ Delete Purchase Transaction", key="btn_del_purchase"):
                    st.session_state.today_data['purchase'].pop(delete_idx)
                    save_today_data(st.session_state.today_data)
                    st.success("✓ Transaction deleted")
                    st.rerun()
    
    # ========== EXPORT TAB ==========
    with tab2:
        st.markdown("### Add Export/Sales Transaction")
        
        export_col1, export_col2 = st.columns(2)
        with export_col1:
            exporter_name = st.text_input("Exporter/Buyer Name", key="exporter_name")
            export_quantity = st.number_input(
                "Quantity (kg):",
                value=0.0,
                min_value=0.0,
                step=0.01,
                key="export_qty"
            )
        
        with export_col2:
            exporter_phone = st.text_input("Exporter/Buyer Phone Number", key="exporter_phone")
            # Allow custom price for export if different from purchase price
            export_price = st.number_input(
                "Price per Unit (₹):",
                value=chilly_price,
                min_value=0.0,
                step=0.01,
                format="%.2f",
                key="export_price"
            )
        
        # Calculate export amount
        export_amount = calculate_amount(export_quantity, export_price)
        st.number_input(
            "Amount Received (₹):",
            value=export_amount,
            disabled=True,
            format="%.2f",
            key="export_amount_display"
        )
        
        if st.button("✅ Add Export/Sale", key="btn_add_export"):
            if exporter_name and exporter_phone and export_quantity > 0:
                new_export = {
                    "exporter_name": exporter_name,
                    "exporter_phone": exporter_phone,
                    "quantity": export_quantity,
                    "price_per_unit": export_price,
                    "amount": export_amount,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                }
                st.session_state.today_data['export'].append(new_export)
                save_today_data(st.session_state.today_data)
                st.success(f"✓ Added export to {exporter_name} - {export_quantity} kg")
                st.rerun()
            else:
                st.error("⚠️ Please fill all fields and ensure quantity > 0")
        
        # Display export transactions
        if st.session_state.today_data['export']:
            st.markdown("### 📋 Today's Exports/Sales")
            export_df = pd.DataFrame(st.session_state.today_data['export'])
            
            # Reorder columns for better display
            display_cols = ['exporter_name', 'exporter_phone', 'quantity', 'price_per_unit', 'amount', 'timestamp']
            display_df = export_df[display_cols].copy()
            display_df.columns = ['Exporter/Buyer', 'Phone', 'Quantity (kg)', 'Price/Unit (₹)', 'Amount (₹)', 'Time']
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Delete transaction option
            st.write("**Delete Transaction:**")
            if len(st.session_state.today_data['export']) > 0:
                delete_idx = st.selectbox(
                    "Select a transaction to delete:",
                    range(len(st.session_state.today_data['export'])),
                    format_func=lambda x: f"{st.session_state.today_data['export'][x]['exporter_name']} - {st.session_state.today_data['export'][x]['quantity']} kg",
                    key="delete_export_idx"
                )
                if st.button("🗑️ Delete Export Transaction", key="btn_del_export"):
                    st.session_state.today_data['export'].pop(delete_idx)
                    save_today_data(st.session_state.today_data)
                    st.success("✓ Transaction deleted")
                    st.rerun()

elif page == "Daily Summary":
    # ========== DAILY SUMMARY PAGE ==========
    st.markdown("<h2 class='section-header'>📊 Daily Consolidation Summary</h2>", unsafe_allow_html=True)
    
    dates = get_all_dates()
    
    if dates:
        selected_date = st.selectbox(
            "Select Date:",
            dates,
            index=0
        )
        
        summary = get_consolidated_summary(selected_date)
        
        if summary:
            # Create columns for overview
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "📥 Total Purchased (kg)",
                    f"{summary['purchase']['total_quantity']:.2f}",
                    delta=f"{summary['purchase']['transaction_count']} transactions"
                )
            
            with col2:
                st.metric(
                    "💰 Amount Paid (₹)",
                    f"₹{summary['purchase']['total_amount']:.2f}"
                )
            
            with col3:
                st.metric(
                    "📤 Total Exported (kg)",
                    f"{summary['export']['total_quantity']:.2f}",
                    delta=f"{summary['export']['transaction_count']} transactions"
                )
            
            with col4:
                st.metric(
                    "💸 Amount Received (₹)",
                    f"₹{summary['export']['total_amount']:.2f}"
                )
            
            # Detailed breakdown
            st.markdown("### 📋 Transaction Details")
            
            detail_col1, detail_col2 = st.columns(2)
            
            with detail_col1:
                st.write("**PURCHASES FROM FARMERS**")
                if summary['purchase']['transaction_count'] > 0:
                    data = load_data_for_date(selected_date)
                    purchase_df = pd.DataFrame(data['purchase'])
                    display_cols = ['farmer_name', 'farmer_phone', 'quantity', 'amount']
                    display_df = purchase_df[display_cols].copy()
                    display_df.columns = ['Farmer', 'Phone', 'Qty (kg)', 'Amount (₹)']
                    st.dataframe(display_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No purchase transactions")
            
            with detail_col2:
                st.write("**EXPORTS/SALES**")
                if summary['export']['transaction_count'] > 0:
                    data = load_data_for_date(selected_date)
                    export_df = pd.DataFrame(data['export'])
                    display_cols = ['exporter_name', 'exporter_phone', 'quantity', 'amount']
                    display_df = export_df[display_cols].copy()
                    display_df.columns = ['Exporter', 'Phone', 'Qty (kg)', 'Amount (₹)']
                    st.dataframe(display_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No export transactions")
            
            # Balance summary
            st.markdown("### ⚖️ Daily Balance")
            balance_col1, balance_col2, balance_col3 = st.columns(3)
            
            with balance_col1:
                st.metric(
                    "Quantity on Hand (kg)",
                    f"{summary['balance']['quantity_on_hand']:.2f}"
                )
            
            with balance_col2:
                profit_loss = summary['balance']['profit_loss']
                color = "green" if profit_loss >= 0 else "red"
                st.metric(
                    "Profit/Loss (₹)",
                    f"₹{profit_loss:.2f}",
                    delta="Profit" if profit_loss >= 0 else "Loss"
                )
            
            with balance_col3:
                avg_purchase_price = (
                    summary['purchase']['total_amount'] / summary['purchase']['total_quantity']
                    if summary['purchase']['total_quantity'] > 0 else 0
                )
                st.metric(
                    "Avg Purchase Price (₹/kg)",
                    f"₹{avg_purchase_price:.2f}"
                )

    else:
        st.info("ℹ️ No data available yet. Start adding transactions in 'Today's Operations' tab.")

elif page == "Balance Sheet":
    # ========== BALANCE SHEET PAGE ==========
    st.markdown("<h2 class='section-header'>📈 Balance Sheet & Reports</h2>", unsafe_allow_html=True)
    
    dates = get_all_dates()
    
    if dates:
        st.markdown("### 📅 Overall Summary")
        
        # Calculate totals across all dates
        total_qty_purchased = 0
        total_amount_paid = 0
        total_qty_exported = 0
        total_amount_received = 0
        
        balance_data = []
        
        for date in dates:
            summary = get_consolidated_summary(date)
            if summary:
                total_qty_purchased += summary['purchase']['total_quantity']
                total_amount_paid += summary['purchase']['total_amount']
                total_qty_exported += summary['export']['total_quantity']
                total_amount_received += summary['export']['total_amount']
                
                balance_data.append({
                    'Date': date,
                    'Purchased (kg)': summary['purchase']['total_quantity'],
                    'Amount Paid (₹)': summary['purchase']['total_amount'],
                    'Exported (kg)': summary['export']['total_quantity'],
                    'Amount Received (₹)': summary['export']['total_amount'],
                    'Qty Balance (kg)': summary['balance']['quantity_on_hand'],
                    'Profit/Loss (₹)': summary['balance']['profit_loss']
                })
        
        # Top metrics
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        with metric_col1:
            st.metric(
                "Total Purchased (kg)",
                f"{total_qty_purchased:.2f}"
            )
        
        with metric_col2:
            st.metric(
                "Total Amount Paid (₹)",
                f"₹{total_amount_paid:.2f}"
            )
        
        with metric_col3:
            st.metric(
                "Total Exported (kg)",
                f"{total_qty_exported:.2f}"
            )
        
        with metric_col4:
            st.metric(
                "Total Amount Received (₹)",
                f"₹{total_amount_received:.2f}"
            )
        
        # Overall profit/loss
        overall_profit = total_amount_received - total_amount_paid
        st.markdown("---")
        
        balance_col1, balance_col2, balance_col3 = st.columns(3)
        
        with balance_col1:
            remaining_qty = total_qty_purchased - total_qty_exported
            st.metric(
                "Remaining Stock (kg)",
                f"{remaining_qty:.2f}"
            )
        
        with balance_col2:
            st.metric(
                "Total Profit/Loss (₹)",
                f"₹{overall_profit:.2f}",
                delta="Profit" if overall_profit >= 0 else "Loss"
            )
        
        with balance_col3:
            avg_profit_per_kg = (
                overall_profit / total_qty_exported
                if total_qty_exported > 0 else 0
            )
            st.metric(
                "Profit per kg (₹/kg)",
                f"₹{avg_profit_per_kg:.2f}"
            )
        
        # Detailed transaction history
        st.markdown("### 📊 Detailed Daily Breakdown")
        
        if balance_data:
            balance_df = pd.DataFrame(balance_data)
            st.dataframe(balance_df, use_container_width=True, hide_index=True)
            
            # Download option
            csv_data = balance_df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv_data,
                file_name=f"chilly_balance_sheet_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No data available")
    else:
        st.info("ℹ️ No data available yet. Start adding transactions in 'Today's Operations' tab.")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 0.9em;'>"
    "🌶️ Chilly Yard Manager v1.0 | Data stored locally in JSON format"
    "</p>",
    unsafe_allow_html=True
)
