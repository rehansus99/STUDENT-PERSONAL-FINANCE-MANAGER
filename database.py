"""
=============================================================================
STUDENT PERSONAL FINANCE MANAGER - DATABASE MODULE
=============================================================================
Course: Computational Thinking and Programming (2026CSAE100)
Bennett University
Author / Lead: Arpeet Chahal (S26CSEU0929) - Database / Backend
Integrated with: Rehan Hussain (Frontend) & Mohammad Huzaif (Logic)

Core Responsibilities:
1. Database Connection Management (MySQL + Automatic SQLite Fallback)
2. Safe Transaction Execution with Commit and Rollback
3. Parameterized SQL Queries to eliminate SQL Injection risks
4. Complete CRUD (Create, Read, Update, Delete) operations
5. Table initialization, indexing, and seed data deployment
=============================================================================
"""

import os
import sqlite3
from contextlib import contextmanager
from typing import List, Dict, Optional, Any, Tuple

# Optional MySQL support via mysql-connector-python
try:
    import mysql.connector
    from mysql.connector import Error as MySQLError
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False
    MySQLError = Exception


class DatabaseManager:
    """
    Enterprise-grade Database Access Layer developed by Arpeet Chahal.
    Features dual-backend support:
    - Primary: MySQL Server
    - Automatic Fallback: Embedded SQLite3 (Zero-setup viva mode)
    """

    def __init__(self, use_mysql: bool = False,
                 host: str = "localhost",
                 user: str = "root",
                 password: str = "password",
                 database: str = "student_finance_db"):
        self.use_mysql = use_mysql and MYSQL_AVAILABLE
        self.db_config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database
        }
        self.sqlite_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "student_finance.db")
        self.db_type = "MySQL" if self.use_mysql else "SQLite"
        self._init_connection()

    def _init_connection(self):
        """Attempts connection to MySQL server, falls back to SQLite if unreachable."""
        if self.use_mysql:
            try:
                conn = mysql.connector.connect(**self.db_config)
                conn.close()
                self.db_type = "MySQL"
                print(f"[DB - Arpeet] Connected successfully to MySQL Server ({self.db_config['database']})")
                return
            except Exception as err:
                print(f"[DB - Arpeet] MySQL connection notice: {err}")
                print(f"[DB - Arpeet] Automatically activating local SQLite database fallback.")
                self.use_mysql = False

        self.db_type = "SQLite"
        print(f"[DB - Arpeet] Active database engine: SQLite ({os.path.basename(self.sqlite_file)})")

    def get_raw_connection(self):
        """Returns a raw connection instance."""
        if self.use_mysql:
            return mysql.connector.connect(**self.db_config)
        else:
            conn = sqlite3.connect(self.sqlite_file)
            conn.row_factory = sqlite3.Row  # Dict-like column access
            return conn

    @contextmanager
    def get_cursor(self):
        """
        Context Manager for safe database transactions.
        Guarantees auto-commit on success, auto-rollback on error, and cursor closure.
        """
        conn = self.get_raw_connection()
        cursor = conn.cursor()
        try:
            yield conn, cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"[DB Error] Transaction rolled back due to error: {e}")
            raise e
        finally:
            cursor.close()
            conn.close()

    def get_placeholder(self) -> str:
        """Returns parameter placeholder based on active engine (%s for MySQL, ? for SQLite)."""
        return "%s" if self.use_mysql else "?"

    # -------------------------------------------------------------------------
    # TABLE INITIALIZATION & SEEDING (DDL & DML)
    # -------------------------------------------------------------------------
    def initialize_tables(self):
        """Creates tables with primary keys, foreign keys, and indexes."""
        with self.get_cursor() as (conn, cursor):
            if self.use_mysql:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS students (
                        student_id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        monthly_budget DECIMAL(10, 2) NOT NULL DEFAULT 10000.00,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS expenses (
                        expense_id INT AUTO_INCREMENT PRIMARY KEY,
                        student_id INT NOT NULL,
                        expense_date DATE NOT NULL,
                        category VARCHAR(50) NOT NULL,
                        amount DECIMAL(10, 2) NOT NULL,
                        description VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
                        INDEX idx_date (expense_date),
                        INDEX idx_cat (category)
                    );
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS savings_goals (
                        goal_id INT AUTO_INCREMENT PRIMARY KEY,
                        student_id INT NOT NULL,
                        goal_name VARCHAR(100) NOT NULL,
                        target_amount DECIMAL(10, 2) NOT NULL,
                        current_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
                    );
                """)
            else:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS students (
                        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        monthly_budget REAL NOT NULL DEFAULT 10000.00,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS expenses (
                        expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        student_id INTEGER NOT NULL,
                        expense_date TEXT NOT NULL,
                        category TEXT NOT NULL,
                        amount REAL NOT NULL,
                        description TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
                    );
                """)
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_exp_date ON expenses(expense_date);
                """)
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_exp_cat ON expenses(category);
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS savings_goals (
                        goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        student_id INTEGER NOT NULL,
                        goal_name TEXT NOT NULL,
                        target_amount REAL NOT NULL,
                        current_amount REAL NOT NULL DEFAULT 0.00,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
                    );
                """)

            # Seed initial records if empty
            cursor.execute("SELECT COUNT(*) FROM students")
            row = cursor.fetchone()
            count = row[0] if row else 0

            if count == 0:
                p = self.get_placeholder()
                cursor.execute(f"INSERT INTO students (student_id, name, monthly_budget) VALUES ({p}, {p}, {p})",
                               (1, "Rehan Hussain", 10000.00))

                sample_expenses = [
                    (1, "2026-10-01", "Food", 250.00, "Lunch at cafeteria"),
                    (1, "2026-10-02", "Transport", 80.00, "Metro card recharge"),
                    (1, "2026-10-04", "Education", 1200.00, "Python Programming textbook"),
                    (1, "2026-10-06", "Food", 450.00, "Weekend dinner with friends"),
                    (1, "2026-10-08", "Entertainment", 500.00, "Cinema ticket and popcorn"),
                    (1, "2026-10-10", "Hostel", 650.00, "Hostel room essentials & laundry"),
                    (1, "2026-10-12", "Shopping", 850.00, "Notebooks and stationary set"),
                    (1, "2026-10-13", "Food", 180.00, "Evening snacks & coffee")
                ]
                exp_placeholders = f"{p}, {p}, {p}, {p}, {p}"
                cursor.executemany(
                    f"INSERT INTO expenses (student_id, expense_date, category, amount, description) VALUES ({exp_placeholders})",
                    sample_expenses
                )

                sample_goals = [
                    (1, "New Headphones", 4000.00, 1800.00),
                    (1, "Semester Travel Fund", 8000.00, 2500.00)
                ]
                goal_placeholders = f"{p}, {p}, {p}, {p}"
                cursor.executemany(
                    f"INSERT INTO savings_goals (student_id, goal_name, target_amount, current_amount) VALUES ({goal_placeholders})",
                    sample_goals
                )
                print("[DB - Arpeet] Successfully seeded database with initial student profile and transactions.")

    # -------------------------------------------------------------------------
    # STUDENT PROFILE OPERATIONS
    # -------------------------------------------------------------------------
    def get_student_profile(self, student_id: int = 1) -> Dict[str, Any]:
        """Fetches student profile and monthly budget."""
        p = self.get_placeholder()
        with self.get_cursor() as (conn, cursor):
            cursor.execute(f"SELECT student_id, name, monthly_budget FROM students WHERE student_id = {p}", (student_id,))
            row = cursor.fetchone()
            if row:
                if self.use_mysql:
                    return {"student_id": row[0], "name": row[1], "monthly_budget": float(row[2])}
                return {"student_id": row["student_id"], "name": row["name"], "monthly_budget": float(row["monthly_budget"])}
            return {"student_id": student_id, "name": "Student", "monthly_budget": 10000.00}

    def update_student_profile(self, student_id: int, name: str, monthly_budget: float) -> bool:
        """Updates student name and monthly budget."""
        p = self.get_placeholder()
        with self.get_cursor() as (conn, cursor):
            cursor.execute(
                f"UPDATE students SET name = {p}, monthly_budget = {p} WHERE student_id = {p}",
                (name, monthly_budget, student_id)
            )
            return True

    # -------------------------------------------------------------------------
    # EXPENSES CRUD (Arpeet Chahal)
    # -------------------------------------------------------------------------
    def add_expense(self, student_id: int, expense_date: str, category: str, amount: float, description: str) -> int:
        """
        Inserts a new expense transaction.
        Returns the newly created primary key ID.
        """
        p = self.get_placeholder()
        with self.get_cursor() as (conn, cursor):
            cursor.execute(
                f"INSERT INTO expenses (student_id, expense_date, category, amount, description) VALUES ({p}, {p}, {p}, {p}, {p})",
                (student_id, expense_date, category, amount, description)
            )
            return cursor.lastrowid

    def get_all_expenses(self, student_id: int = 1) -> List[Dict[str, Any]]:
        """
        Retrieves all expenses for a given student ordered chronologically (newest first).
        """
        p = self.get_placeholder()
        with self.get_cursor() as (conn, cursor):
            cursor.execute(
                f"SELECT expense_id, student_id, expense_date, category, amount, description FROM expenses WHERE student_id = {p} ORDER BY expense_date DESC, expense_id DESC",
                (student_id,)
            )
            rows = cursor.fetchall()
            results = []
            for r in rows:
                if self.use_mysql:
                    results.append({
                        "expense_id": r[0],
                        "student_id": r[1],
                        "expense_date": str(r[2]),
                        "category": r[3],
                        "amount": float(r[4]),
                        "description": r[5] or ""
                    })
                else:
                    results.append({
                        "expense_id": r["expense_id"],
                        "student_id": r["student_id"],
                        "expense_date": str(r["expense_date"]),
                        "category": r["category"],
                        "amount": float(r["amount"]),
                        "description": r["description"] or ""
                    })
            return results

    def get_expense_by_id(self, expense_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves a single expense record by primary key."""
        p = self.get_placeholder()
        with self.get_cursor() as (conn, cursor):
            cursor.execute(
                f"SELECT expense_id, student_id, expense_date, category, amount, description FROM expenses WHERE expense_id = {p}",
                (expense_id,)
            )
            row = cursor.fetchone()
            if not row:
                return None
            if self.use_mysql:
                return {
                    "expense_id": row[0],
                    "student_id": row[1],
                    "expense_date": str(row[2]),
                    "category": row[3],
                    "amount": float(row[4]),
                    "description": row[5]
                }
            return {
                "expense_id": row["expense_id"],
                "student_id": row["student_id"],
                "expense_date": str(row["expense_date"]),
                "category": row["category"],
                "amount": float(row["amount"]),
                "description": row["description"]
            }

    def update_expense(self, expense_id: int, expense_date: str, category: str, amount: float, description: str) -> bool:
        """Updates an existing expense record."""
        p = self.get_placeholder()
        with self.get_cursor() as (conn, cursor):
            cursor.execute(
                f"UPDATE expenses SET expense_date = {p}, category = {p}, amount = {p}, description = {p} WHERE expense_id = {p}",
                (expense_date, category, amount, description, expense_id)
            )
            return True

    def delete_expense(self, expense_id: int) -> bool:
        """Deletes an expense record by its primary key ID."""
        p = self.get_placeholder()
        with self.get_cursor() as (conn, cursor):
            cursor.execute(f"DELETE FROM expenses WHERE expense_id = {p}", (expense_id,))
            return True

    def get_expenses_by_date_range(self, student_id: int, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Filters expenses within a specific date range."""
        p = self.get_placeholder()
        with self.get_cursor() as (conn, cursor):
            cursor.execute(
                f"SELECT expense_id, student_id, expense_date, category, amount, description FROM expenses WHERE student_id = {p} AND expense_date BETWEEN {p} AND {p} ORDER BY expense_date ASC",
                (student_id, start_date, end_date)
            )
            rows = cursor.fetchall()
            results = []
            for r in rows:
                if self.use_mysql:
                    results.append({"expense_id": r[0], "student_id": r[1], "expense_date": str(r[2]), "category": r[3], "amount": float(r[4]), "description": r[5]})
                else:
                    results.append({"expense_id": r["expense_id"], "student_id": r["student_id"], "expense_date": str(r["expense_date"]), "category": r["category"], "amount": float(r["amount"]), "description": r["description"]})
            return results

    def get_category_totals_sql(self, student_id: int = 1) -> Dict[str, float]:
        """Calculates category sums directly using SQL GROUP BY aggregation."""
        p = self.get_placeholder()
        with self.get_cursor() as (conn, cursor):
            cursor.execute(
                f"SELECT category, SUM(amount) FROM expenses WHERE student_id = {p} GROUP BY category ORDER BY SUM(amount) DESC",
                (student_id,)
            )
            rows = cursor.fetchall()
            totals = {}
            for r in rows:
                cat = r[0]
                total = float(r[1])
                totals[cat] = total
            return totals

    # -------------------------------------------------------------------------
    # SAVINGS GOALS CRUD (Arpeet Chahal)
    # -------------------------------------------------------------------------
    def get_savings_goals(self, student_id: int = 1) -> List[Dict[str, Any]]:
        """Retrieves all savings goals for the student."""
        p = self.get_placeholder()
        with self.get_cursor() as (conn, cursor):
            cursor.execute(
                f"SELECT goal_id, student_id, goal_name, target_amount, current_amount FROM savings_goals WHERE student_id = {p} ORDER BY goal_id ASC",
                (student_id,)
            )
            rows = cursor.fetchall()
            results = []
            for r in rows:
                if self.use_mysql:
                    results.append({
                        "goal_id": r[0],
                        "student_id": r[1],
                        "goal_name": r[2],
                        "target_amount": float(r[3]),
                        "current_amount": float(r[4])
                    })
                else:
                    results.append({
                        "goal_id": r["goal_id"],
                        "student_id": r["student_id"],
                        "goal_name": r["goal_name"],
                        "target_amount": float(r["target_amount"]),
                        "current_amount": float(r["current_amount"])
                    })
            return results

    def add_savings_goal(self, student_id: int, goal_name: str, target_amount: float, current_amount: float = 0.0) -> int:
        """Adds a new savings goal."""
        p = self.get_placeholder()
        with self.get_cursor() as (conn, cursor):
            cursor.execute(
                f"INSERT INTO savings_goals (student_id, goal_name, target_amount, current_amount) VALUES ({p}, {p}, {p}, {p})",
                (student_id, goal_name, target_amount, current_amount)
            )
            return cursor.lastrowid

    def update_savings_goal_progress(self, goal_id: int, new_current_amount: float) -> bool:
        """Updates saved amount progress."""
        p = self.get_placeholder()
        with self.get_cursor() as (conn, cursor):
            cursor.execute(
                f"UPDATE savings_goals SET current_amount = {p} WHERE goal_id = {p}",
                (new_current_amount, goal_id)
            )
            return True

    def delete_savings_goal(self, goal_id: int) -> bool:
        """Deletes a savings goal."""
        p = self.get_placeholder()
        with self.get_cursor() as (conn, cursor):
            cursor.execute(f"DELETE FROM savings_goals WHERE goal_id = {p}", (goal_id,))
            return True

    # -------------------------------------------------------------------------
    # DIAGNOSTICS & VIVA HELPERS (Arpeet Chahal)
    # -------------------------------------------------------------------------
    def get_database_info(self) -> Dict[str, Any]:
        """Returns database diagnostics and row counts for viva defense."""
        with self.get_cursor() as (conn, cursor):
            cursor.execute("SELECT COUNT(*) FROM students")
            students_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM expenses")
            expenses_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM savings_goals")
            goals_count = cursor.fetchone()[0]

            return {
                "engine": self.db_type,
                "students_count": students_count,
                "expenses_count": expenses_count,
                "goals_count": goals_count,
                "storage_location": self.sqlite_file if not self.use_mysql else f"MySQL @ {self.db_config['host']}:{self.db_config['database']}"
            }
