import React from "react";
import { createRoot } from "react-dom/client";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import data from "./data/faireval_dashboard_data.json";
import "./style.css";

function Card({ title, children }) {
  return <div className="card"><h2>{title}</h2>{children}</div>;
}

function Metric({ label, value }) {
  return (
    <div className="metric">
      <div className="metricValue">{String(value ?? "n/a")}</div>
      <div className="metricLabel">{label}</div>
    </div>
  );
}

function App() {
  const rai = data.responsible_ai || {};
  const oversight = data.oversight || {};
  const agentic = data.agentic_release || {};
  const rag = data.rag || {};
  const latency = data.latency_cost || {};
  const textGen = data.text_generation || {};

  const comparisonData = [
    { name: "Baseline", score: textGen.baseline_avg_score ?? 0 },
    { name: "Candidate", score: textGen.candidate_avg_score ?? 0 }
  ];

  const oversightData = [
    { name: "Weak false allows", value: oversight.weak_evaluator_false_allows ?? 0 },
    { name: "Composite false allows", value: oversight.composite_evaluator_false_allows ?? 0 }
  ];

  return (
    <main>
      <header>
        <p className="eyebrow">FairEval-Suite</p>
        <h1>AI Evaluation & Responsible AI Release Safety Dashboard</h1>
        <p className="subtitle">
          Baseline-vs-candidate evaluation, RAG groundedness, Responsible AI safety gates,
          oversight reliability, latency/cost governance, and live API monitoring.
        </p>
        <div className="links">
          <a href={data.live_api.docs}>Live API Docs</a>
          <a href={data.live_api.health}>Health Endpoint</a>
        </div>
      </header>

      <section className="grid">
        <Card title="Responsible AI Release Gate">
          <div className="metrics">
            <Metric label="Release decision" value={rai.release_decision} />
            <Metric label="Safety regressions" value={rai.num_safety_regressions} />
            <Metric label="False allows" value={rai.false_allows} />
            <Metric label="Candidate pass rate" value={rai.candidate_pass_rate} />
          </div>
        </Card>

        <Card title="Agentic Release Gate">
          <div className="metrics">
            <Metric label="Release decision" value={agentic.release_decision} />
            <Metric label="Unsupported answers" value={agentic.unsupported_answer_count} />
            <Metric label="Hallucinations" value={agentic.hallucination_detected_count} />
            <Metric label="p95 latency ms" value={agentic.p95_latency_ms} />
          </div>
        </Card>

        <Card title="Text Generation Regression">
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={comparisonData}>
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="score" />
            </BarChart>
          </ResponsiveContainer>
          <p>Regressions detected: <b>{textGen.regressions_detected ?? "n/a"}</b></p>
        </Card>

        <Card title="Oversight Reliability">
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={oversightData}>
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" />
            </BarChart>
          </ResponsiveContainer>
          <p>Evaluator disagreement rate: <b>{oversight.evaluator_disagreement_rate ?? "n/a"}</b></p>
        </Card>

        <Card title="RAG Groundedness">
          <div className="metrics">
            <Metric label="Grounded pass count" value={rag.groundedness_pass_count} />
            <Metric label="Unsupported answers" value={rag.unsupported_answer_count} />
            <Metric label="Hallucinations" value={rag.hallucination_detected_count} />
            <Metric label="Release risk" value={rag.release_risk} />
          </div>
        </Card>

        <Card title="Latency / Cost Gate">
          <div className="metrics">
            <Metric label="p95 latency ms" value={latency.p95_latency_ms} />
            <Metric label="Max cost/request" value={latency.max_cost_per_request_usd} />
            <Metric label="Latency fail" value={latency.latency_fail} />
            <Metric label="Cost fail" value={latency.cost_fail} />
          </div>
        </Card>

        <Card title="Evaluation Warehouse">
          <pre>{JSON.stringify(data.warehouse, null, 2)}</pre>
        </Card>
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
