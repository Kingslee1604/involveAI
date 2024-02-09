import React, { useState } from 'react';
import './MarketResearchForm.css'; // Import the CSS file you'll create

function MarketResearchForm() {
    const [details, setDetails] = useState('');
    const [response, setResponse] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        const apiUrl = 'https://9a8urwmm59.execute-api.us-east-1.amazonaws.com/dev/market-research';
        const fetchedResponse = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ details })
        });
        const data = await fetchedResponse.json();
        setResponse(data.report);
    };

    return (
        <div className="market-research-container">
            <form onSubmit={handleSubmit} className="market-research-form">
                <label>
                    MarketGPT:
                    <input
                        type="text"
                        value={details}
                        onChange={(e) => setDetails(e.target.value)}
                        className="market-research-input"
                    />
                </label>
                <button type="submit" className="submit-button">Submit</button>
            </form>
            {response && (
                <div className="response-container">
                    <h2>Response:</h2>
                    <p>{response}</p>
                </div>
            )}
        </div>
    );
}

export default MarketResearchForm;
