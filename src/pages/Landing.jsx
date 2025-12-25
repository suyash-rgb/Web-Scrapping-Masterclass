// src/pages/Landing.jsx
import { useState } from "react";
import Spinner from "../components/Spinner";

export default function Landing() {
  const [url, setUrl] = useState("");
  const [error, setError] = useState("");
  const [output, setOutput] = useState(
    "Sample scraped text line 1\nSample scraped text line 2"
  );
  const [scraping, setScraping] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  // URL validation
  const validateUrl = (value) => {
    try {
      const parsed = new URL(value);
      if (parsed.protocol !== "https:") {
        return "Please enter a secure URL starting with https://";
      }
      return "";
    } catch {
      return "Invalid URL format.";
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const validationError = validateUrl(url);
    if (validationError) {
      setError(validationError);
      setSubmitted(false);
    } else {
      setError("");
      setSubmitted(true);
      //setOutput("Scraped text will appear here line by line...");

      // Simulate scraping delay
      setTimeout(() => {
        setScraping(false);
        setOutput("Scraped text will appear here line by line...");
      }, 3000);
    }
  };

  const handleStop = () => {
    setSubmitted(false);
    setScraping(false);
    setOutput("");
  };

  // Export functions
  const exportFile = (type) => {
    let blob;
    if (type === "txt") {
      blob = new Blob([output], { type: "text/plain" });
    } else if (type === "json") {
      blob = new Blob([JSON.stringify({ data: output.split("\n") }, null, 2)], {
        type: "application/json",
      });
    } else if (type === "csv") {
      blob = new Blob([output.split("\n").join(",")], { type: "text/csv" });
    }
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `scraped-data.${type}`;
    link.click();
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 px-6">
      <h1 className="text-4xl font-bold text-blue-700 mb-6">ScrapeMate</h1>

      {/* Input Form */}
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-4xl bg-white shadow-md rounded px-8 py-6"
      >
        <label className="block text-gray-700 font-semibold mb-2">
          Enter Website URL:
        </label>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://example.com"
          className="w-full border rounded px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        {error && <p className="text-red-500 text-sm mt-2">{error}</p>}
        <div className="flex space-x-4 mt-4">
          <button
            type="submit"
            className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
          >
            Scrape Data
          </button>
          {submitted && (
            <button
              type="button"
              onClick={handleStop}
              className="bg-red-600 text-white px-6 py-2 rounded hover:bg-red-700"
            >
              Stop Scraping
            </button>
          )}
        </div>
      </form>

      {/* Output Box */}
      {submitted && (
        <div className="w-full max-w-4xl bg-white shadow-md rounded px-8 py-6 mt-6">
          <h2 className="text-lg font-semibold text-gray-700 mb-2">
            Scraped Output:
          </h2>

          {scraping ? (
            <div className="flex flex-col items-center justify-center h-[200px]">
              <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-blue-600 border-solid mb-4"></div>
              <p className="text-gray-600">Scraping in process...</p>
            </div>
          ) : (
            <>
              <textarea
                readOnly
                value={output}
                className="w-full h-[400px] border rounded px-4 py-3 text-sm bg-gray-50 resize-none"
              />
              <div className="flex flex-wrap justify-between mt-4 gap-4">
                <button
                  onClick={() => exportFile("txt")}
                  className="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700"
                >
                  Export .txt
                </button>
                <button
                  onClick={() => exportFile("json")}
                  className="bg-yellow-500 text-white px-6 py-2 rounded hover:bg-yellow-600"
                >
                  Export JSON
                </button>
                <button
                  onClick={() => exportFile("csv")}
                  className="bg-purple-600 text-white px-6 py-2 rounded hover:bg-purple-700"
                >
                  Export CSV
                </button>
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
}
