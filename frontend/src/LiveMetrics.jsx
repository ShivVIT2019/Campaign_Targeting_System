import { useState, useEffect } from "react";
import axios from "axios";

const API_URL = import.meta.env.PROD 
  ? "https://campaign-backend-vuf4.onrender.com"
  : "http://localhost:8000";

function LiveMetrics() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchMetrics();
    // Auto-refresh every 5 seconds
    const interval = setInterval(fetchMetrics, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchMetrics = async () => {
    try {
      const res = await axios.get(`${API_URL}/live-metrics`);
      setMetrics(res.data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div style={{ 
        minHeight: "100vh", 
        backgroundColor: "#1a1a1a", 
        color: "#fff",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
      }}>
        <div style={{ textAlign: "center" }}>
          <p style={{ fontSize: "24px" }}>🔄 Loading Live Metrics...</p>
        </div>
      </div>
    );
  }

  if (error || !metrics) {
    return (
      <div style={{ 
        minHeight: "100vh", 
        backgroundColor: "#1a1a1a", 
        color: "#fff",
        padding: "40px 20px",
        fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
      }}>
        <div style={{ maxWidth: 1200, margin: "0 auto", textAlign: "center" }}>
          <h1 style={{ fontSize: "42px", marginBottom: "20px" }}>📊 Live Performance</h1>
          <p style={{ color: "#dc3545" }}>Error: {error || "Failed to load metrics"}</p>
        </div>
      </div>
    );
  }

  const { summary, trends, segments } = metrics;

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
            📊 Live Performance Dashboard
          </h1>
          <p style={{ fontSize: "16px", color: "#aaa" }}>
            Real-time prediction metrics • Auto-refreshes every 5 seconds
          </p>
        </div>

        {/* Summary Cards */}
        <div style={{ 
          display: "grid", 
          gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))", 
          gap: "20px", 
          marginBottom: "30px" 
        }}>
          <div style={{ 
            backgroundColor: "#242424", 
            padding: "24px", 
            borderRadius: "12px",
            border: "1px solid #333"
          }}>
            <p style={{ margin: "0 0 8px 0", fontSize: "14px", color: "#aaa" }}>Total Predictions</p>
            <p style={{ margin: 0, fontSize: "36px", fontWeight: "bold", color: "#0066ff" }}>
              {summary.total_predictions.toLocaleString()}
            </p>
          </div>

          <div style={{ 
            backgroundColor: "#242424", 
            padding: "24px", 
            borderRadius: "12px",
            border: "1px solid #333"
          }}>
            <p style={{ margin: "0 0 8px 0", fontSize: "14px", color: "#aaa" }}>Target Rate</p>
            <p style={{ margin: 0, fontSize: "36px", fontWeight: "bold", color: "#28a745" }}>
              {summary.target_rate.toFixed(1)}%
            </p>
            <p style={{ margin: "8px 0 0 0", fontSize: "12px", color: "#888" }}>
              {summary.target_count} targeted, {summary.dont_target_count} skipped
            </p>
          </div>

          <div style={{ 
            backgroundColor: "#242424", 
            padding: "24px", 
            borderRadius: "12px",
            border: "1px solid #333"
          }}>
            <p style={{ margin: "0 0 8px 0", fontSize: "14px", color: "#aaa" }}>Avg Probability</p>
            <p style={{ margin: 0, fontSize: "36px", fontWeight: "bold", color: "#ffa500" }}>
              {(summary.avg_probability * 100).toFixed(1)}%
            </p>
          </div>

          <div style={{ 
            backgroundColor: "#242424", 
            padding: "24px", 
            borderRadius: "12px",
            border: "1px solid #333"
          }}>
            <p style={{ margin: "0 0 8px 0", fontSize: "14px", color: "#aaa" }}>Confidence Breakdown</p>
            <div style={{ display: "flex", gap: "10px", marginTop: "10px" }}>
              <div style={{ flex: 1 }}>
                <p style={{ margin: "0 0 4px 0", fontSize: "12px", color: "#28a745" }}>🟢 High</p>
                <p style={{ margin: 0, fontSize: "20px", fontWeight: "bold" }}>
                  {summary.high_confidence}
                </p>
              </div>
              <div style={{ flex: 1 }}>
                <p style={{ margin: "0 0 4px 0", fontSize: "12px", color: "#ffa500" }}>🟡 Med</p>
                <p style={{ margin: 0, fontSize: "20px", fontWeight: "bold" }}>
                  {summary.medium_confidence}
                </p>
              </div>
              <div style={{ flex: 1 }}>
                <p style={{ margin: "0 0 4px 0", fontSize: "12px", color: "#dc3545" }}>🔴 Low</p>
                <p style={{ margin: 0, fontSize: "20px", fontWeight: "bold" }}>
                  {summary.low_confidence}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Recent Probability Trend */}
        {trends.recent_probabilities && trends.recent_probabilities.length > 0 && (
          <div style={{ 
            backgroundColor: "#242424", 
            padding: "30px", 
            borderRadius: "12px",
            border: "1px solid #333",
            marginBottom: "30px"
          }}>
            <h2 style={{ margin: "0 0 20px 0", fontSize: "24px" }}>📈 Recent Probability Trend</h2>
            <div style={{ 
              display: "flex", 
              alignItems: "flex-end", 
              gap: "4px", 
              height: "150px",
              padding: "10px 0"
            }}>
              {trends.recent_probabilities.map((prob, idx) => (
                <div
                  key={idx}
                  style={{
                    flex: 1,
                    height: `${prob * 100}%`,
                    backgroundColor: prob >= 0.5 ? "#28a745" : "#dc3545",
                    borderRadius: "4px 4px 0 0",
                    minHeight: "5px",
                    transition: "all 0.3s ease"
                  }}
                  title={`${(prob * 100).toFixed(1)}%`}
                />
              ))}
            </div>
            <p style={{ margin: "10px 0 0 0", fontSize: "12px", color: "#888", textAlign: "center" }}>
              Last {trends.recent_probabilities.length} predictions
            </p>
          </div>
        )}

        {/* Segments */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px" }}>
          
          {/* Visitor Types */}
          <div style={{ 
            backgroundColor: "#242424", 
            padding: "30px", 
            borderRadius: "12px",
            border: "1px solid #333"
          }}>
            <h2 style={{ margin: "0 0 20px 0", fontSize: "24px" }}>👥 Top Visitor Types</h2>
            {Object.entries(segments.visitor_types).map(([type, count]) => (
              <div key={type} style={{ marginBottom: "16px" }}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "4px" }}>
                  <span style={{ fontSize: "14px" }}>{type.replace("_", " ")}</span>
                  <span style={{ fontSize: "14px", fontWeight: "bold", color: "#0066ff" }}>{count}</span>
                </div>
                <div style={{ 
                  width: "100%", 
                  height: "8px", 
                  backgroundColor: "#1a1a1a", 
                  borderRadius: "4px",
                  overflow: "hidden"
                }}>
                  <div style={{ 
                    width: `${(count / summary.total_predictions) * 100}%`, 
                    height: "100%", 
                    backgroundColor: "#0066ff"
                  }} />
                </div>
              </div>
            ))}
          </div>

          {/* Months */}
          <div style={{ 
            backgroundColor: "#242424", 
            padding: "30px", 
            borderRadius: "12px",
            border: "1px solid #333"
          }}>
            <h2 style={{ margin: "0 0 20px 0", fontSize: "24px" }}>📅 Top Months</h2>
            {Object.entries(segments.months).map(([month, count]) => (
              <div key={month} style={{ marginBottom: "16px" }}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "4px" }}>
                  <span style={{ fontSize: "14px" }}>{month}</span>
                  <span style={{ fontSize: "14px", fontWeight: "bold", color: "#28a745" }}>{count}</span>
                </div>
                <div style={{ 
                  width: "100%", 
                  height: "8px", 
                  backgroundColor: "#1a1a1a", 
                  borderRadius: "4px",
                  overflow: "hidden"
                }}>
                  <div style={{ 
                    width: `${(count / summary.total_predictions) * 100}%`, 
                    height: "100%", 
                    backgroundColor: "#28a745"
                  }} />
                </div>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
}

export default LiveMetrics;
