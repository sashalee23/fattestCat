from bs4 import BeautifulSoup
import requests
import asyncio
import webbrowser
import sys

print("""\

    /\_____/\\
   /  o   o  \\
  ( ==  ^  == )
   )         (
  (           )
 ( (  )   (  ) )
(__(__)___(__)__)

""")

print("\nAccessing cat information database (Animal Welfare League Queensland)... \n")

print("Collecting cat profiles...")

URL= "https://www.awlqld.com.au/adopt/animals/cat/"

def getContent(url, id = "et-main-area"):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id=id)
    return results

cat_weights = []
cat_urls=[]
cat_names = []
page_numbers = []


def weighCat(url):
    profile = getContent(url)
    try:
        data = profile.find('p', string=lambda text: "kg" in text.lower())
        cat_weights.append(float(data.contents[0].strip(" kg")))
    except: 
        cat_weights.append(0)

def collectProfiles(content):
    print("...")
    cats= content.find('div', class_='adopt-box')
    for name in cats.find_all('h3'):
        cat_names.append(name.contents[0])
    for link in cats.find_all('a', string='View Details'):
        cat_urls.append(link['href'])

    

    
firstPage=getContent(URL)
collectProfiles(firstPage)
pages=firstPage.find_all('a', class_='page-numbers', href=True)
for a in pages:
    page_numbers.append(a.contents[0])
for i in range(2, int(page_numbers[-2])+1):
    content=getContent(f'{URL}page/{i}/')
    collectProfiles(content)
print(f'\nI found {len(cat_names)} cats for adoption \n')


print("Weighing them...")
# for url in cat_urls, weigh and print their data
for i in range(0, len(cat_urls)):
    weighCat(cat_urls[i])
    print(f'{i+1}. {cat_names[i]} is {cat_weights[i]} kgs \n')

thiccest_in_the_land = cat_weights.index(max(cat_weights,key=lambda x:float(x)))

print('\n\nThe thiccest in the land is...')

print(f'\n~** {cat_names[thiccest_in_the_land]} - {cat_weights[thiccest_in_the_land]}kgs **~ \n')

view = input(f'Would you like to visit {cat_names[thiccest_in_the_land]}\'s profile? \n Type \'y\' to view, or any other key to exit \n \t >')
if view == "y":
    print("Enjoy :)")
    webbrowser.open(cat_urls[thiccest_in_the_land])
else:
    print ("Goodbye")
    exit()