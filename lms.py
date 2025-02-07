import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    available INTEGER DEFAULT 1
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS borrowers (
    borrower_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS lending (
    lending_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    borrower_id INTEGER,
    lend_date TEXT,
    return_date TEXT,
    FOREIGN KEY (book_id) REFERENCES books (book_id),
    FOREIGN KEY (borrower_id) REFERENCES borrowers (borrower_id)
)
""")

conn.commit()

# Functions for library management
def view_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    if books:
        for book in books:
            print(book)
    else:
        print("No books available.")

def add_book():
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
    conn.commit()
    print(f"Book '{title}' by {author} added successfully.")

def add_borrower():
    name = input("Enter borrower name: ")
    cursor.execute("INSERT INTO borrowers (name) VALUES (?)", (name,))
    conn.commit()
    print(f"Borrower '{name}' added successfully.")

def issue_book():
    book_id = int(input("Enter book ID: "))
    borrower_id = int(input("Enter borrower ID: "))
    lend_date = input("Enter lending date (YYYY-MM-DD): ")
    cursor.execute("SELECT available FROM books WHERE book_id = ?", (book_id,))
    book = cursor.fetchone()
    if book and book[0] == 1:
        cursor.execute("INSERT INTO lending (book_id, borrower_id, lend_date) VALUES (?, ?, ?)",
                       (book_id, borrower_id, lend_date))
        cursor.execute("UPDATE books SET available = 0 WHERE book_id = ?", (book_id,))
        conn.commit()
        print("Book issued successfully.")
    else:
        print("Book not available.")

def return_book():
    book_id = int(input("Enter book ID: "))
    return_date = input("Enter return date (YYYY-MM-DD): ")
    cursor.execute("SELECT lending_id FROM lending WHERE book_id = ? AND return_date IS NULL", (book_id,))
    lending = cursor.fetchone()
    if lending:
        cursor.execute("UPDATE lending SET return_date = ? WHERE lending_id = ?", (return_date, lending[0]))
        cursor.execute("UPDATE books SET available = 1 WHERE book_id = ?", (book_id,))
        conn.commit()
        print("Book returned successfully.")
    else:
        print("No active lending record found for this book.")

def main():
    while True:
        print("\nLibrary Management System")
        print("1. View Books")
        print("2. Add Book")
        print("3. Add Borrower")
        print("4. Issue Book")
        print("5. Return Book")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            view_books()
        elif choice == "2":
            add_book()
        elif choice == "3":
            add_borrower()
        elif choice == "4":
            issue_book()
        elif choice == "5":
            return_book()
        elif choice == "6":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
    conn.close()
