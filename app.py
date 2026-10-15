import os

from flask import Flask, request, jsonify, redirect, session, url_for
from flask_cors import CORS

from src.exam import Exam
from src.exam_database import ExamDatabase
from src.google_calendar_service import GoogleCalendarService


app = Flask(__name__)

app.secret_key = os.getenv(
    "FLASK_SECRET_KEY",
    "local-development-key",
)

CORS(app)

exam_database = ExamDatabase("events.db")
google_calendar_service = GoogleCalendarService()


@app.route("/")
def home():
    return "Backend is running"


@app.route("/authorize")
def authorize_google_calendar():
    redirect_uri = url_for(
        "oauth2callback",
        _external=True,
    )

    try:
        authorization_url, state, code_verifier = (
            google_calendar_service.get_authorization_url(
                redirect_uri
            )
        )
    except FileNotFoundError as error:
        return jsonify({"error": str(error)}), 500

    session["oauth_state"] = state
    session["oauth_code_verifier"] = code_verifier

    return redirect(authorization_url)


@app.route("/oauth2callback")
def oauth2callback():
    state = session.pop("oauth_state", None)
    code_verifier = session.pop(
        "oauth_code_verifier",
        None,
    )

    if not state:
        return jsonify({
            "error": "OAuth state is missing or expired"
        }), 400

    redirect_uri = url_for(
        "oauth2callback",
        _external=True,
    )

    try:
        google_calendar_service.finish_authorization(
            authorization_response=request.url,
            state=state,
            redirect_uri=redirect_uri,
            code_verifier=code_verifier,
        )
    except Exception as error:
        return jsonify({
            "error": f"Google authorization failed: {error}"
        }), 400

    return (
        "Google Calendar connected. "
        "You can return to the syllabus page."
    )


@app.route("/events", methods=["POST"])
def add_event():
    data = request.get_json() or {}

    required_fields = (
        "course",
        "title",
        "date",
    )

    if any(not data.get(field) for field in required_fields):
        return jsonify({
            "error": "course, title, and date are required"
        }), 400

    exam = Exam(
        exam_id=None,
        course=data["course"],
        title=data["title"],
        date=data["date"],
    )

    exam_database.save_exam(exam)

    calendar_added = google_calendar_service.add_exam(exam)

    response = exam.to_dict()
    response["calendar_added"] = calendar_added

    if google_calendar_service.last_event_link:
        response["calendar_link"] = (
            google_calendar_service.last_event_link
        )

    return jsonify(response), 201


@app.route("/events", methods=["GET"])
def get_events():
    exams = exam_database.get_exams()

    return jsonify([
        exam.to_dict()
        for exam in exams
    ])


if __name__ == "__main__":
    app.run(debug=True)