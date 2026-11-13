/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#05080f",
        panel: "#0a1220",
        "panel-elevated": "#0f1a2e",
        line: "#1a2740",
        cyan: {
          DEFAULT: "#22d3ee",
          dim: "#0891b2",
          soft: "rgba(34, 211, 238, 0.12)",
        },
        violet: {
          DEFAULT: "#8b7cf6",
          soft: "rgba(139, 124, 246, 0.14)",
        },
        // Legacy alias — map to cyan so older class names still work during migration
        accent: "#22d3ee",
        violetsoft: "#8b7cf6",
        ok: "#34d399",
        warn: "#fbbf24",
        danger: "#fb7185",
        mute: "#94a3b8",
      },
      fontFamily: {
        sans: ['"IBM Plex Sans"', "ui-sans-serif", "system-ui", "sans-serif"],
        mono: ['"IBM Plex Mono"', "ui-monospace", "monospace"],
      },
      boxShadow: {
        panel: "0 1px 0 rgba(255,255,255,0.04) inset, 0 8px 24px rgba(0,0,0,0.35)",
        focus: "0 0 0 3px rgba(34, 211, 238, 0.35)",
      },
      maxWidth: {
        content: "80rem",
      },
      transitionDuration: {
        fast: "120ms",
        med: "220ms",
        slow: "380ms",
      },
      keyframes: {
        "fade-up": {
          from: { opacity: "0", transform: "translateY(8px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
        "fade-in": {
          from: { opacity: "0" },
          to: { opacity: "1" },
        },
        "slide-in-left": {
          from: { transform: "translateX(-100%)" },
          to: { transform: "translateX(0)" },
        },
        "pulse-soft": {
          "0%, 100%": { opacity: "0.55" },
          "50%": { opacity: "1" },
        },
        shimmer: {
          "0%": { backgroundPosition: "200% 0" },
          "100%": { backgroundPosition: "-200% 0" },
        },
      },
      animation: {
        "fade-up": "fade-up 0.45s ease-out both",
        "fade-in": "fade-in 0.3s ease-out both",
        "slide-in-left": "slide-in-left 0.28s ease-out both",
        "pulse-soft": "pulse-soft 2.4s ease-in-out infinite",
        shimmer: "shimmer 1.6s linear infinite",
      },
    },
  },
  plugins: [],
};
