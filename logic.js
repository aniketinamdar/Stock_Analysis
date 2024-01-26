
function selectAnalysis()
{
    // alert("NIGGA")
    var stockSymbol = document.getElementById('stock').value;
    var exchange = document.getElementById('exchange').value;
    var action = document.getElementById('action').value;
    var resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = ''; // Clear previous results

    switch(action) {
        case 'fundamental':
            displayFundamentalAnalysisForm(resultsDiv, stockSymbol, exchange);
            break;
        case 'technical':
            displayTechnicalAnalysisForm(resultsDiv);
            break;
        case 'intraday':
            displayIntradayForm(resultsDiv, stockSymbol, exchange);
            break;
        case 'swing':
            displaySwingForm(resultsDiv, stockSymbol, exchange);
            break;
    }
};

async function displayFundamentalAnalysisForm(container, stockSymbol, exchange){
    const response = await fetch(`https://aniketinamdar.github.io/Stock_Analysis/fundamental?stk=${stockSymbol}&exc=${exchange}`);
    const result = await response.text();
    container.innerHTML =`<div>${result}</div>`;
};

async function technical_analysis() {
    var stockSymbol = document.getElementById('stock').value;
    var exchange = document.getElementById('exchange').value;
    const inputElement = document.getElementById('chartImage');
    const timeFrame = document.getElementById('timeFrame').value;
    const selectedImage = inputElement.files[0];

    if (selectedImage) {
        const formData = new FormData();
        formData.append('chartImage', selectedImage);

        const result_string = "";

        const response = await fetch(`https://aniketinamdar.github.io/Stock_Analysis/technical?stk=${stockSymbol}&exc=${exchange}&tmf=${timeFrame}`, {
            method: 'POST',
            body: formData
        });
        const result = await response.text();
        document.getElementById('technicalResults').innerHTML = `<div>${result}</div>`;
    } else {
        console.log('No image selected');
    }
};

function displayTechnicalAnalysisForm(container) {
    container.innerHTML = `
        <div id="technicalForm">
        <div class="grid">
            <label for="chartImage">Upload Candlestick Chart Image
            <input type="file" id="chartImage" name="chartImage" required>
            </label>
            
            <label for="timeFrame">Candlestick Time Frame
            <select id="timeFrame" name="timeFrame">
                <option value="1m">1m</option>
                <option value="3m">3m</option>
                <option value="5m">5m</option>
                <option value="15m">15m</option>
                <option value="30m">30m</option>
                <option value="45m">45m</option>
                <option value="1h">1h</option>
                <option value="2h">2h</option>
                <option value="3h">3h</option>
                <option value="4h">4h</option>
                <option value="1D" selected>1D</option>
                <option value="1W">1W</option>
                <option value="1M">1M</option>
            </select>
            </label>
        </div>
            <button id="analyseButton" value="analyze" onclick="technical_analysis()">Analyze</button>
        </div>
        <div id="technicalResults"></div>
    `;
}

async function displayIntradayForm(container, stockSymbol, exchange) {
    const response = await fetch(`https://aniketinamdar.github.io/Stock_Analysis/positions?stk=${stockSymbol}&exc=${exchange}&pmt=intra`);
    const result = await response.text();
    container.innerHTML = `<div>${result}</div>`;
}

async function displaySwingForm(container, stockSymbol, exchange) {
    const response = await fetch(`https://aniketinamdar.github.io/Stock_Analysis/positions?stk=${stockSymbol}&exc=${exchange}&pmt=swing`);
    const result = await response.text();
    container.innerHTML = `<div>${result}</div>`;
}
