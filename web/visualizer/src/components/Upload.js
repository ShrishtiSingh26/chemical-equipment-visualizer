import React, { useState } from "react";

const Upload = ({ onUpload }) => {
  const [fileName, setFileName] = useState("");

  const handleChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFileName(file.name);
      onUpload(e); // Passing the event up to your App.js handleUpload
    }
  };

  return (
    <div className="upload-container">
      <label htmlFor="csv-upload" className="fancy-upload-label">
        <div className="upload-icon">📁</div>
        <div className="upload-text">
          <span className="primary-text">
            {fileName ? "File Selected" : "Click to upload CSV"}
          </span>
          <span className="secondary-text">
            {fileName ? fileName : "or drag and drop here"}
          </span>
        </div>
        <input
          type="file"
          id="csv-upload"
          accept=".csv"
          onChange={handleChange}
          style={{ display: "none" }} // Hide the actual input
        />
      </label>
    </div>
  );
};

export default Upload;