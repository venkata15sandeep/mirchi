import streamlit as st
import pandas as pd
from datetime import datetime
from utils import (
    load_today_data, save_today_data, calculate_amount,
    get_all_dates, load_data_for_date, get_consolidated_summary,
    GRADES, get_farmer_transactions, get_exporter_transactions
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
    # Save to persist any migrations
    save_today_data(st.session_state.today_data)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Option", ["Today's Operations", "Daily Summary", "Balance Sheet"])

if page == "Today's Operations":
    # ========== TODAY'S OPERATIONS PAGE ==========
    st.markdown("<h2 class='section-header'>📊 Today's Operations</h2>", unsafe_allow_html=True)
    
    today_date = datetime.now().strftime("%Y-%m-%d")
    st.write(f"**Date:** {today_date}")
    
    # Set chilly prices for each grade
    st.markdown("### 💰 Set Today's Chilly Prices by Grade")
    
    price_cols = st.columns(5)
    
    for idx, (grade, description) in enumerate(GRADES.items()):
        with price_cols[idx]:
            grade_price = st.number_input(
                f"{grade} (₹/kg):",
                value=st.session_state.today_data['grade_prices'].get(grade, 0.0),
                min_value=0.0,
                step=0.01,
                format="%.2f",
                key=f"grade_price_{grade}"
            )
            st.session_state.today_data['grade_prices'][grade] = grade_price
    
    # Display prices summary
    st.markdown("**Prices Set for Today:**")
    prices_display = []
    for grade, price in st.session_state.today_data['grade_prices'].items():
        prices_display.append(f"{grade}: ₹{price:.2f}/kg")
    st.info(" | ".join(prices_display))
    
    # Create tabs for Purchase and Export flows
    tab1, tab2 = st.tabs(["🛒 Purchase from Farmers", "📦 Export/Sales"])
    
    # ========== PURCHASE TAB ==========
    with tab1:
        st.markdown("### Add Purchase Transaction from Farmer")
        
        purchase_col1, purchase_col2 = st.columns(2)
        with purchase_col1:
            farmer_name = st.text_input("Farmer Name", key="farmer_name")
            farmer_phone = st.text_input("Farmer Phone Number (Primary Key)", key="farmer_phone", placeholder="Unique identifier for farmer")
        
        with purchase_col2:
            mirchi_grade = st.selectbox(
                "Select Mirchi Grade:",
                list(GRADES.keys()),
                key="purchase_grade"
            )
            
            # Display price for selected grade
            grade_price = st.session_state.today_data['grade_prices'].get(mirchi_grade, 0.0)
            st.info(f"💰 Price for {mirchi_grade}: ₹{grade_price:.2f}/kg")
        
        # Bags and weight info
        purchase_col3, purchase_col4 = st.columns(2)
        with purchase_col3:
            num_bags = st.number_input(
                "Number of Bags:",
                value=1,
                min_value=1,
                step=1,
                key="purchase_num_bags"
            )
        
        with purchase_col4:
            weight_per_bag = st.number_input(
                "Weight per Bag (kg):",
                value=0.0,
                min_value=0.0,
                step=0.01,
                key="purchase_weight_per_bag",
                format="%.2f"
            )
        
        # Calculate totals
        total_weight = num_bags * weight_per_bag
        amount = calculate_amount(total_weight, grade_price)
        
        display_col1, display_col2 = st.columns(2)
        with display_col1:
            st.metric("Total Weight (kg)", f"{total_weight:.2f}")
        with display_col2:
            st.metric("Amount to Pay (₹)", f"₹{amount:.2f}")
        
        if st.button("✅ Add Purchase", key="btn_add_purchase"):
            if farmer_name and farmer_phone and total_weight > 0:
                new_purchase = {
                    "farmer_name": farmer_name,
                    "farmer_phone": farmer_phone,
                    "mirchi_grade": mirchi_grade,
                    "num_bags": num_bags,
                    "weight_per_bag": weight_per_bag,
                    "total_weight": total_weight,
                    "price_per_kg": grade_price,
                    "amount": amount,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                }
                st.session_state.today_data['purchase'].append(new_purchase)
                save_today_data(st.session_state.today_data)
                st.success(f"✓ Added purchase from {farmer_name} ({farmer_phone}) - {num_bags} bags × {weight_per_bag}kg = {total_weight:.2f}kg")
                st.rerun()
            else:
                st.error("⚠️ Please fill all fields and ensure weight > 0")
        
        # Display purchase transactions
        if st.session_state.today_data['purchase']:
            st.markdown("### 📋 Today's Purchases")
            purchase_df = pd.DataFrame(st.session_state.today_data['purchase'])
            
            # Check if new format (has mirchi_grade) or old format (has quantity)
            if 'mirchi_grade' in purchase_df.columns:
                # New format
                display_cols = ['farmer_name', 'farmer_phone', 'mirchi_grade', 'num_bags', 'weight_per_bag', 'total_weight', 'price_per_kg', 'amount', 'timestamp']
                display_df = purchase_df[display_cols].copy()
                display_df.columns = ['Name', 'Phone', 'Grade', 'Bags', 'Wt/Bag (kg)', 'Total Wt (kg)', 'Price/kg (₹)', 'Amount (₹)', 'Time']
            else:
                # Old format fallback
                display_cols = ['farmer_name', 'farmer_phone', 'quantity', 'price_per_unit', 'amount', 'timestamp']
                display_df = purchase_df[display_cols].copy()
                display_df.columns = ['Name', 'Phone', 'Qty (kg)', 'Price/Unit (₹)', 'Amount (₹)', 'Time']
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Delete transaction option
            st.write("**Delete Transaction:**")
            if len(st.session_state.today_data['purchase']) > 0:
                delete_idx = st.selectbox(
                    "Select a transaction to delete:",
                    range(len(st.session_state.today_data['purchase'])),
                    format_func=lambda x: f"{st.session_state.today_data['purchase'][x]['farmer_name']} ({st.session_state.today_data['purchase'][x]['farmer_phone']}) - {st.session_state.today_data['purchase'][x].get('total_weight', st.session_state.today_data['purchase'][x].get('quantity', 0)):.2f}kg",
                    key="delete_purchase_idx"
                )
                if st.button("🗑️ Delete Purchase Transaction", key="btn_del_purchase"):
                    st.session_state.today_data['purchase'].pop(delete_idx)
                    save_today_data(st.session_state.today_data)
                    st.success("✓ Transaction deleted")
                    st.rerun()
    
    # ========== EXPORT TAB ==========
    with tab2:
        st.markdown("### Add Export/Sales Transaction to Buyer")
        
        export_col1, export_col2 = st.columns(2)
        with export_col1:
            exporter_name = st.text_input("Buyer/Exporter Name", key="exporter_name")
            exporter_phone = st.text_input("Buyer/Exporter Phone Number (Primary Key)", key="exporter_phone", placeholder="Unique identifier for buyer")
        
        with export_col2:
            export_grade = st.selectbox(
                "Select Mirchi Grade:",
                list(GRADES.keys()),
                key="export_grade"
            )
            
            # Allow custom price for export if different from purchase price
            export_price = st.number_input(
                f"Price for {export_grade} (₹/kg):",
                value=st.session_state.today_data['grade_prices'].get(export_grade, 0.0),
                min_value=0.0,
                step=0.01,
                format="%.2f",
                key="export_price"
            )
        
        # Bags and weight info
        export_col3, export_col4 = st.columns(2)
        with export_col3:
            export_num_bags = st.number_input(
                "Number of Bags:",
                value=1,
                min_value=1,
                step=1,
                key="export_num_bags"
            )
        
        with export_col4:
            export_weight_per_bag = st.number_input(
                "Weight per Bag (kg):",
                value=0.0,
                min_value=0.0,
                step=0.01,
                key="export_weight_per_bag",
                format="%.2f"
            )
        
        # Calculate totals
        export_total_weight = export_num_bags * export_weight_per_bag
        export_amount = calculate_amount(export_total_weight, export_price)
        
        export_display_col1, export_display_col2 = st.columns(2)
        with export_display_col1:
            st.metric("Total Weight (kg)", f"{export_total_weight:.2f}")
        with export_display_col2:
            st.metric("Amount Received (₹)", f"₹{export_amount:.2f}")
        
        if st.button("✅ Add Export/Sale", key="btn_add_export"):
            if exporter_name and exporter_phone and export_total_weight > 0:
                new_export = {
                    "exporter_name": exporter_name,
                    "exporter_phone": exporter_phone,
                    "mirchi_grade": export_grade,
                    "num_bags": export_num_bags,
                    "weight_per_bag": export_weight_per_bag,
                    "total_weight": export_total_weight,
                    "price_per_kg": export_price,
                    "amount": export_amount,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                }
                st.session_state.today_data['export'].append(new_export)
                save_today_data(st.session_state.today_data)
                st.success(f"✓ Added export to {exporter_name} ({exporter_phone}) - {export_num_bags} bags × {export_weight_per_bag}kg = {export_total_weight:.2f}kg")
                st.rerun()
            else:
                st.error("⚠️ Please fill all fields and ensure weight > 0")
        
        # Display export transactions
        if st.session_state.today_data['export']:
            st.markdown("### 📋 Today's Exports/Sales")
            export_df = pd.DataFrame(st.session_state.today_data['export'])
            
            # Check if new format (has mirchi_grade) or old format (has quantity)
            if 'mirchi_grade' in export_df.columns:
                # New format
                display_cols = ['exporter_name', 'exporter_phone', 'mirchi_grade', 'num_bags', 'weight_per_bag', 'total_weight', 'price_per_kg', 'amount', 'timestamp']
                display_df = export_df[display_cols].copy()
                display_df.columns = ['Name', 'Phone', 'Grade', 'Bags', 'Wt/Bag (kg)', 'Total Wt (kg)', 'Price/kg (₹)', 'Amount (₹)', 'Time']
            else:
                # Old format fallback
                display_cols = ['exporter_name', 'exporter_phone', 'quantity', 'price_per_unit', 'amount', 'timestamp']
                display_df = export_df[display_cols].copy()
                display_df.columns = ['Name', 'Phone', 'Qty (kg)', 'Price/Unit (₹)', 'Amount (₹)', 'Time']
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Delete transaction option
            st.write("**Delete Transaction:**")
            if len(st.session_state.today_data['export']) > 0:
                delete_idx = st.selectbox(
                    "Select a transaction to delete:",
                    range(len(st.session_state.today_data['export'])),
                    format_func=lambda x: f"{st.session_state.today_data['export'][x]['exporter_name']} ({st.session_state.today_data['export'][x]['exporter_phone']}) - {st.session_state.today_data['export'][x].get('total_weight', st.session_state.today_data['export'][x].get('quantity', 0)):.2f}kg",
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
                    
                    # Check if new format (has mirchi_grade) or old format (has quantity)
                    if 'mirchi_grade' in purchase_df.columns:
                        display_cols = ['farmer_name', 'farmer_phone', 'mirchi_grade', 'total_weight', 'amount']
                        display_df = purchase_df[display_cols].copy()
                        display_df.columns = ['Farmer', 'Phone', 'Grade', 'Wt (kg)', 'Amount (₹)']
                    else:
                        # Old format fallback
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
                    
                    # Check if new format (has mirchi_grade) or old format (has quantity)
                    if 'mirchi_grade' in export_df.columns:
                        display_cols = ['exporter_name', 'exporter_phone', 'mirchi_grade', 'total_weight', 'amount']
                        display_df = export_df[display_cols].copy()
                        display_df.columns = ['Buyer/Exporter', 'Phone', 'Grade', 'Wt (kg)', 'Amount (₹)']
                    else:
                        # Old format fallback
                        display_cols = ['exporter_name', 'exporter_phone', 'quantity', 'amount']
                        display_df = export_df[display_cols].copy()
                        display_df.columns = ['Buyer/Exporter', 'Phone', 'Qty (kg)', 'Amount (₹)']
                    
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
