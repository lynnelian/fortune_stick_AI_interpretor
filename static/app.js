document.getElementById("question-form").addEventListener("submit", (e) => {
    e.preventDefault();
    
    const question = document.getElementById("question").value;
    
    fetch("/get_answer_from_llm", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
    })
    .then((response) => response.json())
    .then((data) => {
        document.getElementById("answer-text").innerText = data.answer;
        document.getElementById("answer").style.display = "block";
    })
    .catch((error) => {
        console.error("Error:", error);
    });
});