import React, { useEffect, useState } from "react";

function HistoryTable() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/history/")
      .then(res => res.json())
      .then(data => setHistory(data))
      .catch(() => {});
  }, []);

  if (history.length === 0) return null;

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
          {history.map((item, i) => (
            <tr key={i}>
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
