# Library Catalog Management System
A Python-based Library Catalog Management System that uses
Object-Oriented Programming (OOP) concepts and a Tkinter graphical user
interface (GUI). The application allows users to manage a collection of
books, search the catalog, and track borrowing and return status.
--
Features
- Add books: Add Fiction, Non-Fiction, and Reference books.
- View catalog: Display all books in a tabular format.
- Search books: Search for books by title or author.
- Borrow books: Borrow books that are available.
- Return books: Update the status of borrowed books.
- Remove books: Remove a selected book from the catalog.
- View book details: Display complete information about a selected
  book.
- Availability filter: Display only books that are currently
  available.
- Dashboard summary: View the total number of books, available
  books, and borrowed books.
-- 
OOP Concepts Used
The project demonstrates the following Object-Oriented Programming
concepts:
1. Classes and Objects: The Book, LibraryCatalog, and derived
   book classes represent the main entities of the system.
2. Inheritance: FictionBook, NonFictionBook, and
   ReferenceBook inherit common attributes and methods from the
   Book class.
3. Polymorphism: The derived book classes override methods such as
   book_type() and display_details().
4. Encapsulation: Book information and catalog operations are
   organized within their respective classes.
Technologies Used
- Python 3
- Tkinter -- GUI development
- ttk -- Themed GUI widgets and tabular display
Tkinter and ttk are included with most standard Python installations.
Project Structure
Library-Catalog-System/
│
├── project.py    # Core OOP classes and library management operations
├── gui.py        # Tkinter graphical user interface
└── README.md     # Project documentation
Requirements
- Python 3.8 or later
- Tkinter support in the Python installation
No third-party Python packages are required.
How to Run
1. Clone the repository
git clone https://github.com/your-username/Library-Catalog-System.git
2. Open the project folder
cd Library-Catalog-System
3. Run the application
python gui.py
The Library Catalog Management System window will open.
Make sure project.py and gui.py are saved in the same directory
because the GUI imports the catalog classes and sample-data function
from project.py.

Sample Data
The application loads a few sample books when it starts:

  Book ID   Title                       Type
  1         Harry Potter                Fiction
2         Sapiens                     Non-Fiction
3         Oxford English Dictionary   Reference
4         The Da Vinci Code           Fiction

You can add more books through the GUI.
Book Types
- Fiction: Stores a sub-genre, such as Fantasy or Mystery.
- Non-Fiction: Stores a subject area, such as History or Science.
- Reference: Stores an edition and is restricted to in-library
  use. Reference books cannot be borrowed.
How to Use
1. Select a book type and enter the title, author, and additional
   information.
2. Click Add Book to add it to the catalog.
3. Select a book from the table to load its ID into the Book ID field.
4. Use Borrow Book, Return Book, Remove Book, or Show
   Details to manage the selected book.
5. Use the search field to find books by title or author.
6. Click Show All to display the complete catalog or Available
   Only to filter available books.
Limitations
- Book records are stored in memory and are reset when the application
  is closed.
- The application does not currently use a database or user login
  system.
- The sample books are loaded again each time the application starts.
Future Enhancements
- Integrate SQLite or MySQL for permanent data storage.
- Add user and librarian login functionality.
- Maintain borrowing dates and return deadlines.
- Add fine calculation for overdue books.
- Export catalog records to CSV or PDF.
Learning Outcomes
- Understanding and implementing OOP concepts in Python.
- Applying inheritance and polymorphism to represent different book
  categories.
- Developing a desktop GUI using Tkinter.
- Handling user input and GUI events.
- Implementing basic catalog operations such as adding, searching,
  borrowing, and returning books.
--
Author
Divya Rawat
--
This project was developed for academic purposes as a demonstration of
Python Object-Oriented Programming and Tkinter GUI development.
