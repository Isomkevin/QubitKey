export default function CircuitView({ circuit }) {
  if (!circuit) {
    return (
      <p className="text-sm text-slate-400">No circuit data for this source.</p>
    );
  }

  return (
    <div className="space-y-3">
      <p className="text-sm text-slate-300">
        {circuit.num_qubits} qubit Hadamard QRNG circuit
        {circuit.measurements ? " with measurement" : ""}.
      </p>
      {circuit.drawing ? (
        <pre className="overflow-x-auto rounded-md border border-line bg-ink/70 p-3 font-mono text-xs text-slate-200">
          {circuit.drawing}
        </pre>
      ) : (
        <ul className="font-mono text-xs text-slate-300">
          {circuit.gates?.map((gate, idx) => (
            <li key={`${gate.name}-${idx}`}>
              {gate.name}({gate.qubits?.join(",")})
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
