import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import json

st.set_page_config(page_title="Organ Donation App", layout="wide")

# Set seaborn style
sns.set(style="whitegrid")

# Function to connect to the SQLite database
def get_connection():
    conn = sqlite3.connect('DBMS.dbsqlite', check_same_thread=False)
    return conn

# Function to execute SQL queries
def execute_query(query, params=()):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

# Function to fetch data from a table
def fetch_data(table_name):
    conn = get_connection()
    if table_name == "Transaction":
        df = pd.read_sql_query(f'SELECT * FROM "Transaction"', conn)
    else:
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df

# Function to visualize statistics with a count plot
def visualize_statistics(df, column, title):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.countplot(data=df, x=column, ax=ax, palette='Set2', order=df[column].value_counts().index)
    ax.set_title(title, fontsize=16, weight='bold')
    ax.set_xlabel(column.replace("_", " ").title(), fontsize=14)
    ax.set_ylabel("Count", fontsize=14)
    plt.xticks(rotation=45)
    sns.despine()  # Remove top and right spines for a cleaner look
    return fig

# Function to visualize statistics with a 3D pie chart
def visualize_3d_pie(df, column, title):
    counts = df[column].value_counts()
    labels = counts.index
    values = counts.values

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(title_text=title, title_x=0.5)
    
    return fig

# Sidebar for navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Select an option:", ["Doctors", "Donors", "Available Organs", "Organizations", "Patients", "Transactions", "Users"])

# Main UI logic based on sidebar selection
if options == "Doctors":
    st.header("Manage Doctors")
    doctor_df = fetch_data("Doctor")
    st.write(doctor_df)

    # Add button for visualizing Doctors by Organization
    if st.button("Show Doctors by Organization"):
        fig = visualize_statistics(doctor_df, 'Organization_ID', 'Doctors by Organization')
        st.pyplot(fig)

    # Add button for 3D pie chart
    if st.button("Show Doctors by Organization (3D Pie)"):
        pie_fig = visualize_3d_pie(doctor_df, 'Organization_ID', 'Doctors by Organization (3D Pie)')
        st.plotly_chart(pie_fig)

    # Add Doctor
    st.subheader("Add Doctor")
    with st.form("add_doctor_form"):
        doctor_name = st.text_input("Doctor Name")
        department_name = st.text_input("Department Name")
        organization_id = st.number_input("Organization ID", step=1)
        submit_doctor = st.form_submit_button("Add Doctor")
        if submit_doctor:
            query = '''INSERT INTO Doctor (Doctor_Name, Department_Name, Organization_ID) 
                       VALUES (?, ?, ?)'''
            execute_query(query, (doctor_name, department_name, organization_id))
            st.success("Doctor added successfully!")

# Donors section
elif options == "Donors":
    st.header("Manage Donors")
    donor_df = fetch_data("Donor")
    st.write(donor_df)

    # Add button for visualizing Organ Donated
    if st.button("Show Organ Donated"):
        fig = visualize_statistics(donor_df, 'Organ_donated', 'Organ Donated')
        st.pyplot(fig)

    # Add button for 3D pie chart of Organ Donated
    if st.button("Show Organ Donated (3D Pie)"):
        pie_fig = visualize_3d_pie(donor_df, 'Organ_donated', 'Organ Donated (3D Pie)')
        st.plotly_chart(pie_fig)

    # Add Donor
    st.subheader("Add Donor")
    with st.form("add_donor_form"):
        donor_id = st.text_input("Donor ID")
        organ_donated = st.text_input("Organ Donated")
        reason = st.text_area("Reason for Donation")
        org_id = st.number_input("Organization ID", step=1)
        user_id = st.number_input("User ID", step=1)
        submit_donor = st.form_submit_button("Add Donor")
        if submit_donor:
            query = '''INSERT INTO Donor (Donor_ID, Organ_donated, Reason_of_donation, Organization_ID, User_ID) 
                       VALUES (?, ?, ?, ?, ?)'''
            execute_query(query, (donor_id, organ_donated, reason, org_id, user_id))
            st.success("Donor added successfully!")

# Available Organs section
elif options == "Available Organs":
    st.header("Manage Available Organs")
    organ_df = fetch_data("Organ_available")
    st.write(organ_df)

    # Add Available Organ
    st.subheader("Add Available Organ")
    with st.form("add_organ_form"):
        organ_name = st.text_input("Organ Name")
        donor_id = st.number_input("Donor ID", step=1)
        submit_organ = st.form_submit_button("Add Organ")
        if submit_organ:
            query = '''INSERT INTO Organ_available (Organ_name, Donor_ID) 
                       VALUES (?, ?)'''
            execute_query(query, (organ_name, donor_id))
            st.success("Organ added successfully!")

# Organizations section
elif options == "Organizations":
    st.header("Manage Organizations")
    org_df = fetch_data("Organization")
    st.write(org_df)

    # Add buttons for visualizing Organization Location and Government Approval
    if st.button("Show Organizations by Location"):
        fig = visualize_statistics(org_df, 'Location', 'Organizations by Location')
        st.pyplot(fig)

    if st.button("Show Organizations by Government Approval"):
        fig = visualize_statistics(org_df, 'Government_approved', 'Organizations by Government Approval')
        st.pyplot(fig)

    # Add button for 3D pie chart of Government Approved
    if st.button("Show Organizations by Government Approval (3D Pie)"):
        pie_fig = visualize_3d_pie(org_df, 'Government_approved', 'Organizations by Government Approval (3D Pie)')
        st.plotly_chart(pie_fig)

    # Add Organization
    st.subheader("Add Organization")
    with st.form("add_organization_form"):
        org_name = st.text_input("Organization Name")
        location = st.text_input("Location")
        government_approved = st.number_input("Government Approved (1/0)", step=1)
        submit_org = st.form_submit_button("Add Organization")
        if submit_org:
            query = '''INSERT INTO Organization (Organization_name, Location, Government_approved) 
                       VALUES (?, ?, ?)'''
            execute_query(query, (org_name, location, government_approved))
            st.success("Organization added successfully!")

# Patients section
elif options == "Patients":
    st.header("Manage Patients")
    patient_df = fetch_data("Patient")
    st.write(patient_df)

    # Add button for visualizing Organ Required
    if st.button("Show Patients by Organ Required"):
        fig = visualize_statistics(patient_df, 'Organ_req', 'Patients by Organ Required')
        st.pyplot(fig)

    # Add button for 3D pie chart of Organ Required
    if st.button("Show Patients by Organ Required (3D Pie)"):
        pie_fig = visualize_3d_pie(patient_df, 'Organ_req', 'Patients by Organ Required (3D Pie)')
        st.plotly_chart(pie_fig)

    # Add Patient
    st.subheader("Add Patient")
    with st.form("add_patient_form"):
        patient_id = st.number_input("Patient ID", step=1)
        organ_req = st.text_input("Organ Required")
        reason_of_procurement = st.text_area("Reason of Procurement")
        doctor_id = st.number_input("Doctor ID", step=1)
        user_id = st.number_input("User ID", step=1)
        submit_patient = st.form_submit_button("Add Patient")
        if submit_patient:
            query = '''INSERT INTO Patient (Patient_ID, Organ_req, Reason_of_procurement, Doctor_ID, User_ID) 
                       VALUES (?, ?, ?, ?, ?)'''
            execute_query(query, (patient_id, organ_req, reason_of_procurement, doctor_id, user_id))
            st.success("Patient added successfully!")

# Transactions section
elif options == "Transactions":
    st.header("Manage Transactions")
    transaction_df = fetch_data("Transaction")
    st.write(transaction_df)

    # Add Transaction
    st.subheader("Add Transaction")
    with st.form("add_transaction_form"):
        patient_id = st.number_input("Patient ID", step=1)
        organ_id = st.number_input("Organ ID", step=1)
        donor_id = st.number_input("Donor ID", step=1)
        transaction_type = st.selectbox("Transaction Type", ["Donation", "Procurement"])
        submit_transaction = st.form_submit_button("Add Transaction")
        if submit_transaction:
            query = '''INSERT INTO Transaction (Patient_ID, Organ_ID, Donor_ID, Transaction_type) 
                       VALUES (?, ?, ?, ?)'''
            execute_query(query, (patient_id, organ_id, donor_id, transaction_type))
            st.success("Transaction added successfully!")

# Users section
elif options == "Users":
    st.header("Manage Users")
    user_df = fetch_data("User")
    st.write(user_df)

    # Create a container for visualizations
    st.subheader("User Statistics Visualizations")

    # Button to visualize Medical Insurance
    if st.button("Show Users by Medical Insurance"):
        fig_medical_insurance = visualize_statistics(user_df, 'Medical_insurance', 'Users by Medical Insurance')
        st.pyplot(fig_medical_insurance)

    # Button to visualize City
    if st.button("Show Users by City"):
        fig_city = visualize_statistics(user_df, 'City', 'Users by City')
        st.pyplot(fig_city)

    # Button to visualize State
    if st.button("Show Users by State"):
        fig_state = visualize_statistics(user_df, 'State', 'Users by State')
        st.pyplot(fig_state)

    # Add User
    st.subheader("Add User")
    with st.form("add_user_form"):
        name = st.text_input("Name")
        dob = st.date_input("Date of Birth")
        insurance = st.number_input("Medical Insurance", step=1)
        street = st.text_input("Street")
        city = st.text_input("City")
        state = st.text_input("State")
        submit_user = st.form_submit_button("Add User")
        if submit_user:
            query = '''INSERT INTO User (Name, Date_of_Birth, Medical_insurance, Street, City, State) 
                       VALUES (?, ?, ?, ?, ?, ?)'''
            execute_query(query, (name, dob, insurance, street, city, state))
            st.success("User added successfully!")
