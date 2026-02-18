function LandingPage({ onEnter }) {
  return (
    <div className="landing-page">
      <div className="landing-bg-animation"></div>
      <div className="landing-grain"></div>

      <div className="landing-content">
        <div className="landing-icon">🎯</div>
        <h1 className="landing-title">Campaign Targeting System</h1>
        <p className="landing-tagline">
          AI-powered purchase probability prediction for smarter, data-driven marketing
        </p>

        <div className="landing-features">
          <div className="landing-feature">
            <span className="feature-icon">🤖</span>
            <h3>ML-Powered Predictions</h3>
            <p>Random Forest classifier trained on 12,330 shopping sessions with 89.32% AUC-ROC accuracy</p>
          </div>
          <div className="landing-feature">
            <span className="feature-icon">📊</span>
            <h3>Live Performance Dashboard</h3>
            <p>Real-time monitoring of prediction accuracy, targeting rate, and conversion analytics</p>
          </div>
          <div className="landing-feature">
            <span className="feature-icon">🧪</span>
            <h3>A/B Testing Simulator</h3>
            <p>Compare AI targeting vs random selection — see the ~30× ROI improvement in action</p>
          </div>
          <div className="landing-feature">
            <span className="feature-icon">📤</span>
            <h3>Batch Processing</h3>
            <p>Upload CSVs of visitor sessions and get bulk predictions with confidence tiers instantly</p>
          </div>
        </div>

        <div className="landing-stats">
          <div className="landing-stat">
            <span className="landing-stat-value">~30×</span>
            <span className="landing-stat-label">ROI Improvement</span>
          </div>
          <div className="landing-stat">
            <span className="landing-stat-value">89.32%</span>
            <span className="landing-stat-label">AUC-ROC Score</span>
          </div>
          <div className="landing-stat">
            <span className="landing-stat-value">76%</span>
            <span className="landing-stat-label">Ad Spend Saved</span>
          </div>
        </div>

        <button className="btn-explore" onClick={onEnter}>
          <span>🚀</span> Explore the System
        </button>

        <p className="landing-footer">
          Built by <strong>Sivasai Atchyut Akella</strong> · MS Computer Science (AI), Binghamton University
        </p>
      </div>
    </div>
  );
}

export default LandingPage;
