import { useState, useEffect } from "react";

function PredictionHistory() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    // Load history from sessionStorage (clears on page refresh)
    const savedHistory = sessionStorage.getItem('predictionHistory');
    if (savedHistory) {
      setHistory(JSON.parse(savedHistory));
    }

    // Listen for new predictions from App component
    const handleNewPrediction = (event) => {
      const newPrediction = event.detail;
      setHistory(prev => {
        const updated = [newPrediction, ...prev].slice(0, 10); // Keep last 10
        sessionStorage.setItem('predictionHistory', JSON.stringify(updated));
        return updated;
      });
    };

    window.addEventListener('newPrediction', handleNewPrediction);
    return () => window.removeEventListener('newPrediction', handleNewPrediction);
  }, []);

  const formatTime = (isoString) => {
    const date = new Date(isoString);
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit',
      second: '2-digit'
    });
  };

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
          Last {history.length} (clears on refresh)
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