import re
from connect import create_connection, close_connection

def new_expense(category, description, price, user_id):
    '''This method adds new expense to table expenses in DB'''
    cnx, cursor = create_connection()
    sql1 = '''
    SELECT cat_id FROM categories 
    WHERE name = %s
    '''
    cursor.execute(sql1, (category,))
    cat_id = cursor.fetchone()[0]
    sql2 = '''
    INSERT INTO expenses (user_id, cat_id, description, price)
    VALUES (%s, %s, %s, %s)
    '''
    cursor.execute(sql2, (user_id, cat_id, description, price))
    change_user_balance(user_id, price, cursor)
    list_of_expenses(1, cursor)
    close_connection(cursor, cnx)

def change_user_balance(user_id, price, cursor, decrease=True):
    '''This method updates users balance, increase amount of money or descrease.'''
    sql = '''
    SELECT balance FROM users
    WHERE id = %s 
    '''
    cursor.execute(sql, (user_id,))
    balance = cursor.fetchone()[0]
    sql = '''
    UPDATE users SET balance = %s
    WHERE id = %s
    '''
    if decrease:
        cursor.execute(sql, (float(balance) - float(price), user_id))
    else: 
        cursor.execute(sql, (float(balance) + float(price), user_id))

def list_of_expenses(user_id, cursor):
    '''This method returns a list of all expenses related with user_id'''
    sql = '''
    SELECT name, categories.cat_id, description, price, expense_id FROM expenses 
    JOIN categories ON expenses.cat_id = categories.cat_id
    WHERE user_id = %s 
    '''
    cursor.execute(sql, (user_id, ))
    payments = []
    payments = cursor.fetchall()
    return payments


def delete_payment(expense_id, cursor):
    '''This method removes expense from table'''
    sql = '''
    DELETE FROM expenses
    WHERE expense_id = %s
    '''
    cursor.execute(sql, (expense_id, ))


def find_expense(name, user_id, cursor):
    '''This method finds one exact match of expense or zero. To find that match 
    method needs params like name, user_id and cursor to execute sql query'''
    pattern = name
    sql = """
    SELECT name, categories.cat_id, description, price, user_id FROM expenses 
    JOIN categories ON expenses.cat_id = categories.cat_id
    WHERE user_id = %s
    """
    cursor.execute(sql, (user_id, ))
    matches = cursor.fetchall()
    for match in matches:
        if re.search(pattern, match[2]) != None:
            print(match)
            return match

def load_user_info(user_id, cursor):
    '''this method returns userfull informations about user like name username and balance'''
    sql = '''
    SELECT name, surname, balance FROM users
    WHERE id = %s
    '''
    cursor.execute(sql, (user_id, ))
    return cursor.fetchone()

  
