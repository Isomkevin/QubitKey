/** Shared Recharts styling aligned with QubitKey tokens. */
export const chartTheme = {
  grid: "var(--qk-chart-grid)",
  axis: "var(--qk-chart-axis)",
  bar: "var(--qk-chart-bar)",
  barAlt: "var(--qk-chart-bar-alt)",
  tooltip: {
    contentStyle: {
      background: "#0f1a2e",
      border: "1px solid #1a2740",
      borderRadius: "8px",
      color: "#e2e8f0",
      fontSize: "12px",
      fontFamily: '"IBM Plex Sans", sans-serif',
    },
    labelStyle: { color: "#94a3b8", marginBottom: 4 },
    itemStyle: { color: "#e2e8f0", padding: 0 },
    cursor: { fill: "rgba(34, 211, 238, 0.06)" },
  },
};

export const SOURCE_COLORS = {
  qiskit_simulator: "#fbbf24",
  ibm_qpu: "#34d399",
  python_prng: "#94a3b8",
  python_csprng: "#38bdf8",
};
