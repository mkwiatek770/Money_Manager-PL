from flask import Flask, render_template, request, url_for, redirect
from connect import create_connection, close_connection
from psql_func.psql import new_expense, change_user_balance, list_of_expenses, delete_payment, find_expense, load_user_info
from reports import generate_pdf, generate_xls

app = Flask(__name__)


@app.route('/home', methods=('GET', 'POST'))
@app.route('/', methods=('GET', 'POST'))
def home():
    if request.method == 'GET':
        cnx, cursor = create_connection()
        user_info = load_user_info(1, cursor)
        close_connection(cursor, cnx)
        return render_template("start.html", title="Strona Startowa", name=user_info[0], surname=user_info[1], balance=user_info[2])
    else:
        if request.form['btn'] == 'all_expenses':
            return redirect(url_for('expenses'))
        elif request.form['btn'] == 'add_expense':
            return redirect(url_for('add_expense'))   
        elif request.form['btn'] == 'add_money':
            return redirect(url_for('add_money'))
        else:
            return redirect(url_for('single_expense', name=request.form['exp_txt']))    
        

@app.route('/add_expense', methods=('GET', 'POST'))
def add_expense():
    
    if request.method == 'GET':
        cnx, cursor = create_connection()
        user_info = load_user_info(1, cursor)
        categories = []
        sql = '''
        SELECT name FROM categories
        '''
        cursor.execute(sql)
        for category in cursor:
            categories.append(category)
        close_connection(cnx, cursor)
        return render_template('add.html', title='Dodaj wydatek', categories=categories, name=user_info[0], surname=user_info[1], balance=user_info[2])
    else:
        category = request.form['select']
        description = request.form['description']
        price = request.form['price']
        new_expense(category, description, price, 1)
        return "Dodano wydatek do bazy danych! " + "<a href='{}'>Powrót do strony głównej</a>".format(url_for('home')) 


@app.route('/expenses', methods=('GET', 'POST'))
def expenses():
    if request.method == "GET":
        cnx, cursor = create_connection()
        user_info = load_user_info(1, cursor)
        payments = list_of_expenses(1, cursor)
        close_connection(cursor, cnx)
        return render_template('expenses.html', payments=payments, title="Wszystkie wydatki", name=user_info[0], surname=user_info[1], balance=user_info[2])
    else: 
        if request.form['btn'] == 'xls':
            generate_xls(1)
            return "XLS został wygenerowany " + "<a href='{}'>Powrót do strony głównej</a>".format(url_for('home'))  
        elif request.form['btn'] == 'pdf':
            generate_pdf(1)
            return "Pdf został wygenerowany! " + "<a href='{}'>Powrót do strony głównej</a>".format(url_for('home'))   
        else:
            cnx, cursor = create_connection()
            expense_id = request.form['btn'] 
            delete_payment(expense_id, cursor)
            close_connection(cursor, cnx)
            return "Usunięto płatność! " + "<a href='{}'>Powrót do strony głównej</a>".format(url_for('home'))   


@app.route('/expenses/<string:name>', methods=('GET', 'POST'))
def single_expense(name):
    if request.method == 'GET':
        cnx, cursor = create_connection()
        user_info = load_user_info(1, cursor)
        match = find_expense(name, 1, cursor)
        close_connection(cursor, cnx)
        if match != None:
            return render_template('expense.html', match=match)
        return "Nie znaleziono takiego wydatku! " + "<a href='{}'>Powrót do strony głównej</a>".format(url_for('home'))   
    else:
        cnx, cursor = create_connection()
        expense_id = request.form['btn'] 
        delete_payment(expense_id, cursor)
        close_connection(cursor, cnx)
        return "Usunięto płatność! " + "<a href='{}'>Powrót do strony głównej</a>".format(url_for('home'))     


@app.route('/add_money', methods=('GET', 'POST'))
def add_money():
    if request.method == 'GET':
        cnx, cursor = create_connection()
        user_info = load_user_info(1, cursor)
        close_connection(cursor, cnx)
        return render_template('add_money.html', title="Wpłać gotówkę",name=user_info[0], surname=user_info[1], balance=user_info[2])
    else: 
        money_to_add = int(request.form['amt'])
        if money_to_add > 0:
            cnx, cursor = create_connection()
            change_user_balance(1, money_to_add, cursor, decrease=False)
            close_connection(cursor, cnx)
            return "Wpłacono pieniądze! " + "<a href='{}'>Powrót do strony głównej</a>".format(url_for('home'))
#Naprawić problem z dodawaniem pieniędzy z keyerrorem !!!!


if __name__ == "__main__":
    app.run()
