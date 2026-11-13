export function LoadingState({ label = "Loading…" }) {
  return (
    <div
      className="qk-panel overflow-hidden px-4 py-5"
      role="status"
      aria-live="polite"
      aria-busy="true"
    >
      <div className="flex items-center gap-3">
        <span className="relative flex h-2.5 w-2.5">
          <span className="absolute inline-flex h-full w-full animate-pulse-soft rounded-full bg-cyan opacity-60" />
          <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-cyan" />
        </span>
        <p className="text-sm text-slate-300">{label}</p>
      </div>
      <div className="mt-4 space-y-2">
        <div className="h-2 w-full animate-shimmer rounded bg-gradient-to-r from-line via-panel-elevated to-line bg-[length:200%_100%]" />
        <div className="h-2 w-4/5 animate-shimmer rounded bg-gradient-to-r from-line via-panel-elevated to-line bg-[length:200%_100%]" />
        <div className="h-2 w-3/5 animate-shimmer rounded bg-gradient-to-r from-line via-panel-elevated to-line bg-[length:200%_100%]" />
      </div>
    </div>
  );
}

export function ErrorState({ error }) {
  return (
    <div
      className="rounded-lg border border-rose-500/35 bg-rose-950/35 px-4 py-3 text-sm text-rose-100"
      role="alert"
    >
      {error?.message || String(error) || "Something went wrong."}
    </div>
  );
}

export function EmptyState({ message, title }) {
  return (
    <div className="rounded-lg border border-dashed border-line bg-panel/40 px-5 py-10 text-center">
      {title ? <p className="text-sm font-medium text-slate-200">{title}</p> : null}
      <p className={`text-sm text-slate-400 ${title ? "mt-1.5" : ""}`}>{message}</p>
    </div>
  );
}
