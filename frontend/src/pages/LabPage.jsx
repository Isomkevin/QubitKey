import { useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { api } from "../api/client.js";
import CircuitView from "../components/CircuitView.jsx";
import ProvenanceBadge from "../components/ProvenanceBadge.jsx";
import { EmptyState, ErrorState, LoadingState } from "../components/StatusBlock.jsx";
import Badge from "../components/ui/Badge.jsx";
import Button from "../components/ui/Button.jsx";
import Field from "../components/ui/Field.jsx";
import Metric from "../components/ui/Metric.jsx";
import PageHeader from "../components/ui/PageHeader.jsx";
import Panel from "../components/ui/Panel.jsx";
import { chartTheme } from "../components/ui/chartTheme.js";

function ExecutionBadge({ loading, error, result }) {
  if (loading) return <Badge tone="cyan">Running</Badge>;
  if (error) return <Badge tone="danger">Failed</Badge>;
  if (result) return <Badge tone="ok">Completed</Badge>;
  return <Badge tone="mute">Ready</Badge>;
}

export default function LabPage() {
  const [qubits, setQubits] = useState(4);
  const [shots, setShots] = useState(256);
  const [sourceType, setSourceType] = useState("qiskit_simulator");
  const [seed, setSeed] = useState("7");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function onRun(event) {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const payload = {
        source_type: sourceType,
        qubits: Number(qubits),
        shots: Number(shots),
      };
      if (sourceType !== "python_csprng" && seed !== "") {
        payload.seed = Number(seed);
      }
      const data = await api.runQrng(payload);
      setResult(data);
    } catch (err) {
      setResult(null);
      setError(err);
    } finally {
      setLoading(false);
    }
  }

  const chartData = result
    ? Object.entries(result.raw_counts || {})
        .sort((a, b) => a[0].localeCompare(b[0]))
        .slice(0, 32)
        .map(([bitstring, count]) => ({ bitstring, count }))
    : [];

  const seedDisabled = sourceType === "python_csprng" || sourceType === "ibm_qpu";

  return (
    <section className="qk-page">
      <PageHeader
        eyebrow="Experimentation"
        title="Quantum Lab"
        description="Configure a Hadamard measurement experiment. Simulator runs are educational simulations — never physical quantum entropy."
        actions={<ExecutionBadge loading={loading} error={error} result={result} />}
      />

      <div className="grid gap-6 xl:grid-cols-12">
        {/* Config rail */}
        <Panel as="form" onSubmit={onRun} className="space-y-4 xl:col-span-4" elevated>
          <p className="qk-label">Configuration</p>
          <Field label="Source" htmlFor="lab-source">
            <select
              id="lab-source"
              className="qk-select"
              value={sourceType}
              onChange={(e) => setSourceType(e.target.value)}
            >
              <option value="qiskit_simulator">qiskit_simulator</option>
              <option value="python_prng">python_prng</option>
              <option value="python_csprng">python_csprng</option>
              <option value="ibm_qpu">ibm_qpu</option>
            </select>
          </Field>
          <div className="grid grid-cols-2 gap-3">
            <Field label="Qubits" htmlFor="lab-qubits">
              <input
                id="lab-qubits"
                type="number"
                min={1}
                max={8}
                className="qk-input"
                value={qubits}
                onChange={(e) => setQubits(e.target.value)}
              />
            </Field>
            <Field label="Shots" htmlFor="lab-shots">
              <input
                id="lab-shots"
                type="number"
                min={1}
                max={8192}
                className="qk-input"
                value={shots}
                onChange={(e) => setShots(e.target.value)}
              />
            </Field>
          </div>
          <Field
            label="Seed"
            htmlFor="lab-seed"
            hint={seedDisabled ? "Not applicable for this source." : "Educational reproducibility only."}
          >
            <input
              id="lab-seed"
              type="number"
              className="qk-input"
              value={seed}
              onChange={(e) => setSeed(e.target.value)}
              disabled={seedDisabled}
            />
          </Field>
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? "Running…" : "Run experiment"}
          </Button>
        </Panel>

        {/* Stage */}
        <div className="space-y-4 xl:col-span-8">
          {loading ? <LoadingState label="Executing experiment…" /> : null}
          {error ? <ErrorState error={error} /> : null}
          {!loading && !error && !result ? (
            <EmptyState
              title="Ready to measure"
              message="Run an experiment to see the circuit, counts, samples, and provenance."
            />
          ) : null}

          {result ? (
            <div className="animate-fade-up space-y-4">
              <ProvenanceBadge
                sourceType={result.source_type}
                statement={result.provenance_statement}
              />

              <Panel elevated>
                <div className="mb-3 flex items-center justify-between gap-2">
                  <h2 className="text-sm font-medium text-white">Quantum circuit</h2>
                  <Badge tone="violet">centrepiece</Badge>
                </div>
                <CircuitView circuit={result.circuit} />
              </Panel>

              <Panel>
                <h2 className="mb-3 text-sm font-medium text-white">
                  Measurement counts
                  <span className="ml-2 font-mono text-xs text-slate-500">n={result.shots}</span>
                </h2>
                {chartData.length ? (
                  <div className="h-64 sm:h-72">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={chartData} margin={{ bottom: 48, left: 4, right: 8 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke={chartTheme.grid} vertical={false} />
                        <XAxis
                          dataKey="bitstring"
                          stroke={chartTheme.axis}
                          tick={{ fill: chartTheme.axis, fontSize: 10, fontFamily: "IBM Plex Mono" }}
                          angle={-45}
                          textAnchor="end"
                          interval={0}
                          height={56}
                        />
                        <YAxis
                          stroke={chartTheme.axis}
                          tick={{ fill: chartTheme.axis, fontSize: 11 }}
                          width={40}
                        />
                        <Tooltip {...chartTheme.tooltip} />
                        <Bar dataKey="count" fill={chartTheme.bar} radius={[3, 3, 0, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                ) : (
                  <p className="text-sm text-slate-400">No count data in this response.</p>
                )}
              </Panel>

              <Panel>
                <dl className="grid gap-5 sm:grid-cols-3">
                  <Metric label="Shots" value={result.shots} />
                  <Metric
                    label="Qubits"
                    value={result.circuit?.num_qubits ?? "—"}
                  />
                  <Metric
                    label="Seed"
                    value={result.seed ?? "—"}
                    hint={result.seed == null ? "Not applicable" : undefined}
                  />
                </dl>
                <div className="mt-5 border-t border-line pt-4 space-y-2">
                  <p className="qk-label">Experiment ID</p>
                  <p className="qk-mono-meta">{result.experiment_id}</p>
                  <p className="qk-label mt-3">Bit samples (preview)</p>
                  <p className="qk-mono-meta">
                    {(result.bit_samples || []).slice(0, 12).join(" ") || "—"}
                  </p>
                </div>
                {(result.warnings || []).length ? (
                  <ul className="mt-4 list-disc space-y-1 pl-5 text-xs text-amber-200">
                    {result.warnings.map((w) => (
                      <li key={w}>{w}</li>
                    ))}
                  </ul>
                ) : null}
              </Panel>
            </div>
          ) : null}
        </div>
      </div>
    </section>
  );
}
