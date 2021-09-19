from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch, ElasticsearchException
import requests
import json
app = Flask(__name__)

def connectES():
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if es.ping():    
        print("es connected successfully")
    else:
        print("es not connected")
    return es

def insert_data(url):
    try:
        
        response = requests.get(url).json()
        for resp in response:
            es.index(index='myindex', doc_type='article', id=resp['id'], body=resp)
        print('Data stored')

    except:
        print('Error Occurred while inserting data')
        return None

#changes
@app.route('/search', methods=['GET'])
def art_search():
    keyword = request.args.get("keyword")

    try:
        
        resources = es.search(index='myindex', doc_type='article', body={'query': {'match': {'summary': keyword}}})    
        response = jsonify(articles=resources['hits']['hits'])
        print(response)

    except:
        response = jsonify(message='Error Occurred while getting response')

    finally:
        return response


if __name__ == '__main__':
    global es 
    es = connectES()
    insert_data('https://api.spaceflightnewsapi.net/v3/articles')
    app.run(port=8000,debug=True)
    
