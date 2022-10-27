import unittest
import random

class Test_uzytkownicy(unittest.TestCase):
  def test_sprawdz_dodawanie_takiej_samej_nazwy_uzytkownika(self):
    FILENAME_USER = "user.txt"
    imie = "test"
    haslo = str(round((random.random())*10000))
    with open(FILENAME_USER , 'a') as writer:
      writer.writelines(imie +" "+ haslo + "\n")
      writer.close()
    haslo = str(round((random.random())*10000))
    with open(FILENAME_USER , 'a') as writer:
      writer.writelines(imie +" "+ haslo + "\n")
      writer.close()

    f = open('user.txt', 'r')
    lines = f.readlines()
    d = 0
    for line in lines:
      a = line.split()
      a[0] = a[0].strip()
      if "test" == a[0]:
        d += 1
    f.close()
    self.assertGreater(2, d,"Dodano wiecej niz jedengo uzytkownika o tej samej nazwie")


# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from main import home
# from selenium.webdriver.chrome.options import Options
# driver = webdriver.Chrome(options=chrome_options)

# import os

# def test_przekierowania_do_weather():
#   home.session['logged_in'] = True 
#   driver.get("https://zadanieflask.kacpop.repl.co/login")
#   submitbutton = driver.find_element_by_xpath()