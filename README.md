# Student Personal Finance Manager

**School of Computer Science Engineering and Technology**  
**Bennett University**  
**Course Code:** 2026CSAE100 — *Computational Thinking and Programming*

---

## 👥 Team Members & Dedicated Modules

| Student Name | Enrollment No. | Batch / Section | Contribution & File Ownership |
|---|---|---|---|
| **Rehan Hussain** | S26CSEU0991 | B-28, S14 | **GUI / Frontend:** [`gui.py`](gui.py), [`main.py`](main.py) — Tkinter Dashboard, Cards, Tables, Modals, Canvas & Matplotlib Charts |
| **Mohammad Huzaif Khaja Khan** | S26CSEU0971 | B-28, S14 | **Logic / Analysis:** [`logic.py`](logic.py), [`test_logic.py`](test_logic.py) — Calculations, Statistics, Rule-Based Alerts, Velocity, Savings, CSV |
| **Arpeet Chahal** | S26CSEU0929 | B-28, S14 | **Database / Backend:** [`database.py`](database.py), [`schema.sql`](schema.sql), [`test_database.py`](test_database.py) — MySQL + SQLite, CRUD, Aggregations |

---

## 🚀 Key Features

1. **Interactive Dashboard:** Real-time KPI cards (Monthly Budget, Total Spent, Remaining, Highest Spending Category).
2. **Rule-Based Budget Alerts:**
   - `< 80%`: Normal status (Emerald Green)
   - `80% - 100%`: Warning status (Amber)
   - `> 100%`: Exceeded alert (Red)
3. **Daily Burn Rate & Safe Cap:** Computes safe daily allowance for remaining days in the month.
4. **Expense Management:** Full CRUD (Add, View, Edit, Delete) with interactive Treeview table.
5. **Search & Filter:** Real-time text search, category dropdown filter, and filter resets.
6. **Spending Analytics & Insights:**
   - Visual category chart (native Canvas chart + Matplotlib support).
   - Statistical analysis (`statistics` module: Mean, Median, Standard Deviation, Outlier detection).
   - Rule-based algorithmic insights and personalized spending recommendations.
   - Time-based velocity tracking (Today, This Week, This Month).
7. **Savings Goals Tracker:** Interactive progress bars with deposit tracking and feasibility forecasting.
8. **CSV Export:** One-click export to standard CSV format with Excel UTF-8 BOM encoding.
9. **Dual Database Architecture:** Primary MySQL support with seamless automatic SQLite fallback for zero-configuration testing.

---

## 💻 How to Run the Project & Individual Viva Tests

### 1. Launch the Full Application (Rehan's Presentation)
```bash
python main.py
```

### 2. Run Individual Database Verification (Arpeet's Viva)
```bash
python test_database.py
```
*Verifies database connectivity, table initialization, profile updates, CRUD operations, transactions, and SQL GROUP BY queries.*

### 3. Run Individual Logic & Algorithm Verification (Mohammad's Viva)
```bash
python test_logic.py
```
*Verifies input validation, budget alerts, time aggregations, category breakdowns, statistical measures (`statistics` module), outlier detection, and savings forecasting.*

---

## 🧠 Computational Thinking Pillars Demonstrated

- **Decomposition:** System divided into 3 decoupled layers (`gui.py`, `logic.py`, `database.py`).
- **Pattern Recognition:** Identifying dominant spending categories, statistical outliers, and weekly velocity trends.
- **Abstraction:** Modeling financial transactions with essential attributes (`Date, Category, Amount, Description`).
- **Algorithm Design:** Deterministic decision trees for budget alerts, dynamic daily allowances, and savings feasibility.
