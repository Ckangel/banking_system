import streamlit as st
from models.base_account import BankAccount
# Remove the direct import: from models.db_manager import db

# Add this helper function to handle the connection safely
@st.cache_resource
def get_db():
    from models.db_manager import db
    return db

db = get_db() # Use this instead of the direct import

def main():
    st.title("🏦 Secure Python Banking")

    # Session State: This keeps the user logged in as they click buttons
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
        if st.button("Login"):
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
        deposit = st.number_input("Initial Deposit", min_value=0.0)
        
        if st.button("Create Account"):
            db.create_account(new_user, new_pw, acc_type, deposit)
            st.success("Account created! Please login.")

def show_dashboard():
    acc = st.session_state.account
    st.sidebar.header(f"Welcome, {acc.name}")
    st.sidebar.info(f"Type: {acc.account_type()}")
    
    if st.sidebar.button("Logout"):
        st.session_state.account = None
        st.rerun()

    # Main Dashboard Stats
    st.metric("Current Balance", f"${acc.get_balance():,.2f}")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Deposit")
        d_amt = st.number_input("Amount", key="dep", min_value=0.0)
        if st.button("Confirm Deposit"):
            acc.deposit(d_amt)
            st.success("Deposited!")
            st.rerun()

    with col2:
        st.subheader("Withdraw")
        w_amt = st.number_input("Amount", key="with", min_value=0.0)
        if st.button("Confirm Withdrawal"):
            if acc.withdraw(w_amt):
                st.success("Success!")
                st.rerun()
            else:
                st.error("Transaction Denied.")

    st.divider()
    st.subheader("Transaction History")
    history = db.fetch_history(acc.name)
    if history:
        for row in history:
            st.write(f"📅 {row[0]} | **{row[1]}** | :green[+${row[2]}]" if row[2] > 0 else f"📅 {row[0]} | **{row[1]}** | :red[-${abs(row[2])}]")

if __name__ == "__main__":
    main()