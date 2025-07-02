from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import errorcode
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# MySQL connection config (update with your credentials)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Sravanipeddi',  # Change this
    'database': 'budget_db'
}

def get_db_connection(create_db=False):
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        if create_db:
            # Create database if not exists
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        conn.database = DB_CONFIG['database']
        return conn, cursor
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None, None

def create_tables():
    conn, cursor = get_db_connection(create_db=True)
    if conn is None:
        return

    create_table_query = """
    CREATE TABLE IF NOT EXISTS transactions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        description VARCHAR(255),
        amount DECIMAL(10,2),
        category VARCHAR(100),
        date DATE
    )
    """
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()

create_tables()  # Create DB and tables on startup

@app.route('/')
def index():
    conn, cursor = get_db_connection()
    cursor.execute("SELECT description, amount, category, date FROM transactions ORDER BY date DESC")
    transactions = cursor.fetchall()

    # Prepare data for plotting - sum amounts by category
    cursor.execute("SELECT category, SUM(amount) FROM transactions GROUP BY category")
    data = cursor.fetchall()
    categories = [row[0] for row in data]
    amounts = [float(row[1]) for row in data]

    cursor.close()
    conn.close()

    # Create bar chart
    img = io.BytesIO()
    plt.figure(figsize=(8,4))
    plt.bar(categories, amounts, color='skyblue')
    plt.title('Spending by Category')
    plt.ylabel('Amount ($)')
    plt.tight_layout()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('index.html', transactions=transactions, plot_url=plot_url)

@app.route('/add', methods=['POST'])
def add_transaction():
    description = request.form['description']
    amount = request.form['amount']
    category = request.form['category']
    date = request.form['date']

    conn, cursor = get_db_connection()
    cursor.execute(
        "INSERT INTO transactions (description, amount, category, date) VALUES (%s, %s, %s, %s)",
        (description, amount, category, date)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
