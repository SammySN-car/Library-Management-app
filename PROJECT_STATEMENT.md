# Modern Application Development II
## Project Statement

# Library Management System - V2

It is a multi-user app (one requires an administrator and other users) that manages a library's book catalog, member registrations, borrowing/returning of books, and fine management.

---

## Frameworks to be used

These are the mandatory frameworks on which the project has to be built.

- **Flask** for API
- **VueJS** for UI
- **VueJS Advanced with CLI** (only if required, not necessary)
- **Jinja2 templates** if using CDN only for entry point (Not to be used for UI)
- **Bootstrap** for HTML generation and styling (No other CSS framework is allowed)
- **SQLite** for database (No other database is permitted)
- **Redis** for caching
- **Redis and Celery** for batch jobs

> **Note:** All demos should be possible on your local machine.

---

## Roles

The platform will have two roles:

### Admin - root access - It is the superuser of the app and requires no registration

- Admin is also known as the superuser
- There can be only one admin for the app
- Admin can manage the book catalog (add/edit/delete books)
- Each book has details like title, author, ISBN, genre, total copies, and available copies
- Admin can view all registered members and block/unblock them
- Admin can issue books to members and process returns
- Admin can view overdue books and fine details
- Admin can view summary charts on the dashboard (popular books, category-wise distribution, fine collection)

### User - Can borrow books from the library

- Register/Login
- Search the book catalog by title, author, or genre
- Borrow an available book (if copies are available)
- Return a borrowed book
- View borrowing history and pending fines

---

## Terminologies

**User:** The user will register/login and borrow books from the library.

**Admin:** The superuser with full control over the catalog, members, and operations. No registration is required, i.e. the admin should exist whenever the database is created.

**Book:** A physical book in the library catalog. The book may contain the following attributes:

- `id` - primary key
- `title`
- `author`
- `isbn` - unique
- `genre`
- `total_copies`
- `available_copies`
- `price`
- `created_at`
- etc: Additional fields (if any)

**Borrow Record:** Tracks the borrowing and returning of books. The borrow record may contain the following attributes:

- `id` - primary key
- `book_id` (foreign key - book)
- `user_id` (foreign key - users)
- `issue_date`
- `due_date`
- `return_date`
- `fine_amount`
- `status` (issued/returned/overdue)
- etc: Additional fields (if any)

> **Note:** The above tables and fields are not exhaustive, students can add more tables and fields as per their requirements.

---

## Similar apps
- https://openlibrary.org/

---

## Application Wireframe

Library Management System

*(See wireframe image: `Library Management System.png`)*

> **Note:**
> The provided wireframe is intended only to illustrate the application's flow and demonstrate what should appear when a user navigates between pages.
> Replication of the exact views is NOT mandatory.
> Students are encouraged to work on their front-end ideas and designs while maintaining the application's intended functionality and flow.

---

## Core Functionalities

### 1. Admin login and User login

- A login/register form with fields like username, password etc. for the user and a login form for the admin
- The application should have only one admin identified by its role
- You can either use Flask security (session or token) or JWT based Token based authentication to implement role-based access control
- The app must have a suitable model to store and differentiate all types of users

### 2. Admin Dashboard - for the Admin

- The admin should be added, whenever a new database is created.
- The admin creates/edits/deletes books in the catalog. **Note:** Delete only if no active borrows exist for the book.
- The admin can view the availability status of each book and check who has borrowed it if it's currently issued.
- The admin can issue books to users by entering the book ID and member ID, with the due date auto-calculated (e.g., 14 days from issue).
- The admin can process book returns and auto-calculate fines for overdue books ($1 per day overdue).
- The admin can view all registered users and block/unblock them.
- The admin can view the summary charts of books/categories/fines.

### 3. User Dashboard - for the User

- The user can search the catalog by title, author, or genre to find available books.
- The user can request to borrow an available book. **Note:** The system auto-decrements available copies.
- The user can return a borrowed book, and the system auto-increments available copies and calculates any applicable fine.
- The timestamp is recorded between issue date and return date.
- Shows the summary charts on his/her borrowing history.

> **Note:** The database must be created programmatically (via table creation or model code) or through shell. Manual database creation, such as using DB Browser for SQLite, is NOT allowed.

---

### 4. Backend Jobs

#### a. Scheduled Job - Daily reminders
The application should send daily reminders to users on g-chat using Google Chat Webhooks or SMS or mail.

- Check if a user has books overdue or hasn't visited the library recently
- If yes, then send the alert reminding them to return overdue books or discover new titles
- The reminder can be sent in the evening, every day (students can choose the time)

#### b. Scheduled Job - Monthly Activity Report
Devise a monthly report for the user created using HTML and sent via mail.

- The activity report can include books borrowed per month, most borrowed genre, total fines paid, reading streak, or any relevant information to the user etc.
- For the monthly report to be sent, start a job on the first day of every month → create a report using the above parameters → send it as an email

#### c. User Triggered Async Job - Export as CSV
Devise a CSV format details for the borrowing history of the user till date.

- This export is meant to download the borrowing details (record_id, book_title, issue_date, due_date, return_date, fine_amount, status etc.)
- Have a dashboard from where the user can trigger the export
- This should trigger a batch job, and send an alert once done

---

### 5. Performance and Caching

- Add caching where required to increase the performance
- Add cache expiry
- API Performance

---

## Recommended and/or Optional functionalities

- Well-designed PDF reports for Monthly activity reports (Students can choose between HTML and PDF reports)
- External APIs/libraries for creating charts, e.g. ChartJS
- Single Responsive UI for both Mobile and Desktop
- Unified UI that works across devices
- Add to desktop feature
- Implementing frontend validation on all the form fields using HTML5 form validation or JavaScript
- Implementing backend validation within your APIs
- Provide styling and aesthetics to your application by creating a beautiful and responsive front end using simple CSS or Bootstrap
- Incorporate a proper login system to prevent unauthorized access to the app using Flask extensions like flask_login, flask_security etc.
- Book recommendation system based on borrowing history
- Any additional feature you feel is appropriate for the application.

---

## Evaluation

Students have to create and submit a project report (not more than 5 pages) on the portal, along with the actual project submission.

The report must include the following things:
- Student details
- Project details, including the question statement and how you approached the problem statement
- Frameworks and libraries used
- ER diagram of your database, including all the tables and their relations
- API resource endpoints (if any)
- Drive link of the presentation video
- If a student has used any form of AI/LLM for the project, you will need to mention the extent of use in your report

---

## Possible folder structure:

```
library-management/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── resources/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── book.py
│   │       ├── borrow.py
│   │       ├── member.py
│   │       └── report.py
│   ├── celery_tasks.py
│   ├── config.py
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── App.vue
│       ├── main.js
│       ├── router.js
│       ├── style.css
│       ├── api/
│       │   ├── auth.js
│       │   └── client.js
│       ├── components/
│       │   ├── AdminBooks.vue
│       │   ├── AdminDesk.vue
│       │   ├── AdminMembers.vue
│       │   ├── AdminReports.vue
│       │   ├── UserMyBooks.vue
│       │   └── UserSearch.vue
│       └── views/
│           ├── AdminDashboard.vue
│           ├── Login.vue
│           ├── Signup.vue
│           └── UserDashboard.vue
```

---

## Video Presentation Guidelines (Advised):

1. A short Intro (not more than 30 sec)
2. How did you approach the problem statement? (30 sec)
3. Highlight key features of the application (90 sec)
4. Any Additional feature(s) implemented other than core requirements (30 sec)

> **Note:**
> 1. The final video must not exceed 5-10 minutes.
> 2. Keeping your video feed on during recording (like in a screencast) is optional but recommended.
