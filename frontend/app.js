const queryInput = document.getElementById("query");
const submitButton = document.getElementById("submit");
const outputSection = document.getElementById("output");
const errorSection = document.getElementById("error");

const outQuery = document.getElementById("out-query");
const outSummary = document.getElementById("out-summary");
const outKeypoints = document.getElementById("out-keypoints");
const outConfidence = document.getElementById("out-confidence");

async function analyze() {
  const query = queryInput.value.trim();
  if (!query) {
    showError("Please enter a research query before submitting.");
    return;
  }
  clearOutput();
  submitButton.disabled = true;
  submitButton.textContent = "Analyzing...";

  try {
    const response = await fetch("/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Analysis request failed.");
    }

    const result = await response.json();
    outQuery.textContent = result.query;
    outSummary.textContent = result.summary;
    outConfidence.textContent = result.confidence.toFixed(2);
    outKeypoints.innerHTML = result.key_points
      .map((point) => `<li>${point}</li>`)
      .join("");
    outputSection.classList.remove("hidden");
  } catch (err) {
    showError(err.message || "Unexpected error while analyzing.");
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Analyze";
  }
}

function showError(message) {
  errorSection.textContent = message;
  errorSection.classList.remove("hidden");
}

function clearOutput() {
  errorSection.classList.add("hidden");
  outputSection.classList.add("hidden");
  errorSection.textContent = "";
  outQuery.textContent = "";
  outSummary.textContent = "";
  outKeypoints.innerHTML = "";
  outConfidence.textContent = "";
}

submitButton.addEventListener("click", analyze);
queryInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && event.shiftKey === false) {
    event.preventDefault();
    analyze();
  }
});
