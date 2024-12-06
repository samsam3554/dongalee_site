from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime

# Flask 앱 초기화 및 CORS 활성화
app = Flask(__name__)
CORS(app)

# MongoDB 설정
MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
db = client['student_application']  # 데이터베이스 이름
collection = db['dongAlee_application']  # 컬렉션 이름

# 고정된 면접 슬롯 데이터
AVAILABLE_SLOTS = [
    {"date": "2024-12-10", "time": "10:00"},
    {"date": "2024-12-10", "time": "14:00"},
    {"date": "2024-12-11", "time": "10:00"},
    {"date": "2024-12-11", "time": "14:00"}
]

@app.route('/submit', methods=['POST'])
def submit_data():
    """
    학생 지원 데이터를 저장하는 엔드포인트.
    요청 데이터 형식:
    {
        "subjectandname": "컴퓨터공학과, 홍길동",
        "studentnumber": "20241234"
    }
    """
    try:
        data = request.json
        subjectandname = data.get('subjectandname')
        studentnumber = data.get('studentnumber')

        # 필수 값 검증
        if not subjectandname or not studentnumber:
            return jsonify({'error': 'Both subjectandname and studentnumber are required.'}), 400

        # 데이터 저장
        collection.insert_one({
            'subjectandname': subjectandname,
            'studentnumber': studentnumber,
            'created_at': datetime.utcnow()
        })

        return jsonify({'message': '지원해주셔서 감사합니다!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_slots', methods=['GET'])
def get_slots():
    """
    사용 가능한 면접 슬롯 반환.
    """
    return jsonify({"available_slots": AVAILABLE_SLOTS}), 200

@app.route('/select_slot', methods=['POST'])
def select_slot():
    """
    사용자가 선택한 면접 슬롯을 저장하는 엔드포인트.
    요청 데이터 형식:
    {
        "name": "홍길동",
        "date": "2024-12-10",
        "time": "10:00"
    }
    """
    try:
        data = request.json
        name = data.get("name")
        date = data.get("date")
        time = data.get("time")

        # 필수 값 검증
        if not name or not date or not time:
            return jsonify({"error": "Name, date, and time are required."}), 400

        # 유효한 슬롯인지 확인
        if {"date": date, "time": time} not in AVAILABLE_SLOTS:
            return jsonify({"error": "Selected slot is not available."}), 400

        # 데이터 저장
        interview_data = {
            "name": name,
            "date": date,
            "time": time,
            "created_at": datetime.utcnow()
        }
        collection.insert_one(interview_data)

        return jsonify({"message": "Interview slot saved successfully.", "data": interview_data}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
