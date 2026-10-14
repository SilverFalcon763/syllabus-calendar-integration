console.log("script loaded");

const form = document.querySelector("form");

form.addEventListener("submit", (e) => {
  e.preventDefault();

  const newExam = {
    course: document.getElementById("course").value,
    title: document.getElementById("title").value,
    date: document.getElementById("date").value,
  };

  fetch("http://127.0.0.1:5000/events", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(newExam),
  })
    .then((response) => response.json())
    .then((savedExam) => {
      const item = document.createElement("li");

      item.textContent =
        savedExam.course +
        " - " +
        savedExam.title +
        " - " +
        savedExam.date;

      document.getElementById("event-list").appendChild(item);

      const status = document.getElementById("status");

      if (savedExam.calendar_added) {
        status.textContent = "Saved and added to Google Calendar.";

        if (savedExam.calendar_link) {
          status.innerHTML += ` <a href="${savedExam.calendar_link}" target="_blank">Open event</a>`;
        }
      } else {
        status.textContent =
          "Saved locally, but Google Calendar is not connected. Click Connect Google Calendar first.";
      }
    })
    .catch(() => {
      document.getElementById("status").textContent =
        "Could not reach the Flask backend.";
    });
});

fetch("http://127.0.0.1:5000/events")
  .then((response) => response.json())
  .then((exams) => {
    exams.forEach((exam) => {
      const item = document.createElement("li");

      item.textContent =
        exam.course + " - " + exam.title + " - " + exam.date;

      document.getElementById("event-list").appendChild(item);
    });
  })
  .catch(() => {
    document.getElementById("status").textContent =
      "Could not load saved exams from the Flask backend.";
  });