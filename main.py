from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import traceback
import urllib.request
import json
import random
import datetime

from sqlalchemy.orm import sessionmaker
from register import User, Grade, return_sqlalchemysession
from passhasher import hash_string_sha
from pogoda import pobierzpogode

import unittest
from testy import *

# lokalizacja widoków i elementów statystycznych
app = Flask(
  __name__,
  template_folder='templates',
  static_folder='static',
  )

app.secret_key = os.urandom(12)

FILENAME_USER = "user.txt"

@app.route('/')
def home():
  if not session.get('logged_in'):
    return render_template('logowanie.html')
  else:
    return render_template('glowna.html')

# Z formularza z template logowanie, POST
@app.route('/login', methods=["POST"])
def login_user():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    imie = str(POST_USERNAME)
    haslo = str(POST_PASSWORD)
    logged = False

    f = open('user.txt', 'r')
    lines = f.readlines()
    d = 0
    for line in lines:

      a = line.split()
      a[0] = a[0].strip()
      if imie == a[0]:
        b = a[1].strip()
        if haslo == b:
          d +=1

    if d >0:
      logged = True
    try:
      if logged:
        session['logged_in'] = True   
      else:
        # JAK DZIAŁA FLASH https://flask.palletsprojects.com/en/1.1.x/patterns/flashing/
        flash('No user or wrong password provided')
        return render_template('logowanie.html')
    except AttributeError as e:
      flash('No user or wrong password provided')
      #traceback trick to printout the error despite the except
      print(traceback.format_exc())
    return home()

@app.route('/wyloguj')
def wyloguj():
  session['logged_in'] = False
  return "Wylogowano" 

@app.route('/register', methods=['POST', 'GET'])
def do_register():
  POST_USERNAME = str(request.form['username'])
  POST_PASSWORD = str(request.form['password'])

  user = User(POST_USERNAME, POST_PASSWORD)
  

  imie = str(user.username)
  haslo = str(user.password)

  with open(FILENAME_USER , 'a') as writer:
    writer.writelines(imie +" "+ haslo + "\n")
  return home()

@app.route('/signup', methods=["GET"])
def return_registrationpage():
  return render_template('signup.html')

@app.route("/pogoda")
def pokazpogode():
  temp,humid,weathertype,rain,pressure,wind = pobierzpogode()
  return render_template("pogoda.html", temp=temp, humid=humid,weathertype=weathertype, rain=rain, pressure=pressure, wind=wind)

# Propozycja dodatkowego zadania - bootstrap? Przyjrzyj sie temu jak dobrze wyglada ta strona w html
@app.route("/glowna")
def pokazglowna():
  return render_template('glowna.html')

# DODATKOWA FUNKCJA - WYSWIETLANIE LISTY ELEMENTOW W JINJA 2 - oceny
@app.route('/grades', methods=['GET'])
def return_grades():
  #ponizszy kod aby dostepne bylo tylko dla zalogowanych
  # if not session.get('logged_in'):
    # return render_template('login.html')
  # else:
    sqlsession = return_sqlalchemysession()
    grades = sqlsession.query(Grade).all()
    # for x in grades:
      # print ({i.name: getattr(x, i.name) for i in x.__table__.columns})
    return render_template("grades.html", grades=grades)

## Dodawanie nowych ocen (patrz na dol tabelki)
@app.route('/addgrade', methods=['GET'])
def grades():
  # if not session.get('logged_in'):
    # return render_template('login.html')
  # else:
    gradeval = random.choice(['2', '3', '3.5', '4', '4.5', '5'])
    user_id = 99
    added_date = datetime.date.today()
    grade = Grade(gradeval, added_date, user_id)
    sqlsession = return_sqlalchemysession()
    sqlsession.add(grade)
    sqlsession.commit()
    return return_grades()

if __name__ == "__main__":
  app.run(
    host='0.0.0.0',
    port = 8080, debug=True)
  # unittest.main()