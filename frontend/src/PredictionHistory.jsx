import { useState, useEffect } from "react";
import axios from "axios";

const API_URL = "http://localhost:8000";

function PredictionHistory() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHistory();
    const interval = setInterval(fetchHistory, 3000); // Refresh every 3 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchHistory = async () => {
    try {
      const res = await axios.get(`${API_URL}/history`);
      setHistory(res.data.history);
      setLoading(false);
    } catch (err) {
      console.error("Failed to fetch history:", err);
      setLoading(false);
    }
  };

  const formatTime = (isoString) => {
    const date = new Date(isoString);
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit',
      second: '2-digit'
    });
  };

  if (loading) {
    return (
      <div style={{ 
        backgroundColor: "#242424", 
        padding: "20px", 
        borderRadius: "12px",
        border: "1px solid #333",
        textAlign: "center",
        color: "#aaa"
      }}>
        Loading history...
      </div>
    );
  }

  if (history.length === 0) {
    return (
      <div style={{ 
        backgroundColor: "#242424", 
        padding: "20px", 
        borderRadius: "12px",
        border: "1px solid #333",
        textAlign: "center",
        color: "#aaa"
      }}>
        <p style={{ margin: 0, fontSize: "14px" }}>
          📭 No predictions yet. Make your first prediction to see history!
        </p>
      </div>
    );
  }

  return (
    <div style={{ 
      backgroundColor: "#242424", 
      padding: "20px", 
      borderRadius: "12px",
      border: "1px solid #333"
    }}>
      <h3 style={{ 
        margin: "0 0 16px 0", 
        fontSize: "18px", 
        color: "#fff",
        display: "flex",
        alignItems: "center",
        gap: "8px"
      }}>
        🕐 Recent Predictions
        <span style={{ 
          fontSize: "12px", 
          color: "#aaa", 
          fontWeight: "normal",
          marginLeft: "auto"
        }}>
          Last {history.length}
        </span>
      </h3>

      <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
        {history.map((entry, idx) => (
          <div 
            key={entry.prediction_id} 
            style={{ 
              backgroundColor: "#2a2a2a",
              padding: "12px 16px",
              borderRadius: "8px",
              border: `1px solid ${entry.decision === "TARGET" ? "#28a74533" : "#dc354533"}`,
              display: "grid",
              gridTemplateColumns: "60px 120px 1fr 80px 100px",
              alignItems: "center",
              gap: "12px",
              fontSize: "13px",
              animation: idx === 0 ? "slideIn 0.5s ease" : "none"
            }}
          >
            {/* Time */}
            <span style={{ color: "#666", fontSize: "12px" }}>
              {formatTime(entry.timestamp)}
            </span>

            {/* Visitor Info */}
            <span style={{ color: "#aaa" }}>
              {entry.visitor_type.replace("_", " ")}
            </span>

            {/* Month */}
            <span style={{ color: "#888" }}>
              {entry.month}
            </span>

            {/* Probability */}
            <span style={{ 
              color: "#0066ff", 
              fontWeight: "600",
              textAlign: "right"
            }}>
              {(entry.probability * 100).toFixed(1)}%
            </span>

            {/* Decision Badge */}
            <span style={{ 
              padding: "4px 8px",
              borderRadius: "6px",
              backgroundColor: entry.decision === "TARGET" ? "#1a3a1a" : "#3a1a1a",
              color: entry.decision === "TARGET" ? "#28a745" : "#dc3545",
              fontSize: "11px",
              fontWeight: "600",
              textAlign: "center"
            }}>
              {entry.decision === "TARGET" ? "✅ TARGET" : "❌ SKIP"}
            </span>
          </div>
        ))}
      </div>

      <style>{`
        @keyframes slideIn {
          from { opacity: 0; transform: translateX(-20px); }
          to { opacity: 1; transform: translateX(0); }
        }
      `}</style>
    </div>
  );
}

export default PredictionHistory;
 