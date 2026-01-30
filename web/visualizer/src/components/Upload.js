import React from "react";

function Upload({ onUpload }) {
  return (
    <div style={{ marginBottom: 20 }}>
      <input type="file" accept=".csv" onChange={onUpload} />
    </div>
  );
}

export default Upload;
