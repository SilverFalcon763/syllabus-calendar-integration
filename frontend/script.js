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

      // Display the countdown for the newly saved exam
      showCountdown(newExam);

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

      // Check if there are any saved exams
      if (exams.length > 0) {
        // Display the countdown for the most recently saved exam
        showCountdown(exams[exams.length - 1]);
      }

  })
  .catch(() => {
    document.getElementById("status").textContent =
      "Could not load saved exams from the Flask backend.";
  });

  // Get the HTML Element where the countdown will be displayed
  const countdownDisplay = document.getElementById("countdown");

  // Store the countdown interval so it can be stopped when needed
  let countdownInterval; 

  // Get and display the countdown for a specific exam
  function showCountdown(exam) {

    // Send the exam information to Flask to calculate the remaining time
    fetch("http://127.0.0.1:5000/exam-countdown", {
      method: "POST", 
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(exam)
    })
      .then((response) => response.json())
      .then((result) => {
        // Display an error if Flask returns an error
        if (result.error) {
          countdownDisplay.textContent = result.error; 
          return; 
        }

        // Stop the previous countdown before starting a new one
        clearInterval(countdownInterval);

        // Display a message if the exam already started or passed
        if(result.countdown === null) { 
          countdownDisplay.textContent = result.message;
          return; 
        }

        // Get the remaining days, hours, minutes, and seconds
        let days = result.countdown.days;
        let hours = result.countdown.hours;
        let minutes = result.countdown.minutes; 
        let seconds = result.countdown.seconds; 

        // Update the countdown display every second
        function updateCountdown() {
          countdownDisplay.textContent = 
            exam.course + " - " +
            exam.title + ": " +
            days + " days, " + 
            hours + " hours, " +
            minutes + " minutes, " + 
            seconds + " seconds remaining"; 
          
          // Decrease the seconds by one
          seconds--; 

          // Reset seconds and decrease minutes when seconds reaches zero
          if (seconds < 0) {
            seconds = 59; 
            minutes--; 
          }

          // Reset minutes and decrease hours when minutes reach zero
          if (minutes < 0) {
            minutes = 59; 
            hours--; 
          }

          // Reset minutes and decrease hours when minutes reach zero
          if (hours < 0) { 
            hours = 23; 
            days--; 
          }

          // Stop the countdown when the exam starts
          if (days < 0) { 
            countdownDisplay.textContent = "Exam has started!";
            clearInterval(countdownInterval);
            return; 
          }
        }

        // Display the countdown immediately 
        updateCountdown();

        // Repeat the countdown update every 1000 milliseconds
        countdownInterval = setInterval(updateCountdown, 1000); 
      })
      .catch(() => {
        // Display an error if the request to Flask fails
        countdownDisplay.textContent = 
          "Could not load the exam countdown from the Flask backend.";
      });
  }