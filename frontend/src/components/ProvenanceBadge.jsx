const STYLES = {
  qiskit_simulator: "bg-amber-500/12 text-amber-100 ring-amber-400/35",
  ibm_qpu: "bg-emerald-500/12 text-emerald-100 ring-emerald-400/35",
  python_prng: "bg-slate-500/15 text-slate-200 ring-slate-400/35",
  python_csprng: "bg-sky-500/12 text-sky-100 ring-sky-400/35",
};

export default function ProvenanceBadge({ sourceType, statement, compact = false }) {
  const style = STYLES[sourceType] || "bg-panel text-slate-200 ring-line";
  return (
    <div
      className={`rounded-lg px-3 py-2.5 ring-1 ${style} ${compact ? "py-1.5" : ""}`}
      role="status"
    >
      <p className="font-mono text-[11px] uppercase tracking-[0.16em]">{sourceType || "unknown"}</p>
      {statement && !compact ? (
        <p className="mt-1.5 text-xs leading-relaxed opacity-90">{statement}</p>
      ) : null}
    </div>
  );
}
