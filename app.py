from flask import Flask,render_template,redirect, request,render_template_string,session,url_for,flash
from flask_pymongo import PyMongo
import requests
import os
import hashlib
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app=Flask(__name__)
app.config['SECRET_KEY']=os.urandom(24)
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

GOOGLE_CLIENT_ID=os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET=os.getenv('GOOGLE_CLIENT_SECRET')
REDIRECT_URI=os.getenv('REDIRECT_URI')

mongo=PyMongo(app)


    
def hash_slug(url, length=6):
    return hashlib.sha1(url.encode()).hexdigest()[:length]


@app.route('/')
def index():
    user=None
    if 'user' in session:
        user={
            'profile_picture':session['user']['profilePic'],
            'name':session['user']['displayName']
        }
    return render_template('index.html',user=user)

@app.route('/login')
def login():
    return redirect(f'https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=email profile')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_response = requests.post('https://oauth2.googleapis.com/token', data={
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    })
    token_json = token_response.json()
    access_token = token_json.get('access_token')
    user_info_response = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers={
        'Authorization': f'Bearer {access_token}'
    })
    user_info = user_info_response.json()
    session['user'] = {
        'uid': user_info['id'],
        'email': user_info['email'],
        'displayName': user_info['name'],
        'profilePic': user_info['picture']
    }
    return redirect(url_for('index'))
    

@app.route('/shorten',methods=['POST'])
def url_to_shortlink():
    if 'user' not in session:
        flash('you need to login for create short url!')
        return redirect(request.referrer)
    if request.method == 'POST':
        original_url = request.form.get('url')

        if not original_url.startswith(('http://', 'https://')):
            original_url = 'https://' + original_url

        short_code = hash_slug(original_url)
        short_url = request.base_url.replace('shorten','') + short_code

        data={
            'original_url':original_url,
            'short_url':short_url,
            'short_code':short_code,
            'createdAt':datetime.now().strftime('%d-%m-%Y %I:%M:%S %p'),
            'uid':session['user']['uid'],
            'name':session['user']['displayName'],
            'email':session['user']['email']
        }

        existing = mongo.db.links.find_one({
            '$or': [
                {'original_url': original_url},
                {'short_code': short_code}
            ]
        })
        user=None
        if 'user' in session:
            user={
                'profile_picture':session['user']['profilePic'],
                'name':session['user']['displayName']
            }
        if not existing:
            mongo.db.links.insert_one(data)
            return render_template('index.html',short_url=short_url,original_url=original_url,user=user)
        else:
            return render_template('index.html',short_url=existing['short_url'],original_url=existing['original_url'],user=user)
    else:
        return redirect(url_for('index'))
@app.route('/<short_code>')
def redirect_to(short_code):
    if short_code == 'shorten':
        return redirect(url_for('index'))
    original_url=request.base_url
    data=mongo.db.links.find_one({'short_code':short_code})
    if data:
        original_url=data.get('original_url',None)
        return redirect(original_url)
    else:
        return render_template_string('Url Not Found')
    
if __name__ == '__main__':
    app.run(debug=True)