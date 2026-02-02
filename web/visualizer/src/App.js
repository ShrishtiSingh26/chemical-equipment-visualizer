import React, { useState } from "react";
import { uploadCSV, downloadPDF } from "./api";
import "./App.css";

import Upload from "./components/Upload";
import SummaryCards from "./components/SummaryCards";
import EquipmentChart from "./components/EquipmentChart";
import Loading from "./components/Loading";
import HistoryTable from "./components/HistoryTable";

function App() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [chartType, setChartType] = useState("pie");

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

  const handleDownloadPDF = async () => {
    try {
      const blob = await downloadPDF();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "equipment_report.pdf";
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError("Failed to download PDF");
    }
  };

  // Extract summary data for the header box
  const getSummaryData = () => {
    if (!summary) return null;
    
    return {
      totalEquipment: summary.total_equipment || 0,
      avgFlowrate: summary.avg_flowrate ? summary.avg_flowrate.toFixed(2) : "0.00",
      avgPressure: summary.avg_pressure ? summary.avg_pressure.toFixed(2) : "0.00",
      avgTemperature: summary.avg_temperature ? summary.avg_temperature.toFixed(2) : "0.00"
    };
  };

  const summaryData = getSummaryData();

  return (
    <div className="app-wrapper">
      {/* Main Header */}
      <header className="main-header">
        <div className="header-content">
          <div className="logo-section">
            
            <h1 className="app-main-title">Chemical Equipment Dashboard</h1>
          </div>
          <div className="header-info">
            <div className="header-status">
              <span className="status-indicator active"></span>
              <span>System Status: <strong>Operational</strong></span>
            </div>
            {summary && !loading && (
              <button onClick={handleDownloadPDF} className="header-download-btn">
                 Download Full Report
              </button>
            )}
          </div>
        </div>
      </header>

      <div className="app-container">
        <div className="content-wrapper">
          <div className="upload-section">
            <Upload onUpload={handleUpload} />
          </div>

          {loading && <Loading />}

          {error && <p className="error-message" style={{ color: "red", padding: "10px", background: "#ffebee", borderRadius: "6px", margin: "20px 0" }}>{error}</p>}

          {summary && !loading && summaryData && (
            <>
              {/* Summary Header Section */}
              <div className="summary-header">
                <div className="summary-title">
                  <h3>Equipment Overview</h3>
                  <span className="last-updated">Last updated: Just now</span>
                </div>
                <div className="summary-cards-container">
                  <div className="summary-card">
                    <div className="card-icon"></div>
                    <h4>Total Equipment</h4>
                    <p>{summaryData.totalEquipment}</p>
                    <span className="card-subtitle">Active Units</span>
                  </div>
                  <div className="summary-card">
                    <div className="card-icon"></div>
                    <h4>Avg Flowrate</h4>
                    <p>{summaryData.avgFlowrate}</p>
                    <span className="card-subtitle">L/min</span>
                  </div>
                  <div className="summary-card">
                    <div className="card-icon"></div>
                    <h4>Avg Pressure</h4>
                    <p>{summaryData.avgPressure}</p>
                    <span className="card-subtitle">psi</span>
                  </div>
                  <div className="summary-card">
                    <div className="card-icon"></div>
                    <h4>Avg Temperature</h4>
                    <p>{summaryData.avgTemperature}</p>
                    <span className="card-subtitle">°C</span>
                  </div>
                </div>
              </div>

              

              {/* Table and Chart Side by Side */}
              <div className="table-chart-wrapper">
                {/* History Table on Left */}
                <div className="history-section">
                  <div className="history-header">
                    <h3> Processing History</h3>
                    <div className="header-actions">
                      
                    </div>
                  </div>
                  <div className="history-table-container">
                    <HistoryTable />
                  </div>
                </div>

                {/* Chart on Right */}
                <div className="chart-section">
                  <div className="chart-header">
                    <h3> Equipment Distribution</h3>
                    <button
                      onClick={() => setChartType(chartType === "pie" ? "bar" : "pie")}
                      className="chart-toggle-btn"
                    >
                      {chartType === "pie" ? "Switch to Bar Chart" : " Switch to Pie Chart"}
                    </button>
                  </div>
                  <div className="chart-container">
                    <EquipmentChart
                      data={summary.type_distribution}
                      type={chartType}
                    />
                  </div>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;