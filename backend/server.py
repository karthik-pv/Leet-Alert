from flask import Flask, jsonify, request
from dotenv import load_dotenv
from controller import (
    sendDailyMail,
    sendRandomMail,
    register,
    getAllEmails,
)
from flask_mail import Mail
from flask_cors import CORS
from flask_apscheduler import APScheduler
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT"))
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS").lower() == "true"
app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL").lower() == "true"
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

mail = Mail(app)
scheduler = APScheduler()


def scheduled_task():
    with app.app_context():
        sendDailyMail(mail)


@app.route("/register", methods=["POST"])
def register_to_service():
    data = request.json["email"]
    return register(data)


@app.route("/link")
def get_daily_question_from_api():
    return jsonify(sendDailyMail(mail))


@app.route("/getSubscribers")
def get_subs():
    return jsonify({"subscribers": getAllEmails()})


@app.route("/random", methods=["POST"])
def getRandomProblem():
    sendRandomMail(mail=mail, email=request.json["email"])
    return "sent succesfully"


def start_scheduler():
    scheduler.add_job(
        id="Scheduled Task", func=scheduled_task, trigger="cron", hour=21, minute=00
    )
    scheduler.start()


if __name__ == "__main__":
    if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        start_scheduler()
    app.run(debug=True)
