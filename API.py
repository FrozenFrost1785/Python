from flask import Flask, request, jsonify
import sqlite3
import hashlib
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def get_db_connection():
    conn = sqlite3.connect('DBMS.dbsqlite', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    insurance = data.get('insurance')
    street = data.get('street')
    city = data.get('city')
    state = data.get('state')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    hashed_password = hash_password(password)
    
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Insert into the login table
        cursor.execute("INSERT INTO login (username, password) VALUES (?, ?)", (username, hashed_password))

        # Insert into the User table
        cursor.execute('''
            INSERT INTO User (Name, Date_of_Birth, Medical_insurance, Street, City, State)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, password, insurance, street, city, state))

        conn.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 409
    finally:
        conn.close()


@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    hashed_password = hash_password(password)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM login WHERE username = ? AND password = ?", (username, hashed_password))
    user = cursor.fetchone()
    
    conn.close()
    
    if user:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User")
    users = cursor.fetchall()
    conn.close()
    return jsonify([dict(user) for user in users])

@app.route('/api/organizations', methods=['GET'])
def get_organizations():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Organization")
    organizations = cursor.fetchall()
    conn.close()
    return jsonify([dict(org) for org in organizations])

@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Doctor")
    doctors = cursor.fetchall()
    conn.close()
    return jsonify([dict(doctor) for doctor in doctors])

@app.route('/api/patients', methods=['GET'])
def get_patients():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Patient")
    patients = cursor.fetchall()
    conn.close()
    return jsonify([dict(patient) for patient in patients])

@app.route('/api/donors', methods=['GET'])
def get_donors():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Donor")
    donors = cursor.fetchall()
    conn.close()
    return jsonify([dict(donor) for donor in donors])

@app.route('/api/organs', methods=['GET'])
def get_organs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Organ_available")
    organs = cursor.fetchall()
    conn.close()
    return jsonify([dict(organ) for organ in organs])

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM 'Transaction'")
    transactions = cursor.fetchall()
    conn.close()
    return jsonify([dict(transaction) for transaction in transactions])

@app.route('/api/organs', methods=['GET'])
def search_organs():
    Organ = request.args.get('organ')  # Get organ type from the query string
    print(Organ)
    if not Organ:
        return jsonify({"error": "Organ type not provided"}), 400

    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # SQL query to fetch organs by type
        query = "SELECT Organ_ID, Organ_name, Donor_ID FROM Organ_available WHERE Organ_name = ?"
        cursor.execute(query, Organ)
        organs = cursor.fetchall()
        # Check if any organs are found
        if organs:
            organs_list = []
            for organ in organs:
                organs_list.append
                ({
                    "id": organ[0],
                    "organ_type": organ[1],
                    "donor_id": organ[2],
                    # Add other fields if necessary
                })
            return jsonify(organs_list)
        else:
            return jsonify({"message": "No organs available for the selected type."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
    return jsonify(availability)

@app.route('/api/donors/register', methods=['POST'])
def register_donor():
    data = request.json
    
    # Extracting data from the request
    user_id = data.get('user_id')
    donor_id = data.get('donor_id')
    organization_id = data.get('organization_id')
    organ_donated = data.get('organ_donated')
    reason_of_donation = data.get('reason_of_donation')

    # Validate required fields
    if not user_id or not donor_id or not organization_id or not organ_donated or not reason_of_donation:
        return jsonify({"error": "All fields are required"}), 400

    # Connecting to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Insert into the Donor table
        cursor.execute('''
            INSERT INTO Donor (Donor_ID, Organ_donated, Reason_of_donation, Organization_ID, User_ID)
            VALUES (?, ?, ?, ?, ?)
        ''', (donor_id, organ_donated, reason_of_donation, organization_id, user_id))

        conn.commit()
        return jsonify({"message": "Donor registered successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Donor ID already exists or other integrity issue"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# Function to get user stats by user_id
@app.route('/api/user/stats', methods=['GET'])
def get_user_stats():
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({"error": "User ID is required."}), 400

    try:
        # Connect to your SQLite database
        conn = sqlite3.connect('your_database.db')  # Update this line with your database name
        cursor = conn.cursor()
        
        # Fetch user details from the User table
        cursor.execute("SELECT * FROM User WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        
        # Check if the user exists
        if user:
            user_data = {
                "user_id": user[0],
                "name": user[1],        # Assuming column 1 is name
                "dob": user[2],         # Assuming column 2 is date of birth
                "medical_insurance": user[3],
                "medical_history": user[4] ,
                "street": user[5] ,
                "city": user[6],
                "state" : user[7],# Assuming column 3 is email
                # Add other user attributes here as needed
            }
            return jsonify({"user": user_data}), 200
        else:
            return jsonify({"error": "User not found."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
