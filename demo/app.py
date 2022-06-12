from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import json
import requests
import pyshorteners
from hashlib import sha256
import socket
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/yuzarsif/Desktop/software-engineer-task-master/app/demo/app/links.db'
db = SQLAlchemy(app)
@app.route("/")
def index():
    links = Links.query.all()
    """
    [
        {
            "id":1, 
            "link":"example.com", 
            "short_link":"bit.ly/example | tinyurl.com/exapmle", 
            "gen_token":"0000000xa036944e29568d0cff17edbe038f81208fecf9a66be9a2b8321c6ec7"
        }
    ]
    """

    return render_template("index.html", Links_option=[{'Links': 'Bitly'}, {'Links': 'Tinyurl'}], links = links)


@app.route("/add", methods=['POST'])
def addLink():
    Link_Option = request.form.get("Links_option")
    Link = request.form.get("input_link")
    
    #Generate Shorter link
    if Link_Option == 'Bitly':
        s = pyshorteners.Shortener(api_key='99b778a91b033bb2557f85a50dc245e99ea94798')
        Link_shorter = s.bitly.short(Link)

    else:
        res = requests.get('https://tinyurl.com/api-create.php?url=' + Link)
        Link_shorter = res.text

    newLink = Links(link = Link, short_link = str(Link_shorter), gen_token = False, gen_token_key = "0", Value_Nonce = 0)

    db.session.add(newLink)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/create_token/<string:id>")
def createToken(id):
    link = Links.query.filter_by(id=id).first()
    if (link.gen_token == False):
        link.gen_token = True
        data = f"""{[
            {
                "id":link.id, 
                "link":link.link, 
                "short_link":link.short_link, 
                "gen_token":"0000000xa036944e29568d0cff17edbe038f81208fecf9a66be9a2b8321c6ec7"
            }
        ]}"""
        def SHA256(text):
            return sha256(text.encode("ascii")).hexdigest()
        def mine(block_number, transactions, previous_hash, prefix_zeros):
            prefix_str = '0'*prefix_zeros
            for nonce in range(MAX_NONCE):
                text = str(block_number) + transactions + previous_hash + str(nonce)
                new_hash = SHA256(text)
                if new_hash.startswith(prefix_str):
                    print(f"Yay! Successfully mined bitcoins with nonce value:{nonce}")
                    nonce_data.append(int(nonce))
                    return new_hash

            raise BaseException(f"Couldn't find correct has after trying {MAX_NONCE} times")

        nonce_data = []
        transactions=data
        difficulty=link.id # try changing this to higher number and you will see it will take more time for mining as difficulty increases                
        import time
        start = time.time()
        new_hash = mine(link.id,transactions,'0000000xa036944e29568d0cff17edbe038f81208fecf9a66be9a2b8321c6ec7', difficulty)
        total_time = str((time.time() - start))
        mine_info = f"end mining. Mining took: {total_time} seconds"
        link.gen_token_key = str(new_hash)
        link.Value_Nonce = nonce_data[0]
            
    else:
        url = link.link
        # making requests instance
        reqs = requests.get(url)
        # using the BeautifulSoup module
        soup = BeautifulSoup(reqs.text, 'html.parser')
        for title in soup.find_all('title'):
            title.get_text()
        title_html = title.get_text()
        data2 = {
            "url" : f"{link.link}",
            "link" : f"{link.short_link}"
        }
        json_data = json.dumps(data2)
        return render_template("detail.html", link=link, title_html=title_html, json_data=json_data)
    
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def deleteTodo(id):
     link = Links.query.filter_by(id=id).first()
     db.session.delete(link)
     db.session.commit()

     return redirect(url_for("index"))


MAX_NONCE=100000000000000

class Links(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    link = db.Column(db.String(80))
    short_link = db.Column(db.Text)
    gen_token = db.Column(db.Boolean)
    gen_token_key = db.Column(db.Text)
    Value_Nonce = db.Column(db.Integer)

if __name__ == "__main__":
    app.run(debug=True)