import streamlit as st
from models.base_account import BankAccount

@st.cache_resource
def get_db():
    from models.db_manager import db
    return db

db = get_db()

def main():
    st.set_page_config(page_title="Secure Bank", page_icon="🏦")
    st.title("🏦 Secure Python Banking")

    if 'account' not in st.session_state:
        st.session_state.account = None

    if st.session_state.account is None:
        show_login_screen()
    else:
        show_dashboard()

def show_login_screen():
    tab1, tab2 = st.tabs(["Login", "Open Account"])
    
    with tab1:
        user = st.text_input("Username", key="login_user").capitalize()
        pw = st.text_input("Password", type="password", key="login_pw")
        if st.button("Login", use_container_width=True):
            acc = BankAccount.login(user, pw)
            if acc:
                st.session_state.account = acc
                st.rerun()
            else:
                st.error("Invalid credentials.")

    with tab2:
        new_user = st.text_input("New Username").capitalize()
        new_pw = st.text_input("Create Password", type="password")
        acc_type = st.selectbox("Account Type", ["Savings Account", "Current Account"])
        deposit = st.number_input("Initial Deposit", min_value=0.0, step=100.0)
        
        if st.button("Create Account", use_container_width=True):
            db.create_account(new_user, new_pw, acc_type, deposit)
            st.success("Account created! Please login.")

def show_dashboard():
    acc = st.session_state.account

    # --- SIDEBAR ---
    with st.sidebar:
        st.title("🏦 My Profile")
        st.info(f"**User:** {acc.name}\n\n**Type:** {acc.account_type()}")
        st.divider()
        if st.button("Logout", use_container_width=True):
            st.session_state.account = None
            st.rerun()

    # --- MAIN STATS ---
    st.metric("Current Balance", f"${acc.get_balance():,.2f}")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Deposit")
        d_amt = st.number_input("Amount", key="dep", min_value=0.0, step=50.0)
        if st.button("Confirm Deposit", use_container_width=True):
            acc.deposit(d_amt)
            st.success("Deposited!")
            st.rerun()

    with col2:
        st.subheader("Withdraw")
        w_amt = st.number_input("Amount", key="with", min_value=0.0, step=50.0)
        if st.button("Confirm Withdrawal", use_container_width=True):
            if acc.withdraw(w_amt):
                st.success("Success!")
                st.rerun()
            else:
                st.error("Transaction Denied.")

    st.divider()

    # --- TRANSACTION HISTORY ---
    st.subheader("📜 Transaction History")
    history = db.fetch_history(acc.name)
    
    if history:
        for row in history:
            col_date, col_desc, col_amt = st.columns([2, 2, 1])
            with col_date:
                st.caption(row[0])
            with col_desc:
                st.write(f"**{row[1]}**")
            with col_amt:
                if "Withdrawal" in row[1]:
                    st.write(f":red[-${abs(row[2]):,.2f}]")
                else:
                    st.write(f":green[+${row[2]:,.2f}]")
    else:
        st.info("No transactions yet.")

    st.divider()

    # --- FINANCIAL OVERVIEW (Outside the loop!) ---
    st.subheader("📊 Financial Overview")
    if history:
        deposits = sum(row[2] for row in history if row[2] > 0)
        withdrawals = sum(abs(row[2]) for row in history if row[2] < 0)
        
        chart_data = {
            "Category": ["Total Deposits", "Total Withdrawals"], 
            "Amount": [deposits, withdrawals]
        }
        st.bar_chart(data=chart_data, x="Category", y="Amount", color="#2ecc71")
    else:
        st.info("Start banking to see your financial trends!")

if __name__ == "__main__":
    main()