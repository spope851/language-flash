from re import M
import requests
import string
from bs4 import SoupStrainer, BeautifulSoup
import json
alphabet_string = string.ascii_lowercase
alph = list(alphabet_string)

links=[]
def listToString(s):  
    str1 = ""  
    for ele in s:  
        str1 += str(ele)   
    return str1
 
url = "https://en.wiktionary.org/wiki/Appendix:Mandarin_Frequency_lists/1-1000"
FILE = 'words.json'

words = []
r = requests.get(url)
data = r.text
wikitable = SoupStrainer('table')
soup = BeautifulSoup(data, 'html.parser', parse_only=wikitable)
rows = soup.find_all('tr')

'''
    in future you can reverse the remove_files filter to get all the audio from the wiki and use it to study
'''
remove_files = list(filter(lambda row: len(row) != 3, rows))

for row in remove_files:
    items = list(filter(lambda item: item != '\n', row.contents))
    meaning = str(items[3].text).split()
    meaning.pop()
    words.append({
        'traditional': items[0].text,
        'simplified': items[1].text,
        'pinyin': items[2].text,
        'meaning': " ".join(meaning),
    })

handle = open(FILE, "w", encoding='utf8')
json.dump(words, handle, indent=6, ensure_ascii=False)
handle.close()