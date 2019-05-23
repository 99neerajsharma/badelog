#library imports

import requests
from bs4 import BeautifulSoup

#collecting page
page = requests.get("https://insite.iitmandi.ac.in/directory/students/btech2017.php")

#Beautiful Soup Object
soup = BeautifulSoup(page.text , 'lxml')

table_list = soup.select('tr')
heading_list=table_list[8].select('th')
contact_list=table_list[9].select('td')
#table_list[8] has
#soup.getText()
print(contact_list)
