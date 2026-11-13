const TONES = {
  cyan: "bg-cyan/10 text-cyan ring-cyan/30",
  violet: "bg-violet/10 text-violet ring-violet/30",
  ok: "bg-emerald-500/15 text-emerald-200 ring-emerald-400/35",
  warn: "bg-amber-500/15 text-amber-200 ring-amber-400/35",
  danger: "bg-rose-500/15 text-rose-200 ring-rose-400/35",
  mute: "bg-slate-500/15 text-slate-300 ring-slate-400/30",
};

export default function Badge({ children, tone = "mute", className = "" }) {
  return (
    <span
      className={[
        "inline-flex items-center rounded-md px-2 py-0.5 font-mono text-[11px] uppercase tracking-wide ring-1",
        TONES[tone] || TONES.mute,
        className,
      ].join(" ")}
    >
      {children}
    </span>
  );
}
