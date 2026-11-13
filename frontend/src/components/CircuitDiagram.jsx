/**
 * SVG circuit visualisation from API circuit.gates / num_qubits.
 * Represents the configured Hadamard QRNG experiment — not a decorative fake.
 */
export default function CircuitDiagram({ circuit }) {
  if (!circuit?.num_qubits) {
    return (
      <p className="text-sm text-slate-400">No circuit data for this source.</p>
    );
  }

  const n = circuit.num_qubits;
  const gates = circuit.gates || [];
  const hasMeasure = Boolean(circuit.measurements);

  const rowH = 44;
  const padX = 28;
  const padY = 28;
  const labelW = 42;
  const gateW = 36;
  const gateGap = 28;
  const measureW = 40;
  const classicalGap = 18;

  const gateCols = Math.max(gates.length, 1);
  const width =
    padX * 2 +
    labelW +
    gateCols * (gateW + gateGap) +
    (hasMeasure ? measureW + gateGap : 0) +
    24;
  const height = padY * 2 + n * rowH + (hasMeasure ? classicalGap + 20 : 0);

  const wireX0 = padX + labelW;
  const wireX1 = width - padX;

  // Group gates by qubit for column placement (Hadamard QRNG: one H per qubit, sequential)
  const gateByQubit = {};
  gates.forEach((g, idx) => {
    const q = g.qubits?.[0] ?? idx;
    if (gateByQubit[q] == null) gateByQubit[q] = [];
    gateByQubit[q].push({ ...g, col: gateByQubit[q].length });
  });

  return (
    <div className="overflow-x-auto">
      <svg
        viewBox={`0 0 ${width} ${height}`}
        width="100%"
        height={Math.min(height, 360)}
        role="img"
        aria-label={`${n}-qubit Hadamard QRNG circuit${hasMeasure ? " with measurement" : ""}`}
        className="min-w-[280px]"
      >
        {/* Classical register rail */}
        {hasMeasure ? (
          <>
            <line
              x1={wireX0}
              y1={padY + n * rowH + classicalGap}
              x2={wireX1}
              y2={padY + n * rowH + classicalGap}
              stroke="var(--qk-mute)"
              strokeWidth="1.2"
              strokeDasharray="3 3"
            />
            <text
              x={padX}
              y={padY + n * rowH + classicalGap + 4}
              fill="var(--qk-mute)"
              fontSize="11"
              fontFamily="IBM Plex Mono, monospace"
            >
              c
            </text>
          </>
        ) : null}

        {Array.from({ length: n }, (_, q) => {
          const y = padY + q * rowH + rowH / 2;
          const qubitGates = gateByQubit[q] || [];
          return (
            <g key={`q-${q}`}>
              <text
                x={padX}
                y={y + 4}
                fill="var(--qk-mute)"
                fontSize="11"
                fontFamily="IBM Plex Mono, monospace"
              >
                q{q}
              </text>
              <line
                x1={wireX0}
                y1={y}
                x2={wireX1}
                y2={y}
                stroke="var(--qk-line)"
                strokeWidth="1.5"
              />
              {/* faint quantum-state wash */}
              <line
                x1={wireX0}
                y1={y}
                x2={wireX1}
                y2={y}
                stroke="var(--qk-violet)"
                strokeWidth="1"
                opacity="0.25"
              />

              {qubitGates.map((g, i) => {
                const col = g.col ?? i;
                const cx = wireX0 + gateGap + col * (gateW + gateGap) + gateW / 2;
                const name = (g.name || "h").toLowerCase();
                return (
                  <g key={`${q}-${i}-${name}`}>
                    <rect
                      x={cx - gateW / 2}
                      y={y - 14}
                      width={gateW}
                      height={28}
                      rx={4}
                      fill="var(--qk-panel-elevated)"
                      stroke="var(--qk-cyan)"
                      strokeWidth="1.4"
                    />
                    <text
                      x={cx}
                      y={y + 4}
                      textAnchor="middle"
                      fill="var(--qk-cyan)"
                      fontSize="12"
                      fontWeight="600"
                      fontFamily="IBM Plex Sans, sans-serif"
                    >
                      {name === "h" ? "H" : name.toUpperCase()}
                    </text>
                  </g>
                );
              })}

              {hasMeasure ? (
                <g>
                  {(() => {
                    const mx =
                      wireX0 +
                      gateGap +
                      gateCols * (gateW + gateGap) +
                      measureW / 2;
                    const cy = padY + n * rowH + classicalGap;
                    return (
                      <>
                        <rect
                          x={mx - 16}
                          y={y - 14}
                          width={32}
                          height={28}
                          rx={4}
                          fill="var(--qk-panel)"
                          stroke="var(--qk-violet)"
                          strokeWidth="1.3"
                        />
                        {/* meter arc */}
                        <path
                          d={`M ${mx - 8} ${y + 4} A 8 8 0 0 1 ${mx + 8} ${y + 4}`}
                          fill="none"
                          stroke="var(--qk-violet)"
                          strokeWidth="1.4"
                        />
                        <line
                          x1={mx}
                          y1={y + 4}
                          x2={mx + 6}
                          y2={y - 6}
                          stroke="var(--qk-violet)"
                          strokeWidth="1.4"
                          strokeLinecap="round"
                        />
                        <line
                          x1={mx}
                          y1={y + 14}
                          x2={mx}
                          y2={cy}
                          stroke="var(--qk-mute)"
                          strokeWidth="1"
                          strokeDasharray="2 2"
                        />
                        <circle cx={mx} cy={cy} r="2.5" fill="var(--qk-mute)" />
                      </>
                    );
                  })()}
                </g>
              ) : null}
            </g>
          );
        })}
      </svg>
      <p className="mt-2 text-xs text-slate-500">
        {n} qubit Hadamard QRNG circuit
        {hasMeasure ? " with measurement" : ""}.
      </p>
    </div>
  );
}
