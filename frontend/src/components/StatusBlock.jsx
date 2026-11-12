export function LoadingState({ label = "Loading…" }) {
  return (
    <div className="animate-pulse-soft rounded-md border border-line bg-panel/60 px-4 py-6 text-sm text-slate-300">
      {label}
    </div>
  );
}

export function ErrorState({ error }) {
  return (
    <div
      className="rounded-md border border-rose-500/40 bg-rose-950/40 px-4 py-3 text-sm text-rose-100"
      role="alert"
    >
      {error?.message || String(error) || "Something went wrong."}
    </div>
  );
}

export function EmptyState({ message }) {
  return (
    <div className="rounded-md border border-dashed border-line px-4 py-6 text-sm text-slate-400">
      {message}
    </div>
  );
}
