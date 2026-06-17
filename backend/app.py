from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

db = mysql.connector.connect(
    host="localhost",
    port=3307,
    user="root",
    password="MySQL@123",
    database="ai_interview_portal"
)

@app.route('/login', methods=['POST'])
def login():

    print("LOGIN HIT")

    data = request.get_json()

    print(data)

    username = data['username']
    password = data['password']

    cursor = db.cursor(dictionary=True, buffered=True)

    query = """
    SELECT * FROM users
    WHERE username=%s
    AND password=%s
    """

    cursor.execute(query, (username, password))

    user = cursor.fetchone()

    if user:
        return jsonify({
            "message": "Login Successful"
        })

    return jsonify({
        "message": "Invalid Username or Password"
    })
@app.route('/')
def home():
    return "AI Interview Portal Backend Running"
@app.route("/questions")
def get_questions():

    cursor = db.cursor(dictionary=True, buffered=True)

    cursor.execute("SELECT * FROM questions")

    data = cursor.fetchall()

    return jsonify(data)

@app.route('/save_result', methods=['POST'])
def save_result():

    data = request.json

    username = data['username']
    score = data['score']

    cursor = db.cursor()

    query = """
    INSERT INTO results(username, score)
    VALUES(%s, %s)
    """

    cursor.execute(query, (username, score))
    db.commit()

    return jsonify({
        "message": "Result Saved"
    })

@app.route('/add_question', methods=['POST'])
def add_question():

    data = request.json

    question = data['question']
    option1 = data['option1']
    option2 = data['option2']
    option3 = data['option3']
    option4 = data['option4']
    answer = data['answer']

    cursor = db.cursor()

    query = """
    INSERT INTO questions
    (question, option1, option2, option3, option4, answer)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (
            question,
            option1,
            option2,
            option3,
            option4,
            answer
        )
    )

    db.commit()

    return jsonify({
        "message": "Question Added"
    })

@app.route('/register', methods=['POST'])
def register():

    data = request.json

    username = data['username']
    password = data['password']

    cursor = db.cursor()

    query = """
    INSERT INTO users(username, password)
    VALUES(%s, %s)
    """

    cursor.execute(query, (username, password))
    db.commit()

    return jsonify({
        "message": "Registration Successful"
    })
@app.route('/results')
def results():

    cursor = db.cursor(dictionary=True, buffered=True)

    cursor.execute("SELECT * FROM results")

    data = cursor.fetchall()

    return jsonify(data)
if __name__ == "__main__":
    app.run(debug=True)