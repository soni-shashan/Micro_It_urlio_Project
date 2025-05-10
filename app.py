from flask import Flask,render_template,redirect, request,url_for,render_template_string
from flask_pymongo import PyMongo
import os
import hashlib
from datetime import datetime


app=Flask(__name__)
app.config['SECRET_KEY']=os.urandom(24)

app.config["MONGO_URI"] = "mongodb+srv://SHASHAN_LUMBHANI:ERt5Hk7Lu6u9GiNb@tpc.0cuhjqj.mongodb.net/linkly?retryWrites=true&w=majority"

mongo=PyMongo(app)


    
def hash_slug(url, length=6):
    return hashlib.sha1(url.encode()).hexdigest()[:length]


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten',methods=['POST'])
def url_to_shortlink():
    original_url = request.form.get('url')

    if not original_url.startswith(('http://', 'https://')):
        original_url = 'https://' + original_url

    short_code = hash_slug(original_url)
    short_url = request.base_url.replace('shorten','') + short_code

    data={
        'original_url':original_url,
        'short_url':short_url,
        'short_code':short_code,
        'createdAt':datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')
    }

    existing = mongo.db.links.find_one({
        '$or': [
            {'original_url': original_url},
            {'short_code': short_code}
        ]
    })
    if not existing:
        mongo.db.links.insert_one(data)
        return render_template('index.html',short_url=short_url,original_url=original_url)
    else:
        return render_template('index.html',short_url=existing['short_url'],original_url=existing['original_url'])

@app.route('/<short_code>')
def redirect_to(short_code):
    original_url=request.base_url
    data=mongo.db.links.find_one({'short_code':short_code})
    if data:
        original_url=data.get('original_url',None)
        return redirect(original_url)
    else:
        return render_template_string('Url Not Found')
    
if __name__ == '__main__':
    app.run(debug=True)