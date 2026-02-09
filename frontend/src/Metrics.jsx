import { useState, useEffect } from "react";
import axios from "axios";

const API_URL = "http://localhost:8000";

function Metrics() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMetrics();
  }, []);

  const fetchMetrics = async () => {
    try {
      const res = await axios.get(`${API_URL}/model-metrics`);
      setMetrics(res.data);
    } catch (err) {
      console.error(err);
      alert("Failed to load metrics");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div style={{ minHeight: "100vh", backgroundColor: "#1a1a1a", color: "#fff", padding: "40px", textAlign: "center" }}>
        <h1>🔄 Loading Metrics...</h1>
      </div>
    );
  }

  if (!metrics || metrics.error) {
    return (
      <div style={{ minHeight: "100vh", backgroundColor: "#1a1a1a", color: "#fff", padding: "40px" }}>
        <h1>❌ Error Loading Metrics</h1>
        <p>{metrics?.error || "Unknown error"}</p>
      </div>
    );
  }

  const cm = metrics.confusion_matrix;
  const report = metrics.classification_report;

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
            📊 Model Performance Dashboard
          </h1>
          <p style={{ fontSize: "16px", color: "#aaa" }}>
            Campaign Targeting ML Model Evaluation
          </p>
        </div>

        {/* Key Metrics */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "20px", marginBottom: "40px" }}>
          <div style={{ backgroundColor: "#242424", padding: "24px", borderRadius: "12px", border: "1px solid #333" }}>
            <p style={{ margin: "0 0 8px 0", fontSize: "14px", color: "#aaa" }}>ROC-AUC Score</p>
            <p style={{ margin: 0, fontSize: "36px", fontWeight: "bold", color: "#0066ff" }}>
              {(metrics.roc_auc * 100).toFixed(2)}%
            </p>
          </div>

          <div style={{ backgroundColor: "#242424", padding: "24px", borderRadius: "12px", border: "1px solid #333" }}>
            <p style={{ margin: "0 0 8px 0", fontSize: "14px", color: "#aaa" }}>Precision</p>
            <p style={{ margin: 0, fontSize: "36px", fontWeight: "bold", color: "#28a745" }}>
              {(report["1"]["precision"] * 100).toFixed(1)}%
            </p>
          </div>

          <div style={{ backgroundColor: "#242424", padding: "24px", borderRadius: "12px", border: "1px solid #333" }}>
            <p style={{ margin: "0 0 8px 0", fontSize: "14px", color: "#aaa" }}>Recall</p>
            <p style={{ margin: 0, fontSize: "36px", fontWeight: "bold", color: "#ffa500" }}>
              {(report["1"]["recall"] * 100).toFixed(1)}%
            </p>
          </div>

          <div style={{ backgroundColor: "#242424", padding: "24px", borderRadius: "12px", border: "1px solid #333" }}>
            <p style={{ margin: "0 0 8px 0", fontSize: "14px", color: "#aaa" }}>F1-Score</p>
            <p style={{ margin: 0, fontSize: "36px", fontWeight: "bold", color: "#dc3545" }}>
              {(report["1"]["f1-score"] * 100).toFixed(1)}%
            </p>
          </div>
        </div>

        {/* Confusion Matrix */}
        <div style={{ backgroundColor: "#242424", padding: "30px", borderRadius: "12px", border: "1px solid #333", marginBottom: "30px" }}>
          <h2 style={{ margin: "0 0 20px 0", fontSize: "24px" }}>🎯 Confusion Matrix</h2>
          
          <div style={{ display: "grid", gridTemplateColumns: "auto 1fr 1fr", gap: "10px", maxWidth: "500px" }}>
            <div></div>
            <div style={{ textAlign: "center", fontWeight: "bold", color: "#aaa" }}>Predicted: No Purchase</div>
            <div style={{ textAlign: "center", fontWeight: "bold", color: "#aaa" }}>Predicted: Purchase</div>
            
            <div style={{ fontWeight: "bold", color: "#aaa", display: "flex", alignItems: "center" }}>Actual: No Purchase</div>
            <div style={{ backgroundColor: "#1a3a1a", padding: "20px", borderRadius: "8px", textAlign: "center", fontSize: "24px" }}>
              {cm[0][0]}
              <div style={{ fontSize: "12px", color: "#aaa", marginTop: "5px" }}>True Negative</div>
            </div>
            <div style={{ backgroundColor: "#3a1a1a", padding: "20px", borderRadius: "8px", textAlign: "center", fontSize: "24px" }}>
              {cm[0][1]}
              <div style={{ fontSize: "12px", color: "#aaa", marginTop: "5px" }}>False Positive</div>
            </div>
            
            <div style={{ fontWeight: "bold", color: "#aaa", display: "flex", alignItems: "center" }}>Actual: Purchase</div>
            <div style={{ backgroundColor: "#3a1a1a", padding: "20px", borderRadius: "8px", textAlign: "center", fontSize: "24px" }}>
              {cm[1][0]}
              <div style={{ fontSize: "12px", color: "#aaa", marginTop: "5px" }}>False Negative</div>
            </div>
            <div style={{ backgroundColor: "#1a3a1a", padding: "20px", borderRadius: "8px", textAlign: "center", fontSize: "24px" }}>
              {cm[1][1]}
              <div style={{ fontSize: "12px", color: "#aaa", marginTop: "5px" }}>True Positive</div>
            </div>
          </div>

          <p style={{ marginTop: "20px", fontSize: "14px", color: "#aaa" }}>
            Test Set Size: {metrics.test_size} samples | Base Rate: {(metrics.base_rate * 100).toFixed(2)}%
          </p>
        </div>

        {/* Feature Importance */}
        {metrics.feature_importance && (
          <div style={{ backgroundColor: "#242424", padding: "30px", borderRadius: "12px", border: "1px solid #333" }}>
            <h2 style={{ margin: "0 0 20px 0", fontSize: "24px" }}>🔍 Top 20 Feature Importance</h2>
            
            <div style={{ display: "grid", gap: "10px" }}>
              {metrics.feature_importance.features.map((feature, idx) => {
                const importance = metrics.feature_importance.importance[idx];
                const absImportance = Math.abs(importance);
                const maxImportance = Math.max(...metrics.feature_importance.importance.map(Math.abs));
                const barWidth = (absImportance / maxImportance) * 100;
                
                return (
                  <div key={idx} style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                    <div style={{ width: "200px", fontSize: "13px", color: "#ccc", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                      {feature}
                    </div>
                    <div style={{ flex: 1, backgroundColor: "#1a1a1a", borderRadius: "4px", height: "24px", position: "relative" }}>
                      <div style={{ 
                        width: `${barWidth}%`, 
                        height: "100%", 
                        backgroundColor: importance > 0 ? "#28a745" : "#dc3545",
                        borderRadius: "4px",
                        transition: "width 0.3s ease"
                      }}></div>
                    </div>
                    <div style={{ width: "80px", textAlign: "right", fontSize: "13px", color: "#aaa" }}>
                      {importance.toFixed(4)}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

      </div>
    </div>
  );
}

export default Metrics;
