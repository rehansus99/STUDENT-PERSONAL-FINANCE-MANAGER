# Student Personal Finance Manager

**School of Computer Science Engineering and Technology**  
**Bennett University**  
**Course Code:** 2026CSAE100 — *Computational Thinking and Programming*

---

## 👥 Team Members & Contribution

| Student Name | Enrollment No. | Batch / Section | Contribution & Module Ownership |
|---|---|---|---|
| **Rehan Hussain** | S26CSEU0991 | B-28, S14 | **GUI / Frontend:** [`gui.py`](gui.py), [`main.py`](main.py) — Tkinter Dashboard, Cards, Tables, Modals, Canvas & Matplotlib Visuals |
| **Mohammad Huzaif Khaja Khan** | S26CSEU0971 | B-28, S14 | **Logic / Analysis:** [`logic.py`](logic.py), [`test_logic.py`](test_logic.py) — Calculations, Statistics, Rule-Based Alerts, Velocity, Savings, CSV |
| **Arpeet Chahal** | S26CSEU0929 | B-27, S14 | **Database / Backend:** [`database.py`](database.py), [`schema.sql`](schema.sql), [`test_database.py`](test_database.py) — MySQL + SQLite, CRUD, Transactions, Aggregations |

---

## 📖 Project Overview

The **Student Personal Finance Manager** is a desktop application designed specifically for college students to track, manage, analyze, and budget their monthly expenses. It solves common financial challenges faced by students—such as budget exhaustion, unmonitored discretionary spending, and lack of savings progress—by combining daily expense tracking, automated budget alerts, visual analytics, and savings goal monitoring in a single user-friendly interface.

---

## 🚀 Key Features

1. **Executive Dashboard:** Real-time KPI cards displaying Monthly Budget, Total Spent, Remaining Allowance, and Highest Spending Category.
2. **Rule-Based Budget Alerts:**
   - `< 80%`: Normal status (Emerald Green)
   - `80% - 100%`: Warning status (Amber)
   - `≥ 100%`: Critical budget exceeded alert (Coral Red)
3. **Daily Burn Rate & Safe Cap:** Automatically calculates daily run-rate and recommended daily spending cap for remaining days in the month.
4. **Expense Management:** Full CRUD functionality (Add, View, Edit, Delete) with interactive Treeview table.
5. **Real-Time Search & Filtering:** Dynamic text search matching description/category/amount, plus category dropdown filtering.
6. **Spending Analytics & Insights:**
   - Visual category chart (native Tkinter Canvas bar chart + optional Matplotlib pie chart).
   - Statistical analysis using Python's `statistics` module (Mean, Median, Standard Deviation, Outlier detection).
   - Time-based velocity tracking (Today, This Week, This Month).
7. **Savings Goals Tracker:** Target amount tracking with visual progress bars (`ttk.Progressbar`) and deposit management.
8. **Excel-Compatible CSV Export:** One-click export formatted in UTF-8 BOM encoding.
9. **Dual Database Architecture:** Primary MySQL support with seamless automatic SQLite fallback for zero-configuration execution.

---

## 🧠 Computational Thinking Pillars Demonstrated

- **Decomposition:** System cleanly divided into three decoupled tiers: Storage (`database.py`), Business Logic & Computation (`logic.py`), and User Interface (`gui.py`).
- **Pattern Recognition:** Algorithmic identification of spending habits: category dominance (>35% of total spend), weekly velocity pace, and transaction outliers.
- **Abstraction:** Real-world financial noise filtered down to 5 essential attributes: `(expense_id, expense_date, category, amount, description)`.
- **Algorithm Design:** Deterministic decision trees for budget alert thresholds, daily safe allowance formulas, and savings progress calculations.

---

## 💻 How to Run the Application

### Option 1: Master Single-File Application (Recommended)
Run the self-contained single-file application with zero external dependencies:
```bash
python app.py
```
*(On Windows, you can also double-click `run_app.bat` to launch immediately).*

### Option 2: Modular Team Architecture
Run the modular architecture connecting `gui.py`, `logic.py`, and `database.py`:
```bash
python main.py
```

---

## 🧪 Module Verification Tests

Each backend and logic module includes a standalone verification script to test functionality directly in the terminal:

### 1. Database Layer Test (Backend Verification)
```bash
python test_database.py
```
*Verifies database connectivity, table initialization, profile updates, CRUD operations, transactions, and SQL `GROUP BY` aggregations.*

### 2. Logic & Analytics Test (Computational Verification)
```bash
python test_logic.py
```
*Verifies input validation, budget alert triggers, time aggregations, category breakdowns, statistical measures (`statistics.mean`, `median`, `stdev`), outlier detection, and savings forecasting.*

---

## 📂 Project Repository Structure

```text
student_finance_manager/
├── app.py             # Master single-file application (all modules compiled)
├── main.py            # Modular application entry point
├── gui.py             # Frontend: Tkinter layout, cards, tables, modals, charts
├── logic.py           # Business Logic: calculations, alerts, statistics, CSV
├── database.py        # Database Layer: MySQL + SQLite fallback, CRUD queries
├── schema.sql         # Relational database schema DDL script
├── test_database.py   # Database verification script
├── test_logic.py      # Logic & calculations verification script
├── run_app.bat        # Windows 1-click double-click launcher
├── requirements.txt   # Optional enhancements (mysql-connector-python, matplotlib)
├── .gitignore         # Git ignore configuration
└── README.md          # Project documentation
```
