import React, { useState, useEffect } from 'react';
import { FiSun, FiMoon, FiRefreshCw, FiInfo } from 'react-icons/fi';

function App() {
  const [isDarkMode, setIsDarkMode] = useState(true);
  const [selectedFile, setSelectedFile] = useState(null);
  const [showInfo, setShowInfo] = useState(false);
  const [result, setResult] = useState('');
  const [uploadError, setUploadError] = useState('');
  
  // Ensure dark mode is set as default on initial load
  useEffect(() => {
    document.documentElement.classList.add('dark');
  }, []);

  const toggleDarkMode = () => {
    if (isDarkMode) {
      document.documentElement.classList.remove('dark');
    } else {
      document.documentElement.classList.add('dark');
    }
    setIsDarkMode(!isDarkMode);
  };

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleFileUpload = async () => {
    if (!selectedFile) {
      alert("Please select a file to upload.");
      return;
    }
    console.log("Uploading file:", selectedFile);
  
    const formData = new FormData();
    formData.append('file', selectedFile);
  
    try {
      const response = await fetch('http://127.0.0.1:5000/scan', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setResult(data.result);
      setUploadError('');
    } catch (err) {
      setUploadError("Error uploading the file. Please try again.");
      setResult('');
    }
  };

  const handleRefresh = () => {
    window.location.reload();
  };

  const toggleInfo = () => {
    setShowInfo(!showInfo);
  };

  return (
    <div className={`min-h-screen flex flex-col items-center justify-center transition-colors duration-500 ${isDarkMode 
      ? "bg-gradient-to-br from-gray-800 to-gray-900" 
      : "bg-gradient-to-br from-blue-100 via-purple-100 to-pink-100"}`}>
      
      <div className="w-full max-w-md px-4 py-6">
        {/* Options Bar */}
        <div className="flex items-center bg-white dark:bg-gray-800 p-4 rounded-lg shadow-lg mb-6">
          <div className="flex items-center space-x-3">
            <button onClick={toggleDarkMode} className="hover:scale-110 transition-transform hover:text-sky-400">
              {isDarkMode ? <FiSun size={20} /> : <FiMoon size={20} />}
            </button>
            <button onClick={handleRefresh} className="hover:scale-110 transition-transform hover:text-sky-400">
              <FiRefreshCw size={20} />
            </button>
            <button onClick={toggleInfo} className="hover:scale-110 transition-transform hover:text-sky-400">
              <FiInfo size={20} />
            </button>
          </div>
        </div>

        {/* Info Modal */}
        {showInfo && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg max-w-sm w-full">
              <h2 className="text-xl font-bold mb-4">About Malware Detection</h2>
              <p className="mb-4">
                This system uses a machine learning model to scan uploaded files for malware.
                The results indicate whether a file is safe or potentially malicious.
              </p>
              <button
                onClick={toggleInfo}
                className="w-full py-2 bg-sky-500 hover:bg-sky-600 text-white rounded-md transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        )}

        {/* Malware Detection Box */}
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg text-center space-y-4">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Malware Detection System
          </h1>
          <p className="text-gray-800 dark:text-gray-300">
            Upload a file to scan for potential malware threats.
          </p>

          {/* File Upload Section */}
          <div className="space-y-4">
            <input
              type="file"
              onChange={handleFileChange}
              className="block w-full text-sm text-gray-900 dark:text-gray-300 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-gray-200 dark:file:bg-gray-700 dark:file:text-gray-300 hover:file:bg-gray-300 dark:hover:file:bg-gray-600"
            />
            <button
              onClick={handleFileUpload}
              className="w-full px-4 py-2 bg-gradient-to-r from-sky-500 to-blue-500 hover:from-sky-600 hover:to-blue-600 text-white rounded-md transition-colors"
            >
              Upload &amp; Scan File
            </button>
          </div>

          {/* Results Section */}
          <div className="bg-gray-100 dark:bg-gray-900 p-4 rounded-md">
            {uploadError ? (
              <p className="text-sm text-red-500">{uploadError}</p>
            ) : (
              <p className="text-sm text-gray-900 dark:text-white">
                {result || "Scan results will appear here..."}
              </p>
            )}
          </div>

        </div>
      </div>
    </div>
  );
}

export default App;
