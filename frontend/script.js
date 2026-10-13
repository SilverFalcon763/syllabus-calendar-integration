console.log("script loaded");

const form = document.querySelector("form");

form.addEventListener("submit", (e) => {
  e.preventDefault();
  console.log("check");

  const newEvent = {
    course: document.getElementById("course").value,
    title: document.getElementById("title").value,
    date: document.getElementById("date").value,
  };
  console.log(newEvent);

  fetch("http://127.0.0.1:5000/events", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(newEvent),
  });

  const item = document.createElement("li");
  item.textContent =
    newEvent.course + " - " + newEvent.title + " - " + newEvent.date;
  document.getElementById("event-list").appendChild(item);
});

fetch("http://127.0.0.1:5000/events")
  .then((response) => response.json())
  .then((events) => {
    events.forEach((event) => {
      const item = document.createElement("li");
      item.textContent = event.course + " - " + event.title + " - " + event.date;
      document.getElementById("event-list").appendChild(item);
    });
  });