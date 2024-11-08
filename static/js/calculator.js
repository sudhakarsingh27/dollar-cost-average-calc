// Initialize form with default values
function initializeForm() {
    // Set default ticker
    document.getElementById("ticker").value = "AAPL";
    
    // Set default amount
    document.getElementById("amount").value = "10";
    
    // Set default frequency
    document.getElementById("frequency").value = "daily";
    
    // Set start date to first Monday of 2024 (January 1st, 2024)
    document.getElementById("start-date").value = "2024-01-01";
    
    // Set end date to today
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    document.getElementById("end-date").value = `${year}-${month}-${day}`;
}

// Handle form submission
function handleDateSubmission(ticker, amount, frequency, startDate, endDate) {
    fetch('/api/submit-dates', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            ticker: ticker,
            amount: parseFloat(amount),
            frequency: frequency,
            start_date: startDate, 
            end_date: endDate
        }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        displayResults(data);
        createChart(data);
    })
    .catch((error) => {
        document.getElementById("result").innerText = `Error: ${error.message}`;
        console.error('Error:', error);
    });
}

// Display results in table format
function displayResults(data) {
    let resultsHTML = `
        <div style="margin-top: 30px;">
            <h3 style="text-align: center;">Investment Results for ${data.symbol}</h3>
            <table>
                <!-- ... rest of your table HTML ... -->
            </table>
            <div style="margin-top: 40px;">
                <canvas id="investmentChart"></canvas>
            </div>
        </div>
    `;
    document.getElementById("result").innerHTML = resultsHTML;
}

// Create chart visualization
function createChart(data) {
    const ctx = document.getElementById('investmentChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Daily', 'Weekly', 'Monthly'],
            datasets: [
                {
                    label: 'Total Invested',
                    data: [
                        data.results.daily.total_invested,
                        data.results.weekly.total_invested,
                        data.results.monthly.total_invested
                    ],
                    backgroundColor: 'rgba(54, 162, 235, 0.8)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1,
                    order: 2
                },
                {
                    label: 'Profit/Loss',
                    data: [
                        data.results.daily.profit_loss,
                        data.results.weekly.profit_loss,
                        data.results.monthly.profit_loss
                    ],
                    backgroundColor: [
                        data.results.daily.profit_loss >= 0 ? 'rgba(75, 192, 192, 0.8)' : 'rgba(255, 99, 132, 0.8)',
                        data.results.weekly.profit_loss >= 0 ? 'rgba(75, 192, 192, 0.8)' : 'rgba(255, 99, 132, 0.8)',
                        data.results.monthly.profit_loss >= 0 ? 'rgba(75, 192, 192, 0.8)' : 'rgba(255, 99, 132, 0.8)'
                    ],
                    borderColor: [
                        data.results.daily.profit_loss >= 0 ? 'rgba(75, 192, 192, 1)' : 'rgba(255, 99, 132, 1)',
                        data.results.weekly.profit_loss >= 0 ? 'rgba(75, 192, 192, 1)' : 'rgba(255, 99, 132, 1)',
                        data.results.monthly.profit_loss >= 0 ? 'rgba(75, 192, 192, 1)' : 'rgba(255, 99, 132, 1)'
                    ],
                    borderWidth: 1,
                    order: 1
                }
            ]
        },
        options: {
            // ... rest of your chart options ...
        }
    });
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    initializeForm();

    document.getElementById("dateForm").addEventListener("submit", function(event) {
        event.preventDefault();
        
        const ticker = document.getElementById("ticker").value;
        const amount = document.getElementById("amount").value;
        const frequency = document.getElementById("frequency").value;
        const startDate = document.getElementById("start-date").value;
        const endDate = document.getElementById("end-date").value;

        handleDateSubmission(ticker, amount, frequency, startDate, endDate);
    });

    document.getElementById('ticker').addEventListener('input', function(e) {
        const input = e.target;
        const value = input.value.toUpperCase();
        if (value !== input.value) {
            input.value = value;
        }
    });
}); 