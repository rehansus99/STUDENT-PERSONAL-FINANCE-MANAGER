"""
=============================================================================
STUDENT PERSONAL FINANCE MANAGER - MAIN APPLICATION ENTRY POINT
=============================================================================
Course: Computational Thinking and Programming (2026CSAE100)
Bennett University
Team Members:
- Rehan Hussain (S26CSEU0991) - GUI / Frontend
- Mohammad Huzaif Khaja Khan (S26CSEU0971) - Logic / Analysis
- Arpeet Chahal (S26CSEU0929) - Database / Backend

To Run:
    python main.py
=============================================================================
"""

import sys
import os

# Ensure local module directory is in Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import DatabaseManager
from gui import FinanceManagerApp


def main():
    print("=" * 65)
    print("  STUDENT PERSONAL FINANCE MANAGER (Bennett University - 2026)")
    print("  Developed by: Rehan Hussain, Mohammad Huzaif, Arpeet Chahal")
    print("=" * 65)

    # 1. Initialize Database Manager (Tries MySQL, auto-falls back to SQLite)
    # If your local MySQL is configured, set use_mysql=True and provide credentials:
    db = DatabaseManager(
        use_mysql=False,  # Set to True if local MySQL server is active with credentials
        host="localhost",
        user="root",
        password="password",
        database="student_finance_db"
    )

    # 2. Setup tables and verify seed data
    db.initialize_tables()

    # 3. Launch Tkinter GUI
    app = FinanceManagerApp(db_manager=db)
    print("[App] Launching Graphical User Interface...")
    app.mainloop()
    print("[App] Application closed gracefully.")


if __name__ == "__main__":
    main()
