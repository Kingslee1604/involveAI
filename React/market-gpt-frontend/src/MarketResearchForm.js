import React, { useState } from 'react';

function MarketResearchForm() {
    const [details, setDetails] = useState('');
    const [response, setResponse] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        const fetchedResponse = await fetch('http://127.0.0.1:8000/market-research', {
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
        <div>
            <form onSubmit={handleSubmit}>
                <label>
                    Market Research Details:
                    <input
                        type="text"
                        value={details}
                        onChange={(e) => setDetails(e.target.value)}
                    />
                </label>
                <button type="submit">Submit</button>
            </form>
            {response && (
                <div className="response">
                    <h2>Response:</h2>
                    <p>{response}</p>
                </div>
            )}
        </div>
    );
}

export default MarketResearchForm;
