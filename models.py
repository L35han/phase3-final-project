import sqlite3
from sqlite3 import Error

def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect('employees.db')
    except Error as e:
        print(e)
    return conn

def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS workers (
                            id INTEGER PRIMARY KEY,
                            name VARCHAR(50)NOT NULL,
                            age INTEGER NOT NULL,
                            email VARCHAR(40) NOT NULL);''')
    except Error as e:
        print(e)

def Worker():
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value) < 1:
            raise ValueError("Name must be a non-empty string.")
        self._name = value

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if not isinstance(value, int) or value < 1:
            raise ValueError("Age must be a positive integer.")
        self._age = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not isinstance(value, str) or len(value) < 1:
            raise ValueError("Email must be a non-empty string.")
        self._email = value

    def save_to_db(self, conn):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO workers (name, age, email) VALUES (?, ?, ?)", (self.name, self.age, self.email))
        conn.commit()
        self.id = cursor.lastrowid

    @classmethod
    def get_all(cls, conn):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM workers")
        rows = cursor.fetchall()
        return [cls(*row) for row in rows]

    @classmethod
    def find_by_id(cls, conn, worker_id):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM workers WHERE id=?", (worker_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        else:
            return cls(*row)

    @classmethod
    def find_by_name(cls, conn, name):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM workers WHERE name=?", (name,))
        row = cursor.fetchone()
        if row is None:
            return None
        else:
            return cls(*row)

def main():
    conn = create_connection()
    if conn is not None:
        create_table(conn)
        while True:
            print("1. Add worker")
            print("2. Delete worker")
            print("3. List workers")
            print("4. View worker")
            print("5. Find worker by name")
            print("6. Exit")
            choice = int(input("Enter your choice: "))
            if choice == 1:
                name = input("Enter worker name: ")
                age = int(input("Enter worker age: "))
                email = input("Enter worker email: ")
                worker = Worker(name, age, email)
                worker.save_to_db(conn)
            elif choice == 2:
                worker_id = int(input("Enter worker ID: "))
                worker = Worker.find_by_id(conn, worker_id)
                if worker is not None:
                    worker.delete_from_db(conn)
            elif choice == 3:
                workers = Worker.get_all(conn)
                for worker in workers:
                    print(worker)
            elif choice == 4:
                worker_id = int(input("Enter worker ID: "))
                worker = Worker.find_by_id(conn, worker_id)
                if worker is not None:
                    print(worker)
            elif choice == 5:
                name = input("Enter worker name: ")
                worker = Worker.find_by_name(conn, name)
                if worker is not None:
                    print(worker)
            elif choice == 6:
                break
            else:
                print("Invalid choice.")
                