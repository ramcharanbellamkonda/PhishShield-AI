window.onload = async () => {
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  let response = await fetch("http://127.0.0.1:5000/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ url: tab.url })
  });

  let data = await response.json();

  let resultEl = document.getElementById("result");
  let detailsEl = document.getElementById("details");

  resultEl.innerText = `${data.result} (${data.risk}%)`;
  resultEl.className = data.result === "Phishing" ? "phishing" : "safe";

  detailsEl.innerText = data.reason;
};