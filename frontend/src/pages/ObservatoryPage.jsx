import { useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { api } from "../api/client.js";
import ProvenanceBadge from "../components/ProvenanceBadge.jsx";
import { EmptyState, ErrorState, LoadingState } from "../components/StatusBlock.jsx";
import Button from "../components/ui/Button.jsx";
import Field from "../components/ui/Field.jsx";
import Metric from "../components/ui/Metric.jsx";
import PageHeader from "../components/ui/PageHeader.jsx";
import Panel from "../components/ui/Panel.jsx";
import { SOURCE_COLORS, chartTheme } from "../components/ui/chartTheme.js";

function formatNum(value, digits = 4) {
  if (value == null || Number.isNaN(Number(value))) return "—";
  return Number(value).toFixed(digits);
}

function chiSquareSummary(metrics) {
  const chi = metrics?.chi_square;
  if (!chi || typeof chi !== "object") return null;
  if (chi.statistic != null) {
    return {
      statistic: chi.statistic,
      p_value: chi.p_value,
      passed: chi.passed ?? chi.accept_null,
    };
  }
  return chi;
}

export default function ObservatoryPage() {
  const [sampleBits, setSampleBits] = useState(1024);
  const [qubits, setQubits] = useState(4);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showTable, setShowTable] = useState(false);

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
      value: Number(src.metrics?.frequency_ones || 0),
      fill: SOURCE_COLORS[src.source_type] || chartTheme.bar,
    })) || [];

  const entropyData =
    result?.sources?.map((src) => ({
      source: src.source_type,
      value: Number(src.metrics?.empirical_shannon_entropy_bits || 0),
      fill: SOURCE_COLORS[src.source_type] || chartTheme.barAlt,
    })) || [];

  return (
    <section className="qk-page">
      <PageHeader
        eyebrow="Analysis"
        title="Entropy Observatory"
        description="Compare equal-sized samples across educational and classical sources. Passing these diagnostics does not prove cryptographic security."
      />

      <Panel as="form" onSubmit={onCompare} className="flex flex-wrap items-end gap-4" elevated>
        <Field label="Sample bits" htmlFor="obs-bits" className="w-36">
          <input
            id="obs-bits"
            type="number"
            min={8}
            max={100000}
            className="qk-input"
            value={sampleBits}
            onChange={(e) => setSampleBits(e.target.value)}
          />
        </Field>
        <Field label="Qubits" htmlFor="obs-qubits" className="w-28">
          <input
            id="obs-qubits"
            type="number"
            min={1}
            max={8}
            className="qk-input"
            value={qubits}
            onChange={(e) => setQubits(e.target.value)}
          />
        </Field>
        <Button type="submit" disabled={loading}>
          {loading ? "Comparing…" : "Compare sources"}
        </Button>
      </Panel>

      {loading ? <LoadingState label="Generating comparable datasets…" /> : null}
      {error ? <ErrorState error={error} /> : null}
      {!loading && !error && !result ? (
        <EmptyState
          title="Awaiting comparison"
          message="Run a comparison to inspect frequency, entropy, runs, and autocorrelation."
        />
      ) : null}

      {result ? (
        <div className="animate-fade-up space-y-6">
          <div className="qk-callout-warn">
            <p className="text-sm font-medium text-amber-100">Scientific caveat</p>
            <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-amber-50/90">
              {(result.caveats || []).map((c) => (
                <li key={c}>{c}</li>
              ))}
            </ul>
          </div>

          <div className="flex flex-wrap items-center justify-between gap-2">
            <p className="text-sm text-slate-400">
              Equal sample size · seed{" "}
              <span className="font-mono text-xs text-slate-300">42</span> (educational)
            </p>
            <Button
              type="button"
              variant="ghost"
              size="sm"
              onClick={() => setShowTable((v) => !v)}
            >
              {showTable ? "Hide metric table" : "Show metric table"}
            </Button>
          </div>

          {/* Separated charts — own scales */}
          <div className="grid gap-4 lg:grid-cols-2">
            <Panel elevated>
              <h2 className="text-sm font-medium text-white">Bit balance · P(one)</h2>
              <p className="mt-1 text-xs text-slate-500">Ideal fair coin ≈ 0.5</p>
              <div className="mt-3 h-56">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={frequencyData} margin={{ left: 0, right: 8 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke={chartTheme.grid} vertical={false} />
                    <XAxis
                      dataKey="source"
                      stroke={chartTheme.axis}
                      tick={{ fill: chartTheme.axis, fontSize: 10 }}
                      interval={0}
                      angle={-15}
                      textAnchor="end"
                      height={48}
                    />
                    <YAxis
                      domain={[0, 1]}
                      stroke={chartTheme.axis}
                      tick={{ fill: chartTheme.axis, fontSize: 11 }}
                      width={36}
                    />
                    <Tooltip {...chartTheme.tooltip} formatter={(v) => [formatNum(v), "P(one)"]} />
                    <Bar dataKey="value" radius={[3, 3, 0, 0]}>
                      {frequencyData.map((entry) => (
                        <Cell key={entry.source} fill={entry.fill} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </Panel>

            <Panel elevated>
              <h2 className="text-sm font-medium text-white">Empirical Shannon entropy</h2>
              <p className="mt-1 text-xs text-slate-500">Bits per sample bit · ideal binary ≈ 1.0</p>
              <div className="mt-3 h-56">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={entropyData} margin={{ left: 0, right: 8 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke={chartTheme.grid} vertical={false} />
                    <XAxis
                      dataKey="source"
                      stroke={chartTheme.axis}
                      tick={{ fill: chartTheme.axis, fontSize: 10 }}
                      interval={0}
                      angle={-15}
                      textAnchor="end"
                      height={48}
                    />
                    <YAxis
                      domain={[0, "auto"]}
                      stroke={chartTheme.axis}
                      tick={{ fill: chartTheme.axis, fontSize: 11 }}
                      width={36}
                    />
                    <Tooltip
                      {...chartTheme.tooltip}
                      formatter={(v) => [formatNum(v), "H (bits)"]}
                    />
                    <Bar dataKey="value" radius={[3, 3, 0, 0]}>
                      {entropyData.map((entry) => (
                        <Cell key={entry.source} fill={entry.fill} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </Panel>
          </div>

          {/* Per-source metric panels */}
          <div className="grid gap-4 md:grid-cols-3">
            {result.sources.map((src) => {
              const chi = chiSquareSummary(src.metrics);
              return (
                <Panel key={src.source_type} className="space-y-4">
                  <ProvenanceBadge
                    sourceType={src.source_type}
                    statement={src.provenance_statement}
                  />
                  <dl className="grid grid-cols-2 gap-4">
                    <Metric label="Bits" value={src.metrics?.bit_count ?? "—"} />
                    <Metric label="P(one)" value={formatNum(src.metrics?.frequency_ones)} />
                    <Metric
                      label="Shannon H"
                      value={formatNum(src.metrics?.empirical_shannon_entropy_bits)}
                    />
                    <Metric label="Longest run" value={src.metrics?.longest_run ?? "—"} />
                    <Metric
                      label="Lag-1 corr"
                      value={formatNum(src.metrics?.lag1_autocorrelation)}
                      className="col-span-2"
                    />
                  </dl>
                  {chi ? (
                    <div className="border-t border-line pt-3 text-xs text-slate-400">
                      <p className="qk-label mb-1">Chi-square</p>
                      <p className="font-mono text-slate-300">
                        χ²={formatNum(chi.statistic, 3)}
                        {chi.p_value != null ? ` · p=${formatNum(chi.p_value, 3)}` : ""}
                        {chi.passed != null ? ` · ${chi.passed ? "accept" : "reject"} H₀` : ""}
                      </p>
                    </div>
                  ) : null}
                </Panel>
              );
            })}
          </div>

          {showTable ? (
            <Panel className="overflow-x-auto" padding={false}>
              <table className="w-full min-w-[640px] text-left text-sm">
                <thead className="border-b border-line bg-panel-elevated/80 text-xs uppercase tracking-wider text-slate-500">
                  <tr>
                    <th className="px-4 py-3 font-medium">Source</th>
                    <th className="px-4 py-3 font-medium">Bits</th>
                    <th className="px-4 py-3 font-medium">P(one)</th>
                    <th className="px-4 py-3 font-medium">Shannon H</th>
                    <th className="px-4 py-3 font-medium">Longest run</th>
                    <th className="px-4 py-3 font-medium">Lag-1</th>
                  </tr>
                </thead>
                <tbody>
                  {result.sources.map((src) => (
                    <tr key={src.source_type} className="border-b border-line/60 last:border-0">
                      <td className="px-4 py-3 font-mono text-xs text-slate-200">
                        {src.source_type}
                      </td>
                      <td className="px-4 py-3 font-mono text-xs">{src.metrics?.bit_count}</td>
                      <td className="px-4 py-3 font-mono text-xs">
                        {formatNum(src.metrics?.frequency_ones)}
                      </td>
                      <td className="px-4 py-3 font-mono text-xs">
                        {formatNum(src.metrics?.empirical_shannon_entropy_bits)}
                      </td>
                      <td className="px-4 py-3 font-mono text-xs">{src.metrics?.longest_run}</td>
                      <td className="px-4 py-3 font-mono text-xs">
                        {formatNum(src.metrics?.lag1_autocorrelation)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </Panel>
          ) : null}
        </div>
      ) : null}
    </section>
  );
}
