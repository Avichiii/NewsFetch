import urllib.request, urllib.parse
import ssl
import json
import sqlite3

conn = sqlite3.connect('news.sqlite')
cur = conn.cursor()

cur.executescript('''
    CREATE TABLE IF NOT EXISTS Category (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        catagory TEXT      
    );
                  
    CREATE TABLE IF NOT EXISTS News (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        title TEXT,
        description TEXT,
        sourceurl TEXT,
        imageurl TEXT
    );
''')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


API_KEY = '2e699f13ae5975daa94a97f277689be3'
END_POINT = 'https://gnews.io/api/v4/top-headlines?'


print('''
    Available Categories are =>
        >>> general, 
        >>> world, 
        >>> nation, 
        >>> business, 
        >>> technology, 
        >>> entertainment, 
        >>> sports, 
        >>> science
        >>> health
''')

inp = input('Enter category <: ').lower()
if inp == '':
    inp = 'general'

param = {}
param['category'] = inp
param['lang'] = 'en'
param['max'] = 10
param['apikey'] = API_KEY

url = END_POINT + urllib.parse.urlencode(param)
print(url)
data = urllib.request.urlopen(url).read().decode()

try:
    js = json.loads(data)
except:
    print('There is something wrong with the query')
    exit(0)

if js['totalArticles'] == 0:
    print('There are no Articles available')
    exit(0)

articles = js['articles']
count = 1
for article in articles:
        title = article['title']
        description = article['description']
        sourceurl = article['url']
        imageurl = article['image']

        # print((title, description, sourceurl, imageurl))

        if imageurl == '': imageurl = 'None'
        try:
            cur.execute('SELECT id FROM News WHERE sourceurl = ?', (sourceurl,))
            row = cur.fetchone()

            if row is None:
                cur.execute('''INSERT OR IGNORE INTO News 
                    (title, description, sourceurl, imageurl) values (?,?,?,?)''', 
                    (title, description, sourceurl, imageurl))    
                
                print(f'''
                    saving {count} article to the database...
                    >>> title => {title}    
                    ''')

            else:
                pass
            
            count += 1

        except Exception as e:
            print(f'An exception has occured => {e}')
            exit(0)

conn.commit()
cur.close()

print('Program has finished.')


