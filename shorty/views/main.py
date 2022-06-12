from flask import Flask, Blueprint, jsonify,render_template

Main = Blueprint('Main', __name__, template_folder='templates')

@Main.route('/')
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

    return jsonify({"status":"ok"})
