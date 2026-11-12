import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client.js";
import { ErrorState, LoadingState } from "../components/StatusBlock.jsx";

export default function OverviewPage() {
  const [config, setConfig] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const data = await api.config();
        if (!cancelled) setConfig(data);
      } catch (err) {
        if (!cancelled) setError(err);
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <section className="animate-fade-up space-y-6">
      <div className="max-w-3xl">
        <h2 className="text-3xl font-semibold text-white">Explore quantum measurement randomness</h2>
        <p className="mt-3 text-slate-300">
          Run Hadamard QRNG experiments, compare educational and classical sources, and try a local
          TOTP demo — with explicit provenance on every result.
        </p>
        <div className="mt-5 flex flex-wrap gap-3">
          <Link
            to="/lab"
            className="rounded-md bg-accent px-4 py-2 text-sm font-medium text-white hover:bg-blue-500"
          >
            Open Quantum Lab
          </Link>
          <Link
            to="/observatory"
            className="rounded-md border border-line px-4 py-2 text-sm text-slate-200 hover:bg-panel"
          >
            Entropy Observatory
          </Link>
        </div>
      </div>

      {loading ? <LoadingState label="Loading backend configuration…" /> : null}
      {error ? <ErrorState error={error} /> : null}

      {config ? (
        <div className="grid gap-4 md:grid-cols-2">
          <div className="rounded-md border border-line bg-panel/50 p-4">
            <h3 className="text-sm font-medium text-white">Source availability</h3>
            <ul className="mt-3 space-y-2 text-sm text-slate-300">
              {Object.entries(config.sources || {}).map(([key, value]) => (
                <li key={key} className="flex items-start justify-between gap-3">
                  <span className="font-mono text-xs">{key}</span>
                  <span className={value.available ? "text-emerald-300" : "text-amber-300"}>
                    {value.available ? "available" : value.reason || "unavailable"}
                  </span>
                </li>
              ))}
            </ul>
          </div>
          <div className="rounded-md border border-line bg-panel/50 p-4">
            <h3 className="text-sm font-medium text-white">Scientific disclaimers</h3>
            <ul className="mt-3 list-disc space-y-2 pl-5 text-sm text-slate-300">
              {(config.disclaimers || []).map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
        </div>
      ) : null}
    </section>
  );
}
