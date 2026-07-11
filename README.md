# Library Management System

A premium full-stack web application designed for digital library cataloging and book issuing. Built using a light academic ivory and gold theme, this system provides role-based access for librarians (admins) and members (users) to perform cataloging, search, track issuance status, and export reports.

---

## Features

### 1. User Roles & Authentication
*   **Librarian (Admin)**: Pre-seeded in the database (`admin` / password: `admin`). Manages the catalog, issues/returns books, and tracks active readers.
*   **Member (User)**: Register via signup. Allows search and discovery of books, viewing currently issued items, and downloading personal reading history.
*   **JWT Security**: Secure endpoints using Flask-JWT-Extended token headers.

### 2. Catalog Management (Admin)
*   **CRUD Operations**: Full create, read, update, and delete access for books.
*   **Stock Tracking**: Automatic tracking of copies available in real time.

### 3. Issue & Return Desk (Admin)
*   **Interactive Controls**: Easy issuance of books to specific user IDs, and handling returns or cancellations with a single click.

### 4. Reading Feed (User)
*   **Book Search**: Dynamically search library items by title, author, or genre.
*   **Reading Log**: Review currently borrowed books, return dates, and history.

### 5. Async Backend Jobs & Analytics
*   **Reports**: Clean Chart.js visualization of popular genres, active members, and overall book count stats.
*   **CSV Exports**: User-triggered background job that processes reading history to CSV and lets users download it.

---

## Tech Stack
*   **Backend**: Flask, Flask-SQLAlchemy, Flask-RESTful, Flask-JWT-Extended
*   **Frontend**: Vue 3 (Composition API), Axios, Bootstrap 5 (CDN), Chart.js
*   **Database**: SQLite

---

## Installation & Setup

### 1. Backend Setup
1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```
2.  Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Start the Flask server:
    ```bash
    python -m backend.run
    ```
    *The server runs at `http://localhost:5000` and automatically initializes the SQLite database with the default Librarian account.*

### 2. Frontend Setup
1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2.  Install Node dependencies:
    ```bash
    npm install
    ```
3.  Start the Vite dev server:
    ```bash
    npm run dev
    ```
    *The frontend will run at `http://localhost:5173`.*

---

## API Documentation

### Authentication
*   `POST /register` - Registers a new user.
*   `POST /login` - Log in and receive a JWT access token, user role, and ID.

### Admin Catalog & Issue Controls
*   `GET /admin/home` - Retrieve all books and inventory count.
*   `POST /admin/add_lot` - Create a new book item.
*   `PUT /admin/edit_lot/<id>` - Modify book details.
*   `DELETE /admin/delete_lot/<id>` - Remove book from catalog.
*   `POST /user/book/<id>` - Issue book to a member.
*   `PUT /user/release/<id>` - Return book / close issue log.

### User Dashboard & Reports
*   `GET /books` - Search and list available books.
*   `GET /user/home` - Retrieve user's active/past issued books.
*   `GET /admin/summary` - Admin analytics data.
*   `GET /user/export_csv` - Trigger Celery job for exporting CSV.
*   `GET /user/export_csv/<file_name>` - Download completed CSV export.
