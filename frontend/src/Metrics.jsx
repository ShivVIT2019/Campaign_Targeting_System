import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Metrics.css';

const API_URL = import.meta.env.PROD 
  ? 'https://campaign-backend-vuf4.onrender.com'
  : 'http://localhost:8000';

function Metrics() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchMetrics();
  }, []);

  const fetchMetrics = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await axios.get(`${API_URL}/metrics`);
      console.log('Metrics response:', res.data);
      setMetrics(res.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to load metrics');
      setLoading(false);
      console.error('Error fetching metrics:', err);
    }
  };

  if (loading) {
    return (
      <div className="metrics-container">
        <h2>📊 Model Performance</h2>
        <div className="loading">Loading metrics...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="metrics-container">
        <h2>📊 Model Performance</h2>
        <div className="error-message">{error}</div>
        <button onClick={fetchMetrics} className="retry-btn">Retry</button>
      </div>
    );
  }

  if (!metrics || !metrics.live_metrics) {
    return (
      <div className="metrics-container">
        <h2>📊 Model Performance</h2>
        <div className="error-message">Invalid metrics data</div>
      </div>
    );
  }

  const { live_metrics, model_info, static_metrics } = metrics;

  return (
    <div className="metrics-container">
      <h2>📊 Live Model Performance</h2>
      
      <div className="metrics-section">
        <h3>🎯 Real-Time Predictions</h3>
        <div className="metrics-grid">
          <div className="metric-card">
            <div className="metric-icon">🎯</div>
            <div className="metric-value">{live_metrics.total_predictions}</div>
            <div className="metric-label">Total Predictions</div>
          </div>

          <div className="metric-card">
            <div className="metric-icon">📈</div>
            <div className="metric-value">{live_metrics.targeting_rate.toFixed(1)}%</div>
            <div className="metric-label">Targeting Rate</div>
          </div>

          <div className="metric-card">
            <div className="metric-icon">💯</div>
            <div className="metric-value">{live_metrics.average_probability.toFixed(1)}%</div>
            <div className="metric-label">Avg Purchase Probability</div>
          </div>

          <div className="metric-card">
            <div className="metric-icon">🤖</div>
            <div className="metric-value" style={{fontSize: '14px'}}>{model_info.model_type}</div>
            <div className="metric-label">Model Type</div>
          </div>
        </div>
      </div>

      <div className="metrics-section">
        <h3>📊 Decision Breakdown</h3>
        <div className="breakdown-stats">
          <div className="stat-item target">
            <span className="stat-label">🎯 Target</span>
            <span className="stat-value">{live_metrics.target_count}</span>
          </div>
          <div className="stat-item no-target">
            <span className="stat-label">❌ Don't Target</span>
            <span className="stat-value">{live_metrics.dont_target_count}</span>
          </div>
        </div>
      </div>

      <div className="metrics-section">
        <h3>🎚️ Confidence Distribution</h3>
        <div className="breakdown-stats">
          <div className="stat-item" style={{background: '#d4edda', borderColor: '#28a745'}}>
            <span className="stat-label">🟢 High</span>
            <span className="stat-value">{live_metrics.high_confidence}</span>
          </div>
          <div className="stat-item" style={{background: '#fff3cd', borderColor: '#ffc107'}}>
            <span className="stat-label">🟡 Medium</span>
            <span className="stat-value">{live_metrics.medium_confidence}</span>
          </div>
          <div className="stat-item" style={{background: '#f8d7da', borderColor: '#dc3545'}}>
            <span className="stat-label">🔴 Low</span>
            <span className="stat-value">{live_metrics.low_confidence}</span>
          </div>
        </div>
      </div>

      <div className="metrics-section">
        <h3>📚 Training Performance</h3>
        <div className="metrics-grid">
          <div className="metric-card">
            <div className="metric-value">{(static_metrics.accuracy * 100).toFixed(2)}%</div>
            <div className="metric-label">Accuracy</div>
          </div>
          <div className="metric-card">
            <div className="metric-value">{(static_metrics.roc_auc * 100).toFixed(2)}%</div>
            <div className="metric-label">ROC-AUC</div>
          </div>
          <div className="metric-card">
            <div className="metric-value">{(static_metrics.precision * 100).toFixed(2)}%</div>
            <div className="metric-label">Precision</div>
          </div>
          <div className="metric-card">
            <div className="metric-value">{(static_metrics.recall * 100).toFixed(2)}%</div>
            <div className="metric-label">Recall</div>
          </div>
        </div>
      </div>

      <div className="model-details">
        <h3>ℹ️ Model Information</h3>
        <p><strong>Features:</strong> {model_info.features}</p>
        <p><strong>Training Date:</strong> {model_info.training_date}</p>
        <p><strong>Base Rate:</strong> {(model_info.base_rate * 100).toFixed(2)}%</p>
        <p><strong>Threshold:</strong> {(model_info.threshold * 100)}%</p>
      </div>
    </div>
  );
}

export default Metrics;
