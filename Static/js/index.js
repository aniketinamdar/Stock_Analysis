
function selectAnalysis()
{
    // e.preventDefault();
    // alert("NIGGA")
    var stockSymbol = document.getElementById('stockSymbol').value;
    var exchange = document.getElementById('exchange').value;
    var action = document.getElementById('action').value;
    var resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = ''; // Clear previous results

    switch(action) {
        case 'fundamental':
            displayFundamentalAnalysis(resultsDiv);
            break;
        case 'technical':
            displayTechnicalAnalysisForm(resultsDiv);
            break;
        case 'intraday':
            displayIntradayForm(resultsDiv);
            break;
        case 'swing':
            displaySwingForm(resultsDiv);
            break;
    }
};

function displayFundamentalAnalysis(container) {
    container.innerHTML = '<p>[Display 2-3 paragraphs of technical analysis text here]</p>';

}

function displayTechnicalAnalysisForm(container) {
    container.innerHTML = `
        <div id="technicalForm">
            <label for="chartImage">Upload Chart Image:</label>
            <input type="file" id="chartImage" name="chartImage" required>

            <label for="timeFrame">Time Frame:</label>
            <select id="timeFrame" name="timeFrame">
                <option value="5m">5 Minutes</option>
                <option value="15m">15 Minutes</option>
                <option value="1h">1 Hour</option>
                <option value="1d">1 Day</option>
            </select>

            <input type="submit" value="Analyze Chart">
        </div>
        <div id="technicalResults"></div>
    `;

    document.getElementById('technicalForm').addEventListener('submit', function(e) {
        e.preventDefault();
        // Process and display technical analysis results
        document.getElementById('technicalResults').innerHTML = '<p>[Display 2-3 paragraphs of technical analysis text here]</p>';
    });
}

function displayIntradayForm(container) {
    // Similar logic for Intraday Form
}

function displaySwingForm(container) {
    // Similar logic for Swing Form
}
