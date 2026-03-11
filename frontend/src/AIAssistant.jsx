import { useState, useRef, useEffect } from "react";
import axios from "axios";

const API_URL = import.meta.env.PROD
  ? "https://campaign-targeting-backend-405497784425.us-central1.run.app"
  : "http://localhost:8000";

const SUGGESTED_QUESTIONS = [
  "Which features drive the highest purchase probability?",
  "How does the A/B testing framework work?",
  "What is the ROI improvement over random selection?",
  "Explain the confidence tiers in this system",
  "Which visitor types convert best?",
  "How should I interpret the risk score?",
];

// Simple markdown renderer — handles **bold**, *italic*, bullet lists
function renderMarkdown(text) {
  const lines = text.split("\n");
  const elements = [];
  let key = 0;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Bullet points: lines starting with * or -
    if (/^\s*[\*\-]\s+/.test(line)) {
      const content = line.replace(/^\s*[\*\-]\s+/, "");
      elements.push(
        <div key={key++} style={{ display: "flex", gap: "0.5rem", marginBottom: "0.2rem" }}>
          <span style={{ color: "var(--accent-primary)", flexShrink: 0 }}>•</span>
          <span>{inlineMarkdown(content)}</span>
        </div>
      );
    }
    // Empty line = spacer
    else if (line.trim() === "") {
      elements.push(<div key={key++} style={{ height: "0.4rem" }} />);
    }
    // Normal line
    else {
      elements.push(
        <div key={key++} style={{ marginBottom: "0.1rem" }}>
          {inlineMarkdown(line)}
        </div>
      );
    }
  }

  return elements;
}

// Handle **bold** and *italic* inline
function inlineMarkdown(text) {
  const parts = text.split(/(\*\*[^*]+\*\*|\*[^*]+\*)/g);
  return parts.map((part, i) => {
    if (/^\*\*[^*]+\*\*$/.test(part)) {
      return <strong key={i}>{part.slice(2, -2)}</strong>;
    } else if (/^\*[^*]+\*$/.test(part)) {
      return <em key={i}>{part.slice(1, -1)}</em>;
    }
    return part;
  });
}

function AIAssistant() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "👋 Hi! I'm the Campaign AI Assistant. Ask me anything about the targeting system — model features, ROI, A/B testing, or how to interpret predictions.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async (question) => {
    const q = question || input.trim();
    if (!q) return;

    setMessages((prev) => [...prev, { role: "user", text: q }]);
    setInput("");
    setLoading(true);

    try {
      const res = await axios.post(`${API_URL}/chat`, { question: q });
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: res.data.answer },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: "⚠️ Sorry, I couldn't connect to the AI backend. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="ai-assistant-container">
      {/* Header */}
      <div className="glass-card" style={{ marginBottom: "1.5rem" }}>
        <div className="card-header">
          <div className="card-icon">🤖</div>
          <div>
            <h2 className="card-title">Campaign AI Assistant</h2>
            <p style={{ color: "var(--text-muted)", fontSize: "0.85rem", marginTop: "0.25rem" }}>
              Powered by Google Gemini · RAG over campaign analytics data
            </p>
          </div>
        </div>
      </div>

      {/* Suggested Questions */}
      <div className="glass-card" style={{ marginBottom: "1.5rem" }}>
        <p style={{ color: "var(--text-muted)", fontSize: "0.85rem", marginBottom: "0.75rem" }}>
          💡 Try asking:
        </p>
        <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem" }}>
          {SUGGESTED_QUESTIONS.map((q) => (
            <button
              key={q}
              onClick={() => sendMessage(q)}
              disabled={loading}
              style={{
                background: "rgba(99,102,241,0.15)",
                border: "1px solid rgba(99,102,241,0.3)",
                borderRadius: "20px",
                padding: "0.4rem 0.9rem",
                color: "var(--text-primary)",
                fontSize: "0.8rem",
                cursor: "pointer",
                transition: "all 0.2s",
              }}
              onMouseOver={(e) => (e.target.style.background = "rgba(99,102,241,0.3)")}
              onMouseOut={(e) => (e.target.style.background = "rgba(99,102,241,0.15)")}
            >
              {q}
            </button>
          ))}
        </div>
      </div>

      {/* Chat Window */}
      <div
        className="glass-card"
        style={{
          minHeight: "420px",
          maxHeight: "420px",
          overflowY: "auto",
          display: "flex",
          flexDirection: "column",
          gap: "1rem",
          marginBottom: "1rem",
          padding: "1.5rem",
        }}
      >
        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              display: "flex",
              justifyContent: msg.role === "user" ? "flex-end" : "flex-start",
            }}
          >
            <div
              style={{
                maxWidth: "75%",
                padding: "0.75rem 1rem",
                borderRadius: msg.role === "user" ? "18px 18px 4px 18px" : "18px 18px 18px 4px",
                background:
                  msg.role === "user"
                    ? "linear-gradient(135deg, #6366f1, #8b5cf6)"
                    : "rgba(255,255,255,0.07)",
                border: msg.role === "assistant" ? "1px solid rgba(255,255,255,0.1)" : "none",
                color: "var(--text-primary)",
                fontSize: "0.9rem",
                lineHeight: "1.6",
              }}
            >
              {msg.role === "assistant" && (
                <span style={{ fontSize: "0.75rem", color: "var(--text-muted)", display: "block", marginBottom: "0.3rem" }}>
                  🤖 AI Assistant
                </span>
              )}
              {msg.role === "assistant" ? renderMarkdown(msg.text) : msg.text}
            </div>
          </div>
        ))}

        {loading && (
          <div style={{ display: "flex", justifyContent: "flex-start" }}>
            <div
              style={{
                padding: "0.75rem 1rem",
                borderRadius: "18px 18px 18px 4px",
                background: "rgba(255,255,255,0.07)",
                border: "1px solid rgba(255,255,255,0.1)",
                color: "var(--text-muted)",
                fontSize: "0.9rem",
              }}
            >
              🤖 Thinking...
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input Box */}
      <div style={{ display: "flex", gap: "0.75rem", alignItems: "center" }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask about the campaign system..."
          disabled={loading}
          className="form-input"
          style={{ flex: 1, margin: 0 }}
        />
        <button
          onClick={() => sendMessage()}
          disabled={loading || !input.trim()}
          className="btn-predict"
          style={{
            padding: "0.75rem 1.5rem",
            minWidth: "auto",
            opacity: loading || !input.trim() ? 0.5 : 1,
          }}
        >
          {loading ? "..." : "Send 🚀"}
        </button>
      </div>
    </div>
  );
}

export default AIAssistant;
