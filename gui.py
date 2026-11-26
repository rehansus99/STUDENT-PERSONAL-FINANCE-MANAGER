"""
=============================================================================
STUDENT PERSONAL FINANCE MANAGER - GUI / FRONTEND MODULE
=============================================================================
Course: Computational Thinking and Programming (2026CSAE100)
Bennett University
Author / Lead: Rehan Hussain (S26CSEU0991) - GUI / Frontend
Team Members: Mohammad Huzaif (Logic) & Arpeet Chahal (Database)

Features:
- Modern Card-Based Responsive Layout with Tkinter & TTK
- Interactive Sidebar Navigation
- Dynamic Dashboard with KPI Cards & Budget Alert Badges
- Expense Management (Treeview, Add/Edit/Delete Modals, Search, Filter)
- Spending Analytics (Native Canvas Visual Chart + Rule-Based Insights)
- Savings Goals Tracker with Visual Progress Bars
- CSV Export with System File Dialog
- 100% Zero-External-Dependency Compatible (Pure Standard Library)
=============================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from typing import Optional, Dict, Any, List

# Import Project Layers
from database import DatabaseManager
import logic

# Try importing matplotlib for embedded charts (optional enhancement)
try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


# =============================================================================
# COLOR PALETTE & UI THEME CONSTANTS
# =============================================================================
COLOR_BG = "#F8FAFC"            # Light Slate Background
COLOR_SIDEBAR = "#0F172A"       # Deep Slate Navy
COLOR_SIDEBAR_HOVER = "#1E293B" # Dark Slate
COLOR_SIDEBAR_ACTIVE = "#2563EB"# Vibrant Blue
COLOR_CARD_BG = "#FFFFFF"       # Crisp White Card
COLOR_TEXT_MAIN = "#0F172A"     # High-contrast Dark
COLOR_TEXT_MUTED = "#64748B"    # Slate Gray
COLOR_PRIMARY = "#2563EB"       # Primary Action Blue
COLOR_PRIMARY_HOVER = "#1D4ED8"
COLOR_SUCCESS = "#10B981"       # Emerald Green
COLOR_WARNING = "#F59E0B"       # Amber Warning
COLOR_DANGER = "#EF4444"        # Coral Red
COLOR_BORDER = "#E2E8F0"        # Subtle Border Gray

FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_SUBTITLE = ("Segoe UI", 11, "bold")
FONT_HEADING = ("Segoe UI", 12, "bold")
FONT_BODY = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")
FONT_KPI_VAL = ("Segoe UI", 18, "bold")
FONT_KPI_LBL = ("Segoe UI", 9)


class FinanceManagerApp(tk.Tk):
    """
    Main Application Window for Student Personal Finance Manager.
    Created by Rehan Hussain (Frontend Lead).
    """

    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db = db_manager
        
        # Window Setup
        self.title("Student Personal Finance Manager | Bennett University")
        self.geometry("1100x720")
        self.minsize(980, 620)
        self.configure(bg=COLOR_BG)

        # Application State
        self.current_student_id = 1
        self.current_page_name = "dashboard"
        self.sidebar_buttons = {}

        # Configure Custom TTK Styles
        self._configure_styles()

        # Build Main Layout Shell
        self._create_main_shell()

        # Show Initial Page
        self.show_page("dashboard")

    # =========================================================================
    # THEME & STYLE CONFIGURATION
    # =========================================================================
    def _configure_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        # Treeview (Table) Styling
        style.configure(
            "Treeview",
            background=COLOR_CARD_BG,
            foreground=COLOR_TEXT_MAIN,
            rowheight=30,
            fieldbackground=COLOR_CARD_BG,
            font=FONT_BODY,
            borderwidth=0
        )
        style.configure(
            "Treeview.Heading",
            background="#E2E8F0",
            foreground=COLOR_TEXT_MAIN,
            font=FONT_SUBTITLE,
            padding=6,
            relief="flat"
        )
        style.map(
            "Treeview",
            background=[("selected", "#DBEAFE")],
            foreground=[("selected", COLOR_PRIMARY)]
        )

        # Progressbar Styling
        style.configure(
            "Green.Horizontal.TProgressbar",
            troughcolor="#E2E8F0",
            background=COLOR_SUCCESS,
            thickness=16
        )

        # Combobox
        style.configure("TCombobox", font=FONT_BODY, padding=4)

    # =========================================================================
    # APPLICATION SHELL (SIDEBAR + MAIN CONTENT AREA)
    # =========================================================================
    def _create_main_shell(self):
        # 1. Left Sidebar Navigation
        self.sidebar_frame = tk.Frame(self, bg=COLOR_SIDEBAR, width=230)
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False)

        # Brand / App Title in Sidebar
        brand_frame = tk.Frame(self.sidebar_frame, bg=COLOR_SIDEBAR, pady=24, padx=16)
        brand_frame.pack(fill="x")

        tk.Label(
            brand_frame,
            text="BENNETT FINANCE",
            font=("Segoe UI", 13, "bold"),
            fg="#FFFFFF",
            bg=COLOR_SIDEBAR
        ).pack(anchor="w")

        tk.Label(
            brand_frame,
            text="Student Expense Manager",
            font=("Segoe UI", 9),
            fg="#94A3B8",
            bg=COLOR_SIDEBAR
        ).pack(anchor="w", pady=(2, 0))

        # Divider
        tk.Frame(self.sidebar_frame, bg="#334155", height=1).pack(fill="x", padx=14, pady=8)

        # Navigation Buttons
        nav_items = [
            ("dashboard", "📊  Dashboard"),
            ("expenses",  "💸  Expense Manager"),
            ("analytics", "📈  Spending Analytics"),
            ("savings",   "🎯  Savings Goals"),
            ("profile",   "⚙️  Profile & Budget")
        ]

        for page_id, label_text in nav_items:
            btn = tk.Button(
                self.sidebar_frame,
                text=label_text,
                font=("Segoe UI", 10, "bold"),
                anchor="w",
                padx=16,
                pady=10,
                bg=COLOR_SIDEBAR,
                fg="#CBD5E1",
                activebackground=COLOR_SIDEBAR_HOVER,
                activeforeground="#FFFFFF",
                bd=0,
                cursor="hand2",
                command=lambda pid=page_id: self.show_page(pid)
            )
            btn.pack(fill="x", padx=8, pady=3)
            self.sidebar_buttons[page_id] = btn

        # Sidebar Footer: DB Status & Student Info
        footer_frame = tk.Frame(self.sidebar_frame, bg=COLOR_SIDEBAR, padx=16, pady=16)
        footer_frame.pack(side="bottom", fill="x")

        db_type = self.db.db_type
        status_color = COLOR_SUCCESS if db_type == "MySQL" else "#38BDF8"
        
        status_box = tk.Frame(footer_frame, bg="#1E293B", padx=10, pady=8)
        status_box.pack(fill="x")
        
        tk.Label(
            status_box,
            text=f"● Database: {db_type}",
            font=("Segoe UI", 8, "bold"),
            fg=status_color,
            bg="#1E293B"
        ).pack(anchor="w")

        tk.Label(
            status_box,
            text="Course: 2026CSAE100",
            font=("Segoe UI", 8),
            fg="#94A3B8",
            bg="#1E293B"
        ).pack(anchor="w", pady=(2, 0))

        # 2. Right Main Content Area
        self.content_container = tk.Frame(self, bg=COLOR_BG)
        self.content_container.pack(side="right", fill="both", expand=True)

        # Page Frames Cache
        self.pages = {}
        self.pages["dashboard"] = tk.Frame(self.content_container, bg=COLOR_BG)
        self.pages["expenses"] = tk.Frame(self.content_container, bg=COLOR_BG)
        self.pages["analytics"] = tk.Frame(self.content_container, bg=COLOR_BG)
        self.pages["savings"] = tk.Frame(self.content_container, bg=COLOR_BG)
        self.pages["profile"] = tk.Frame(self.content_container, bg=COLOR_BG)

        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")

        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)

    def show_page(self, page_name: str):
        """Switches active page and refreshes its components."""
        self.current_page_name = page_name

        # Update sidebar button highlights
        for pid, btn in self.sidebar_buttons.items():
            if pid == page_name:
                btn.configure(bg=COLOR_SIDEBAR_ACTIVE, fg="#FFFFFF")
            else:
                btn.configure(bg=COLOR_SIDEBAR, fg="#CBD5E1")

        # Raise frame to top
        frame = self.pages[page_name]
        frame.tkraise()

        # Refresh contents dynamically
        if page_name == "dashboard":
            self._render_dashboard(frame)
        elif page_name == "expenses":
            self._render_expenses(frame)
        elif page_name == "analytics":
            self._render_analytics(frame)
        elif page_name == "savings":
            self._render_savings(frame)
        elif page_name == "profile":
            self._render_profile(frame)

    # =========================================================================
    # 1. DASHBOARD VIEW (Rehan)
    # =========================================================================
    def _render_dashboard(self, parent: tk.Frame):
        # Clear existing children
        for widget in parent.winfo_children():
            widget.destroy()

        profile = self.db.get_student_profile(self.current_student_id)
        expenses = self.db.get_all_expenses(self.current_student_id)

        # Mohammad's Logic Computations
        budget_summary = logic.calculate_budget_summary(profile["monthly_budget"], expenses)
        cat_summary = logic.get_category_summary(expenses)
        time_summary = logic.get_time_summary(expenses)

        # Header Title & Quick Action
        header = tk.Frame(parent, bg=COLOR_BG, padx=28, pady=20)
        header.pack(fill="x")

        title_frame = tk.Frame(header, bg=COLOR_BG)
        title_frame.pack(side="left")

        tk.Label(
            title_frame,
            text=f"Welcome, {profile['name']}!",
            font=FONT_TITLE,
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_BG
        ).pack(anchor="w")

        tk.Label(
            title_frame,
            text="Here is your personal monthly financial summary and spending health.",
            font=FONT_BODY,
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_BG
        ).pack(anchor="w", pady=(2, 0))

        # Quick Add Expense Button in Header
        add_btn = tk.Button(
            header,
            text="+ Add New Expense",
            font=FONT_BOLD,
            bg=COLOR_PRIMARY,
            fg="#FFFFFF",
            activebackground=COLOR_PRIMARY_HOVER,
            activeforeground="#FFFFFF",
            bd=0,
            padx=16,
            pady=8,
            cursor="hand2",
            command=self.open_add_expense_dialog
        )
        add_btn.pack(side="right")

        # ---------------------------------------------------------------------
        # Dynamic Rule-Based Alert Banner (Section 7.9)
        # ---------------------------------------------------------------------
        alert_banner = tk.Frame(
            parent,
            bg=budget_summary["badge_bg"],
            padx=20,
            pady=12,
            highlightbackground=budget_summary["alert_color"],
            highlightthickness=1
        )
        alert_banner.pack(fill="x", padx=28, pady=(0, 16))

        tk.Label(
            alert_banner,
            text=f"[{budget_summary['alert_title']}]",
            font=("Segoe UI", 10, "bold"),
            fg=budget_summary["alert_color"],
            bg=budget_summary["badge_bg"]
        ).pack(side="left", padx=(0, 10))

        tk.Label(
            alert_banner,
            text=budget_summary["alert_message"],
            font=FONT_BODY,
            fg=COLOR_TEXT_MAIN,
            bg=budget_summary["badge_bg"]
        ).pack(side="left")

        # ---------------------------------------------------------------------
        # KPI Cards (Monthly Budget, Total Spent, Remaining, Highest Category)
        # ---------------------------------------------------------------------
        kpi_container = tk.Frame(parent, bg=COLOR_BG, padx=28)
        kpi_container.pack(fill="x", pady=(0, 20))

        kpi_cards = [
            ("Monthly Budget", f"₹{budget_summary['monthly_budget']:,.2f}", "#3B82F6", "Fixed monthly allowance"),
            ("Total Spent", f"₹{budget_summary['total_spent']:,.2f}", budget_summary["alert_color"], f"{budget_summary['used_percentage']}% of budget used"),
            ("Remaining Funds", f"₹{budget_summary['remaining']:,.2f}", COLOR_SUCCESS if budget_summary['remaining'] >= 0 else COLOR_DANGER, "Available to spend"),
            ("Highest Category", cat_summary["highest_category"], "#8B5CF6", f"₹{cat_summary['highest_amount']:,.2f} ({cat_summary['highest_percentage']}%)")
        ]

        for i, (label, val, accent_color, subtext) in enumerate(kpi_cards):
            card = tk.Frame(kpi_container, bg=COLOR_CARD_BG, padx=16, pady=14, relief="flat", highlightbackground=COLOR_BORDER, highlightthickness=1)
            card.pack(side="left", fill="both", expand=True, padx=(0 if i == 0 else 10, 0))

            tk.Label(card, text=label, font=FONT_KPI_LBL, fg=COLOR_TEXT_MUTED, bg=COLOR_CARD_BG).pack(anchor="w")
            tk.Label(card, text=val, font=FONT_KPI_VAL, fg=accent_color, bg=COLOR_CARD_BG).pack(anchor="w", pady=(4, 2))
            tk.Label(card, text=subtext, font=("Segoe UI", 8), fg=COLOR_TEXT_MUTED, bg=COLOR_CARD_BG).pack(anchor="w")

        # ---------------------------------------------------------------------
        # Time Summary Cards (Today, This Week, This Month) - Section 7.6
        # ---------------------------------------------------------------------
        time_bar = tk.Frame(parent, bg=COLOR_CARD_BG, padx=20, pady=10, highlightbackground=COLOR_BORDER, highlightthickness=1)
        time_bar.pack(fill="x", padx=28, pady=(0, 20))

        tk.Label(time_bar, text="Spending Velocity:", font=FONT_SUBTITLE, fg=COLOR_TEXT_MAIN, bg=COLOR_CARD_BG).pack(side="left", padx=(0, 24))

        tk.Label(time_bar, text=f"📅 Today: ₹{time_summary['today']:,.2f}", font=FONT_BODY, fg=COLOR_TEXT_MAIN, bg=COLOR_CARD_BG).pack(side="left", padx=16)
        tk.Label(time_bar, text="|", fg=COLOR_BORDER, bg=COLOR_CARD_BG).pack(side="left")
        tk.Label(time_bar, text=f"📆 This Week: ₹{time_summary['this_week']:,.2f}", font=FONT_BODY, fg=COLOR_TEXT_MAIN, bg=COLOR_CARD_BG).pack(side="left", padx=16)
        tk.Label(time_bar, text="|", fg=COLOR_BORDER, bg=COLOR_CARD_BG).pack(side="left")
        tk.Label(time_bar, text=f"🗓️ This Month: ₹{time_summary['this_month']:,.2f}", font=FONT_BODY, fg=COLOR_TEXT_MAIN, bg=COLOR_CARD_BG).pack(side="left", padx=16)

        # ---------------------------------------------------------------------
        # Recent Transactions Table (Section 7.5)
        # ---------------------------------------------------------------------
        recent_frame = tk.Frame(parent, bg=COLOR_CARD_BG, padx=20, pady=16, highlightbackground=COLOR_BORDER, highlightthickness=1)
        recent_frame.pack(fill="both", expand=True, padx=28, pady=(0, 20))

        recent_header = tk.Frame(recent_frame, bg=COLOR_CARD_BG)
        recent_header.pack(fill="x", pady=(0, 10))

        tk.Label(recent_header, text="Recent Expenses", font=FONT_HEADING, fg=COLOR_TEXT_MAIN, bg=COLOR_CARD_BG).pack(side="left")
        
        view_all_btn = tk.Button(
            recent_header,
            text="View Full History →",
            font=FONT_BOLD,
            fg=COLOR_PRIMARY,
            bg=COLOR_CARD_BG,
            bd=0,
            cursor="hand2",
            command=lambda: self.show_page("expenses")
        )
        view_all_btn.pack(side="right")

        # Table columns
        columns = ("date", "category", "amount", "description")
        tree = ttk.Treeview(recent_frame, columns=columns, show="headings", height=6)
        tree.heading("date", text="Date")
        tree.heading("category", text="Category")
        tree.heading("amount", text="Amount (₹)")
        tree.heading("description", text="Description")

        tree.column("date", width=120, anchor="center")
        tree.column("category", width=140, anchor="center")
        tree.column("amount", width=120, anchor="e")
        tree.column("description", width=360, anchor="w")

        tree.pack(fill="both", expand=True)

        for exp in expenses[:6]:
            tree.insert("", "end", values=(
                exp["expense_date"],
                exp["category"],
                f"₹{exp['amount']:,.2f}",
                exp["description"]
            ))

    # =========================================================================
    # 2. EXPENSE MANAGEMENT VIEW (Rehan)
    # =========================================================================
    def _render_expenses(self, parent: tk.Frame):
        for widget in parent.winfo_children():
            widget.destroy()

        # Header with Title
        header = tk.Frame(parent, bg=COLOR_BG, padx=28, pady=16)
        header.pack(fill="x")

        tk.Label(
            header,
            text="Expense Management",
            font=FONT_TITLE,
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_BG
        ).pack(side="left")

        # Action Buttons in Header
        action_box = tk.Frame(header, bg=COLOR_BG)
        action_box.pack(side="right")

        csv_btn = tk.Button(
            action_box,
            text="📥 Export CSV",
            font=FONT_BOLD,
            bg="#059669",
            fg="#FFFFFF",
            bd=0,
            padx=14,
            pady=7,
            cursor="hand2",
            command=self._handle_csv_export
        )
        csv_btn.pack(side="left", padx=(0, 10))

        add_btn = tk.Button(
            action_box,
            text="+ Add Expense",
            font=FONT_BOLD,
            bg=COLOR_PRIMARY,
            fg="#FFFFFF",
            bd=0,
            padx=14,
            pady=7,
            cursor="hand2",
            command=self.open_add_expense_dialog
        )
        add_btn.pack(side="left")

        # ---------------------------------------------------------------------
        # Filter & Search Toolbar (Section 7.12)
        # ---------------------------------------------------------------------
        toolbar = tk.Frame(parent, bg=COLOR_CARD_BG, padx=16, pady=12, highlightbackground=COLOR_BORDER, highlightthickness=1)
        toolbar.pack(fill="x", padx=28, pady=(0, 14))

        # Search Box
        tk.Label(toolbar, text="Search:", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(side="left", padx=(0, 6))
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(toolbar, textvariable=self.search_var, font=FONT_BODY, width=22)
        search_entry.pack(side="left", padx=(0, 20))
        self.search_var.trace_add("write", lambda *args: self._apply_expense_filters())

        # Category Dropdown Filter
        tk.Label(toolbar, text="Category:", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(side="left", padx=(0, 6))
        self.cat_filter_var = tk.StringVar(value="All")
        cat_options = ["All", "Food", "Transport", "Education", "Entertainment", "Shopping", "Hostel", "Other"]
        cat_combo = ttk.Combobox(toolbar, textvariable=self.cat_filter_var, values=cat_options, state="readonly", width=14)
        cat_combo.pack(side="left", padx=(0, 20))
        cat_combo.bind("<<ComboboxSelected>>", lambda e: self._apply_expense_filters())

        # Clear Filters Button
        clear_btn = tk.Button(
            toolbar,
            text="Reset Filters",
            font=("Segoe UI", 9),
            bg="#F1F5F9",
            fg=COLOR_TEXT_MAIN,
            bd=0,
            padx=10,
            pady=4,
            cursor="hand2",
            command=self._reset_filters
        )
        clear_btn.pack(side="left")

        # ---------------------------------------------------------------------
        # Expenses Treeview Table (Section 7.2)
        # ---------------------------------------------------------------------
        table_container = tk.Frame(parent, bg=COLOR_CARD_BG, padx=16, pady=14, highlightbackground=COLOR_BORDER, highlightthickness=1)
        table_container.pack(fill="both", expand=True, padx=28, pady=(0, 14))

        columns = ("id", "date", "category", "amount", "description")
        self.exp_tree = ttk.Treeview(table_container, columns=columns, show="headings", selectmode="browse")

        self.exp_tree.heading("id", text="ID")
        self.exp_tree.heading("date", text="Date")
        self.exp_tree.heading("category", text="Category")
        self.exp_tree.heading("amount", text="Amount (₹)")
        self.exp_tree.heading("description", text="Description")

        self.exp_tree.column("id", width=50, anchor="center")
        self.exp_tree.column("date", width=110, anchor="center")
        self.exp_tree.column("category", width=130, anchor="center")
        self.exp_tree.column("amount", width=120, anchor="e")
        self.exp_tree.column("description", width=400, anchor="w")

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.exp_tree.yview)
        self.exp_tree.configure(yscrollcommand=scrollbar.set)

        self.exp_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ---------------------------------------------------------------------
        # Bottom Action Bar (Edit / Delete)
        # ---------------------------------------------------------------------
        btn_bar = tk.Frame(parent, bg=COLOR_BG, padx=28, pady=0)
        btn_bar.pack(fill="x", pady=(0, 16))

        edit_btn = tk.Button(
            btn_bar,
            text="✏️ Edit Selected",
            font=FONT_BOLD,
            bg="#475569",
            fg="#FFFFFF",
            bd=0,
            padx=16,
            pady=8,
            cursor="hand2",
            command=self._handle_edit_selected
        )
        edit_btn.pack(side="left", padx=(0, 10))

        delete_btn = tk.Button(
            btn_bar,
            text="🗑️ Delete Selected",
            font=FONT_BOLD,
            bg=COLOR_DANGER,
            fg="#FFFFFF",
            bd=0,
            padx=16,
            pady=8,
            cursor="hand2",
            command=self._handle_delete_selected
        )
        delete_btn.pack(side="left")

        # Load initial records
        self._load_expenses_into_tree()

    def _load_expenses_into_tree(self, records: Optional[List[Dict[str, Any]]] = None):
        """Populates Treeview with records."""
        for item in self.exp_tree.get_children():
            self.exp_tree.delete(item)

        if records is None:
            records = self.db.get_all_expenses(self.current_student_id)

        for exp in records:
            self.exp_tree.insert("", "end", values=(
                exp["expense_id"],
                exp["expense_date"],
                exp["category"],
                f"₹{exp['amount']:,.2f}",
                exp["description"]
            ))

    def _apply_expense_filters(self):
        """Applies real-time search & dropdown filters."""
        all_exps = self.db.get_all_expenses(self.current_student_id)
        filtered = logic.filter_expenses(
            all_exps,
            category_filter=self.cat_filter_var.get(),
            search_query=self.search_var.get()
        )
        self._load_expenses_into_tree(filtered)

    def _reset_filters(self):
        self.search_var.set("")
        self.cat_filter_var.set("All")
        self._load_expenses_into_tree()

    def _handle_edit_selected(self):
        selected = self.exp_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select an expense row from the table to edit.")
            return

        values = self.exp_tree.item(selected[0], "values")
        exp_id = int(values[0])
        # Clean amount string
        amount_clean = values[3].replace("₹", "").replace(",", "").strip()

        expense_data = {
            "expense_id": exp_id,
            "date": values[1],
            "category": values[2],
            "amount": amount_clean,
            "description": values[4]
        }
        self.open_edit_expense_dialog(expense_data)

    def _handle_delete_selected(self):
        selected = self.exp_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select an expense row from the table to delete.")
            return

        values = self.exp_tree.item(selected[0], "values")
        exp_id = int(values[0])

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to permanently delete Expense #{exp_id} ({values[2]} - {values[3]})?"
        )
        if confirm:
            self.db.delete_expense(exp_id)
            messagebox.showinfo("Success", f"Expense #{exp_id} has been deleted.")
            self._apply_expense_filters()

    def _handle_csv_export(self):
        expenses = self.db.get_all_expenses(self.current_student_id)
        if not expenses:
            messagebox.showinfo("Export Info", "No expense records found to export.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            initialfile=f"expense_report_{datetime.now().strftime('%Y%m%d')}.csv"
        )
        if filepath:
            success, msg = logic.export_to_csv(expenses, filepath)
            if success:
                messagebox.showinfo("Export Complete", msg)
            else:
                messagebox.showerror("Export Failed", msg)

    # =========================================================================
    # 3. SPENDING ANALYTICS & INSIGHTS VIEW (Rehan + Mohammad)
    # =========================================================================
    def _render_analytics(self, parent: tk.Frame):
        for widget in parent.winfo_children():
            widget.destroy()

        profile = self.db.get_student_profile(self.current_student_id)
        expenses = self.db.get_all_expenses(self.current_student_id)

        budget_summary = logic.calculate_budget_summary(profile["monthly_budget"], expenses)
        cat_summary = logic.get_category_summary(expenses)
        time_summary = logic.get_time_summary(expenses)
        insights = logic.get_rule_based_insights(budget_summary, cat_summary, time_summary)

        # Header
        header = tk.Frame(parent, bg=COLOR_BG, padx=28, pady=20)
        header.pack(fill="x")

        tk.Label(
            header,
            text="Spending Analytics & Patterns",
            font=FONT_TITLE,
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_BG
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Visual breakdown of category expenses and rule-based financial recommendations.",
            font=FONT_BODY,
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_BG
        ).pack(anchor="w", pady=(2, 0))

        # Main 2-Column Layout (Left: Chart, Right: Insights & Breakdown)
        main_split = tk.Frame(parent, bg=COLOR_BG, padx=28)
        main_split.pack(fill="both", expand=True, pady=(0, 20))

        # LEFT COLUMN: Visual Chart
        left_card = tk.Frame(main_split, bg=COLOR_CARD_BG, padx=20, pady=18, highlightbackground=COLOR_BORDER, highlightthickness=1)
        left_card.pack(side="left", fill="both", expand=True, padx=(0, 14))

        tk.Label(left_card, text="Category Spending Chart", font=FONT_HEADING, bg=COLOR_CARD_BG).pack(anchor="w", pady=(0, 12))

        # Render Chart: Matplotlib if available, otherwise Native Tkinter Canvas
        self._render_category_chart(left_card, cat_summary["totals"])

        # RIGHT COLUMN: Rule-Based Insights & Category List
        right_frame = tk.Frame(main_split, bg=COLOR_BG)
        right_frame.pack(side="right", fill="both", expand=True)

        # 1. Insights Box (Section 7.10)
        insights_card = tk.Frame(right_frame, bg="#EFF6FF", padx=16, pady=14, highlightbackground="#BFDBFE", highlightthickness=1)
        insights_card.pack(fill="x", pady=(0, 14))

        tk.Label(
            insights_card,
            text="💡 Rule-Based Insights & Recommendations",
            font=FONT_SUBTITLE,
            fg="#1E40AF",
            bg="#EFF6FF"
        ).pack(anchor="w", pady=(0, 8))

        for insight in insights:
            tk.Label(
                insights_card,
                text=insight,
                font=("Segoe UI", 9),
                fg="#1E293B",
                bg="#EFF6FF",
                wraplength=380,
                justify="left"
            ).pack(anchor="w", pady=3)

        # 2. Category Contribution Table
        cat_table_card = tk.Frame(right_frame, bg=COLOR_CARD_BG, padx=16, pady=14, highlightbackground=COLOR_BORDER, highlightthickness=1)
        cat_table_card.pack(fill="both", expand=True)

        tk.Label(cat_table_card, text="Category Breakdown", font=FONT_HEADING, bg=COLOR_CARD_BG).pack(anchor="w", pady=(0, 8))

        cat_tree = ttk.Treeview(cat_table_card, columns=("cat", "spent", "pct"), show="headings", height=5)
        cat_tree.heading("cat", text="Category")
        cat_tree.heading("spent", text="Total (₹)")
        cat_tree.heading("pct", text="Share (%)")

        cat_tree.column("cat", width=120, anchor="center")
        cat_tree.column("spent", width=100, anchor="e")
        cat_tree.column("pct", width=80, anchor="center")

        cat_tree.pack(fill="both", expand=True)

        for cat, total in cat_summary["totals"].items():
            pct = cat_summary["percentages"].get(cat, 0.0)
            cat_tree.insert("", "end", values=(cat, f"₹{total:,.2f}", f"{pct}%"))

    def _render_category_chart(self, parent_frame: tk.Frame, category_totals: Dict[str, float]):
        """
        Renders Matplotlib pie chart if installed, or native Tkinter bar chart as fallback.
        Ensures 100% reliability during viva demonstrations.
        """
        if not category_totals:
            tk.Label(parent_frame, text="No expense data available to plot.", font=FONT_BODY, bg=COLOR_CARD_BG, fg=COLOR_TEXT_MUTED).pack(pady=40)
            return

        if MATPLOTLIB_AVAILABLE:
            fig = Figure(figsize=(4.2, 3.8), dpi=95, facecolor="#FFFFFF")
            ax = fig.add_subplot(111)

            labels = list(category_totals.keys())
            values = list(category_totals.values())
            colors = ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#EC4899", "#14B8A6"]

            ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=140, colors=colors[:len(labels)], textprops={"fontsize": 8})
            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=parent_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
        else:
            # Native Tkinter Canvas Bar Chart (Zero dependencies!)
            chart_canvas = tk.Canvas(parent_frame, bg="#FFFFFF", highlightthickness=0, height=280)
            chart_canvas.pack(fill="both", expand=True, pady=10)

            max_val = max(category_totals.values()) if category_totals else 1.0
            colors = ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#EC4899", "#14B8A6"]

            y_pos = 20
            for i, (cat, val) in enumerate(category_totals.items()):
                bar_width = int((val / max_val) * 190)
                color = colors[i % len(colors)]

                # Category Label
                chart_canvas.create_text(80, y_pos + 10, text=cat, anchor="e", font=("Segoe UI", 9, "bold"), fill=COLOR_TEXT_MAIN)
                # Bar
                chart_canvas.create_rectangle(90, y_pos, 90 + bar_width, y_pos + 20, fill=color, outline="")
                # Value Label
                chart_canvas.create_text(100 + bar_width, y_pos + 10, text=f"₹{val:,.0f}", anchor="w", font=("Segoe UI", 8), fill=COLOR_TEXT_MUTED)

                y_pos += 34

    # =========================================================================
    # 4. SAVINGS GOALS VIEW (Rehan)
    # =========================================================================
    def _render_savings(self, parent: tk.Frame):
        for widget in parent.winfo_children():
            widget.destroy()

        goals = self.db.get_savings_goals(self.current_student_id)

        # Header
        header = tk.Frame(parent, bg=COLOR_BG, padx=28, pady=20)
        header.pack(fill="x")

        title_frame = tk.Frame(header, bg=COLOR_BG)
        title_frame.pack(side="left")

        tk.Label(title_frame, text="Savings Goals Tracker", font=FONT_TITLE, fg=COLOR_TEXT_MAIN, bg=COLOR_BG).pack(anchor="w")
        tk.Label(title_frame, text="Track target savings and monitor your financial discipline.", font=FONT_BODY, fg=COLOR_TEXT_MUTED, bg=COLOR_BG).pack(anchor="w")

        add_goal_btn = tk.Button(
            header,
            text="+ Add New Goal",
            font=FONT_BOLD,
            bg=COLOR_PRIMARY,
            fg="#FFFFFF",
            bd=0,
            padx=14,
            pady=8,
            cursor="hand2",
            command=self.open_add_goal_dialog
        )
        add_goal_btn.pack(side="right")

        # Goals Container
        container = tk.Frame(parent, bg=COLOR_BG, padx=28)
        container.pack(fill="both", expand=True, pady=(0, 20))

        if not goals:
            empty_card = tk.Frame(container, bg=COLOR_CARD_BG, padx=24, pady=40, highlightbackground=COLOR_BORDER, highlightthickness=1)
            empty_card.pack(fill="x")
            tk.Label(empty_card, text="No savings goals created yet.", font=FONT_HEADING, bg=COLOR_CARD_BG, fg=COLOR_TEXT_MUTED).pack()
            return

        for goal in goals:
            g_id = goal["goal_id"]
            name = goal["goal_name"]
            target = goal["target_amount"]
            current = goal["current_amount"]
            pct = min((current / target * 100.0), 100.0) if target > 0 else 0.0

            card = tk.Frame(container, bg=COLOR_CARD_BG, padx=20, pady=16, highlightbackground=COLOR_BORDER, highlightthickness=1)
            card.pack(fill="x", pady=(0, 12))

            top_row = tk.Frame(card, bg=COLOR_CARD_BG)
            top_row.pack(fill="x")

            tk.Label(top_row, text=name, font=FONT_HEADING, fg=COLOR_TEXT_MAIN, bg=COLOR_CARD_BG).pack(side="left")
            tk.Label(top_row, text=f"Progress: {pct:.1f}%", font=FONT_BOLD, fg=COLOR_PRIMARY, bg=COLOR_CARD_BG).pack(side="right")

            # Progress Bar
            pbar = ttk.Progressbar(card, style="Green.Horizontal.TProgressbar", length=200, mode="determinate", value=pct)
            pbar.pack(fill="x", pady=10)

            # Bottom details & action buttons
            bottom_row = tk.Frame(card, bg=COLOR_CARD_BG)
            bottom_row.pack(fill="x")

            amt_text = f"Saved: ₹{current:,.2f}  /  Target: ₹{target:,.2f}  (Remaining: ₹{max(0, target - current):,.2f})"
            tk.Label(bottom_row, text=amt_text, font=FONT_BODY, fg=COLOR_TEXT_MUTED, bg=COLOR_CARD_BG).pack(side="left")

            action_sub = tk.Frame(bottom_row, bg=COLOR_CARD_BG)
            action_sub.pack(side="right")

            deposit_btn = tk.Button(
                action_sub,
                text="+ Deposit",
                font=("Segoe UI", 9, "bold"),
                bg="#DBEAFE",
                fg=COLOR_PRIMARY,
                bd=0,
                padx=10,
                pady=4,
                cursor="hand2",
                command=lambda gid=g_id, gcur=current: self.open_deposit_goal_dialog(gid, gcur)
            )
            deposit_btn.pack(side="left", padx=(0, 8))

            del_goal_btn = tk.Button(
                action_sub,
                text="Delete",
                font=("Segoe UI", 9),
                bg="#FEE2E2",
                fg=COLOR_DANGER,
                bd=0,
                padx=8,
                pady=4,
                cursor="hand2",
                command=lambda gid=g_id, gname=name: self._handle_delete_goal(gid, gname)
            )
            del_goal_btn.pack(side="left")

    def _handle_delete_goal(self, goal_id: int, goal_name: str):
        if messagebox.askyesno("Confirm Deletion", f"Delete savings goal '{goal_name}'?"):
            self.db.delete_savings_goal(goal_id)
            self._render_savings(self.pages["savings"])

    # =========================================================================
    # 5. PROFILE & SETTINGS VIEW (Rehan)
    # =========================================================================
    def _render_profile(self, parent: tk.Frame):
        for widget in parent.winfo_children():
            widget.destroy()

        profile = self.db.get_student_profile(self.current_student_id)

        header = tk.Frame(parent, bg=COLOR_BG, padx=28, pady=20)
        header.pack(fill="x")

        tk.Label(header, text="Student Profile & Budget Settings", font=FONT_TITLE, fg=COLOR_TEXT_MAIN, bg=COLOR_BG).pack(anchor="w")

        card = tk.Frame(parent, bg=COLOR_CARD_BG, padx=24, pady=24, highlightbackground=COLOR_BORDER, highlightthickness=1)
        card.pack(fill="x", padx=28)

        # Student Name Entry
        tk.Label(card, text="Student Name:", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(anchor="w", pady=(0, 4))
        name_entry = tk.Entry(card, font=FONT_BODY, width=35)
        name_entry.insert(0, profile["name"])
        name_entry.pack(anchor="w", pady=(0, 16))

        # Monthly Budget Entry
        tk.Label(card, text="Monthly Budget Allowance (₹):", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(anchor="w", pady=(0, 4))
        budget_entry = tk.Entry(card, font=FONT_BODY, width=35)
        budget_entry.insert(0, str(profile["monthly_budget"]))
        budget_entry.pack(anchor="w", pady=(0, 20))

        # Save Changes Button
        def save_profile():
            new_name = name_entry.get().strip()
            if not new_name:
                messagebox.showerror("Error", "Name cannot be blank.")
                return
            try:
                new_budget = float(budget_entry.get().strip())
                if new_budget <= 0:
                    messagebox.showerror("Error", "Budget must be greater than zero.")
                    return
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid numeric budget.")
                return

            self.db.update_student_profile(self.current_student_id, new_name, new_budget)
            messagebox.showinfo("Success", "Profile and monthly budget updated successfully!")
            self.show_page("dashboard")

        save_btn = tk.Button(
            card,
            text="Save Settings",
            font=FONT_BOLD,
            bg=COLOR_PRIMARY,
            fg="#FFFFFF",
            bd=0,
            padx=18,
            pady=8,
            cursor="hand2",
            command=save_profile
        )
        save_btn.pack(anchor="w")

    # =========================================================================
    # MODAL DIALOGS (Add/Edit Expense, Goals)
    # =========================================================================
    def open_add_expense_dialog(self):
        self._show_expense_dialog(title="Add New Expense", is_edit=False)

    def open_edit_expense_dialog(self, expense_data: Dict[str, Any]):
        self._show_expense_dialog(title=f"Edit Expense #{expense_data['expense_id']}", is_edit=True, initial_data=expense_data)

    def _show_expense_dialog(self, title: str, is_edit: bool, initial_data: Optional[Dict[str, Any]] = None):
        dialog = tk.Toplevel(self)
        dialog.title(title)
        dialog.geometry("420x420")
        dialog.resizable(False, False)
        dialog.configure(bg=COLOR_CARD_BG)
        dialog.grab_set()  # Modal lock

        # Center dialog
        dialog.transient(self)

        content = tk.Frame(dialog, bg=COLOR_CARD_BG, padx=24, pady=20)
        content.pack(fill="both", expand=True)

        tk.Label(content, text=title, font=FONT_HEADING, bg=COLOR_CARD_BG).pack(anchor="w", pady=(0, 16))

        # 1. Date
        tk.Label(content, text="Date (YYYY-MM-DD):", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(anchor="w")
        date_entry = tk.Entry(content, font=FONT_BODY)
        default_date = initial_data["date"] if is_edit else datetime.now().strftime("%Y-%m-%d")
        date_entry.insert(0, default_date)
        date_entry.pack(fill="x", pady=(2, 12))

        # 2. Category
        tk.Label(content, text="Category:", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(anchor="w")
        cat_options = ["Food", "Transport", "Education", "Entertainment", "Shopping", "Hostel", "Other"]
        cat_combo = ttk.Combobox(content, values=cat_options, state="readonly", font=FONT_BODY)
        default_cat = initial_data["category"] if is_edit else "Food"
        cat_combo.set(default_cat)
        cat_combo.pack(fill="x", pady=(2, 12))

        # 3. Amount
        tk.Label(content, text="Amount (₹):", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(anchor="w")
        amt_entry = tk.Entry(content, font=FONT_BODY)
        default_amt = str(initial_data["amount"]) if is_edit else ""
        amt_entry.insert(0, default_amt)
        amt_entry.pack(fill="x", pady=(2, 12))

        # 4. Description
        tk.Label(content, text="Description:", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(anchor="w")
        desc_entry = tk.Entry(content, font=FONT_BODY)
        default_desc = initial_data["description"] if is_edit else ""
        desc_entry.insert(0, default_desc)
        desc_entry.pack(fill="x", pady=(2, 20))

        # Action Buttons
        btn_box = tk.Frame(content, bg=COLOR_CARD_BG)
        btn_box.pack(fill="x")

        def submit():
            raw_date = date_entry.get()
            raw_cat = cat_combo.get()
            raw_amt = amt_entry.get()
            raw_desc = desc_entry.get()

            # Delegate Validation to Mohammad's Logic Layer
            is_valid, err_msg, cleaned = logic.validate_expense(raw_date, raw_cat, raw_amt, raw_desc)
            if not is_valid:
                messagebox.showerror("Validation Error", err_msg, parent=dialog)
                return

            if is_edit:
                self.db.update_expense(
                    expense_id=initial_data["expense_id"],
                    expense_date=cleaned["date"],
                    category=cleaned["category"],
                    amount=cleaned["amount"],
                    description=cleaned["description"]
                )
                messagebox.showinfo("Success", "Expense updated successfully!", parent=dialog)
            else:
                self.db.add_expense(
                    student_id=self.current_student_id,
                    expense_date=cleaned["date"],
                    category=cleaned["category"],
                    amount=cleaned["amount"],
                    description=cleaned["description"]
                )
                messagebox.showinfo("Success", "Expense recorded successfully!", parent=dialog)

            dialog.destroy()
            self.show_page(self.current_page_name)

        save_btn = tk.Button(
            btn_box,
            text="Save Record",
            font=FONT_BOLD,
            bg=COLOR_PRIMARY,
            fg="#FFFFFF",
            bd=0,
            padx=16,
            pady=8,
            cursor="hand2",
            command=submit
        )
        save_btn.pack(side="left", padx=(0, 10))

        cancel_btn = tk.Button(
            btn_box,
            text="Cancel",
            font=FONT_BODY,
            bg="#E2E8F0",
            fg=COLOR_TEXT_MAIN,
            bd=0,
            padx=14,
            pady=8,
            cursor="hand2",
            command=dialog.destroy
        )
        cancel_btn.pack(side="left")

    def open_add_goal_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Add New Savings Goal")
        dialog.geometry("380x320")
        dialog.resizable(False, False)
        dialog.configure(bg=COLOR_CARD_BG)
        dialog.grab_set()

        content = tk.Frame(dialog, bg=COLOR_CARD_BG, padx=24, pady=20)
        content.pack(fill="both", expand=True)

        tk.Label(content, text="New Savings Goal", font=FONT_HEADING, bg=COLOR_CARD_BG).pack(anchor="w", pady=(0, 14))

        tk.Label(content, text="Goal Name:", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(anchor="w")
        name_entry = tk.Entry(content, font=FONT_BODY)
        name_entry.pack(fill="x", pady=(2, 10))

        tk.Label(content, text="Target Amount (₹):", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(anchor="w")
        target_entry = tk.Entry(content, font=FONT_BODY)
        target_entry.pack(fill="x", pady=(2, 10))

        tk.Label(content, text="Initial Saved Amount (₹):", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(anchor="w")
        current_entry = tk.Entry(content, font=FONT_BODY)
        current_entry.insert(0, "0")
        current_entry.pack(fill="x", pady=(2, 18))

        def submit_goal():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Goal name is required.", parent=dialog)
                return
            try:
                target = float(target_entry.get().strip())
                current = float(current_entry.get().strip())
                if target <= 0 or current < 0:
                    messagebox.showerror("Error", "Amounts must be positive.", parent=dialog)
                    return
            except ValueError:
                messagebox.showerror("Error", "Invalid numeric values.", parent=dialog)
                return

            self.db.add_savings_goal(self.current_student_id, name, target, current)
            dialog.destroy()
            self._render_savings(self.pages["savings"])

        tk.Button(
            content,
            text="Create Goal",
            font=FONT_BOLD,
            bg=COLOR_PRIMARY,
            fg="#FFFFFF",
            bd=0,
            padx=16,
            pady=8,
            cursor="hand2",
            command=submit_goal
        ).pack(anchor="w")

    def open_deposit_goal_dialog(self, goal_id: int, current_amount: float):
        dialog = tk.Toplevel(self)
        dialog.title("Deposit to Goal")
        dialog.geometry("320x220")
        dialog.resizable(False, False)
        dialog.configure(bg=COLOR_CARD_BG)
        dialog.grab_set()

        content = tk.Frame(dialog, bg=COLOR_CARD_BG, padx=20, pady=16)
        content.pack(fill="both", expand=True)

        tk.Label(content, text="Deposit to Savings Goal", font=FONT_SUBTITLE, bg=COLOR_CARD_BG).pack(anchor="w", pady=(0, 10))
        tk.Label(content, text="Deposit Amount (₹):", font=FONT_BOLD, bg=COLOR_CARD_BG).pack(anchor="w")

        dep_entry = tk.Entry(content, font=FONT_BODY)
        dep_entry.pack(fill="x", pady=(2, 16))

        def submit_deposit():
            try:
                amt = float(dep_entry.get().strip())
                if amt <= 0:
                    messagebox.showerror("Error", "Deposit must be greater than zero.", parent=dialog)
                    return
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number.", parent=dialog)
                return

            self.db.update_savings_goal_progress(goal_id, current_amount + amt)
            dialog.destroy()
            self._render_savings(self.pages["savings"])

        tk.Button(
            content,
            text="Confirm Deposit",
            font=FONT_BOLD,
            bg=COLOR_SUCCESS,
            fg="#FFFFFF",
            bd=0,
            padx=14,
            pady=7,
            cursor="hand2",
            command=submit_deposit
        ).pack(anchor="w")
