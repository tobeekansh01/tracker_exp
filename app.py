from flask import Flask, render_template, request , redirect
import sqlite3 # Built-in Python library for databases

app = Flask(__name__)

def init_db():
    # Connect to the database file (it creates it if it doesn't exist)
    conn = sqlite3.connect('tracker_db')
    cursor= conn.cursor()
    # Create the table using SQL commands if it isn't already there
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            amount REAL NOT NULL,
            item_type TEXT NOT NULL
            )
    ''')
    conn.commit()
    conn.close()
 # Run the database setup function right when the app starts
init_db()           



# We add methods=['GET', 'POST'] so this URL can both show the page and receive form data
@app.route('/' , methods =['GET','POST'])
def home():
    # 1. Grab the data from the HTML form using the 'name' attributes we just made
    if request.method == 'POST':
        name = request.form.get('item_name')
        amount = request.form.get('amount')
        item_type = request.form.get('item_type')
        #connect to database and insert the new row
        conn = sqlite3.connect('tracker_db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO expenses(item_name,amount,item_type) VALUES(?,?,?)',(name,amount,item_type)

        )
        conn.commit()
        conn.close()
        return redirect('/')
    # For GET requests: Fetch all expenses from the database file
    conn = sqlite3.connect('tracker_db')
    cursor=conn.cursor()
    cursor.execute('SELECT item_name,amount,item_type, ID FROM expenses')
    rows= cursor.fetchall()# Grabs all rows as a list of tuples
    conn.close()
    db_expenses=[]
    for row in rows:
        db_expenses.append({
            'name':row[0],
            'amount':row[1],
            'type':row[2],
            'ID':row[3]
        })
    return render_template('index.html', expenses=db_expenses)

              
@app.route('/delete/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    conn = sqlite3.connect('tracker_db')
    cursor = conn.cursor()
    # Execute the SQL command to delete the row matching the specific ID
    cursor.execute('DELETE FROM expenses WHERE ID = ?', (expense_id,))
    conn.commit()
    conn.close()
    return redirect('/')
if __name__ == '__main__':
    app.run(debug=True)