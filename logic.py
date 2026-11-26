"""
=============================================================================
STUDENT PERSONAL FINANCE MANAGER - LOGIC & ANALYTICS MODULE
=============================================================================
Course: Computational Thinking and Programming (2026CSAE100)
Bennett University
Author / Lead: Mohammad Huzaif Khaja Khan (S26CSEU0971) - Logic & Analysis
Integrated with: Rehan Hussain (Frontend) & Arpeet Chahal (Database)

Core Responsibilities:
1. Pure Computational Thinking Algorithms (No GUI code, No direct SQL queries)
2. Statistical Analysis using Python's 'statistics' module (Mean, Median, Stdev)
3. Budget Calculations, Velocity Tracking & Rule-Based Alerts (<80%, 80-100%, >100%)
4. Category Breakdown, Percentage Contributions & Pattern Recognition
5. Rule-Based Financial Insights & Outlier Detection
6. Savings Goal Projections & Feasibility Forecast
7. Robust CSV File Export with UTF-8 BOM encoding
=============================================================================
"""

import csv
import calendar
import statistics
from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Dict, Tuple, Any, Optional


# -----------------------------------------------------------------------------
# 1. INPUT VALIDATION ALGORITHM (Mohammad Huzaif)
# -----------------------------------------------------------------------------
def validate_expense(date_str: str, category: str, amount_str: str, description: str) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Validates user input with defensive exception handling before database insertion.
    Demonstrates: Abstraction & Decision Making.
    """
    # 1. Date format validation (YYYY-MM-DD)
    try:
        parsed_date = datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
    except ValueError:
        return False, "Invalid Date format! Please use YYYY-MM-DD (e.g., 2026-10-14).", {}

    # 2. Category domain validation
    valid_categories = ["Food", "Transport", "Education", "Entertainment", "Shopping", "Hostel", "Other"]
    clean_cat = category.strip()
    if clean_cat not in valid_categories:
        return False, f"Invalid category! Must be one of: {', '.join(valid_categories)}", {}

    # 3. Numeric Amount validation
    try:
        amount = float(amount_str.strip())
        if amount <= 0:
            return False, "Expense amount must be a positive number greater than 0.", {}
        if amount > 1000000:
            return False, "Amount exceeds realistic college threshold (₹1,000,000).", {}
    except ValueError:
        return False, "Amount must be a valid numeric number.", {}

    # 4. Description normalization
    desc = description.strip()
    if not desc:
        desc = f"{clean_cat} expense"

    cleaned_data = {
        "date": parsed_date.strftime("%Y-%m-%d"),
        "category": clean_cat,
        "amount": round(amount, 2),
        "description": desc
    }
    return True, "", cleaned_data


# -----------------------------------------------------------------------------
# 2. BUDGET CALCULATIONS & RULE-BASED ALERTS (Section 7.4 & 7.9)
# -----------------------------------------------------------------------------
def calculate_budget_summary(monthly_budget: float, expenses: List[Dict[str, Any]], ref_date: datetime.date = None) -> Dict[str, Any]:
    """
    Computes total expenditure, remaining allowance, budget consumption percentage,
    and rule-based status alerts.
    Also calculates recommended daily spending limit for remaining days in the month.
    """
    if ref_date is None:
        ref_date = datetime.now().date()

    total_spent = sum(float(e["amount"]) for e in expenses)
    remaining = float(monthly_budget) - total_spent

    if monthly_budget > 0:
        used_percentage = (total_spent / monthly_budget) * 100.0
    else:
        used_percentage = 0.0

    # Rule-Based Alert Engine (Section 7.9)
    if used_percentage >= 100.0:
        status = "EXCEEDED"
        alert_title = "CRITICAL ALERT"
        alert_msg = f"Budget exceeded by ₹{abs(remaining):,.2f}! Immediate freeze on non-essential spending."
        alert_color = "#EF4444"  # Red
        badge_bg = "#FEE2E2"
    elif used_percentage >= 80.0:
        status = "WARNING"
        alert_title = "BUDGET WARNING"
        alert_msg = f"Approaching limit: {used_percentage:.1f}% consumed. Only ₹{remaining:,.2f} remaining."
        alert_color = "#F59E0B"  # Amber
        badge_bg = "#FEF3C7"
    else:
        status = "NORMAL"
        alert_title = "ON TRACK"
        alert_msg = f"Spending within normal range ({used_percentage:.1f}% used). Remaining: ₹{remaining:,.2f}."
        alert_color = "#10B981"  # Emerald Green
        badge_bg = "#D1FAE5"

    # Computational Thinking: Daily spending burn-rate and safe daily cap
    _, total_days_in_month = calendar.monthrange(ref_date.year, ref_date.month)
    days_passed = max(1, ref_date.day)
    days_left = max(1, total_days_in_month - days_passed + 1)

    daily_burn_rate = total_spent / days_passed
    recommended_daily_cap = max(0.0, remaining / days_left) if remaining > 0 else 0.0

    return {
        "monthly_budget": float(monthly_budget),
        "total_spent": round(total_spent, 2),
        "remaining": round(remaining, 2),
        "used_percentage": round(used_percentage, 1),
        "status": status,
        "alert_title": alert_title,
        "alert_message": alert_msg,
        "alert_color": alert_color,
        "badge_bg": badge_bg,
        "daily_burn_rate": round(daily_burn_rate, 2),
        "recommended_daily_cap": round(recommended_daily_cap, 2),
        "days_remaining_in_month": days_left
    }


# -----------------------------------------------------------------------------
# 3. TIME-BASED VELOCITY TRACKING (Section 7.6)
# -----------------------------------------------------------------------------
def get_time_summary(expenses: List[Dict[str, Any]], ref_date: datetime.date = None) -> Dict[str, Any]:
    """
    Computes Today's, This Week's, and This Month's spending using date arithmetic.
    """
    if ref_date is None:
        ref_date = datetime.now().date()

    today_str = ref_date.strftime("%Y-%m-%d")
    week_start = ref_date - timedelta(days=ref_date.weekday())  # Monday of current week
    current_month_prefix = ref_date.strftime("%Y-%m")

    today_spent = 0.0
    week_spent = 0.0
    month_spent = 0.0

    for exp in expenses:
        try:
            exp_date = datetime.strptime(str(exp["expense_date"]), "%Y-%m-%d").date()
        except ValueError:
            continue

        amt = float(exp["amount"])

        # 1. Today
        if exp_date == ref_date:
            today_spent += amt

        # 2. This Week (Monday to current day)
        if week_start <= exp_date <= ref_date:
            week_spent += amt

        # 3. This Month
        if str(exp["expense_date"]).startswith(current_month_prefix):
            month_spent += amt

    return {
        "today": round(today_spent, 2),
        "this_week": round(week_spent, 2),
        "this_month": round(month_spent, 2)
    }


# -----------------------------------------------------------------------------
# 4. CATEGORY ANALYSIS & PATTERN RECOGNITION (Section 7.7)
# -----------------------------------------------------------------------------
def get_category_summary(expenses: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Computes totals and percentage contributions per category.
    Identifies highest spending category (Pattern Recognition).
    """
    if not expenses:
        return {
            "totals": {},
            "percentages": {},
            "highest_category": "None",
            "highest_amount": 0.0,
            "highest_percentage": 0.0,
            "total_expenses_count": 0
        }

    totals = defaultdict(float)
    total_spent = 0.0

    for exp in expenses:
        amt = float(exp["amount"])
        cat = exp["category"]
        totals[cat] += amt
        total_spent += amt

    # Find highest category
    highest_cat = max(totals, key=totals.get)
    highest_amt = totals[highest_cat]
    highest_pct = (highest_amt / total_spent * 100.0) if total_spent > 0 else 0.0

    percentages = {}
    for cat, amt in totals.items():
        percentages[cat] = round((amt / total_spent * 100.0), 1) if total_spent > 0 else 0.0

    # Sort descending
    sorted_totals = dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))

    return {
        "totals": sorted_totals,
        "percentages": percentages,
        "highest_category": highest_cat,
        "highest_amount": round(highest_amt, 2),
        "highest_percentage": round(highest_pct, 1),
        "total_expenses_count": len(expenses)
    }


# -----------------------------------------------------------------------------
# 5. STATISTICAL ANALYSIS ENGINE (Python 'statistics' library)
# -----------------------------------------------------------------------------
def calculate_spending_statistics(expenses: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Applies standard statistical measures to transaction records.
    Demonstrates practical use of Python's standard 'statistics' library.
    """
    if not expenses:
        return {
            "count": 0,
            "mean": 0.0,
            "median": 0.0,
            "stdev": 0.0,
            "min_transaction": 0.0,
            "max_transaction": 0.0
        }

    amounts = [float(e["amount"]) for e in expenses]

    mean_val = statistics.mean(amounts)
    median_val = statistics.median(amounts)
    stdev_val = statistics.stdev(amounts) if len(amounts) >= 2 else 0.0
    min_val = min(amounts)
    max_val = max(amounts)

    return {
        "count": len(amounts),
        "mean": round(mean_val, 2),
        "median": round(median_val, 2),
        "stdev": round(stdev_val, 2),
        "min_transaction": round(min_val, 2),
        "max_transaction": round(max_val, 2)
    }


# -----------------------------------------------------------------------------
# 6. RULE-BASED SPENDING INSIGHTS & OUTLIER DETECTION (Section 7.10)
# -----------------------------------------------------------------------------
def get_rule_based_insights(budget_summary: Dict[str, Any],
                            category_summary: Dict[str, Any],
                            time_summary: Dict[str, Any],
                            expenses: Optional[List[Dict[str, Any]]] = None) -> List[str]:
    """
    Rule-based financial recommendations and spending behavior patterns.
    Clean, deterministic if-elif-else logic with zero black-box ML.
    """
    insights = []
    highest_cat = category_summary.get("highest_category")
    highest_pct = category_summary.get("highest_percentage", 0.0)
    highest_amt = category_summary.get("highest_amount", 0.0)
    used_pct = budget_summary.get("used_percentage", 0.0)
    remaining = budget_summary.get("remaining", 0.0)
    daily_cap = budget_summary.get("recommended_daily_cap", 0.0)

    # Rule 1: Category Dominance (>35% of total spend)
    if highest_cat and highest_cat != "None":
        insights.append(
            f"🔍 Category Concentration: {highest_cat} is your single largest expense, totaling ₹{highest_amt:,.2f} ({highest_pct}% of total spending)."
        )
        if highest_pct >= 35.0:
            insights.append(
                f"💡 Category Cap Tip: Because {highest_cat} takes over a third of your allowance, try setting a weekly sub-budget for it."
            )

    # Rule 2: Budget Health & Daily Run-Rate
    if used_pct >= 85.0:
        insights.append(
            f"⚠️ Budget Alert: You have exhausted {used_pct}% of your budget. Maintain a strict daily spending cap of ₹{daily_cap:,.2f} for the remaining days."
        )
    elif used_pct < 50.0 and category_summary.get("total_expenses_count", 0) > 0:
        insights.append(
            f"✅ Budget Health: Great financial discipline! You have spent only {used_pct}% of your budget, leaving room to fund your savings goals."
        )

    # Rule 3: Weekly Pace Run-Rate
    week_spent = time_summary.get("this_week", 0.0)
    monthly_budget = budget_summary.get("monthly_budget", 10000.0)
    ideal_weekly_pace = monthly_budget / 4.0 if monthly_budget > 0 else 2500.0

    if week_spent > ideal_weekly_pace:
        insights.append(
            f"📈 Weekly Pace Warning: This week's spending (₹{week_spent:,.2f}) exceeded the target average weekly allowance (₹{ideal_weekly_pace:,.2f})."
        )

    # Rule 4: Outlier Detection (Transactions > 2.5x Mean)
    if expenses and len(expenses) >= 3:
        stats = calculate_spending_statistics(expenses)
        threshold = stats["mean"] * 2.2
        large_txns = [e for e in expenses if float(e["amount"]) > threshold]
        if large_txns:
            highest_txn = large_txns[0]
            insights.append(
                f"⚡ Outlier Detected: Transaction '{highest_txn.get('description', '')}' (₹{float(highest_txn['amount']):,.2f}) is significantly above your average transaction of ₹{stats['mean']:,.2f}."
            )

    if not insights:
        insights.append("📊 Record additional daily transactions to generate custom spending recommendations.")

    return insights


# -----------------------------------------------------------------------------
# 7. SAVINGS GOALS FEASIBILITY PROJECTION (Section 7.8)
# -----------------------------------------------------------------------------
def calculate_savings_projections(goals: List[Dict[str, Any]], remaining_monthly_budget: float) -> List[Dict[str, Any]]:
    """
    Calculates progress percentage, remaining deficit, and estimated months to achieve
    each goal based on unspent monthly allowance.
    """
    projections = []
    for g in goals:
        target = float(g.get("target_amount", 0.0))
        current = float(g.get("current_amount", 0.0))
        deficit = max(0.0, target - current)
        pct = (current / target * 100.0) if target > 0 else 0.0

        if deficit == 0:
            est_months = 0
            feasibility_text = "Goal Achieved! 🎉"
        elif remaining_monthly_budget > 0:
            est_months = max(1, round(deficit / remaining_monthly_budget, 1))
            feasibility_text = f"~{est_months} months at current surplus rate"
        else:
            est_months = None
            feasibility_text = "Requires budget surplus"

        projections.append({
            "goal_id": g.get("goal_id"),
            "goal_name": g.get("goal_name"),
            "target": target,
            "current": current,
            "deficit": deficit,
            "progress_pct": round(pct, 1),
            "feasibility_text": feasibility_text
        })
    return projections


# -----------------------------------------------------------------------------
# 8. SEARCH & FILTERING ENGINE (Section 7.12)
# -----------------------------------------------------------------------------
def filter_expenses(expenses: List[Dict[str, Any]],
                    category_filter: str = "All",
                    month_filter: str = "All",
                    search_query: str = "") -> List[Dict[str, Any]]:
    """
    Filters expense records by category, month (YYYY-MM), and text query.
    Demonstrates clean list comprehensions and string processing.
    """
    filtered = []
    search_lower = search_query.strip().lower()

    for exp in expenses:
        # Category check
        if category_filter != "All" and exp["category"] != category_filter:
            continue

        # Month check (expense_date: YYYY-MM-DD)
        if month_filter != "All" and not str(exp["expense_date"]).startswith(month_filter):
            continue

        # Search query check (matches description, category, or amount)
        if search_lower:
            desc_match = search_lower in exp.get("description", "").lower()
            cat_match = search_lower in exp.get("category", "").lower()
            amt_match = search_lower in str(exp.get("amount", ""))
            if not (desc_match or cat_match or amt_match):
                continue

        filtered.append(exp)

    return filtered


# -----------------------------------------------------------------------------
# 9. CSV FILE EXPORT (Section 7.13)
# -----------------------------------------------------------------------------
def export_to_csv(expenses: List[Dict[str, Any]], filepath: str) -> Tuple[bool, str]:
    """
    Exports expense records to a clean CSV file using Python's standard csv module.
    Uses 'utf-8-sig' for native compatibility with Microsoft Excel.
    """
    if not filepath:
        return False, "Filepath is empty."

    try:
        with open(filepath, mode="w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            # Write Header
            writer.writerow(["Expense ID", "Date", "Category", "Amount (INR)", "Description"])
            # Write Data Rows
            for exp in expenses:
                writer.writerow([
                    exp.get("expense_id", ""),
                    exp.get("expense_date", ""),
                    exp.get("category", ""),
                    f"{float(exp.get('amount', 0)):.2f}",
                    exp.get("description", "")
                ])
        return True, f"Successfully exported {len(expenses)} records to CSV."
    except Exception as e:
        return False, f"Failed to export CSV: {str(e)}"
