import sqlite3
import requests
from bs4 import BeautifulSoup as BS
from datetime import datetime
import json


class BD():
    con = sqlite3.connect('data_base.db', check_same_thread=False)  #connect database (bd)
    cursor = con.cursor() 

    def __init__(self):    

        #create table for menu
        BD.cursor.execute('''CREATE TABLE IF NOT EXISTS menu
                            (day int, title text, model text, price text, path text)''') 
        
        self.parse() #start parse from site


    def _set_bd(self, day, title, dish, price, path):
        """ 
            Save item (dish) to bd
            day, title, dish, price, img_path
        """

        query = '''INSERT INTO menu VALUES 
                        (?, ?, ?, ?, ?)'''
        
        BD.cursor.execute(query, (day, title, dish, price, path))
        BD.con.commit()
            

    def get_bd(self, types):
        """ The method checks if the menu is up to date and (return menu or start parse) """
        
        #check day of the week update menu
        with open('date.json', 'r') as date_json:
            day = json.load(date_json)

        #The menu is actually 
        if day == int(self._day()):
            menu = [] 
            #enumeration category (types)
            for type in types:
                for item in BD.cursor.execute(''' SELECT * FROM menu WHERE title = ? ''', (type,)):
                    menu.append( item ) #add item(dish) to menu
            return menu

        #need update menu (start parse and again start this method)
        else:
            self.parse()
            self.get_bd()
        


    def _day(self):
        """ return number today of the week (1-7) """
        today = datetime.today()
        return today.isoweekday()
    
    
    def _save_img(self, item):
        """ parse img, save img and return image path """

        #parse img
        img_url=item.find('img', class_="img-responsive center-block")['src'] #find img_url
        img = requests.get(img_url) #download img
        img_path = 'img\ ' + item.find('h4').get_text(strip = True) + '.jpg' #parse name category img

        #create file and save img
        img_file = open(img_path, 'wb')
        img_file.write(img.content)
        img_file.close()

        #return image path
        return 'img\ ' + item.find('h4').get_text(strip = True) + '.jpg'


    def _clear_bd(self):
        """ Function to clear the table """

        sql_delete_query = """DELETE from menu""" 
        BD.cursor.execute(sql_delete_query)
        BD.con.commit() 

    def parse(self):
        """ Parse menu from site and save it to database """

        self._clear_bd() #clear all database

        r = requests.get("http://eatandmeet.sk/") #connection to the site
        html = BS(r.content, 'html.parser') #parse html code from site

        #id + day for today's menu
        today = str(self._day())  #today of the week (return 1-7)
        id_today = 'day-' + today  
        blok = html.find(id = id_today) 
        items = blok.find_all('div', class_='col-lg-6 col-md-6 col-sm-6') #parse all elements today's menu

        for item in items: #item - dish
            #save img to folder and return path img
            path_img = self._save_img(item)  

            title = item.find('h4').get_text(strip = True)  #find category menu (polievka, sladke,  menu)
            #delete number in title (menu 2 -> menu, polievka 1 -> polievka)
            if ' ' in title: 
                title = title[:title.index(' ')]

            #find composition and price item (dish)
            menu = item.find('p',  class_="desc").get_text(strip = True) 
            price = item.find('span', class_="price").get_text(strip = True)
            price = price.replace("/", " ||  ") #replace 1.50$/1.00$ -> 1.50$ || 1.00$
            
            #save info item and image path to database 
            self._set_bd(today, title, menu, price, path_img) 

        #save today of the week to json-file
        with open('date.json', 'w') as date_json:
            json.dump(int(today), date_json)
        
        #console log
        print ('------ Parse END -------')




if __name__ == '__main__':
    bd = BD()
    bd.parse()
    bd.get_bd()