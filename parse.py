import bd
import requests
from bs4 import BeautifulSoup as BS
from datetime import datetime


def save_img(item):
    img_url=item.find('img', class_="img-responsive center-block")['src']
    img = requests.get(img_url)
    img_path = 'img\ ' + item.find('h4').get_text(strip = True) + '.jpg'
    img_file = open(img_path, 'wb')
    img_file.write(img.content)
    img_file.close()
    return 'img\ ' + item.find('h4').get_text(strip = True) + '.jpg'


def day():
    today = datetime.today()
    return today.isoweekday()


def print_menu(count):
    message_menu = ''
    for item in count:
        for countent in item.values():
            message_menu += countent + '\n'
        message_menu += '\n'
    
    return message_menu


def parse():
    r = requests.get("http://eatandmeet.sk/")
    html = BS(r.content, 'html.parser')

    id_today = 'day-' + str(day())
    blok = html.find(id = id_today)
    items = blok.find_all('div', class_='col-lg-6 col-md-6 col-sm-6')

    for item in items:
        path_img = save_img(item) 
        title = item.find('h4').get_text(strip = True)
        menu = item.find('p',  class_="desc").get_text(strip = True)
        price = item.find('span', class_="price").get_text(strip = True)
        
        bd.set_bd(title, menu, price, path_img)
    


if __name__ == '__main__':
    print(parse())
    bd.output_bd()