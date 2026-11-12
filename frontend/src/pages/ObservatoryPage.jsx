import { useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { api } from "../api/client.js";
import ProvenanceBadge from "../components/ProvenanceBadge.jsx";
import { EmptyState, ErrorState, LoadingState } from "../components/StatusBlock.jsx";

export default function ObservatoryPage() {
  const [sampleBits, setSampleBits] = useState(1024);
  const [qubits, setQubits] = useState(4);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function onCompare(event) {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const data = await api.compare({
        sample_bits: Number(sampleBits),
        qubits: Number(qubits),
        sources: ["qiskit_simulator", "python_prng", "python_csprng"],
        seed: 42,
      });
      setResult(data);
    } catch (err) {
      setResult(null);
      setError(err);
    } finally {
      setLoading(false);
    }
  }

  const frequencyData =
    result?.sources?.map((src) => ({
      source: src.source_type,
      frequency_ones: Number(src.metrics?.frequency_ones || 0),
      entropy: Number(src.metrics?.empirical_shannon_entropy_bits || 0),
      sample_bits: src.metrics?.bit_count,
    })) || [];

  return (
    <section className="animate-fade-up space-y-6">
      <div>
        <h2 className="text-2xl font-semibold text-white">Entropy Observatory</h2>
        <p className="mt-2 max-w-3xl text-sm text-slate-300">
          Compare equal-sized samples across educational and classical sources. Passing these
          diagnostics does not prove cryptographic security.
        </p>
      </div>

      <form
        onSubmit={onCompare}
        className="flex flex-wrap items-end gap-4 rounded-md border border-line bg-panel/40 p-4"
      >
        <label className="text-sm text-slate-300">
          Sample bits
          <input
            type="number"
            min={8}
            max={100000}
            className="mt-1 block rounded-md border border-line bg-ink px-2 py-2"
            value={sampleBits}
            onChange={(e) => setSampleBits(e.target.value)}
          />
        </label>
        <label className="text-sm text-slate-300">
          Qubits
          <input
            type="number"
            min={1}
            max={8}
            className="mt-1 block rounded-md border border-line bg-ink px-2 py-2"
            value={qubits}
            onChange={(e) => setQubits(e.target.value)}
          />
        </label>
        <button
          type="submit"
          className="rounded-md bg-accent px-4 py-2 text-sm font-medium text-white hover:bg-blue-500 disabled:opacity-60"
          disabled={loading}
        >
          {loading ? "Comparing…" : "Compare sources"}
        </button>
      </form>

      {loading ? <LoadingState label="Generating comparable datasets…" /> : null}
      {error ? <ErrorState error={error} /> : null}
      {!loading && !error && !result ? (
        <EmptyState message="Run a comparison to inspect frequency, entropy, and caveats." />
      ) : null}

      {result ? (
        <div className="space-y-4">
          <div className="h-72 rounded-md border border-line bg-panel/40 p-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={frequencyData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1c2a45" />
                <XAxis dataKey="source" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" domain={[0, 1]} />
                <Tooltip />
                <Legend />
                <Bar dataKey="frequency_ones" name="P(one)" fill="#3b82f6" />
                <Bar dataKey="entropy" name="Empirical Shannon H" fill="#7c6cf0" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="grid gap-3 md:grid-cols-3">
            {result.sources.map((src) => (
              <div key={src.source_type} className="space-y-2 rounded-md border border-line bg-panel/40 p-3">
                <ProvenanceBadge
                  sourceType={src.source_type}
                  statement={src.provenance_statement}
                />
                <dl className="grid grid-cols-2 gap-2 text-xs text-slate-300">
                  <div>
                    <dt>Bits</dt>
                    <dd className="font-mono">{src.metrics.bit_count}</dd>
                  </div>
                  <div>
                    <dt>Longest run</dt>
                    <dd className="font-mono">{src.metrics.longest_run}</dd>
                  </div>
                  <div>
                    <dt>Lag-1 corr</dt>
                    <dd className="font-mono">
                      {Number(src.metrics.lag1_autocorrelation || 0).toFixed(4)}
                    </dd>
                  </div>
                  <div>
                    <dt>P(one)</dt>
                    <dd className="font-mono">
                      {Number(src.metrics.frequency_ones || 0).toFixed(4)}
                    </dd>
                  </div>
                </dl>
              </div>
            ))}
          </div>

          <ul className="list-disc space-y-1 rounded-md border border-amber-500/30 bg-amber-950/20 px-5 py-3 text-sm text-amber-100">
            {(result.caveats || []).map((c) => (
              <li key={c}>{c}</li>
            ))}
          </ul>
        </div>
      ) : null}
    </section>
  );
}
