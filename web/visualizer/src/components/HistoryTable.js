import React, { useEffect, useState } from "react";
import { fetchHistory } from "../api";

function HistoryTable() {
  const [history, setHistory] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadHistory() {
      try {
        const data = await fetchHistory();

        // SAFETY CHECK (prevents map error)
        if (Array.isArray(data)) {
          setHistory(data);
        } else {
          setHistory([]);
        }
      } catch (err) {
        setError("Failed to load history");
      }
    }

    loadHistory();
  }, []);

  if (error) {
    return <p style={{ color: "red" }}>{error}</p>;
  }

  if (history.length === 0) {
    return <p>No upload history yet.</p>;
  }

  return (
    <div>
      <h3>Upload History (Last 5)</h3>

      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>Filename</th>
            <th>Uploaded At</th>
            <th>Total Equipment</th>
          </tr>
        </thead>

        <tbody>
          {history.map((item, index) => (
            <tr key={index}>
              <td>{item.filename}</td>
              <td>{new Date(item.uploaded_at).toLocaleString()}</td>
              <td>{item.summary.total_equipment}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default HistoryTable;
