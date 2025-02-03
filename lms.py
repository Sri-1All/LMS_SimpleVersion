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
def add_book(title, author):
    cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
    conn.commit()
    print(f"Book '{title}' by {author} added successfully.")

def search_book(title):
    cursor.execute("SELECT * FROM books WHERE title LIKE ?", ("%" + title + "%",))
    books = cursor.fetchall()
    if books:
        for book in books:
            print(book)
    else:
        print("No books found.")

def add_borrower(name):
    cursor.execute("INSERT INTO borrowers (name) VALUES (?)", (name,))
    conn.commit()
    print(f"Borrower '{name}' added successfully.")

def issue_book(book_id, borrower_id, lend_date):
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

def return_book(book_id, return_date):
    cursor.execute("SELECT lending_id FROM lending WHERE book_id = ? AND return_date IS NULL", (book_id,))
    lending = cursor.fetchone()
    if lending:
        cursor.execute("UPDATE lending SET return_date = ? WHERE lending_id = ?", (return_date, lending[0]))
        cursor.execute("UPDATE books SET available = 1 WHERE book_id = ?", (book_id,))
        conn.commit()
        print("Book returned successfully.")
    else:
        print("No active lending record found for this book.")

# Sample usage
if __name__ == "__main__":
    add_book("Python Programming", "Guido van Rossum")
    add_borrower("Alice")
    issue_book(1, 1, "2025-02-03")
    return_book(1, "2025-02-10")

# Close connection
conn.close()
