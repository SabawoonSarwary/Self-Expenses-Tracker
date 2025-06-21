from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

# Database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database tables
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            month TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()

# Home
@app.route('/')
def index():
    return render_template('index.html')

# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            flash("Please fill in all fields.", "danger")
            return redirect(url_for('register'))
        if password != confirmation:
            flash("Passwords do not match.", "danger")
            return redirect(url_for('register'))

        hash_pw = generate_password_hash(password)

        conn = get_db_connection()
        db = conn.cursor()

        db.execute("SELECT id FROM users WHERE username = ?", (username,))
        if db.fetchone():
            flash("Username already taken.", "danger")
            conn.close()
            return redirect(url_for('register'))

        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_pw))
        conn.commit()
        conn.close()

        flash("Registered successfully! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template("register.html")

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Please fill in both fields.", "danger")
            return redirect(url_for('login'))

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f"Welcome back, {user['username']}!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password.", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    user_id = session['user_id']

    # Query expenses grouped by category
    categories_rows = conn.execute('''
        SELECT category, SUM(amount) as total
        FROM expenses
        WHERE user_id = ?
        GROUP BY category
    ''', (user_id,)).fetchall()

    # Extract labels and values
    expense_labels = [row['category'] for row in categories_rows]
    expense_values = [row['total'] for row in categories_rows]

    # Calculate total expenses
    total_expenses = sum(expense_values)

    # Get current month's budget if any
    current_month = datetime.now().strftime("%Y-%m")
    budget_row = conn.execute(
        "SELECT amount FROM budgets WHERE user_id = ? AND month = ?", (user_id, current_month)
    ).fetchone()

    budget_amount = budget_row['amount'] if budget_row else None
    remaining = budget_amount - total_expenses if budget_amount is not None else None

    conn.close()

    return render_template(
        'dashboard.html',
        expense_labels=expense_labels,
        expense_values=expense_values,
        total_expenses=total_expenses,
        budget_amount=budget_amount,
        remaining=remaining
    )
# Add Expense
@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        amount = request.form.get('amount')
        date = request.form.get('date')

        if not name or not category or not amount or not date:
            flash("Please fill in all fields.", "danger")
            return redirect(url_for('add_expense'))

        try:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO expenses (user_id, name, category, amount, date) VALUES (?, ?, ?, ?, ?)",
                (session['user_id'], name, category, float(amount), date)
            )
            conn.commit()
            conn.close()
            flash("Expense added successfully!", "success")
        except:
            flash("Something went wrong while adding expense.", "danger")

        return redirect(url_for('expense_history'))

    return render_template('add_expense.html')

# Expense History
@app.route('/history', methods=['GET', 'POST'])
def expense_history():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    user_id = session['user_id']

    categories = conn.execute(
        "SELECT DISTINCT category FROM expenses WHERE user_id = ?", (user_id,)
    ).fetchall()

    selected_category = 'All'
    start_date = ''
    end_date = ''
    query = "SELECT * FROM expenses WHERE user_id = ?"
    params = [user_id]

    if request.method == 'POST':
        selected_category = request.form.get('category', 'All')
        start_date = request.form.get('start_date', '')
        end_date = request.form.get('end_date', '')

        if selected_category != 'All':
            query += " AND category = ?"
            params.append(selected_category)

        if start_date:
            query += " AND date >= ?"
            params.append(start_date)

        if end_date:
            query += " AND date <= ?"
            params.append(end_date)

    query += " ORDER BY date DESC"

    expenses = conn.execute(query, params).fetchall()
    conn.close()

    return render_template(
        'history.html',
        expenses=expenses,
        categories=categories,
        selected_category=selected_category,
        start_date=start_date,
        end_date=end_date
    )

# Budget
@app.route('/budget', methods=['GET', 'POST'])
def budget():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()

    if request.method == 'POST':
        month = request.form.get('month')
        amount = request.form.get('amount')

        if not month or not amount:
            flash("Please provide both month and amount.", "danger")
            return redirect(url_for('budget'))

        existing = conn.execute(
            "SELECT id FROM budgets WHERE user_id = ? AND month = ?", (session['user_id'], month)
        ).fetchone()

        if existing:
            conn.execute("UPDATE budgets SET amount = ? WHERE id = ?", (float(amount), existing['id']))
        else:
            conn.execute("INSERT INTO budgets (user_id, month, amount) VALUES (?, ?, ?)",
                         (session['user_id'], month, float(amount)))

        conn.commit()
        flash("Budget saved successfully.", "success")
        return redirect(url_for('budget'))

    current_month = datetime.now().strftime("%Y-%m")
    budget = conn.execute(
        "SELECT amount FROM budgets WHERE user_id = ? AND month = ?", (session['user_id'], current_month)
    ).fetchone()

    total_spent = conn.execute(
        "SELECT SUM(amount) as total FROM expenses WHERE user_id = ? AND strftime('%Y-%m', date) = ?",
        (session['user_id'], current_month)
    ).fetchone()

    conn.close()

    total_spent_value = total_spent['total'] if total_spent and total_spent['total'] else 0
    budget_amount = budget['amount'] if budget else None
    remaining = budget_amount - total_spent_value if budget else None

    return render_template('budget.html', budget=budget, total_spent=total_spent_value,
                           remaining=remaining, current_month=current_month)

# Edit Expense
@app.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    expense = conn.execute(
        "SELECT * FROM expenses WHERE id = ? AND user_id = ?", (expense_id, session['user_id'])
    ).fetchone()

    if not expense:
        conn.close()
        return "Expense not found or unauthorized", 404

    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        amount = request.form.get('amount')
        date = request.form.get('date')

        if not name or not category or not amount or not date:
            flash("Please fill in all fields.", "danger")
            return redirect(url_for('edit_expense', expense_id=expense_id))

        conn.execute(
            "UPDATE expenses SET name = ?, category = ?, amount = ?, date = ? WHERE id = ? AND user_id = ?",
            (name, category, float(amount), date, expense_id, session['user_id'])
        )
        conn.commit()
        conn.close()
        flash("Expense updated successfully.", "success")
        return redirect(url_for('expense_history'))

    conn.close()
    return render_template('edit_expense.html', expense=expense)

# Delete Expense
@app.route('/delete/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    conn.execute("DELETE FROM expenses WHERE id = ? AND user_id = ?", (expense_id, session['user_id']))
    conn.commit()
    conn.close()
    flash("Expense deleted successfully.", "success")
    return redirect(url_for('expense_history'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)