import React, { useState } from "react";
import { uploadCSV } from "./api";

import Upload from "./components/Upload";
import SummaryCards from "./components/SummaryCards";
import EquipmentChart from "./components/EquipmentChart";
import Loading from "./components/Loading";
import HistoryTable from "./components/HistoryTable";


function App() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleUpload = async (e) => {
    const file = e.target.files[0];

    if (!file) {
      setError("Please select a CSV file.");
      return;
    }

    setError("");
    setLoading(true);

    try {
      const data = await uploadCSV(file);
      setSummary(data);
    } catch (err) {
      setError("Failed to upload file or fetch data from server.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 40, fontFamily: "Arial" }}>
      <h2>Chemical Equipment Parameter Visualizer</h2>

      <Upload onUpload={handleUpload} />

      {loading && <Loading />}

      {error && (
        <p style={{ color: "red", fontWeight: "bold" }}>
          {error}
        </p>
      )}

      {summary && !loading && (
        <>
          <SummaryCards summary={summary} />

          <div style={{ maxWidth: 500, marginTop: 30 }}>
            <EquipmentChart data={summary.type_distribution} />
          </div>
           {/* History Table */}
    <div style={{ marginTop: 40 }}>
      <HistoryTable />
    </div>
        </>
      )}
    </div>
  );
}

export default App;
