const STYLES = {
  qiskit_simulator: "bg-amber-500/15 text-amber-200 ring-amber-400/40",
  ibm_qpu: "bg-emerald-500/15 text-emerald-200 ring-emerald-400/40",
  python_prng: "bg-slate-500/20 text-slate-200 ring-slate-400/40",
  python_csprng: "bg-sky-500/15 text-sky-200 ring-sky-400/40",
};

export default function ProvenanceBadge({ sourceType, statement }) {
  const style = STYLES[sourceType] || "bg-panel text-slate-200 ring-line";
  return (
    <div className={`rounded-md px-3 py-2 text-sm ring-1 ${style}`} role="status">
      <p className="font-mono text-xs uppercase tracking-wide">{sourceType || "unknown"}</p>
      {statement ? <p className="mt-1 text-xs leading-relaxed opacity-90">{statement}</p> : null}
    </div>
  );
}
