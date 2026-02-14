 import { useState, useEffect } from "react";
import axios from "axios";
import Metrics from "./Metrics.jsx";
import BatchUpload from "./BatchUpload.jsx";
import PredictionHistory from "./PredictionHistory.jsx";
import ABTestSimulator from "./ABTestSimulator.jsx";
import LiveMetrics from "./LiveMetrics.jsx";
import "./AppRedesign.css";

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
      .then(res => setTotalPredictions(res.data.live_metrics.total_predictions))
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
      
      const historyEntry = {
        prediction_id: res.data.prediction_id,
        timestamp: res.data.timestamp,
        visitor_type: form.VisitorType,
        month: form.Month,
        probability: res.data.probability,
        decision: res.data.decision
      };
      window.dispatchEvent(new CustomEvent('newPrediction', { detail: historyEntry }));
    } catch (err) {
      alert("Error connecting to backend: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const Navigation = () => (
    <nav className="main-nav">
      <div className="nav-container">
        <button
          onClick={() => setCurrentPage("predict")}
          className={`nav-tab ${currentPage === "predict" ? "active" : ""}`}
        >
          <span className="nav-icon">🎯</span>
          <span className="nav-label">Predictions</span>
        </button>
        
        <button
          onClick={() => setCurrentPage("live")}
          className={`nav-tab ${currentPage === "live" ? "active" : ""}`}
        >
          <span className="nav-icon">📊</span>
          <span className="nav-label">Live Performance</span>
        </button>

        <button
          onClick={() => setCurrentPage("metrics")}
          className={`nav-tab ${currentPage === "metrics" ? "active" : ""}`}
        >
          <span className="nav-icon">🤖</span>
          <span className="nav-label">Model Info</span>
        </button>

        <button
          onClick={() => setCurrentPage("batch")}
          className={`nav-tab ${currentPage === "batch" ? "active" : ""}`}
        >
          <span className="nav-icon">📤</span>
          <span className="nav-label">Batch Upload</span>
        </button>

        <button
          onClick={() => setCurrentPage("abtest")}
          className={`nav-tab ${currentPage === "abtest" ? "active" : ""}`}
        >
          <span className="nav-icon">🧪</span>
          <span className="nav-label">A/B Test</span>
        </button>
      </div>
    </nav>
  );

  return (
    <div className="app">
      <div className="bg-animation"></div>
      <div className="grain-overlay"></div>
      
      <header className="app-header">
        <div className="header-icon">🎯</div>
        <h1 className="header-title">Campaign Targeting System</h1>
        <p className="header-subtitle">AI-powered purchase probability prediction for targeted marketing</p>
        <div className="header-stats">
          <div className="stat-badge">
            <span className="stat-label">Total Predictions</span>
            <span className="stat-value">{totalPredictions.toLocaleString()}</span>
          </div>
          <div className="stat-badge">
            <span className="stat-label">Model Accuracy</span>
            <span className="stat-value">89.32%</span>
          </div>
          <div className="stat-badge">
            <span className="stat-label">ROI Improvement</span>
            <span className="stat-value">~30×</span>
          </div>
        </div>
      </header>

      <Navigation />

      <main className="main-content">
        {currentPage === "predict" && (
          <div className="predict-container">
            <div className="form-grid">
              {/* Visitor Information Card */}
              <div className="glass-card">
                <div className="card-header">
                  <div className="card-icon">👤</div>
                  <h2 className="card-title">Visitor Information</h2>
                </div>

                <div className="form-group">
                  <label className="form-label">Month</label>
                  <select 
                    value={form.Month} 
                    onChange={(e) => update("Month", e.target.value)}
                    className="form-select"
                  >
                    {months.map(m => <option key={m} value={m}>{m}</option>)}
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Visitor Type</label>
                  <select 
                    value={form.VisitorType} 
                    onChange={(e) => update("VisitorType", e.target.value)}
                    className="form-select"
                  >
                    {visitorTypes.map(vt => (
                      <option key={vt} value={vt}>
                        {vt.replace('_', ' ')}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={form.Weekend}
                      onChange={(e) => update("Weekend", e.target.checked)}
                      className="form-checkbox"
                    />
                    <span>Weekend Visit</span>
                  </label>
                </div>
              </div>

              {/* Behavior Metrics Card */}
              <div className="glass-card">
                <div className="card-header">
                  <div className="card-icon">📊</div>
                  <h2 className="card-title">Behavior Metrics</h2>
                </div>

                {[
                  ["Administrative", "Account/Settings Pages Visited"],
                  ["Administrative_Duration", "Time on Account Pages (seconds)"],
                  ["Informational", "Help/Info Pages Visited"],
                  ["Informational_Duration", "Time on Help Pages (seconds)"],
                  ["ProductRelated", "Products Viewed"],
                  ["ProductRelated_Duration", "Time Viewing Products (seconds)"],
                  ["PageValues", "Shopping Intent Score (0-100)"],
                ].map(([key, label]) => (
                  <div key={key} className="form-group">
                    <label className="form-label">{label}</label>
                    <input
                      type="number"
                      step="any"
                      value={form[key]}
                      onChange={(e) => update(key, parseFloat(e.target.value) || 0)}
                      className="form-input"
                    />
                  </div>
                ))}

                <div className="form-group">
                  <label className="form-label">Did they leave quickly?</label>
                  <select 
                    value={form.BounceRates} 
                    onChange={(e) => update("BounceRates", parseFloat(e.target.value))} 
                    className="form-select"
                  >
                    <option value="0">No - They stayed and browsed</option>
                    <option value="0.5">Maybe - Brief visit</option>
                    <option value="1">Yes - Left immediately</option>
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Exited without purchase?</label>
                  <select 
                    value={form.ExitRates} 
                    onChange={(e) => update("ExitRates", parseFloat(e.target.value))} 
                    className="form-select"
                  >
                    <option value="0">No - Made a purchase</option>
                    <option value="0.5">Unsure - Still browsing</option>
                    <option value="1">Yes - Left without buying</option>
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Is it near a holiday?</label>
                  <select 
                    value={form.SpecialDay} 
                    onChange={(e) => update("SpecialDay", parseFloat(e.target.value))} 
                    className="form-select"
                  >
                    <option value="0">No</option>
                    <option value="0.2">5+ days away</option>
                    <option value="0.4">3-4 days away</option>
                    <option value="0.6">1-2 days away</option>
                    <option value="0.8">Tomorrow</option>
                    <option value="1">Today is the holiday</option>
                  </select>
                </div>
              </div>

              {/* System Identifiers Card */}
              <div className="glass-card">
                <div className="card-header">
                  <div className="card-icon">💻</div>
                  <h2 className="card-title">System Identifiers</h2>
                </div>

                <div className="form-group">
                  <label className="form-label">Operating System</label>
                  <select 
                    value={form.OperatingSystems} 
                    onChange={(e) => update("OperatingSystems", e.target.value)}
                    className="form-select"
                  >
                    {OS_OPTIONS.map(os => (
                      <option key={os.value} value={os.value}>{os.label}</option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Browser</label>
                  <select 
                    value={form.Browser} 
                    onChange={(e) => update("Browser", e.target.value)}
                    className="form-select"
                  >
                    {BROWSER_OPTIONS.map(br => (
                      <option key={br.value} value={br.value}>{br.label}</option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Region</label>
                  <select 
                    value={form.Region} 
                    onChange={(e) => update("Region", e.target.value)}
                    className="form-select"
                  >
                    {REGION_OPTIONS.map(reg => (
                      <option key={reg.value} value={reg.value}>{reg.label}</option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Traffic Source</label>
                  <select 
                    value={form.TrafficType} 
                    onChange={(e) => update("TrafficType", e.target.value)}
                    className="form-select"
                  >
                    {TRAFFIC_TYPE_OPTIONS.map(tt => (
                      <option key={tt.value} value={tt.value}>{tt.label}</option>
                    ))}
                  </select>
                </div>
              </div>
            </div>

            <div className="predict-action">
              <button
                onClick={onPredict}
                disabled={loading}
                className={`btn-predict ${loading ? 'loading' : ''}`}
              >
                {loading ? (
                  <>
                    <span className="spinner"></span>
                    Analyzing...
                  </>
                ) : (
                  <>
                    <span>🚀</span>
                    Generate Prediction
                  </>
                )}
              </button>
            </div>

            {result && (
              <div className={`result-card ${result.decision === "TARGET" ? "target" : "no-target"}`}>
                <div className="result-header">
                  <h2>Prediction Result</h2>
                  <span className="result-id">ID: {result.prediction_id}</span>
                </div>

                <div className="result-metrics">
                  <div className="metric-box">
                    <span className="metric-label">Purchase Probability</span>
                    <span className="metric-value primary">{(result.probability * 100).toFixed(2)}%</span>
                  </div>

                  <div className="metric-box">
                    <span className="metric-label">Decision</span>
                    <span className={`metric-value ${result.decision === "TARGET" ? "success" : "danger"}`}>
                      {result.decision === "TARGET" ? "✅ TARGET" : "❌ DO NOT TARGET"}
                    </span>
                  </div>

                  <div className="metric-box">
                    <span className="metric-label">Confidence</span>
                    <span className={`metric-value ${
                      result.confidence_level === "HIGH" ? "success" : 
                      result.confidence_level === "MEDIUM" ? "warning" : "danger"
                    }`}>
                      {result.confidence_level === "HIGH" ? "🟢" : 
                       result.confidence_level === "MEDIUM" ? "🟡" : "🔴"} {result.confidence_level}
                    </span>
                  </div>
                </div>

                <div className="risk-score">
                  <div className="risk-header">
                    <span>Decision Risk Score</span>
                    <span className="risk-value">{result.risk_score.toFixed(1)}/100</span>
                  </div>
                  <div className="risk-bar">
                    <div 
                      className={`risk-fill ${
                        result.risk_score < 20 ? "low" :
                        result.risk_score < 40 ? "medium-low" :
                        result.risk_score < 60 ? "medium" : "high"
                      }`}
                      style={{ width: `${result.risk_score}%` }}
                    ></div>
                  </div>
                  <p className="risk-description">
                    {result.risk_score < 20 ? "✅ Very confident decision" :
                     result.risk_score < 40 ? "✓ Reliable decision" :
                     result.risk_score < 60 ? "⚠️ Moderate uncertainty" : 
                     "⚠️ Decision near threshold - review carefully"}
                  </p>
                </div>

                <div className="result-details">
                  <p>
                    <strong>Threshold:</strong> {result.threshold} | 
                    <strong> Base Conversion Rate:</strong> {(result.base_rate * 100).toFixed(2)}%
                  </p>
                  <p className="result-recommendation">
                    {result.decision === "TARGET" 
                      ? "✨ This visitor shows high purchase intent. Prioritize for targeted campaigns."
                      : "💡 Low conversion probability. Consider alternative engagement strategies."}
                  </p>
                </div>
              </div>
            )}

            <PredictionHistory />
          </div>
        )}

        {currentPage === "live" && <LiveMetrics />}
        {currentPage === "metrics" && <Metrics />}
        {currentPage === "batch" && <BatchUpload />}
        {currentPage === "abtest" && <ABTestSimulator />}
      </main>
    </div>
  );
}

export default App;
