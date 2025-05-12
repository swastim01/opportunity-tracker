import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

export default function App() {
  const [programName, setProgramName] = useState('');
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    try {
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ program: programName, email: email })
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      setResult({ error: 'Something went wrong. Try again.' });
    }

    setLoading(false);
  };

  return (
    <div className="container mt-5">
      <h2 className="mb-4">🔍 Opportunity Tracker</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group mb-3">
          <label>Enter Program Name</label>
          <input
            type="text"
            className="form-control"
            value={programName}
            onChange={(e) => setProgramName(e.target.value)}
            placeholder="e.g. Atlassian Women in Tech"
            required
          />
        </div>
        <div className="form-group mb-3">
          <label>Your Email (for alerts)</label>
          <input
            type="email"
            className="form-control"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            required
          />
        </div>
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Processing...' : 'Analyze & Notify Me'}
        </button>
      </form>

      {result && (
        <div className="mt-4">
          {result.error ? (
            <div className="alert alert-danger">{result.error}</div>
          ) : (
            <div className="alert alert-success">
              <h5>✅ Result</h5>
              <p><strong>Program:</strong> {result.program}</p>
              <p><strong>Predicted Deadline:</strong> {result.predicted}</p>
              <p><strong>Top Links:</strong></p>
              <ul>
                {result.links.map((link, i) => (
                  <li key={i}><a href={link} target="_blank" rel="noreferrer">{link}</a></li>
                ))}
              </ul>
              <p className="mt-2 text-muted">📧 An email with this info was sent to <strong>{email}</strong></p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
