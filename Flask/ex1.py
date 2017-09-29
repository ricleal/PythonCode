from flask import Flask, jsonify, request, send_from_directory
import json


'''
$ pip install Flask --user


'''

# app = Flask(__name__)
# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')

data = [
    {
        "job_id": "1",
        "job_title": "Reduction 1",
        "date_modified": "2017-08-17T17:23:28.091Z",
        "results": [
            {
                "id": "1",
                "filename": "A1_m_Iq",
                "url": "/files/A1_m_Iq.txt"
            },
            {
                "id": "2",
                "filename": "aC3_6_T12hS90_w_Iq",
                "url": "/files/aC3_6_T12hS90_w_Iq.txt"
            },
            {
                "id": "3",
                "filename": "A3_m_Iq",
                "url": "/files/A3_m_Iq.txt"
            },
            {
                "id": "4",
                "filename": "A1_m_Iqxy",
                "url": "/files/A1_m_Iqxy.dat"
            }
        ]
    },
    {
        "job_id": "2",
        "job_title": "Reduction 2",
        "date_modified": "2017-09-17T17:23:20.091Z",
        "results": [
            {
                "id": "1",
                "filename": "A4_m_Iq",
                "url": "/files/A3_m_Iq.txt"
            },
            {
                "id": "2",
                "filename": "A3_w_Iq",
                "url": "/files/A3_w_Iq.txt"
            },
            {
                "id": "3",
                "filename": "A2_m_Iqxy",
                "url": "/files/A2_m_Iqxy.dat"
            }
        ]
    }
]

@app.route("/")
def hello():
    return "<h1>Hello World!</h1>"

@app.route('/save', methods=['POST'])
def save():
    '''
    To test:
    curl -H "Content-Type: application/json" -X POST -d \
    '{"id":"1","content":"12456"}' http://localhost:5000/save
    '''
    json_data = request.json
    print(80*"*")
    print(json_data)
    print(80*"*")
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/fetch', methods=['GET'])
def fetch():
    print(request)
    return jsonify(data)

@app.route('/file/<path:path>')
def file_download(path):
    '''
    this serves files in the data directory
    Test:
    curl http://localhost:5000/file/file1.csv
    '''
    return send_from_directory('data', path)

if __name__ == "__main__":
    print("Staring server")
    # app.run()
    app.run(host= '0.0.0.0',debug=True)
