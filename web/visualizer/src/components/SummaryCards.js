import React from "react";

function SummaryCards({ summary }) {
  return (
    <>
      <p>Total Equipment: {summary.total_equipment}</p>
      <p>Avg Flowrate: {summary.avg_flowrate.toFixed(2)}</p>
      <p>Avg Pressure: {summary.avg_pressure.toFixed(2)}</p>
      <p>Avg Temperature: {summary.avg_temperature.toFixed(2)}</p>
    </>
  );
}

export default SummaryCards;
