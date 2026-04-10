import streamlit as st
import time
from models.base_account import BankAccount

@st.cache_resource
def get_db():
    from models.db_manager import db
    return db

db = get_db()

st.set_page_config(page_title="Secure Bank", page_icon="🏦", layout="wide")

def main():
    if 'account' not in st.session_state:
        st.session_state.account = None

    if st.session_state.account is None:
        show_login_screen()
    else:
        show_dashboard()

def show_login_screen():
    st.title("🏦 Secure Python Banking")
    tab1, tab2 = st.tabs(["Login", "Open Account"])
    with tab1:
        user = st.text_input("Username").capitalize()
        pw = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            acc = BankAccount.login(user, pw)
            if acc:
                st.session_state.account = acc
                st.rerun()
            else: st.error("Invalid credentials.")

    with tab2:
        new_user = st.text_input("New Username").capitalize()
        new_pw = st.text_input("Create Password", type="password")
        acc_type = st.selectbox("Account Type", ["Savings Account", "Current Account"])
        deposit = st.number_input("Initial Deposit ($)", min_value=0.0)
        if st.button("Create Account", use_container_width=True):
            acc_num = db.create_account(new_user, new_pw, acc_type, deposit)
            if acc_num:
                st.success(f"Created! ID: {acc_num}")
                time.sleep(2)
                st.rerun()
            else: st.error("User exists.")

def show_dashboard():
    acc = st.session_state.account
    
    # --- SIDEBAR: Profile Information ---
    with st.sidebar:
        st.title("🏦 My Profile")
        st.info(f"**User:** {acc.name}\n\n**Account ID:** {acc.acc_number}")
        st.divider()
        if st.button("Logout", use_container_width=True):
            st.session_state.account = None
            st.rerun()

    # --- TAB LOGIC: Admin vs User ---
    if acc.name == "Admin":
        t1, t2 = st.tabs(["My Dashboard", "🏛️ Admin Panel"])
    else:
        t1 = st.container()

    with t1:
        st.header(f"Welcome, {acc.name}")
        st.metric("Current Available Balance", f"${acc.get_balance():,.2f}")
        
        # Action Columns: Deposits & Withdrawals
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Add Funds")
            amt_d = st.number_input("Deposit Amount ($)", key="d", min_value=0.0)
            if st.button("Confirm Deposit", use_container_width=True):
                if acc.deposit(amt_d):
                    st.rerun()
        with c2:
            st.subheader("Withdraw Funds")
            amt_w = st.number_input("Withdrawal Amount ($)", key="w", min_value=0.0)
            if st.button("Confirm Withdraw", use_container_width=True):
                if acc.withdraw(amt_w):
                    st.rerun()
                else:
                    st.error("Transaction Denied: Check limits or balance.")

        st.divider()
        
        # Transfer Section
        st.subheader("📤 Send Money")
        with st.expander("New Fund Transfer"):
            dest = st.text_input("Recipient Account ID (10 digits)")
            t_amt = st.number_input("Amount to Send ($)", key="t", min_value=0.0)
            if st.button("Send Funds", use_container_width=True):
                success, msg = db.transfer_funds(acc.name, dest, t_amt)
                if success:
                    st.success(msg)
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(msg)

        st.divider()
        
        # History & Charts
        history = db.fetch_history(acc.name)
        if history:
            st.subheader("📜 Recent Transactions")
            # Table View for A11y
            st.table([{"Date": r[0], "Description": r[1], "Amount": f"${r[2]:,.2f}"} for r in history])
            
            # --- CHART LOGIC RE-INTEGRATED ---
            st.divider()
            st.subheader("📊 Financial Overview")
            
            # Logic: Sum everything based on the sign of the amount
            # Deposits are positive, Withdrawals/Transfers Sent are negative
            inflow = sum(float(r[2]) for r in history if float(r[2]) > 0)
            outflow = sum(abs(float(r[2])) for r in history if float(r[2]) < 0)

            chart_data = [
                {"Activity": "Total Inflow (Deposits/Received)", "Amount ($)": inflow},
                {"Activity": "Total Outflow (Withdrawals/Sent)", "Amount ($)": outflow}
            ]
            
            # Render Chart
            st.bar_chart(data=chart_data, x="Activity", y="Amount ($)", color="#2ecc71")
            st.caption(f"Summary: Inflow ${inflow:,.2f} | Outflow ${outflow:,.2f}")
        else:
            st.info("No transaction history available yet.")

    # --- ADMIN TAB CONTENT ---
    if acc.name == "Admin":
        with t2:
            st.header("System Administration")
            accounts = db.fetch_all_accounts()
            if accounts:
                st.subheader("Global Account List")
                # Showing all users to the Admin
                st.table([{"Account ID": r[0], "User": r[1], "Type": r[2], "Balance": f"${r[3]:,.2f}"} for r in accounts])
                
                total_bank_cash = sum(r[3] for r in accounts)
                st.metric("Total Bank Liquidity", f"${total_bank_cash:,.2f}", help="Sum of all user balances")
            else:
                st.warning("No registered accounts found in database.")
                
if __name__ == "__main__":
    main()