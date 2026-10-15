# syllabus-calendar-intergration

## Original Team Members

- Gabriel Elias
- Rory Campbell
- Ubaydulla Noorullah
- Deandre Chandler

## Project Description 

SyllabusFlow is a web application designed to help students organize important academic events from their course syllabi. The application uses artificial intelligence to search for events such as exams, quizzes, and class meetings in order to organize them into a calendar. SyllabusFlow will allow students to add important school dates to Google Calendar and create custom reminders. 

## Main Features 

- Upload and process course syllabi
- Use artificial intelligence to identiy important course events 
- Organize exam deadlines, quiz deadlines, and important meetings in a calendar
- Integrate events with Google Calendar
- Set custom reminders for upcoming deadlines and class meetings 

## Technologies Used

- Frontend: HTML, JavaScript
- Backend: Python with Flask
- Database: SQLite
- Testing: pytest
- Cross-origin communication: Flask-CORS
- Calendar integration: Google Calendar API
- Authentication: Google OAuth 2.0

## Project Status 

SyllabusFlow is currently under development. The team is working on the system design, requirements, and an early working version of the application. The Google Calendar integration can authorize a user, save exam information locally, and create a matching calendar event.

## REQ 2 Explaination

This requirement means that after a student uploads a syllabus, the system will use AI to find the most important academic dates, such as exams, quizzes, and assignments. The extracted dates will then be intergrated into Google Calendar in order to organize their events. 

Acceptance Criterion: When a valid syllabus is uploaded into the web application with multiple dates, the system identifies and displays those dates with their accurate information. The student can then add the relevant dates to their Google Calendar.

## Project structure

```text
.
├── app.py
├── requirements.txt
├── src/
│   ├── exam.py
│   ├── exam_database.py
│   └── google_calendar_service.py
├── frontend/
│   ├── index.html
│   └── script.js
├── credentials.json       # local only; do not commit
├── token.json             # generated after OAuth; do not commit
└── events.db              # generated SQLite database; do not commit
```

## Requirements

- Python 3.13 or a compatible Python 3 version
- pip
- Git
- A web browser
- A Google account for testing

SQLite is included with Python and does not require a separate installation.

## First-time setup

### 1. Clone the repository

```powershell
git clone https://github.com/SilverFalcon763/syllabus-calendar-integration
cd syllabus-calendar-integration
```

### 2. Configure Google Cloud OAuth

The Google Calendar integration requires a Google Cloud OAuth application.

#### If the existing project is being used

The original project owner must provide the project’s `credentials.json` file to the new team through a secure channel. Do not commit this file to GitHub.

Because the application is published, new team members can authorize their own Google accounts when they connect Google Calendar.

#### If a new Google Cloud project is created

1. Open the Google Cloud Console:
   https://console.cloud.google.com/
2. Create a new project.
3. Open **APIs & Services → Library**.
4. Search for and enable **Google Calendar API**.
5. Open **Google Auth Platform → Branding** and configure the application name and support email.
6. Add the team members as test users.
7. Go to **Google Auth Platform → Clients** or **APIs & Services → Credentials**.
8. Create an OAuth client.
9. Select **Web application** as the application type.
10. Add this authorized redirect URI:

```text
http://127.0.0.1:5000/oauth2callback

### 3. Install dependencies

From the repository root:

```powershell
python -m pip install -r requirements.txt
```

### Terminal: start Flask

```powershell
$env:OAUTHLIB_INSECURE_TRANSPORT="1"
python app.py
```

The environment variable is required only because local development uses HTTP. Do not use it in production.

The backend should start at:

```text
http://127.0.0.1:5000
```

Than in a new terminal type:
```text
open frontend/index.html
```

## Google Calendar authorization

1. Open the frontend from ...\syllabus-calendar-integration\frontend\index.html.
2. Click **Connect Google Calendar**.
3. Sign in with a Google account.
4. Approve the requested calendar permission.
5. Wait for the callback confirmation.
6. Return to the syllabus page using the back arrows.

After successful authorization, the application creates `token.json`. This file must not be committed.

## Add an exam

1. Enter the course name.
2. Enter the exam title.
3. Select the exam date.
4. Click the submit button.
5. Confirm that the exam appears in the event list.
6. Confirm that the status reports whether it was added to Google Calendar.
7. Click the **Open event** calendar link to verify that it was added to the Google Calendar.

The application should also save the exam in `events.db`, which is created automatically.

## API routes

| Method | Route | Purpose |
|---|---|---|
| GET | `/` | Confirms that the Flask backend is running. |
| GET | `/authorize` | Starts Google OAuth authorization. |
| GET | `/oauth2callback` | Completes OAuth and saves authorization. |
| POST | `/events` | Saves an exam and attempts calendar insertion. |
| GET | `/events` | Returns locally saved exams. |



## Common problems

### `OAuth 2 MUST utilize https`

The app is generating an HTTP OAuth URL where HTTPS is required.

- For local testing, set `OAUTHLIB_INSECURE_TRANSPORT="1"` in the same terminal used to run Flask.

### The frontend cannot reach Flask

Confirm that `python app.py` is still running

## Security notes

Never commit:

```text
credentials.json
token.json
events.db
```
