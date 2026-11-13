const VARIANTS = {
  primary:
    "bg-cyan text-ink hover:bg-cyan/90 active:bg-cyan-dim disabled:bg-cyan/40 disabled:text-ink/60",
  secondary:
    "border border-line bg-panel text-slate-100 hover:bg-panel-elevated hover:border-cyan/30 active:bg-ink",
  ghost: "text-slate-300 hover:bg-panel hover:text-white",
  danger:
    "border border-rose-500/40 bg-rose-950/40 text-rose-100 hover:bg-rose-950/60",
};

const SIZES = {
  sm: "px-3 py-1.5 text-xs min-h-[36px]",
  md: "px-4 py-2.5 text-sm min-h-[44px]",
  lg: "px-5 py-3 text-sm min-h-[48px]",
};

export default function Button({
  children,
  variant = "primary",
  size = "md",
  className = "",
  type = "button",
  ...props
}) {
  return (
    <button
      type={type}
      className={[
        "inline-flex items-center justify-center gap-2 rounded-md font-medium transition duration-fast",
        "focus-visible:outline-none disabled:cursor-not-allowed disabled:opacity-60",
        VARIANTS[variant] || VARIANTS.primary,
        SIZES[size] || SIZES.md,
        className,
      ].join(" ")}
      {...props}
    >
      {children}
    </button>
  );
}
