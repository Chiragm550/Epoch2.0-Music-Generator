"use client";

import { useState } from "react";

export default function UploadPage() {
  const [invokeComplete, setInvokeComplete] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [uploadStatus, setUploadStatus] = useState("");

  const handleFileChange = (event) => {
    setSelectedFiles([...event.target.files]); // Store multiple files
  };

  const handleUpload = async () => {
    if (selectedFiles.length === 0) {
      alert("Please select at least one file!");
      return;
    }

    const formData = new FormData();
    selectedFiles.forEach((file) => formData.append("files", file)); // Append multiple files

    try {
      const response = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();
      if (response.ok) {
        setUploadStatus(`Files uploaded successfully:\n${result.uploadedFiles.join("\n")}`);
      } else {
        setUploadStatus(`Upload failed: ${result.message}`);
      }
    } catch (error) {
      setUploadStatus("An error occurred while uploading the files.");
    }

  };



  const handleInvoke = async () => {
    setInvokeComplete(false);
    const response = await fetch("http://localhost:5000/invoke", {
      method: "POST",
    });
    const data = await response.json();
    alert(data.message);
        setInvokeComplete(true);
  };


  



  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-white p-6 shadow-lg rounded-lg mx-auto max-w-lg">
      <h1 className="text-2xl font-bold text-blue-600 mb-4">Upload MP3 Files</h1>
      <input 
        type="file" 
        accept=".mp3" 
        multiple 
        onChange={handleFileChange} 
        className="mb-4 border p-2 rounded w-full"
      />
      <button 
        onClick={handleUpload} 
        className="bg-blue-600 text-white px-6 py-3 rounded-lg shadow-md hover:bg-blue-700 transition">
        Upload
      </button>
      {uploadStatus && <p className="mt-4 text-green-600">{uploadStatus}</p>}


      <button
        onClick={handleInvoke}
        className="px-4 py-2 bg-blue-500 text-white rounded"
      >
      { "Invoke"}
      </button>
      {invokeComplete && (
        <div>
          <audio controls>
          <source src="http://localhost:5000/musicgen_out.wav" type="audio/wav" />
            Your browser does not support the audio element.
          </audio>
        </div>
      )}

    </div>
  );
}
