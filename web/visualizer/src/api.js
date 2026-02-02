const API_BASE = "http://127.0.0.1:8000";

// demo credentials
const USERNAME = "admin";
const PASSWORD = "123";

const AUTH_HEADERS = {
  Authorization: "Basic " + btoa(`${USERNAME}:${PASSWORD}`),
};

export const uploadCSV = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE}/api/upload/`, {
    method: "POST",
    body: formData,
    headers: AUTH_HEADERS,
  });

  if (!res.ok) throw new Error("Upload failed");
  return res.json();
};

export const fetchHistory = async () => {
  const res = await fetch(`${API_BASE}/api/history/`, {
    headers: AUTH_HEADERS,
  });
  return res.json();
};

export const downloadPDF = async () => {
  const res = await fetch(`${API_BASE}/api/report/`, {
    headers: AUTH_HEADERS,
  });
  return res.blob();
};
