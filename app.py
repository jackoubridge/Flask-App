from flask import Flask, render_template, redirect, request, flash, url_for, jsonify, session, make_response
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urlencode
import json
from json import dumps
from flask_socketio import SocketIO, emit
from flask_login import login_user, current_user, LoginManager, login_manager, UserMixin, login_required, logout_user
import requests
from sqlalchemy.dialects.postgresql import JSON

import steammarket as sm

app = Flask(__name__)

app.app_context().push()

# Flips Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key = True)
  steamId = db.Column(db.String(16), unique = True, default = '123')
  personaname = db.Column(db.String(30), default = 'Anonymous')
  avatarLink = db.Column(db.String(30), default = '')
  createdFlips = db.relationship('Flip', backref='creator', foreign_keys = 'Flip.creatorId')
  joinedFlips = db.relationship('Flip', backref='joiner', foreign_keys = 'Flip.joinerId')
  status = db.Column(db.String(10), default="user")
  inventory = db.Column(JSON)

class Flip(db.Model):
  id = db.Column(db.Integer, primary_key=True, nullable = False)

  creatorId = db.Column(db.String(17), db.ForeignKey('user.id'))
  creatorValue = db.Column(db.DECIMAL(5), nullable = False, default = 0.00)
  
  joinerId = db.Column(db.String(17), db.ForeignKey('user.id'), nullable = True, default = "None")
  joinerValue = db.Column(db.DECIMAL(5), nullable = True)

  creatorChoseRed = db.Column(db.Boolean, nullable = False)

  creatorSkins = db.Column(JSON)


@login_manager.user_loader
def user_loader(user_id):
  return User.query.get(int(user_id))

# Web Sockets
socketio = SocketIO(app, async_mode='eventlet')
@socketio.on('connect')
def handle_connect():
  print('Client connected')

@app.route('/')
def index():
  return redirect('/play')

@app.route('/play', methods=['POST', 'GET'])
def play():
  database_data = Flip.query.order_by(Flip.id)
  return render_template('play.html', flips = database_data)

@app.route('/tos')
def tos():
  return render_template('tos.html')

@app.route('/provablyfair')
def provablyfair():
  return render_template('provablyfair.html')

@app.route('/myprofile')
@login_required
def myprofile():
  return render_template('myprofile.html')

@app.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect('play')

@app.route('/newflip', methods=['POST'])
@login_required
def newflip():
  
  selected_skins = request.form.getlist('selectedskins')
  skinlist = []

  inventory = current_user.inventory
  for skin in inventory:
    if skin['asset_id'] in selected_skins:
      skinlist.append(skin)
  

  choice = request.form.get('inlineRadioOptions')
  choseRed = True
  if choice == 'black':
    choseRed = False
  
  new_flip = Flip(creatorId = current_user.id, creatorChoseRed = choseRed, creatorSkins = skinlist)
  db.session.add(new_flip)
  db.session.commit()
  
  socketio.emit('new_flip', { 'id': new_flip.id, 'creatorId' : new_flip.creator.id, 'creatorPersonaname': new_flip.creator.personaname, 'creatorAvatar' : new_flip.creator.avatarLink, 'creatorStatus' : new_flip.creator.status, 'creatorChoseRed' : new_flip.creatorChoseRed, 'creatorSkins': skinlist}, broadcast=True)
  return ('', 204)

@app.route('/joinflip', methods=['POST'])
@login_required
def joinFlip():
  flip = Flip.query.filter_by(id=request.form.get('id')).first()
  flip.joinerId = current_user.id
  db.session.commit()
  socketio.emit('updateflip', { 'id': flip.id, 'creatorId' : flip.creator.id, 'creatorPersonaname': flip.creator.personaname, 'creatorAvatar' : flip.creator.avatarLink, 'creatorStatus' : flip.creator.status, 'creatorChoseRed': flip.creatorChoseRed, 'joinerId' : flip.joiner.id, 'joinerPersonaname': flip.joiner.personaname, 'joinerAvatar': flip.joiner.avatarLink, 'joinerStatus' : flip.joiner.status}, broadcast=True)
  return ('', 204)

@app.route('/getinventory', methods=['POST', 'GET'])
@login_required
def getinvent():

  # Future code for getting user Steam inventory, API needs setup

  # tradable_skins = {'assets': [], 'descriptions': []}
  # try:
  #   link = "https://steamcommunity.com/inventory/" + current_user.steamId +"/252490/2?l=english&count=30"
  #   skins = requests.get(link).json()

  #   for x in range(len(skins['descriptions'])):
  #     if skins['descriptions'][x]['tradable'] == 1:
  #       tradable_skins['assets'].append(skins['assets'][x])
  #       tradable_skins['descriptions'].append(skins['descriptions'][x])
    
  # except Exception as e:
  #   print(e)

  prices = []

  # Hardcoded inventory for now

  tradable_skins = {
  "assets": [
    {
      "amount": "1",
      "appid": 252490,
      "assetid": "5224777830850461539",
      "classid": "1140551711",
      "contextid": "2",
      "instanceid": "5237645417"
    },
    {
      "amount": "1",
      "appid": 252490,
      "assetid": "5224777830850460795",
      "classid": "1140551659",
      "contextid": "2",
      "instanceid": "5237645417"
    },
    {
      "amount": "1",
      "appid": 252490,
      "assetid": "5224777830850460780",
      "classid": "1140551659",
      "contextid": "2",
      "instanceid": "5237645417"
    },
    {
      "amount": "1",
      "appid": 252490,
      "assetid": "5224777830850460768",
      "classid": "1140551659",
      "contextid": "2",
      "instanceid": "5237645417"
    }
  ],
  "descriptions": [
    {
      "appid": 252490,
      "background_color": "42413e",
      "classid": "1129415388",
      "commodity": 1,
      "currency": 0,
      "descriptions": [
        {
          "type": "html",
          "value": "This is like a normal tshirt, but it has sleeves that extend to your wrists.<br><br><span style=\"color: #FF9800\">This is a skin for the <span style=\"color: #ffdba5\">Longsleeve T-Shirt</span> item. You will be able to apply this skin at a repair bench or when you craft the item in game.</span><br><br><span style=\"color: #5098ce\">Breaks down into <span style=\"color: #ffffff\">1 x Cloth</span></span>"
        }
      ],
      "icon_url": "6TMcQ7eX6E0EZl2byXi7vaVKyDk_zQLX05x6eLCFM9neAckxGDf7qU2e2gu64OnAeQ7835Je5GLDfCk4nReh8DEiv5dROq8-q7c2Qv5bKM0qVQ",
      "icon_url_large": "6TMcQ7eX6E0EZl2byXi7vaVKyDk_zQLX05x6eLCFM9neAckxGDf7qU2e2gu64OnAeQ7835Je5GLDfDY0jhyo8DEiv5dROq8-q7c2Qv7B0EpJxA",
      "instanceid": "0",
      "market_hash_name": "Orange Longsleeve T-Shirt",
      "market_marketable_restriction": 7,
      "market_name": "Orange Longsleeve T-Shirt",
      "market_tradable_restriction": 7,
      "marketable": 1,
      "name": "Orange Longsleeve T-Shirt",
      "name_color": "a7ec2e",
      "tags": [
        {
          "category": "itemclass",
          "internal_name": "tshirt.long",
          "localized_category_name": "Item Type",
          "localized_tag_name": "Long TShirt"
        },
        {
          "category": "steamcat",
          "internal_name": "steamcat.clothing",
          "localized_category_name": "Category",
          "localized_tag_name": "Clothing"
        }
      ],
      "tradable": 1,
      "type": ""
    },
    {
      "appid": 252490,
      "background_color": "42413e",
      "classid": "1166495354",
      "commodity": 1,
      "currency": 0,
      "descriptions": [
        {
          "type": "html",
          "value": "A hat with a protrusion on the front which under the right conditions prevents the sun from entering the wearer's eye.<br><br><span style=\"color: #FF9800\">This is a skin for the <span style=\"color: #ffdba5\">Baseball Cap</span> item. You will be able to apply this skin at a repair bench or when you craft the item in game.</span><br><br><span style=\"color: #5098ce\">Breaks down into <span style=\"color: #ffffff\">1 x Cloth</span></span>"
        }
      ],
      "icon_url": "6TMcQ7eX6E0EZl2byXi7vaVKyDk_zQLX05x6eLCFM9neAckxGDf7qU2e2gu64OnAeQ7835Je5GHFfCk4nReh8DEiv5dYMKw6rrA_R_m_GOiIU1s",
      "icon_url_large": "6TMcQ7eX6E0EZl2byXi7vaVKyDk_zQLX05x6eLCFM9neAckxGDf7qU2e2gu64OnAeQ7835Je5GHFfDY0jhyo8DEiv5dYMKw6rrA_R_m_tNp0fwE",
      "instanceid": "0",
      "market_hash_name": "Green Cap",
      "market_marketable_restriction": 7,
      "market_name": "Green Cap",
      "market_tradable_restriction": 7,
      "marketable": 1,
      "name": "Green Cap",
      "name_color": "a7ec2e",
      "tags": [
        {
          "category": "itemclass",
          "internal_name": "hat.cap",
          "localized_category_name": "Item Type",
          "localized_tag_name": "Cap"
        },
        {
          "category": "steamcat",
          "internal_name": "steamcat.clothing",
          "localized_category_name": "Category",
          "localized_tag_name": "Clothing"
        }
      ],
      "tradable": 1,
      "type": ""
    },
    {
      "appid": 252490,
      "background_color": "42413e",
      "classid": "1127157321",
      "commodity": 1,
      "currency": 0,
      "descriptions": [
        {
          "type": "html",
          "value": "Stylish blue jeans<br><br><span style=\"color: #FF9800\">This is a skin for the <span style=\"color: #ffdba5\">Pants</span> item. You will be able to apply this skin at a repair bench or when you craft the item in game.</span><br><br><span style=\"color: #5098ce\">Breaks down into <span style=\"color: #ffffff\">1 x Cloth</span></span>"
        }
      ],
      "icon_url": "6TMcQ7eX6E0EZl2byXi7vaVKyDk_zQLX05x6eLCFM9neAckxGDf7qU2e2gu64OnAeQ7835Je5GLEfCk4nReh8DEiv5dbO686pbwyRP28apax_hM",
      "icon_url_large": "6TMcQ7eX6E0EZl2byXi7vaVKyDk_zQLX05x6eLCFM9neAckxGDf7qU2e2gu64OnAeQ7835Je5GLEfDY0jhyo8DEiv5dbO686pbwyRP28EfTtEa0",
      "instanceid": "0",
      "market_hash_name": "Blue Jeans",
      "market_marketable_restriction": 7,
      "market_name": "Blue Jeans",
      "market_tradable_restriction": 7,
      "marketable": 1,
      "name": "Blue Jeans",
      "name_color": "a7ec2e",
      "tags": [
        {
          "category": "itemclass",
          "internal_name": "pants",
          "localized_category_name": "Item Type",
          "localized_tag_name": "Pants"
        },
        {
          "category": "steamcat",
          "internal_name": "steamcat.clothing",
          "localized_category_name": "Category",
          "localized_tag_name": "Clothing"
        }
      ],
      "tradable": 1,
      "type": ""
    },
    {
      "appid": 252490,
      "background_color": "42413e",
      "classid": "1132469013",
      "commodity": 1,
      "currency": 0,
      "descriptions": [
        {
          "type": "html",
          "value": "A jacket with a desert camo pattern<br><br><span style=\"color: #FF9800\">This is a skin for the <span style=\"color: #ffdba5\">Jacket</span> item. You will be able to apply this skin at a repair bench or when you craft the item in game.</span><br><br><span style=\"color: #5098ce\">Breaks down into <span style=\"color: #ffffff\">1 x Cloth</span></span>"
        }
      ],
      "icon_url": "6TMcQ7eX6E0EZl2byXi7vaVKyDk_zQLX05x6eLCFM9neAckxGDf7qU2e2gu64OnAeQ7835Je5GPHfCk4nReh8DEiv5dRPa84rbc1Sfwm3f7jXg",
      "icon_url_large": "6TMcQ7eX6E0EZl2byXi7vaVKyDk_zQLX05x6eLCFM9neAckxGDf7qU2e2gu64OnAeQ7835Je5GPHfDY0jhyo8DEiv5dRPa84rbc1Sfwe05zwGQ",
      "instanceid": "0",
      "market_hash_name": "Desert Jacket",
      "market_marketable_restriction": 7,
      "market_name": "Desert Jacket",
      "market_tradable_restriction": 7,
      "marketable": 1,
      "name": "Desert Jacket",
      "name_color": "a7ec2e",
      "tags": [
        {
          "category": "itemclass",
          "internal_name": "jacket",
          "localized_category_name": "Item Type",
          "localized_tag_name": "Jacket"
        },
        {
          "category": "steamcat",
          "internal_name": "steamcat.clothing",
          "localized_category_name": "Category",
          "localized_tag_name": "Clothing"
        }
      ],
      "tradable": 1,
      "type": ""
    }
  ]
  }

  user_inventory = []

  for j in range(len(tradable_skins['assets'])):
    assetid = str(tradable_skins['assets'][j]['assetid'])
    image_url = str(tradable_skins['descriptions'][j]['icon_url'])
    name = str(tradable_skins['descriptions'][j]['market_hash_name'])
    price = round(float(sm.get_item(252490, tradable_skins['descriptions'][j]['market_hash_name'], currency='USD')['median_price'].replace("$", "")), 2)
    item = {"asset_id":assetid,"image_url":image_url,"name":name,"price":price}

    user_inventory.append(item)

  current_user.inventory = user_inventory
  db.session.commit()

  return make_response(jsonify(tradable_skins), 200)

@app.route("/auth")
def auth_with_steam():

  url1 = request.url.replace("/auth", "")

  steam_openid_url = 'https://steamcommunity.com/openid/login'
  params = {
    'openid.ns': "http://specs.openid.net/auth/2.0",
    'openid.identity': "http://specs.openid.net/auth/2.0/identifier_select",
    'openid.claimed_id': "http://specs.openid.net/auth/2.0/identifier_select",
    'openid.mode': 'checkid_setup',
    'openid.return_to': url1 + '/auth-success',
    'openid.realm': url1 + '/'
  }

  query_string = urlencode(params)
  auth_url = steam_openid_url + "?" + query_string
  
  return redirect(auth_url)

@app.route("/auth-success")
def auth_success():
  steamid = str(json.loads(dumps((request.args)))['openid.claimed_id']).replace('https://steamcommunity.com/openid/id/','')
  api_key = ""

  user = User.query.filter_by(steamId=steamid).first()

  slink = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=" + api_key + "&steamids=" + steamid

  r = requests.get(slink)
  response = r.json()

  personaname = response['response']['players'][0]['personaname']
  avatar = response['response']['players'][0]['avatarfull']

  if not user:
    db.session.add(User(steamId = steamid, personaname= personaname, avatarLink = avatar))
    db.session.commit()
    user = User.query.filter_by(steamId=steamid).first()
  else:
    user.personaname = personaname
    user.avatarLink = avatar
    db.session.commit()

  login_user(user, remember=True)
  return redirect('play')

if __name__ == "__main__":

  app.secret_key = 'super secret key'
  socketio.run(app, port=5000, host='localhost', debug=True)
