import { forwardRef } from "react";

const IconButton = forwardRef(function IconButton(
  { children, label, className = "", type = "button", ...props },
  ref,
) {
  return (
    <button
      ref={ref}
      type={type}
      aria-label={label}
      title={label}
      className={[
        "inline-flex h-11 w-11 items-center justify-center rounded-md border border-line",
        "bg-panel text-slate-200 transition duration-fast",
        "hover:border-cyan/40 hover:text-white",
        "focus-visible:outline-none disabled:opacity-50",
        className,
      ].join(" ")}
      {...props}
    >
      {children}
    </button>
  );
});

export default IconButton;
