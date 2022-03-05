import sqlite3
import parse


con = sqlite3.connect('data_base.db')
cursor = con.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS menu
                    (title text, model text, price text, path text)''')


def set_bd(title, model, price, path):
    
    query = '''INSERT INTO menu VALUES 
                    (?, ?, ?, ?)'''
    
    cursor.execute(query, (title, model, price, path))
    con.commit()
        
def output_bd():
    for row in cursor.execute(''' SELECT * FROM menu'''):
            print(row)
        
