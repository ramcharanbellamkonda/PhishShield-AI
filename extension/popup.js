let currentURL = "";

chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {

    currentURL = tabs[0].url;

    document.getElementById("url").innerHTML = currentURL;

});

document.getElementById("scanBtn").addEventListener("click", async () => {

    const result = document.getElementById("result");

    // Don't scan Chrome internal pages
    if (
        currentURL.startsWith("chrome://") ||
        currentURL.startsWith("edge://") ||
        currentURL.startsWith("about:") ||
        currentURL.startsWith("chrome-extension://")
    ) {

        result.innerHTML = "⚠ Open a website first.";

        result.style.color = "orange";

        return;
    }

    result.innerHTML = "🔄 Scanning...";

    result.style.color = "#3b82f6";

    try {

        const response = await fetch("http://127.0.0.1:5000/predict", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                url: currentURL
            })

        });

        const data = await response.json();

        if (data.prediction === "Legitimate") {

            result.innerHTML = `
                🟢 <b>SAFE</b><br><br>
                Confidence : ${data.confidence}%<br>
                Risk : ${data.risk}
            `;

            result.style.color = "#22c55e";

        } else {

            result.innerHTML = `
                🔴 <b>PHISHING</b><br><br>
                Confidence : ${data.confidence}%<br>
                Risk : ${data.risk}
            `;

            result.style.color = "#ef4444";

        }

    } catch (error) {

        console.error(error);

        result.innerHTML = "❌ Flask Server Not Running";

        result.style.color = "red";

    }

});