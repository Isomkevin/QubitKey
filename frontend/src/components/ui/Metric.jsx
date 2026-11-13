export default function Metric({ label, value, hint, className = "" }) {
  return (
    <div className={className}>
      <dt className="qk-label">{label}</dt>
      <dd className="mt-1 font-mono text-xl font-medium tracking-tight text-white sm:text-2xl">
        {value}
      </dd>
      {hint ? <p className="mt-1 text-xs text-slate-500">{hint}</p> : null}
    </div>
  );
}
