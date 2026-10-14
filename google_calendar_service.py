import os
from datetime import date as Date, timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .exam import Exam


SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


class GoogleCalendarService:
    def __init__(
        self,
        calendar_id: str = "primary",
        credentials_file: str = "credentials.json",
        token_file: str = "token.json",
    ):
        self.calendar_id = calendar_id
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.credentials = None
        self.last_event_link = None

    def authorize_user(self) -> bool:
        """Load or refresh saved Google OAuth credentials."""

        if self.credentials and self.credentials.valid:
            return True

        if os.path.exists(self.token_file):
            self.credentials = Credentials.from_authorized_user_file(
                self.token_file,
                SCOPES,
            )

        if (
            self.credentials
            and self.credentials.expired
            and self.credentials.refresh_token
        ):
            self.credentials.refresh(Request())
            self._save_credentials()

        return bool(self.credentials and self.credentials.valid)

    def get_authorization_url(
        self,
        redirect_uri: str,
    ) -> tuple[str, str, str | None]:
        """Create the Google authorization URL and PKCE verifier."""

        if not os.path.exists(self.credentials_file):
            raise FileNotFoundError(
                f"Could not find {self.credentials_file}"
            )

        flow = Flow.from_client_secrets_file(
            self.credentials_file,
            scopes=SCOPES,
            redirect_uri=redirect_uri,
            autogenerate_code_verifier=True,
        )

        authorization_url, state = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            prompt="consent",
        )

        return authorization_url, state, flow.code_verifier

    def finish_authorization(
        self,
        authorization_response: str,
        state: str,
        redirect_uri: str,
        code_verifier: str | None = None,
    ) -> bool:
        """Finish OAuth after Google redirects back to Flask."""

        flow = Flow.from_client_secrets_file(
            self.credentials_file,
            scopes=SCOPES,
            state=state,
            redirect_uri=redirect_uri,
            autogenerate_code_verifier=False,
        )

        flow.code_verifier = code_verifier
        flow.fetch_token(
            authorization_response=authorization_response
        )

        self.credentials = flow.credentials
        self._save_credentials()

        return self.authorize_user()

    def _save_credentials(self):
        with open(self.token_file, "w", encoding="utf-8") as token_file:
            token_file.write(self.credentials.to_json())

    def _event_payload(self, exam: Exam) -> dict:
        """Convert an Exam into an all-day Google Calendar event."""

        start_date = Date.fromisoformat(exam.get_date())
        end_date = start_date + timedelta(days=1)

        return {
            "summary": f"{exam.course}: {exam.title}",
            "description": exam.get_details(),
            "start": {
                "date": start_date.isoformat()
            },
            "end": {
                "date": end_date.isoformat()
            },
        }

    def add_exam(self, exam: Exam) -> bool:
        """Add an exam to Google Calendar."""

        if not self.authorize_user():
            return False

        try:
            calendar = build(
                "calendar",
                "v3",
                credentials=self.credentials,
                cache_discovery=False,
            )

            created_event = (
                calendar.events()
                .insert(
                    calendarId=self.calendar_id,
                    body=self._event_payload(exam),
                )
                .execute()
            )

            self.last_event_link = created_event.get("htmlLink")
            return True

        except (HttpError, TimeoutError, OSError):
            return False