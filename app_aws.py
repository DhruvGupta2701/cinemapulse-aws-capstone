from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import boto3
import uuid
from datetime import datetime

# ================= APP =================
app = Flask(__name__)
app.secret_key = "cinemapulse_aws_secret"

AWS_REGION = "us-east-1"

# ================= AWS CLIENTS (IAM ROLE) =================
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
sns = boto3.client("sns", region_name=AWS_REGION)

USERS_TABLE = dynamodb.Table("CinemaPulseUsers")
FEEDBACK_TABLE = dynamodb.Table("CinemaPulseFeedback")

SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:YOUR_ACCOUNT_ID:CinemaPulseFeedbackAlerts"

# ================= MOVIES (STATIC – OK FOR EXAM) =================
movies = {
    "jawan": {
        "id": "MOVIE_JAWAN",
        "name": "Jawan",
        "genre": "Action",
        "language": "Hindi",
        "image": "https://wallpaperaccess.com/full/9335215.jpg",
        "rating": 0
    },
    "oppenheimer": {
        "id": "MOVIE_OPPENHEIMER",
        "name": "Oppenheimer",
        "genre": "Drama",
        "language": "English",
        "image": "https://i.pinimg.com/originals/25/74/bc/2574bcaa1d5a9fe6a54e4fd058aefb55.jpg",
        "rating": 0
    }
}

# ================= HELPERS =================
def is_logged_in():
    return "user_email" in session

def simple_sentiment(comment):
    comment = comment.lower()
    if any(w in comment for w in ["amazing", "great", "excellent", "love"]):
        return "Positive"
    if any(w in comment for w in ["bad", "boring", "waste"]):
        return "Negative"
    return "Neutral"

# ================= ROUTES =================
@app.route("/")
def home():
    return render_template("index.html", logged_in=is_logged_in())

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# ================= AUTH =================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    USERS_TABLE.put_item(
        Item={
            "email": request.form["email"],
            "name": request.form["name"],
            "password": request.form["password"],
            "favorite_genre": request.form["favorite_genre"],
            "age_group": request.form["age_group"],
            "created_at": str(datetime.utcnow())
        }
    )
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    email = request.form["email"]
    password = request.form["password"]

    user = USERS_TABLE.get_item(Key={"email": email}).get("Item")
    if user and user["password"] == password:
        session["user_email"] = email
        return redirect(url_for("user_dashboard"))

    return "Invalid credentials"

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# ================= USER DASHBOARD =================
@app.route("/user/dashboard")
def user_dashboard():
    if not is_logged_in():
        return redirect(url_for("login"))

    feedbacks = FEEDBACK_TABLE.scan().get("Items", [])
    return render_template("user_dashboard.html", movies=movies.values(), feedbacks=feedbacks)

# ================= FEEDBACK =================
@app.route("/movie/feedback/add", methods=["POST"])
def add_feedback():
    if not is_logged_in():
        return redirect(url_for("login"))

    feedback_id = str(uuid.uuid4())
    sentiment = simple_sentiment(request.form["comment"])

    FEEDBACK_TABLE.put_item(
        Item={
            "feedback_id": feedback_id,
            "movie_id": request.form["movie_id"],
            "user_email": session["user_email"],
            "rating": int(request.form["rating"]),
            "comment": request.form["comment"],
            "sentiment": sentiment,
            "timestamp": str(datetime.utcnow())
        }
    )

    # SNS Notification
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject="New CinemaPulse Feedback",
        Message=f"""
Movie ID: {request.form['movie_id']}
Rating: {request.form['rating']}
Sentiment: {sentiment}
"""
    )

    return redirect(url_for("user_dashboard"))

# ================= ADMIN =================
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "GET":
        return render_template("admin_login.html")
    if request.form["email"] == "admin@example.com" and request.form["password"] == "admin123":
        session["admin_logged_in"] = True
        return redirect(url_for("admin_dashboard"))
    return "Invalid admin credentials"

@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    feedbacks = FEEDBACK_TABLE.scan().get("Items", [])
    return render_template("admin_dashboard.html", movies=movies, feedbacks=feedbacks)

# ================= ENTRY =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
