import requests
from flask import Flask, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False


def fetch_aktuel_data(url):
    body = requests.get(url)
    soup = BeautifulSoup(body.text, 'html.parser')

    pages = soup.find('div', {'class': 's1e6b0v8-3 iFVIwI'}).find_all('div')
    images = []
    for page in pages:
        page_val = page.find('div')
        if page_val is not None:
            img = page_val.find('img')
            if img.has_key('data-src'):
                images.append(img['data-src'])
            else:
                images.append(img['src'])
    return {'images': images}


def fetch_diyanet_data(url):
    body = requests.get(url)
    soup = BeautifulSoup(body.text, 'html.parser')
    
    ayet = soup.find('div', {'class': 'ayet'}).find(
        'p', {'class': 'ahd-content-text'}).text.strip()

    ayet_info = soup.find('div', {'class': 'ayet'}).find_next_sibling("div").find(
        'p', {'class': 'alt-sure-title'}).text.strip()

    dua = soup.find('div', {'class': 'dua'}).find(
        'p', {'class': 'ahd-content-text'}).text.strip()

    dua_info = soup.find('div', {'class': 'dua'}).find(
        'p', {'class': 'alt-sure-title'}).text.strip()

    hadis = soup.find('div', {'class': 'hadis'}).find(
        'p', {'class': 'ahd-content-text'}).text.strip()

    hadis_info = soup.find('div', {'class': 'hadis'}).find_next_sibling("div").find(
        'p', {'class': 'alt-sure-title'}).text.strip()

    data = {'ayet': ayet, 'ayet_info': ayet_info, 'dua': dua, 'dua_info': dua_info, 'hadis': hadis, 'hadis_info': hadis_info}
    return data


@app.route('/api/diyanet')
def diyanet():
    diyanet_data = fetch_diyanet_data('https://www.diyanet.gov.tr/tr-TR')
    return jsonify(diyanet_data)


@app.route('/api/aktuel')
def aktuel():
    aktuel_data = fetch_aktuel_data('https://www.cimri.com/brosur/a101-com-tr?id=11423')
    return jsonify(aktuel_data)


app.run(host='0.0.0.0', port=80)
