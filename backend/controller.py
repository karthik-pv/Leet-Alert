import os
from flask import Flask, jsonify
import requests
import html2text
from flask_mail import Message
from dbConnect import connectToDatabase
import re
import random


app = Flask(__name__)
h = html2text.HTML2Text()
db = connectToDatabase()


def getRandomQuestionFromLeet():
    skip = random.randint(1, 3000)
    url = os.getenv("LEETCODE_API_URL")
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://leetcode.com",
    }
    query = """
       query getRandomProblems($categorySlug: String,$skip: Int , $limit: Int, $filters: QuestionListFilterInput) {
            randomQuestionList: questionList(
                categorySlug: $categorySlug
                limit: $limit
                skip: $skip
                filters: $filters
            ) {
                questions: data {
                title
                content
                }
            }
            }
   """
    payload = {
        "query": query,
        "variables": {
            "categorySlug": "algorithms",
            "limit": 1,
            "skip": skip,
            "filters": {},
        },
    }
    try:

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as err:
        return jsonify({"error": f"Other error occurred: {err}"}), 500


def getDailyQuestion():
    url = os.getenv("LEETCODE_API_URL")
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://leetcode.com",
    }
    query = """
        query getDailyProblem {
            activeDailyCodingChallengeQuestion {
                link,
                question{
                    title
                    content
                }
            }
        }
    """
    payload = {"query": query}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return (
            "<h1>"
            + data["data"]["activeDailyCodingChallengeQuestion"]["question"]["title"]
            + "</h1>"
            + "\n\n\n\n"
            + data["data"]["activeDailyCodingChallengeQuestion"]["question"]["content"]
        )
    except Exception as err:
        return jsonify({"error": f"Other error occurred: {err}"}), 500


def getRandomQuestion():
    content = None
    while content is None:
        temp = getRandomQuestionFromLeet()
        content = (
            temp.get("data", {})
            .get("randomQuestionList", {})
            .get("questions", [])[0]
            .get("content", {})
        )
    return (
        "<h1>"
        + temp.get("data", {})
        .get("randomQuestionList", {})
        .get("questions", [])[0]
        .get("title", {})
        + "</h1>"
        + "\n\n\n\n"
        + temp.get("data", {})
        .get("randomQuestionList", {})
        .get("questions", [])[0]
        .get("content", {})
    )


def sendMail(mail, html, recipient, subject):
    msg = Message(
        subject,
        recipients=recipient,
        html=html,
    )
    mail.send(msg)
    return "Email sent succesfully!"


def sendDailyMail(mail):
    sendMail(
        mail=mail,
        html=getDailyQuestion(),
        recipient=getAllEmails(),
        subject="Leetcode Daily",
    )


def sendRandomMail(mail, email):
    sendMail(
        mail=mail,
        html=getRandomQuestion(),
        recipient=[email],
        subject="Random Leetcode Problem",
    )


def validate_email(email):
    pattern = r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def register(email):
    if not email:
        return jsonify({"error": "Email ID is required"}), 400

    if not validate_email(email):
        return jsonify({"error": "Invalid email format"}), 400

    existing_email = db.subscribers.find_one({"email": email})
    if existing_email:
        return (
            jsonify(
                {"message": "Email already exists", "id": str(existing_email["_id"])}
            ),
            200,
        )

    try:
        result = db.subscribers.insert_one({"email": email})
        return (
            jsonify(
                {
                    "message": "Email ID stored successfully",
                    "id": str(result.inserted_id),
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": f"Failed to store email ID: {str(e)}"}), 500


def getAllEmails():
    try:
        pipeline = [{"$project": {"_id": 0, "email": 1}}]
        cursor = db["subscribers"].aggregate(pipeline)
        emails = [doc["email"] for doc in cursor]
        return emails
    except Exception as e:
        print(f"Error: {e}")
