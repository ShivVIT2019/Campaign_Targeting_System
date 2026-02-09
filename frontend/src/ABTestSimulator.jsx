import { useState } from "react";
import axios from "axios";

const API_URL = import.meta.env.PROD 
  ? "https://campaign-backend-vuf4.onrender.com"
  : "http://localhost:8000";

function ABTestSimulator() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResults(null);
  };

  const handleSimulate = async () => {
    if (!file) {
      alert("Please select a CSV file first");
      return;
    }

    setLoading(true);
    setResults(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await axios.post(`${API_URL}/simulate-ab-test`, formData, {
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

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2
    }).format(value);
  };

  const getStrategyColor = (strategyKey) => {
    if (!results) return "#333";
    const roi = results.strategies[strategyKey].roi;
    if (roi > 200) return "#28a745";
    if (roi > 0) return "#7fba00";
    if (roi > -50) return "#ffa500";
    return "#dc3545";
  };

  return (
    <div style={{ 
      minHeight: "100vh", 
      backgroundColor: "#1a1a1a", 
      color: "#fff",
      padding: "40px 20px",
      fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    }}>
      <div style={{ maxWidth: 1200, margin: "0 auto" }}>
        
        {/* Header */}
        <div style={{ textAlign: "center", marginBottom: "40px" }}>
          <h1 style={{ fontSize: "42px", margin: "0 0 10px 0" }}>
            🧪 A/B Test Simulator
          </h1>
          <p style={{ fontSize: "16px", color: "#aaa" }}>
            Compare ML targeting vs traditional strategies and calculate ROI
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
          <h2 style={{ margin: "0 0 20px 0", fontSize: "24px" }}>Upload Campaign Data</h2>
          
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
              id="ab-file-upload"
            />
            <label 
              htmlFor="ab-file-upload"
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
            onClick={handleSimulate}
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
            {loading ? "🔄 Simulating..." : "🧪 Run A/B Test Simulation"}
          </button>
        </div>

        {/* Results */}
        {results && (
          <>
            {/* Overview */}
            <div style={{ 
              backgroundColor: "#242424", 
              padding: "30px", 
              borderRadius: "12px",
              border: "1px solid #333",
              marginBottom: "30px"
            }}>
              <h2 style={{ margin: "0 0 20px 0", fontSize: "24px" }}>📊 Campaign Overview</h2>
              
              <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "20px" }}>
                <div style={{ backgroundColor: "#2a2a2a", padding: "20px", borderRadius: "8px" }}>
                  <p style={{ margin: "0 0 8px 0", fontSize: "14px", color: "#aaa" }}>Total Visitors</p>
                  <p style={{ margin: 0, fontSize: "36px", fontWeight: "bold", color: "#0066ff" }}>
                    {results.total_visitors.toLocaleString()}
                  </p>
                </div>

                <div style={{ backgroundColor: "#2a2a2a", padding: "20px", borderRadius: "8px" }}>
                  <p style={{ margin: "0 0 8px 0", fontSize: "14px", color: "#aaa" }}>Cost per Contact</p>
                  <p style={{ margin: 0, fontSize: "36px", fontWeight: "bold", color: "#ffa500" }}>
                    {formatCurrency(results.comparison.cost_per_contact)}
                  </p>
                </div>

                <div style={{ backgroundColor: "#2a2a2a", padding: "20px", borderRadius: "8px" }}>
                  <p style={{ margin: "0 0 8px 0", fontSize: "14px", color: "#aaa" }}>Revenue per Conversion</p>
                  <p style={{ margin: 0, fontSize: "36px", fontWeight: "bold", color: "#28a745" }}>
                    {formatCurrency(results.comparison.revenue_per_conversion)}
                  </p>
                </div>
              </div>
            </div>

            {/* Strategy Comparison */}
            <div style={{ 
              backgroundColor: "#242424", 
              padding: "30px", 
              borderRadius: "12px",
              border: "1px solid #333",
              marginBottom: "30px"
            }}>
              <h2 style={{ margin: "0 0 20px 0", fontSize: "24px" }}>🎯 Strategy Comparison</h2>
              
              <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: "20px" }}>
                {Object.entries(results.strategies).map(([key, strategy]) => (
                  <div 
                    key={key}
                    style={{ 
                      backgroundColor: "#2a2a2a", 
                      padding: "24px", 
                      borderRadius: "8px",
                      border: `2px solid ${getStrategyColor(key)}`
                    }}
                  >
                    <h3 style={{ margin: "0 0 16px 0", fontSize: "18px", color: "#fff" }}>
                      {strategy.name}
                      {results.comparison.best_strategy === key && key === "ml_model" && (
                        <span style={{ marginLeft: "10px", fontSize: "20px" }}>🏆</span>
                      )}
                    </h3>

                    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px", marginBottom: "16px" }}>
                      <div>
                        <p style={{ margin: "0 0 4px 0", fontSize: "12px", color: "#888" }}>Contacted</p>
                        <p style={{ margin: 0, fontSize: "20px", fontWeight: "bold" }}>
                          {strategy.contacted.toLocaleString()}
                        </p>
                      </div>

                      <div>
                        <p style={{ margin: "0 0 4px 0", fontSize: "12px", color: "#888" }}>Conversions</p>
                        <p style={{ margin: 0, fontSize: "20px", fontWeight: "bold", color: "#0066ff" }}>
                          {strategy.expected_conversions.toFixed(1)}
                        </p>
                      </div>

                      <div>
                        <p style={{ margin: "0 0 4px 0", fontSize: "12px", color: "#888" }}>Cost</p>
                        <p style={{ margin: 0, fontSize: "20px", fontWeight: "bold", color: "#dc3545" }}>
                          {formatCurrency(strategy.cost)}
                        </p>
                      </div>

                      <div>
                        <p style={{ margin: "0 0 4px 0", fontSize: "12px", color: "#888" }}>Revenue</p>
                        <p style={{ margin: 0, fontSize: "20px", fontWeight: "bold", color: "#28a745" }}>
                          {formatCurrency(strategy.revenue)}
                        </p>
                      </div>
                    </div>

                    <div style={{ borderTop: "1px solid #444", paddingTop: "12px" }}>
                      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "8px" }}>
                        <span style={{ fontSize: "14px", color: "#aaa" }}>ROI</span>
                        <span style={{ 
                          fontSize: "24px", 
                          fontWeight: "bold", 
                          color: strategy.roi > 0 ? "#28a745" : "#dc3545" 
                        }}>
                          {strategy.roi.toFixed(1)}%
                        </span>
                      </div>
                      <div style={{ display: "flex", justifyContent: "space-between" }}>
                        <span style={{ fontSize: "14px", color: "#aaa" }}>Profit</span>
                        <span style={{ 
                          fontSize: "18px", 
                          fontWeight: "600", 
                          color: strategy.profit > 0 ? "#28a745" : "#dc3545" 
                        }}>
                          {formatCurrency(strategy.profit)}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Winner */}
            <div style={{ 
              backgroundColor: "#1a3a1a", 
              border: "2px solid #28a745",
              padding: "30px", 
              borderRadius: "12px",
              textAlign: "center"
            }}>
              <h2 style={{ margin: "0 0 10px 0", fontSize: "28px" }}>
                🏆 ML Model Wins!
              </h2>
              <p style={{ margin: "0 0 20px 0", fontSize: "16px", color: "#aaa" }}>
                {results.comparison.ml_vs_random_lift > 0 ? 
                  `${results.comparison.ml_vs_random_lift.toFixed(1)}% better ROI than random selection` :
                  "ML targeting optimizes campaign performance"}
              </p>
              <div style={{ display: "flex", justifyContent: "center", gap: "40px" }}>
                <div>
                  <p style={{ margin: "0 0 8px 0", fontSize: "14px", color: "#aaa" }}>Best ROI</p>
                  <p style={{ margin: 0, fontSize: "36px", fontWeight: "bold", color: "#28a745" }}>
                    {results.strategies.ml_model.roi.toFixed(1)}%
                  </p>
                </div>
                <div>
                  <p style={{ margin: "0 0 8px 0", fontSize: "14px", color: "#aaa" }}>Best Profit</p>
                  <p style={{ margin: 0, fontSize: "36px", fontWeight: "bold", color: "#28a745" }}>
                    {formatCurrency(results.strategies.ml_model.profit)}
                  </p>
                </div>
              </div>
            </div>
          </>
        )}

      </div>
    </div>
  );
}

export default ABTestSimulator;
