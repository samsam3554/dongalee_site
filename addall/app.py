from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  # CORS 활성화

# MongoDB Atlas URI
MONGO_URI = "mongodb+srv://samsam3554:58774485aaa@cluster0.vv2h9.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client['studentDB']
collection = db['students']

# 라우트 설정
@app.route('/submit', methods=['POST'])
def submit_data():
    try:
        # 요청에서 JSON 데이터 추출
        data = request.json
        subjectandname = data.get('subjectandname')
        studentnumber = data.get('studentnumber')

        # MongoDB에 데이터 삽입
        collection.insert_one({'학과,이름': subjectandname, '학번': studentnumber})
        return jsonify({'message': '지원해주셔서 감사합니다!'}), 200 
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
