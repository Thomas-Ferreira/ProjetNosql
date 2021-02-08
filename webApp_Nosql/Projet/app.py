import requests
from flask import Flask, request, render_template, url_for, jsonify
import json
import re
import dns
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('form.html')

@app.route('/api')
def api():
    return render_template("register.html")

@app.route('/new_entry', methods=['POST', 'GET'])
def connect():
    if request.method == 'POST':
        Title=str(request.form["Titre"])
        item = 0 
        client = MongoClient("mongodb+srv://user1:root@cluster0.iw7et.mongodb.net/ProjetNosql?retryWrites=true&w=majority")
        db = client.ProjetNosql
        films=db.Films

        reponse = films.find({"Title": Title},{"Title":1})
        log=0
        for log in reponse:
            log

        if log != 0:
            error = 'Film déjà present sur notre site.'
            pageWeb = "form.html"
        else:
            error = 'film ajouté'
            pageWeb = "reponse.html"

            while item < len(Title):
                if Title[item] == " ":
                    Title.replace(" ","+")
                item += 1
            res=requests.get('http://www.omdbapi.com/?apikey=27de6cde&t=%s'%(Title))
            json_item = json.loads(res.text)
            films.insert_one(json_item)

        
        return render_template(pageWeb, error=error)


@app.route('/find_movie',methods=['POST', 'GET'])
def find_movie():
    if request.method == 'POST':
        movie_title=request.form["Titre"]
        client = MongoClient("mongodb+srv://user1:root@cluster0.iw7et.mongodb.net/ProjetNosql?retryWrites=true&w=majority")
        db = client.ProjetNosql
        films=db.Films
        
        items = list(films.find({"Title":movie_title}))

        reponse = {items[1]}

    return render_template("form.html", reponse=reponse)

if __name__ == '__main__':
    app.run(debug=True)



