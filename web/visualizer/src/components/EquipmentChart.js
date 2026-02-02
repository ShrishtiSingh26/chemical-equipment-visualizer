import React from "react";
import { Pie, Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
} from "chart.js";

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement
);

function EquipmentChart({ data, type }) {
  const chartData = {
    labels: Object.keys(data),
    datasets: [
      {
        label: "Equipment Count",
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
  };

  return type === "bar" ? (
    <Bar data={chartData} />
  ) : (
    <Pie data={chartData} />
  );
}

export default EquipmentChart;
