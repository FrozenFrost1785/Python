import streamlit as st
import sqlite3
import subprocess

def login(username, password):
    # Connect to the SQLite database
    conn = sqlite3.connect('DBMS.dbsqlite', check_same_thread=False)
    cursor = conn.cursor()

    # Fetch the stored password for the given username
    cursor.execute("SELECT password FROM login WHERE username = ?", (username,))
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        stored_password = result[0]
        # Verify the password (plain text comparison)
        return password == stored_password
    
    return False

# Streamlit app
def main():
    st.title("Login Page")
    
    # Create a login form
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        submit_button = st.form_submit_button("Login")

    if submit_button:
        if login(username, password):
            st.success("Login successful!")

            # Redirect to the Frontend app
            st.write("Redirecting to the application...")
            subprocess.run(["streamlit", "run", "Frontend.py"])
            st.stop()  # Stop the Streamlit app to prevent running further code
        else:
            st.error("Invalid username or password. Please try again.")


if __name__ == "__main__":
    main()
