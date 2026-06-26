import os
from flask import Flask, request, jsonify, send_file
from models import db,Business,ChatMessage
from werkzeug.security import generate_password_hash,check_password_hash
from ai_assistant import get_ai_response

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///business.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route("/")
def home():
    return "AI Business Support System Running"

@app.route("/register-page")
def register_page():
    return send_file("register.html")
@app.route("/register", methods=["POST"])
def register():

    data = request.json

    new_business = Business(
        business_name=data["business_name"],
        email=data["email"],
        password=generate_password_hash(data["password"]),
        information=data.get("information")
    )

    db.session.add(new_business)
    db.session.commit()

    return jsonify({
        "message": "Business registered successfully"
    })
@app.route("/chat-page/<int:business_id>")
def chat_page(business_id):
    return send_file("chat.html")
@app.route("/dashboard/<int:business_id>")
def dashboard(business_id):
    return send_file("dashboard.html")
@app.route("/business/<int:business_id>")
def business_info(business_id):

    business = Business.query.get(business_id)

    return jsonify({
        "name": business.business_name
    })
@app.route("/login-page")
def login_page():
    return send_file("login.html")
    

@app.route("/login", methods=["POST"])
def login():

    data = request.json

    business = Business.query.filter_by(
        email=data["email"],
        password=data["password"]
    ).first()

    if business:
        return jsonify({
            "id": business.id
        })

    return jsonify({
        "message": "Invalid login details"
    })
@app.route("/history/<int:business_id>")
def history(business_id):

    chats = ChatMessage.query.filter_by(
        business_id=business_id
    ).all()

    return jsonify([
        {
            "customer": chat.customer_message,
            "ai": chat.ai_response,
            "time":chat.created_at
        }
        for chat in chats
    ])
@app.route("/stats/<int:business_id>")
def stats(business_id):

    total_chats = ChatMessage.query.filter_by(
        business_id=business_id
    ).count()

    return jsonify({
        "total_chats": total_chats
    })

@app.route("/chat/<int:business_id>", methods=["POST"])
def chat(business_id):

    data = request.json
    question = data["question"]

    business = Business.query.get(business_id)

    if not business:
        return jsonify({"answer": "Business not found"}), 404

    business_info = business.information

    answer = get_ai_response(question, business_info)

    chat = ChatMessage(
        business_id=business.id,
        customer_message=question,
        ai_response=answer
    )

    db.session.add(chat)
    db.session.commit()

    return jsonify({
        "answer": answer
    })

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)