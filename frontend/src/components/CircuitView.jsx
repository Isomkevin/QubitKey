import { useState } from "react";
import CircuitDiagram from "./CircuitDiagram.jsx";
import Button from "./ui/Button.jsx";

export default function CircuitView({ circuit }) {
  const [showDrawing, setShowDrawing] = useState(false);

  if (!circuit) {
    return (
      <p className="text-sm text-slate-400">No circuit data for this source.</p>
    );
  }

  return (
    <div className="space-y-3">
      <CircuitDiagram circuit={circuit} />

      {circuit.drawing ? (
        <div>
          <Button
            type="button"
            variant="ghost"
            size="sm"
            onClick={() => setShowDrawing((v) => !v)}
            className="!min-h-0 px-0 text-cyan hover:bg-transparent"
          >
            {showDrawing ? "Hide Qiskit text drawing" : "Show Qiskit text drawing"}
          </Button>
          {showDrawing ? (
            <pre className="mt-2 overflow-x-auto rounded-md border border-line bg-ink/80 p-3 font-mono text-xs text-slate-200">
              {circuit.drawing}
            </pre>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}
