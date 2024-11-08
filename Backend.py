import sqlite3

def initialize_db():
    conn = sqlite3.connect('DBMS.dbsqlite', check_same_thread=False)
    cursor = conn.cursor()

    # Create login table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS login (
            username TEXT NOT NULL,
            password TEXT NOT NULL
        );
    ''')

    # Insert default admin login
    cursor.execute("INSERT INTO login (username, password) VALUES ('admin', 'admin');")

    # Create User table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS User (
            User_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Date_of_Birth TEXT NOT NULL,
            Medical_insurance INTEGER,
            Medical_history TEXT,
            Street TEXT,
            City TEXT,
            State TEXT
        );
    ''')

    # Create User_phone_no table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS User_phone_no (
            User_ID INTEGER NOT NULL,
            phone_no TEXT,
            FOREIGN KEY(User_ID) REFERENCES User(User_ID) ON DELETE CASCADE
        );
    ''')

    # Create Organization table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Organization (
            Organization_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Organization_name TEXT NOT NULL,
            Location TEXT,
            Government_approved INTEGER
        );
    ''')

    # Create Doctor table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Doctor (
            Doctor_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Doctor_Name TEXT NOT NULL,
            Department_Name TEXT NOT NULL,
            Organization_ID INTEGER NOT NULL,
            FOREIGN KEY(Organization_ID) REFERENCES Organization(Organization_ID) ON DELETE CASCADE
        );
    ''')

    # Create Patient table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Patient (
            Patient_ID INTEGER NOT NULL,
            Organ_req TEXT NOT NULL,
            Reason_of_procurement TEXT,
            Doctor_ID INTEGER NOT NULL,
            User_ID INTEGER NOT NULL,
            PRIMARY KEY(Patient_ID, Organ_req),
            FOREIGN KEY(User_ID) REFERENCES User(User_ID) ON DELETE CASCADE,
            FOREIGN KEY(Doctor_ID) REFERENCES Doctor(Doctor_ID) ON DELETE CASCADE
        );
    ''')

    # Create Donor table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Donor (
            Donor_ID INTEGER NOT NULL,
            Organ_donated TEXT NOT NULL,
            Reason_of_donation TEXT,
            Organization_ID INTEGER NOT NULL,
            User_ID INTEGER NOT NULL,
            PRIMARY KEY(Donor_ID, Organ_donated),
            FOREIGN KEY(User_ID) REFERENCES User(User_ID) ON DELETE CASCADE,
            FOREIGN KEY(Organization_ID) REFERENCES Organization(Organization_ID) ON DELETE CASCADE
        );
    ''')

    # Create Organ_available table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Organ_available (
            Organ_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Organ_name TEXT NOT NULL,
            Donor_ID INTEGER NOT NULL,
            FOREIGN KEY(Donor_ID) REFERENCES Donor(Donor_ID) ON DELETE CASCADE
        );
    ''')

    # Create Transaction table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "Transaction" (
            Patient_ID INTEGER NOT NULL,
            Organ_ID INTEGER NOT NULL,
            Donor_ID INTEGER NOT NULL,
            Date_of_transaction TEXT NOT NULL,
            Status INTEGER NOT NULL,
            PRIMARY KEY(Patient_ID, Organ_ID),
            FOREIGN KEY(Patient_ID) REFERENCES Patient(Patient_ID) ON DELETE CASCADE,
            FOREIGN KEY(Donor_ID) REFERENCES Donor(Donor_ID) ON DELETE CASCADE
        );
    ''')


    # Create Organization_phone_no table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Organization_phone_no (
            Organization_ID INTEGER NOT NULL,
            Phone_no TEXT,
            FOREIGN KEY(Organization_ID) REFERENCES Organization(Organization_ID) ON DELETE CASCADE
        );
    ''')

    # Create Doctor_phone_no table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Doctor_phone_no (
            Doctor_ID INTEGER NOT NULL,
            Phone_no TEXT,
            FOREIGN KEY(Doctor_ID) REFERENCES Doctor(Doctor_ID) ON DELETE CASCADE
        );
    ''')

    # Create Organization_head table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Organization_head (
            Organization_ID INTEGER NOT NULL,
            Employee_ID INTEGER NOT NULL,
            Name TEXT NOT NULL,
            Date_of_joining TEXT NOT NULL,
            Term_length INTEGER NOT NULL,
            PRIMARY KEY(Organization_ID, Employee_ID),
            FOREIGN KEY(Organization_ID) REFERENCES Organization(Organization_ID) ON DELETE CASCADE
        );
    ''')

    # Create log table for triggers
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS log (
            querytime TEXT,
            comment TEXT
        );
    ''')

    # Commit changes and close connection
    conn.commit()
    conn.close()
    
def create_triggers():
    conn = sqlite3.connect('DBMS.dbsqlite', check_same_thread=False)
    cursor = conn.cursor()

    # Enable foreign keys in SQLite
    cursor.execute('PRAGMA foreign_keys = ON;')

    # Add Donor triggers
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS ADD_DONOR_LOG
        AFTER INSERT ON Donor
        BEGIN
            INSERT INTO log (querytime, comment)
            VALUES (datetime('now'), 'Inserted new Donor ' || NEW.Donor_ID);
        END;
    ''')

    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS UPD_DONOR_LOG
        AFTER UPDATE ON Donor
        BEGIN
            INSERT INTO log (querytime, comment)
            VALUES (datetime('now'), 'Updated Donor Details ' || NEW.Donor_ID);
        END;
    ''')

    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS DEL_DONOR_LOG
        AFTER DELETE ON Donor
        BEGIN
            INSERT INTO log (querytime, comment)
            VALUES (datetime('now'), 'Deleted Donor ' || OLD.Donor_ID);
        END;
    ''')

    # Add Patient triggers
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS ADD_PATIENT_LOG
        AFTER INSERT ON Patient
        BEGIN
            INSERT INTO log (querytime, comment)
            VALUES (datetime('now'), 'Inserted new Patient ' || NEW.Patient_ID);
        END;
    ''')

    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS UPD_PATIENT_LOG
        AFTER UPDATE ON Patient
        BEGIN
            INSERT INTO log (querytime, comment)
            VALUES (datetime('now'), 'Updated Patient Details ' || NEW.Patient_ID);
        END;
    ''')

    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS DEL_PATIENT_LOG
        AFTER DELETE ON Patient
        BEGIN
            INSERT INTO log (querytime, comment)
            VALUES (datetime('now'), 'Deleted Patient ' || OLD.Patient_ID);
        END;
    ''')

    # Add Transaction trigger
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS ADD_TRANSACTION_LOG
        AFTER INSERT ON "Transaction"
        BEGIN
            INSERT INTO log (querytime, comment)
            VALUES (datetime('now'), 'Added Transaction :: Patient ID: ' || NEW.Patient_ID || ' Donor ID: ' || NEW.Donor_ID);
        END;
    ''')

    conn.commit()
    conn.close()


# Initialize the database
initialize_db()
create_triggers()