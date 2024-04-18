import sqlite3

def create_tables(db_file):
    # Connect to the SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect(db_file)

    # Creates a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Defines the SQL statement to create HIRED_EMPLOYEES table
    create_hired_employees_sql_table = """
    CREATE TABLE IF NOT EXISTS HIRED_EMPLOYEES (
        Id INTEGER PRIMARY KEY,
        Name TEXT,
        Datetime TEXT,
        DepartmentId INTEGER,
        JobId INTEGER
    )
    """

    # Defines the SQL statement to create DEPARTMENTS table
    create_departments_sql_table = """
    CREATE TABLE IF NOT EXISTS DEPARTMENTS (
        Id INTEGER PRIMARY KEY,
        Department TEXT NOT NULL
    )
    """

    # Defines the SQL statement to create JOBS table
    create_jobs_sql_table = """
    CREATE TABLE IF NOT EXISTS JOBS (
        Id INTEGER PRIMARY KEY,
        Job TEXT NOT NULL
    )
    """

    # Executes the SQL statements to create the tables
    cursor.execute(create_hired_employees_sql_table)
    cursor.execute(create_departments_sql_table)
    cursor.execute(create_jobs_sql_table)

    # Close the connection
    conn.close()

    return(print(f'Tables created successfully into the database: {db_file}'))

if __name__ == '__main__':
    create_tables('target_database.db')