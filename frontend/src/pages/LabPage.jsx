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

  return (
    <section className="animate-fade-up space-y-6">
      <div>
        <h2 className="text-2xl font-semibold text-white">Quantum Lab</h2>
        <p className="mt-2 max-w-3xl text-sm text-slate-300">
          Configure a Hadamard measurement experiment. Simulator runs are educational simulations —
          never physical quantum entropy.
        </p>
      </div>

      <form
        onSubmit={onRun}
        className="grid gap-4 rounded-md border border-line bg-panel/40 p-4 md:grid-cols-4"
      >
        <label className="text-sm text-slate-300">
          Source
          <select
            className="mt-1 w-full rounded-md border border-line bg-ink px-2 py-2"
            value={sourceType}
            onChange={(e) => setSourceType(e.target.value)}
          >
            <option value="qiskit_simulator">qiskit_simulator</option>
            <option value="python_prng">python_prng</option>
            <option value="python_csprng">python_csprng</option>
            <option value="ibm_qpu">ibm_qpu</option>
          </select>
        </label>
        <label className="text-sm text-slate-300">
          Qubits
          <input
            type="number"
            min={1}
            max={8}
            className="mt-1 w-full rounded-md border border-line bg-ink px-2 py-2"
            value={qubits}
            onChange={(e) => setQubits(e.target.value)}
          />
        </label>
        <label className="text-sm text-slate-300">
          Shots
          <input
            type="number"
            min={1}
            max={8192}
            className="mt-1 w-full rounded-md border border-line bg-ink px-2 py-2"
            value={shots}
            onChange={(e) => setShots(e.target.value)}
          />
        </label>
        <label className="text-sm text-slate-300">
          Seed (educational only)
          <input
            type="number"
            className="mt-1 w-full rounded-md border border-line bg-ink px-2 py-2"
            value={seed}
            onChange={(e) => setSeed(e.target.value)}
            disabled={sourceType === "python_csprng" || sourceType === "ibm_qpu"}
          />
        </label>
        <div className="md:col-span-4">
          <button
            type="submit"
            className="rounded-md bg-accent px-4 py-2 text-sm font-medium text-white hover:bg-blue-500 disabled:opacity-60"
            disabled={loading}
          >
            {loading ? "Running…" : "Run experiment"}
          </button>
        </div>
      </form>

      {loading ? <LoadingState label="Executing experiment…" /> : null}
      {error ? <ErrorState error={error} /> : null}
      {!loading && !error && !result ? (
        <EmptyState message="Run an experiment to see counts, samples, and provenance." />
      ) : null}

      {result ? (
        <div className="space-y-4">
          <ProvenanceBadge
            sourceType={result.source_type}
            statement={result.provenance_statement}
          />
          <div className="grid gap-4 lg:grid-cols-2">
            <div className="rounded-md border border-line bg-panel/40 p-4">
              <h3 className="mb-3 text-sm font-medium text-white">Circuit</h3>
              <CircuitView circuit={result.circuit} />
            </div>
            <div className="rounded-md border border-line bg-panel/40 p-4">
              <h3 className="mb-3 text-sm font-medium text-white">
                Counts preview (n={result.shots})
              </h3>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1c2a45" />
                    <XAxis dataKey="bitstring" hide />
                    <YAxis stroke="#94a3b8" />
                    <Tooltip />
                    <Bar dataKey="count" fill="#3b82f6" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
          <div className="rounded-md border border-line bg-panel/40 p-4 text-sm text-slate-300">
            <p>
              Experiment ID: <span className="font-mono text-xs">{result.experiment_id}</span>
            </p>
            <p className="mt-2">
              Bit samples:{" "}
              <span className="font-mono text-xs">
                {(result.bit_samples || []).slice(0, 12).join(" ")}
              </span>
            </p>
            {(result.warnings || []).length ? (
              <ul className="mt-3 list-disc pl-5 text-amber-200">
                {result.warnings.map((w) => (
                  <li key={w}>{w}</li>
                ))}
              </ul>
            ) : null}
          </div>
        </div>
      ) : null}
    </section>
  );
}
