import React from "react";
import { Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

function EquipmentChart({ data }) {
  return (
    <Pie
      data={{
        labels: Object.keys(data),
        datasets: [
          {
            data: Object.values(data),
            backgroundColor: [
              "#FF6384",
              "#36A2EB",
              "#FFCE56",
              "#4BC0C0",
              "#9966FF",
              "#FF9F40",
            ],
          },
        ],
      }}
    />
  );
}

export default EquipmentChart;
