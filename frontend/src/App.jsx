import { useState, useEffect } from "react";
import axios from "axios";
import Metrics from "./Metrics.jsx";
import BatchUpload from "./BatchUpload.jsx";
import PredictionHistory from "./PredictionHistory.jsx";
import ABTestSimulator from "./ABTestSimulator.jsx";
import LiveMetrics from "./LiveMetrics.jsx";

const API_URL = import.meta.env.PROD 
  ? "https://campaign-backend-vuf4.onrender.com"
  : "http://localhost:8000";

const BROWSER_OPTIONS = [
  { value: "1", label: "Chrome" },
  { value: "2", label: "Firefox" },
  { value: "3", label: "Safari" },
  { value: "4", label: "Edge" },
  { value: "5", label: "Opera" },
  { value: "6", label: "Internet Explorer" }
];

const OS_OPTIONS = [
  { value: "1", label: "Windows" },
  { value: "2", label: "macOS" },
  { value: "3", label: "Linux" },
  { value: "4", label: "iOS" },
  { value: "5", label: "Android" },
  { value: "6", label: "Chrome OS" },
  { value: "7", label: "Other" },
  { value: "8", label: "Unknown" }
];

const REGION_OPTIONS = [
  { value: "1", label: "North America" },
  { value: "2", label: "Europe" },
  { value: "3", label: "Asia" },
  { value: "4", label: "South America" },
  { value: "5", label: "Africa" },
  { value: "6", label: "Oceania" },
  { value: "7", label: "Middle East" },
  { value: "8", label: "Australia/Pacific" },
  { value: "9", label: "Other" }
];

const TRAFFIC_TYPE_OPTIONS = [
  { value: "1", label: "Direct Traffic" },
  { value: "2", label: "Organic Search" },
  { value: "3", label: "Paid Search" },
  { value: "4", label: "Social Media" },
  { value: "5", label: "Email Campaign" },
  { value: "6", label: "Referral" },
  { value: "7", label: "Display Ads" },
  { value: "8", label: "Other" }
];

function App() {
  const [currentPage, setCurrentPage] = useState("predict");
  
  const [form, setForm] = useState({
    Administrative: 0,
    Administrative_Duration: 0.0,
    Informational: 0,
    Informational_Duration: 0.0,
    ProductRelated: 1,
    ProductRelated_Duration: 0.0,
    BounceRates: 0.02,
    ExitRates: 0.05,
    PageValues: 0.0,
    SpecialDay: 0.0,
    Month: "May",
    OperatingSystems: "2",
    Browser: "2",
    Region: "1",
    TrafficType: "2",
    VisitorType: "Returning_Visitor",
    Weekend: false,
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [totalPredictions, setTotalPredictions] = useState(0);
  
  useEffect(() => {
    axios.get(`${API_URL}/metrics`)
      .then(res => setTotalPredictions(res.data.total_predictions))
      .catch(() => setTotalPredictions(0));
  }, [currentPage, result]);

  const visitorTypes = ["Returning_Visitor", "New_Visitor", "Other"];
  const months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

  const update = (key, value) => {
    setForm(prev => ({ ...prev, [key]: value }));
  };

  const onPredict = async () => {
    setLoading(true);
    setResult(null);
    try {
      const res = await axios.post(`${API_URL}/predict`, form);
      setResult(res.data);
    } catch (err) {
      alert("Error connecting to backend: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const inputStyle = {
    width: "100%",
    padding: "10px",
    marginBottom: "12px",
    borderRadius: "6px",
    border: "1px solid #444",
    backgroundColor: "#2a2a2a",
    color: "#fff",
    fontSize: "14px",
  };

  const labelStyle = {
    display: "block",
    marginBottom: "6px",
    fontSize: "13px",
    fontWeight: "500",
    color: "#ccc",
  };

  const Navigation = () => (
    <div style={{ 
      backgroundColor: "#1a1a1a", 
      padding: "20px", 
      display: "flex", 
      gap: "10px", 
      justifyContent: "center",
      alignItems: "center",
      borderBottom: "1px solid #333",
      position: "relative"
    }}>
      {(currentPage === "predict" || currentPage === "batch" || currentPage === "live") && (
        <div style={{
          position: "absolute",
          right: "20px",
          padding: "8px 16px",
          backgroundColor: "#242424",
          borderRadius: "8px",
          border: "1px solid #333",
          fontSize: "14px",
          color: "#aaa",
          pointerEvents: "none" 
        }}>
          <span style={{ color: "#0066ff", fontWeight: "bold", fontSize: "18px" }}>
            {totalPredictions.toLocaleString()}
          </span>
          {" "}predictions made
        </div>
      )}

      <button
        onClick={() => setCurrentPage("predict")}
        style={{
          padding: "12px 24px",
          borderRadius: "8px",
          border: "none",
          backgroundColor: currentPage === "predict" ? "#0066ff" : "#333",
          color: "#fff",
          cursor: "pointer",
          fontWeight: "600"
        }}
      >
        🎯 Predictions
      </button>
      
      <button
        onClick={() => setCurrentPage("metrics")}
        style={{
          padding: "12px 24px",
          borderRadius: "8px",
          border: "none",
          backgroundColor: currentPage === "metrics" ? "#0066ff" : "#333",
          color: "#fff",
          cursor: "pointer",
          fontWeight: "600"
        }}
      >
        📊 Model Metrics
      </button>

      <button
        onClick={() => setCurrentPage("batch")}
        style={{
          padding: "12px 24px",
          borderRadius: "8px",
          border: "none",
          backgroundColor: currentPage === "batch" ? "#0066ff" : "#333",
          color: "#fff",
          cursor: "pointer",
          fontWeight: "600"
        }}
      >
        📤 Batch Upload
      </button>

      <button
        onClick={() => setCurrentPage("abtest")}
        style={{
          padding: "12px 24px",
          borderRadius: "8px",
          border: "none",
          backgroundColor: currentPage === "abtest" ? "#0066ff" : "#333",
          color: "#fff",
          cursor: "pointer",
          fontWeight: "600"
        }}
      >
        🧪 A/B Test
      </button>

      <button
        onClick={() => setCurrentPage("live")}
        style={{
          padding: "12px 24px",
          borderRadius: "8px",
          border: "none",
          backgroundColor: currentPage === "live" ? "#0066ff" : "#333",
          color: "#fff",
          cursor: "pointer",
          fontWeight: "600"
        }}
      >
        📊 Live Performance
      </button>
    </div>
  );

  if (currentPage === "batch") {
    return (
      <div>
        <Navigation />
        <BatchUpload />
      </div>
    );
  }

  if (currentPage === "metrics") {
    return (
      <div>
        <Navigation />
        <Metrics />
      </div>
    );
  }

  if (currentPage === "abtest") {
    return (
      <div>
        <Navigation />
        <ABTestSimulator />
      </div>
    );
  }

  if (currentPage === "live") {
    return (
      <div>
        <Navigation />
        <LiveMetrics />
      </div>
    );
  }

  return (
    <div style={{ 
      minHeight: "100vh", 
      backgroundColor: "#1a1a1a", 
      color: "#fff",
      padding: "0",
      fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    }}>
      <Navigation />

      <div style={{ padding: "40px 20px" }}>
        <div style={{ maxWidth: 1600, margin: "0 auto" }}>
          <div style={{ textAlign: "center", marginBottom: "40px" }}>
            <h1 style={{ fontSize: "42px", margin: "0 0 10px 0", display: "flex", alignItems: "center", justifyContent: "center", gap: "12px" }}>
              <span>🎯</span> Campaign Targeting System
            </h1>
            <p style={{ fontSize: "16px", color: "#aaa", margin: 0 }}>
              AI-powered purchase probability prediction for targeted marketing
            </p>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "24px", marginBottom: "30px" }}>
            
            <div style={{ 
              backgroundColor: "#242424", 
              borderRadius: "12px", 
              padding: "24px",
              border: "1px solid #333"
            }}>
              <h2 style={{ margin: "0 0 20px 0", fontSize: "20px", color: "#fff" }}>👤 Visitor Information</h2>

              <label style={labelStyle}>Month</label>
              <select value={form.Month} onChange={(e) => update("Month", e.target.value)} style={inputStyle}>
                {months.map(m => <option key={m} value={m}>{m}</option>)}
              </select>

              <label style={labelStyle}>Visitor Type</label>
              <select value={form.VisitorType} onChange={(e) => update("VisitorType", e.target.value)} style={inputStyle}>
                {visitorTypes.map(v => <option key={v} value={v}>{v.replace("_", " ")}</option>)}
              </select>

              <label style={{ ...labelStyle, display: "flex", alignItems: "center", cursor: "pointer", marginBottom: "20px" }}>
                <input
                  type="checkbox"
                  checked={form.Weekend}
                  onChange={(e) => update("Weekend", e.target.checked)}
                  style={{ marginRight: "10px", width: "18px", height: "18px", cursor: "pointer" }}
                />
                Weekend Visit
              </label>

              <h3 style={{ margin: "24px 0 16px 0", fontSize: "16px", color: "#aaa", borderTop: "1px solid #333", paddingTop: "20px" }}>
                🖥️ System Identifiers
              </h3>

              <div>
                <label style={labelStyle}>Operating System</label>
                <select 
                  value={form.OperatingSystems} 
                  onChange={(e) => update("OperatingSystems", e.target.value)} 
                  style={inputStyle}
                >
                  <option value="">Select Operating System</option>
                  {OS_OPTIONS.map(option => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label style={labelStyle}>Browser</label>
                <select 
                  value={form.Browser} 
                  onChange={(e) => update("Browser", e.target.value)} 
                  style={inputStyle}
                >
                  <option value="">Select Browser</option>
                  {BROWSER_OPTIONS.map(option => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label style={labelStyle}>Region</label>
                <select 
                  value={form.Region} 
                  onChange={(e) => update("Region", e.target.value)} 
                  style={inputStyle}
                >
                  <option value="">Select Region</option>
                  {REGION_OPTIONS.map(option => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label style={labelStyle}>Traffic Source</label>
                <select 
                  value={form.TrafficType} 
                  onChange={(e) => update("TrafficType", e.target.value)} 
                  style={inputStyle}
                >
                  <option value="">Select Traffic Source</option>
                  {TRAFFIC_TYPE_OPTIONS.map(option => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div style={{ 
              backgroundColor: "#242424", 
              borderRadius: "12px", 
              padding: "24px",
              border: "1px solid #333"
            }}>
              <h2 style={{ margin: "0 0 20px 0", fontSize: "20px", color: "#fff" }}>📊 Behavior Metrics</h2>

              {[
                ["Administrative", "Administrative Pages"],
                ["Administrative_Duration", "Administrative Duration (s)"],
                ["Informational", "Informational Pages"],
                ["Informational_Duration", "Informational Duration (s)"],
                ["ProductRelated", "Product Pages"],
                ["ProductRelated_Duration", "Product Duration (s)"],
                ["BounceRates", "Bounce Rate"],
                ["ExitRates", "Exit Rate"],
                ["PageValues", "Page Value"],
                ["SpecialDay", "Special Day Proximity"],
              ].map(([key, label]) => (
                <div key={key}>
                  <label style={labelStyle}>{label}</label>
                  <input
                    type="number"
                    step="any"
                    value={form[key]}
                    onChange={(e) => update(key, parseFloat(e.target.value) || 0)}
                    style={inputStyle}
                  />
                </div>
              ))}
            </div>
          </div>

          <div style={{ textAlign: "center", marginBottom: "30px" }}>
            <button
              onClick={onPredict}
              disabled={loading}
              style={{ 
                padding: "16px 48px", 
                fontSize: "18px",
                fontWeight: "600",
                borderRadius: "10px", 
                cursor: loading ? "not-allowed" : "pointer",
                backgroundColor: loading ? "#555" : "#0066ff",
                color: "white",
                border: "none",
                boxShadow: loading ? "none" : "0 4px 12px rgba(0, 102, 255, 0.4)",
                transition: "all 0.3s ease",
                transform: loading ? "scale(1)" : "scale(1)",
              }}
              onMouseEnter={(e) => !loading && (e.target.style.transform = "scale(1.05)")}
              onMouseLeave={(e) => !loading && (e.target.style.transform = "scale(1)")}
            >
              {loading ? "🔄 Analyzing..." : "🚀 Predict Purchase Probability"}
            </button>
          </div>

          {result && (
            <div style={{ 
              backgroundColor: result.decision === "TARGET" ? "#1a3a1a" : "#3a1a1a",
              border: `2px solid ${result.decision === "TARGET" ? "#28a745" : "#dc3545"}`,
              borderRadius: "12px", 
              padding: "30px",
              animation: "fadeIn 0.5s ease-in"
            }}>
              <h2 style={{ margin: "0 0 20px 0", fontSize: "24px" }}>📊 Prediction Result</h2>
              
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "20px", marginBottom: "20px" }}>
                <div style={{ backgroundColor: "#2a2a2a", padding: "20px", borderRadius: "8px" }}>
                  <p style={{ margin: "0 0 8px 0", fontSize: "14px", color: "#aaa" }}>Purchase Probability</p>
                  <p style={{ margin: 0, fontSize: "36px", fontWeight: "bold", color: "#0066ff" }}>
                    {(result.probability * 100).toFixed(2)}%
                  </p>
                </div>

                <div style={{ backgroundColor: "#2a2a2a", padding: "20px", borderRadius: "8px" }}>
                  <p style={{ margin: "0 0 8px 0", fontSize: "14px", color: "#aaa" }}>Decision</p>
                  <p style={{ 
                    margin: 0, 
                    fontSize: "28px", 
                    fontWeight: "bold", 
                    color: result.decision === "TARGET" ? "#28a745" : "#dc3545" 
                  }}>
                    {result.decision === "TARGET" ? "✅ TARGET" : "❌ DO NOT TARGET"}
                  </p>
                </div>

                <div style={{ backgroundColor: "#2a2a2a", padding: "20px", borderRadius: "8px" }}>
                  <p style={{ margin: "0 0 8px 0", fontSize: "14px", color: "#aaa" }}>Confidence</p>
                  <p style={{ 
                    margin: 0, 
                    fontSize: "28px", 
                    fontWeight: "bold", 
                    color: result.confidence_level === "HIGH" ? "#28a745" : 
                           result.confidence_level === "MEDIUM" ? "#ffa500" : "#dc3545"
                  }}>
                    {result.confidence_level === "HIGH" ? "🟢" : 
                     result.confidence_level === "MEDIUM" ? "🟡" : "🔴"} {result.confidence_level}
                  </p>
                </div>
              </div>

              <div style={{ 
                backgroundColor: "#2a2a2a", 
                padding: "20px", 
                borderRadius: "8px",
                marginBottom: "20px"
              }}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "10px" }}>
                  <span style={{ fontSize: "14px", color: "#aaa" }}>Decision Risk Score</span>
                  <span style={{ fontSize: "14px", fontWeight: "bold", color: "#fff" }}>
                    {result.risk_score.toFixed(1)}/100
                  </span>
                </div>
                <div style={{ 
                  width: "100%", 
                  height: "12px", 
                  backgroundColor: "#1a1a1a", 
                  borderRadius: "6px",
                  overflow: "hidden"
                }}>
                  <div style={{ 
                    width: `${result.risk_score}%`, 
                    height: "100%", 
                    backgroundColor: result.risk_score < 20 ? "#28a745" :
                                    result.risk_score < 40 ? "#7fba00" :
                                    result.risk_score < 60 ? "#ffa500" : "#dc3545",
                    transition: "width 0.5s ease"
                  }} />
                </div>
                <p style={{ margin: "10px 0 0 0", fontSize: "12px", color: "#888" }}>
                  {result.risk_score < 20 ? "✅ Very confident decision" :
                   result.risk_score < 40 ? "✓ Reliable decision" :
                   result.risk_score < 60 ? "⚠️ Moderate uncertainty" : "⚠️ Decision near threshold - review carefully"}
                </p>
              </div>

              <div style={{ fontSize: "14px", color: "#999", borderTop: "1px solid #444", paddingTop: "16px" }}>
                <p style={{ margin: "4px 0" }}>
                  <strong>Threshold:</strong> {result.threshold} | 
                  <strong> Base Conversion Rate:</strong> {(result.base_rate * 100).toFixed(2)}%
                </p>
                <p style={{ margin: "8px 0 0 0", fontSize: "13px", fontStyle: "italic" }}>
                  {result.decision === "TARGET" 
                    ? "✨ This visitor shows high purchase intent. Prioritize for targeted campaigns."
                    : "💡 Low conversion probability. Consider alternative engagement strategies."}
                </p>
              </div>
            </div>
          )}
        </div>
      </div>

      <div style={{ 
        padding: "0 20px 40px 20px",
        backgroundColor: "#1a1a1a"
      }}>
        <div style={{ maxWidth: 1600, margin: "0 auto" }}>
          <PredictionHistory />
        </div>
      </div>

      <style>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
      `}</style>
    </div>
  );
}

export default App;
