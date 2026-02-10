import { useState } from "react";
import axios from "axios";

const API_URL = import.meta.env.PROD 
  ? "https://campaign-backend-vuf4.onrender.com"
  : "http://localhost:8000";

function BatchUpload() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResults(null);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a CSV file first");
      return;
    }

    setLoading(true);
    setResults(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await axios.post(`${API_URL}/predict-batch`, formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });

      setResults(res.data);
    } catch (err) {
      console.error(err);
      alert("Error: " + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const downloadResults = () => {
    if (!results) return;

    // Convert to CSV
    const predictions = results.predictions;
    const headers = Object.keys(predictions[0]).join(",");
    const rows = predictions.map(p => Object.values(p).join(","));
    const csv = [headers, ...rows].join("\n");

    // Download
    const blob = new Blob([csv], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "predictions.csv";
    a.click();
  };

  const downloadSampleCSV = () => {
    // Sample CSV with 3 example rows
    const sampleData = `Administrative,Administrative_Duration,Informational,Informational_Duration,ProductRelated,ProductRelated_Duration,BounceRates,ExitRates,PageValues,SpecialDay,Month,OperatingSystems,Browser,Region,TrafficType,VisitorType,Weekend
0,0,0,0,1,0,0.02,0.05,0,0,May,2,2,1,2,Returning_Visitor,False
2,40,1,15,5,120,0.01,0.03,25,0,Dec,1,1,1,1,New_Visitor,True
1,20,0,0,3,60,0.015,0.04,10,0.2,Nov,2,1,1,2,Returning_Visitor,False`;

    const blob = new Blob([sampleData], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "sample_visitors.csv";
    a.click();
  };

  return (
    <div style={{ 
      minHeight: "100vh", 
      backgroundColor: "#1a1a1a", 
      color: "#fff",
      padding: "40px 20px",
      fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    }}>
      <div style={{ maxWidth: 1000, margin: "0 auto" }}>
        
        {/* Header */}
        <div style={{ textAlign: "center", marginBottom: "40px" }}>
          <h1 style={{ fontSize: "42px", margin: "0 0 10px 0" }}>
            📊 Batch Prediction Upload
          </h1>
          <p style={{ fontSize: "16px", color: "#aaa" }}>
            Upload a CSV file to get predictions for multiple visitors at once
          </p>
        </div>

        {/* Upload Section */}
        <div style={{ 
          backgroundColor: "#242424", 
          padding: "40px", 
          borderRadius: "12px",
          border: "1px solid #333",
          marginBottom: "30px"
        }}>
          <h2 style={{ margin: "0 0 20px 0", fontSize: "24px" }}>Upload CSV File</h2>
          
          <div style={{ 
            border: "2px dashed #444", 
            borderRadius: "8px", 
            padding: "40px", 
            textAlign: "center",
            marginBottom: "20px"
          }}>
            <input
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              style={{ display: "none" }}
              id="file-upload"
            />
            <label 
              htmlFor="file-upload"
              style={{
                display: "inline-block",
                padding: "12px 24px",
                backgroundColor: "#333",
                borderRadius: "8px",
                cursor: "pointer",
                marginBottom: "10px"
              }}
            >
              📁 Choose CSV File
            </label>
            
            {file && (
              <p style={{ margin: "10px 0 0 0", color: "#0066ff" }}>
                Selected: {file.name}
              </p>
            )}
          </div>

          <button
            onClick={handleUpload}
            disabled={!file || loading}
            style={{
              width: "100%",
              padding: "16px",
              fontSize: "18px",
              fontWeight: "600",
              borderRadius: "8px",
              border: "none",
              backgroundColor: (!file || loading) ? "#555" : "#0066ff",
              color: "#fff",
              cursor: (!file || loading) ? "not-allowed" : "pointer"
            }}
          >
            {loading ? "🔄 Processing..." : "🚀 Upload & Predict"}
          </button>

          {/* Download Sample CSV Button */}
          <div style={{ marginTop: "20px", textAlign: "center" }}>
            <button
              onClick={downloadSampleCSV}
              style={{
                padding: "12px 24px",
                fontSize: "14px",
                fontWeight: "600",
                borderRadius: "8px",
                border: "1px solid #0066ff",
                backgroundColor: "transparent",
                color: "#0066ff",
                cursor: "pointer"
              }}
            >
              📥 Download Sample CSV Template
            </button>
            <p style={{ margin: "10px 0 0 0", fontSize: "12px", color: "#888" }}>
              Download a pre-filled example to see the correct format
            </p>
          </div>

          {/* Sample Format */}
          <div style={{ 
            marginTop: "30px", 
            padding: "20px", 
            backgroundColor: "#1a1a1a", 
            borderRadius: "8px" 
          }}>
            <h3 style={{ margin: "0 0 10px 0", fontSize: "16px", color: "#aaa" }}>
              📋 Required CSV Format:
            </h3>
            <code style={{ fontSize: "12px", color: "#0066ff" }}>
              Administrative, Administrative_Duration, Informational, Informational_Duration,
              ProductRelated, ProductRelated_Duration, BounceRates, ExitRates, PageValues,
              SpecialDay, Month, OperatingSystems, Browser, Region, TrafficType,
              VisitorType, Weekend
            </code>
          </div>
        </div>

        {/* Results */}
        {results && (
          <div style={{ 
            backgroundColor: "#242424", 
            padding: "30px", 
            borderRadius: "12px",
            border: "1px solid #333"
          }}>
            <h2 style={{ margin: "0 0 20px 0", fontSize: "24px" }}>📊 Results</h2>
            
            {/* Summary */}
            <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "20px", marginBottom: "30px" }}>
              <div style={{ backgroundColor: "#2a2a2a", padding: "20px", borderRadius: "8px" }}>
                <p style={{ margin: "0 0 8px 0", fontSize: "14px", color: "#aaa" }}>Total Predictions</p>
                <p style={{ margin: 0, fontSize: "36px", fontWeight: "bold", color: "#0066ff" }}>
                  {results.total_predictions}
                </p>
              </div>

              <div style={{ backgroundColor: "#2a2a2a", padding: "20px", borderRadius: "8px" }}>
                <p style={{ margin: "0 0 8px 0", fontSize: "14px", color: "#aaa" }}>Target</p>
                <p style={{ margin: 0, fontSize: "36px", fontWeight: "bold", color: "#28a745" }}>
                  {results.target_count}
                </p>
              </div>

              <div style={{ backgroundColor: "#2a2a2a", padding: "20px", borderRadius: "8px" }}>
                <p style={{ margin: "0 0 8px 0", fontSize: "14px", color: "#aaa" }}>Do Not Target</p>
                <p style={{ margin: 0, fontSize: "36px", fontWeight: "bold", color: "#dc3545" }}>
                  {results.total_predictions - results.target_count}
                </p>
              </div>
            </div>

            {/* Download Button */}
            <button
              onClick={downloadResults}
              style={{
                width: "100%",
                padding: "16px",
                fontSize: "18px",
                fontWeight: "600",
                borderRadius: "8px",
                border: "none",
                backgroundColor: "#28a745",
                color: "#fff",
                cursor: "pointer",
                marginBottom: "20px"
              }}
            >
              💾 Download Results as CSV
            </button>

            {/* Preview Table */}
            <div style={{ overflowX: "auto" }}>
              <h3 style={{ margin: "0 0 15px 0", fontSize: "18px" }}>Preview (First 10 Rows)</h3>
              <table style={{ width: "100%", fontSize: "13px", borderCollapse: "collapse" }}>
                <thead>
                  <tr style={{ backgroundColor: "#1a1a1a" }}>
                    <th style={{ padding: "12px", textAlign: "left" }}>Visitor Type</th>
                    <th style={{ padding: "12px", textAlign: "left" }}>Month</th>
                    <th style={{ padding: "12px", textAlign: "right" }}>Product Pages</th>
                    <th style={{ padding: "12px", textAlign: "right" }}>Page Values</th>
                    <th style={{ padding: "12px", textAlign: "right" }}>Probability</th>
                    <th style={{ padding: "12px", textAlign: "left" }}>Decision</th>
                  </tr>
                </thead>
                <tbody>
                  {results.predictions.slice(0, 10).map((pred, idx) => (
                    <tr key={idx} style={{ borderBottom: "1px solid #333" }}>
                      <td style={{ padding: "12px" }}>{pred.VisitorType}</td>
                      <td style={{ padding: "12px" }}>{pred.Month}</td>
                      <td style={{ padding: "12px", textAlign: "right" }}>{pred.ProductRelated}</td>
                      <td style={{ padding: "12px", textAlign: "right" }}>{pred.PageValues}</td>
                      <td style={{ padding: "12px", textAlign: "right" }}>
                        {(pred.probability * 100).toFixed(1)}%
                      </td>
                      <td style={{ padding: "12px" }}>
                        <span style={{ 
                          padding: "4px 8px", 
                          borderRadius: "4px",
                          backgroundColor: pred.decision === "TARGET" ? "#1a3a1a" : "#3a1a1a",
                          color: pred.decision === "TARGET" ? "#28a745" : "#dc3545",
                          fontSize: "12px",
                          fontWeight: "600"
                        }}>
                          {pred.decision === "TARGET" ? "TARGET" : "SKIP"}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}

export default BatchUpload;