#library imports
from bs4 import BeautifulSoup
import csv
import requests

#collecting page
page = requests.get("https://insite.iitmandi.ac.in/directory/students/btech2017.php")

#Beautiful Soup Object
soup = BeautifulSoup(page.text , 'lxml')

new_list=[]
row_list=[]
heading=[]

table_list = soup.select('tr')
heading_list=table_list[8].select('h5')

for x in heading_list:
    heading.append(x.text)

i=0
for contact_list in table_list[9:] :
    i+=1

for j in range(9,(9+i-1)) :
    x = table_list[j].select('td')
    for y in x:
        row_list.append(y.text)
    new_list.append(row_list)
    row_list=[]

#Writing into CSV file
f = csv.writer(open('btech2017.csv', 'w'))
f.writerow(heading)

for row in new_list:
    f.writerow(row)
