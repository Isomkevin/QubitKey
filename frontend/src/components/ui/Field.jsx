export default function Field({ label, hint, children, className = "", htmlFor }) {
  return (
    <div className={className}>
      {label ? (
        <label htmlFor={htmlFor} className="qk-label">
          {label}
        </label>
      ) : null}
      {children}
      {hint ? <p className="mt-1.5 text-xs text-slate-500">{hint}</p> : null}
    </div>
  );
}
