import sqlite3
import requests
from bs4 import BeautifulSoup as BS
from datetime import datetime
import json


class BD():
    con = sqlite3.connect('data_base.db', check_same_thread=False)
    cursor = con.cursor()

    def __init__(self):    
        BD.cursor.execute('''CREATE TABLE IF NOT EXISTS menu
                            (day int, title text, model text, price text, path text)''')
        
        self.parse()


    def _set_bd(self, day, title, model, price, path):
        
        query = '''INSERT INTO menu VALUES 
                        (?, ?, ?, ?, ?)'''
        print(title)
        BD.cursor.execute(query, (day, title, model, price, path))
        BD.con.commit()
            

    def get_bd(self, types):

        with open('date.json', 'r') as date_json:
            day = json.load(date_json)

        if day == int(self._day()):
            menu = []
            for type in types:
                for item in BD.cursor.execute(''' SELECT * FROM menu WHERE title = ? ''', (type,)):
                    menu.append( item )
            return menu

        else:
            self.parse()
            self.get_bd()
        


    def _day(self):
        today = datetime.today()
        return today.isoweekday()
    
    
    def _save_img(self, item):
        img_url=item.find('img', class_="img-responsive center-block")['src']
        img = requests.get(img_url)
        img_path = 'img\ ' + item.find('h4').get_text(strip = True) + '.jpg'
        img_file = open(img_path, 'wb')
        img_file.write(img.content)
        img_file.close()
        return 'img\ ' + item.find('h4').get_text(strip = True) + '.jpg'

    def _clear_bd(self):
        sql_delete_query = """DELETE from menu"""
        BD.cursor.execute(sql_delete_query)
        BD.con.commit()

    def parse(self):
        self._clear_bd()
        r = requests.get("http://eatandmeet.sk/")
        html = BS(r.content, 'html.parser')
        today = str(self._day())
        id_today = 'day-' + today
        blok = html.find(id = id_today)
        items = blok.find_all('div', class_='col-lg-6 col-md-6 col-sm-6')

        for item in items:
            path_img = self._save_img(item) 
            title = item.find('h4').get_text(strip = True)
            if ' ' in title:
                title = title[:title.index(' ')]
            menu = item.find('p',  class_="desc").get_text(strip = True)
            price = item.find('span', class_="price").get_text(strip = True)
            
            self._set_bd(today, title, menu, price, path_img)   

        with open('date.json', 'w') as date_json:
            json.dump(int(today), date_json)




if __name__ == '__main__':
    bd = BD()
    bd.parse()
    bd.get_bd()