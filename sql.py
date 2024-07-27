import sqlite3

def create_connection(db_file):
    """ Create a database connection to the SQLite database specified by db_file """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """ Create a table from the create_table_sql statement """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def insert_data(conn, insert_sql, data):
    """ Insert data into table """
    try:
        c = conn.cursor()
        c.executemany(insert_sql, data)
    except sqlite3.Error as e:
        print(e)

def main():
    database = "student.db"

    sql_create_student_table = """
    CREATE TABLE IF NOT EXISTS STUDENT (
        NAME VARCHAR(25),
        CLASS VARCHAR(25),
        BATCH VARCHAR(25),
        GRADE CHAR
    );
    """

    sql_create_teacher_table = """
    CREATE TABLE IF NOT EXISTS TEACHER (
        NAME VARCHAR(25),
        CLASS VARCHAR(25),
        BATCH VARCHAR(25),
        GRADE CHAR
    );
    """

    student_data = [
        ('Naman Mathur', 'Computer Science', 'B4', 'A'),
        ('Aryan Nagpal', 'Computer Science', 'B3', 'B'),
        ('Aditya Bhat', 'Computer Science', 'B4', 'A'),
        ('Anurag Joshi', 'IT', 'A2', 'B'),
        ('Lyoksh Mehta', 'IT', 'A1', 'A'),
        ('Nargis Rungta', 'IT', 'A1', 'A')
    ]

    teacher_data = [
        ('Alka Yadav', 'Computer Science', 'B4', 'NA'),
        ('Sambhav Misra', 'Computer Science', 'B3', 'NA'),
        ('Jamun Tiwari', 'IT', 'A1', 'NA'),
        ('Tribhuvan Singh', 'IT', 'A2', 'NA')
    ]

    sql_insert_student = '''INSERT INTO STUDENT(NAME, CLASS, BATCH, GRADE) VALUES (?, ?, ?, ?);'''
    sql_insert_teacher = '''INSERT INTO TEACHER(NAME, CLASS, BATCH, GRADE) VALUES (?, ?, ?, ?);'''

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_student_table)
        create_table(conn, sql_create_teacher_table)
        insert_data(conn, sql_insert_student, student_data)
        insert_data(conn, sql_insert_teacher, teacher_data)

        print("Inserted Records are as follows:")

        try:
            c = conn.cursor()
            c.execute("SELECT * FROM STUDENT")
            rows = c.fetchall()
            for row in rows:
                print(row)

            c.execute("SELECT * FROM TEACHER")
            rows = c.fetchall()
            for row in rows:
                print(row)

        except sqlite3.Error as e:
            print(e)

        conn.commit()
        conn.close()
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    main()
