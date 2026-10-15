import os

from flask import Flask, request, jsonify, redirect, session, url_for
from flask_cors import CORS

# Import the class that calculates the time remaining until an exam
from src.create_exam_timer import CreateExamTimer

# Import the class that formats and displays the countdown 
from src.display_exam_times import DisplayExamTimes

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

# Create an object to calculate the time remaining until an exam
timer = CreateExamTimer()

# Create an object to format and display the exam countdown
display = DisplayExamTimes()

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

# Create a route to calculate the exam countdown
@app.route("/exam-countdown", methods=["POST"])
def exam_countdown():
    # Get the exam information sent from the frontend
    data = request.get_json() or {}
    # Check if the required information is provided
    if not data.get("course") or not data.get("title") or not data.get("date"):
        return jsonify({
            "error": "course, title, and date are required"
        }), 400

    try: 
        # Create an Exam object using the provided information
        exam = Exam(
            exam_id=None, 
            course=data["course"],
            title=data["title"],
            date=data["date"],
        )

        # Calculate the time remaining until the exam
        countdown = timer.createTimer(exam)

        # Create a message displaying the countdown
        message = display.displayTimes(countdown)

        # Send the countdown and messge back to the frontend
        return jsonify({
            "countdown": countdown,
            "message": message
        })
    
    # Return an error if the date or data types are invalid 
    except (ValueError, TypeError) as error: 
        return jsonify({"error": str(error)}), 400

if __name__ == "__main__":
    app.run(debug=True)