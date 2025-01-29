document.getElementById("predictionForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    
    // Collect form data
    const formData = {
        age: parseInt(document.getElementById("age").value),
        sex: document.getElementById("sex").value,
        bmi: parseFloat(document.getElementById("bmi").value),
        children: parseInt(document.getElementById("children").value),
        smoker: document.getElementById("smoker").value,
        region: document.getElementById("region").value
    };

    // Send POST request to the API
    const response = await fetch("https://medical-insurance-cost-prediction-b9kw.onrender.com/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
    });

    const result = await response.json();
    document.getElementById("result").textContent = `Predicted Cost: $${result.predicted_cost}`;
});
