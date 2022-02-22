#PIP INSTALLS
#pip install tkinter
#pip install selenium
#pip install pandas
#pip install xlwt

#IMPORTS
import warnings
import collections
import sys
import time
import tkinter
from tkinter import *
from tkinter import simpledialog
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

#SETUP
warnings.filterwarnings("ignore", category=DeprecationWarning,)
warnings.filterwarnings("ignore", category=FutureWarning)
with open("C:/webdrivers/URLs.txt", "r") as file:
    previous_urls = [line.rstrip('\n') for line in file]
database = []
username = 'user'
password = 'pass'
root = Tk()
root.iconify()
driver = webdriver.Chrome(executable_path="C:/webdrivers/chromedriver.exe")
old_names = []

#GETTING USER INPUT
address = simpledialog.askstring("input string", "Please Enter The Link")
for urls in previous_urls:
    if address in previous_urls:
        tkinter.messagebox.showerror(title=None, message='This URL exists within the previous URL list. Use a new URL or delete the old one from the text file in: "C:/webdrivers/URLs"')
        driver.close()
        sys.exit(0)
liked_by = address + "liked_by/"

#LOGGING IN
driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
time.sleep(1)
driver.find_element(By.NAME, "username").send_keys(username)
driver.find_element(By.NAME, "password").send_keys(password)
driver.find_element(By.NAME, "password").send_keys(u'\ue007')
time.sleep(3)

#NAVIGATING TO PAGE
driver.get(address)
Tk.destroy(self=root)
time.sleep(1)

#OPEN LIST OF USERS WHO HAVE LIKED
element = driver.find_element(By.XPATH, '/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[2]/div/div/div/a')
element.click()
time.sleep(1)

#FIND PEOPLE WHO HAVE LIKED
num_likes = driver.find_element(By.XPATH, '/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[2]/div/div/div/a/div/span').get_attribute('innerHTML').strip()
scroll_box= driver.find_element(By.XPATH,'/html/body/div[6]/div/div')

#DEFINES METHOD TO SCROLL THROUGH THE LIKE BOX
def scroll():
    driver.execute_script('p1 = document.querySelector("body > div.RnEpo.Yx5HN > div > div > div.qF0y9.Igw0E.IwRSH.eGOV_.vwCYk.i0EQd > div")')
    driver.execute_script('p1.scrollBy(0,400)')
    time.sleep(0.3)

#GETTING LIKERS, AND SCROLLING UNTIL END OF PAGE THEN ADDING THE NAMES TO USERS AND THE LINK TO URLs
while True:
    links = scroll_box.find_elements(By.TAG_NAME, 'a')
    names = [name.text for name in links if name.text != '' and name.text not in database]
    if old_names == names:
        break
    database.extend(names)
    scroll()
    old_names = names
with open("C:/webdrivers/Users.txt", "a") as txt_file:
    for line in database:
        txt_file.write(line + "\n")
with open("C:/webdrivers/URLs.txt", "a") as txt_file:
    txt_file.write(address+"\n")
driver.close()

#SORTING
with open("C:/webdrivers/Users.txt", "r") as f:
    text = f.read()

word_freq = collections.Counter(text.lower().split())
with open("C:/webdrivers/Output.txt", "w") as f:
    for word, freq in word_freq.most_common():
        f.write("%s %d\n"%(word, freq))

#CONVERTING TO SPREADSHEET
df = pd.read_csv("C:/webdrivers/Output.txt", header=None, delim_whitespace=True, names=['Username','Occurences'])
df.to_excel(r'C:/webdrivers/InstagramEngagement.xls',index=False, header=None)