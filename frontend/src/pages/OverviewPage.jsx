import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client.js";
import { ErrorState, LoadingState } from "../components/StatusBlock.jsx";
import Badge from "../components/ui/Badge.jsx";
import { buttonClassName } from "../components/ui/Button.jsx";
import Panel from "../components/ui/Panel.jsx";

function SourceRow({ name, info }) {
  const available = Boolean(info?.available);
  return (
    <li className="flex items-start justify-between gap-4 border-b border-line/60 py-3 last:border-0">
      <div className="min-w-0">
        <p className="font-mono text-xs text-slate-200">{name}</p>
        {!available && info?.reason ? (
          <p className="mt-1 text-xs text-slate-500">{info.reason}</p>
        ) : null}
      </div>
      <Badge tone={available ? "ok" : "warn"}>{available ? "available" : "unavailable"}</Badge>
    </li>
  );
}

export default function OverviewPage() {
  const [config, setConfig] = useState(null);
  const [health, setHealth] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const [cfg, hp] = await Promise.allSettled([api.config(), api.health()]);
        if (cancelled) return;
        if (cfg.status === "fulfilled") setConfig(cfg.value);
        else throw cfg.reason;
        if (hp.status === "fulfilled") setHealth(hp.value);
        else setHealth({ status: "unreachable" });
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

  const features = config?.features || {};
  const apiOk = health && health.status !== "unreachable";

  return (
    <section className="qk-page">
      {/* Hero — brand-forward */}
      <div className="relative overflow-hidden rounded-xl border border-line bg-panel/70 px-5 py-8 shadow-panel sm:px-8 sm:py-10">
        <div
          className="pointer-events-none absolute inset-0 opacity-60"
          style={{
            background:
              "radial-gradient(600px 280px at 0% 0%, rgba(34,211,238,0.12), transparent 55%)",
          }}
          aria-hidden="true"
        />
        <div className="relative max-w-2xl">
          <p className="font-mono text-[11px] uppercase tracking-[0.24em] text-cyan">QubitKey</p>
          <h1 className="mt-3 text-3xl font-semibold tracking-tight text-white sm:text-4xl">
            Quantum Entropy.
            <span className="block text-slate-300">Stronger Digital Identity.</span>
          </h1>
          <p className="mt-4 max-w-xl text-sm leading-relaxed text-slate-400 sm:text-[15px]">
            An open-source quantum entropy laboratory — run Hadamard QRNG experiments, compare
            educational and classical sources, and explore a standards-based TOTP demo with explicit
            provenance on every result.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Link to="/lab" className={buttonClassName()}>
              Open Quantum Lab
            </Link>
            <Link to="/observatory" className={buttonClassName({ variant: "secondary" })}>
              Entropy Observatory
            </Link>
          </div>
        </div>
      </div>

      {loading ? <LoadingState label="Loading laboratory status…" /> : null}
      {error ? <ErrorState error={error} /> : null}

      {config ? (
        <>
          {/* Status strip — unequal visual weight */}
          <div className="grid gap-4 lg:grid-cols-12">
            <Panel className="lg:col-span-7" elevated>
              <div className="flex flex-wrap items-center justify-between gap-3">
                <div>
                  <p className="qk-label">Laboratory status</p>
                  <p className="mt-1 text-sm text-slate-200">
                    Backend configuration from{" "}
                    <span className="font-mono text-xs text-cyan">/api/config</span>
                  </p>
                </div>
                <Badge tone={apiOk ? "ok" : "warn"}>
                  {apiOk ? "API reachable" : "API waking or unreachable"}
                </Badge>
              </div>
              <ul className="mt-4">
                {Object.entries(config.sources || {}).map(([key, value]) => (
                  <SourceRow key={key} name={key} info={value} />
                ))}
              </ul>
            </Panel>

            <div className="flex flex-col gap-4 lg:col-span-5">
              <Panel>
                <p className="qk-label">Features</p>
                <dl className="mt-3 space-y-3">
                  {[
                    ["Analysis", features.analysis],
                    ["TOTP", features.totp],
                    ["PQC (experimental)", features.pqc],
                  ].map(([label, on]) => (
                    <div key={label} className="flex items-center justify-between gap-3">
                      <dt className="text-sm text-slate-300">{label}</dt>
                      <dd>
                        <Badge tone={on ? "cyan" : "mute"}>{on ? "enabled" : "disabled"}</Badge>
                      </dd>
                    </div>
                  ))}
                </dl>
              </Panel>

              <Panel className="flex-1">
                <p className="qk-label">Quick actions</p>
                <div className="mt-3 flex flex-col gap-2">
                  <Link
                    to="/lab"
                    className="rounded-md border border-line px-3 py-2.5 text-sm text-slate-200 transition hover:border-cyan/40 hover:bg-ink"
                  >
                    Run a Hadamard experiment →
                  </Link>
                  <Link
                    to="/observatory"
                    className="rounded-md border border-line px-3 py-2.5 text-sm text-slate-200 transition hover:border-cyan/40 hover:bg-ink"
                  >
                    Compare randomness sources →
                  </Link>
                  <Link
                    to="/authenticator"
                    className="rounded-md border border-line px-3 py-2.5 text-sm text-slate-200 transition hover:border-cyan/40 hover:bg-ink"
                  >
                    Enroll TOTP authenticator →
                  </Link>
                </div>
              </Panel>
            </div>
          </div>

          {(config.disclaimers || []).length ? (
            <div className="qk-callout-warn">
              <p className="qk-label !text-amber-200/80">Scientific disclaimers</p>
              <ul className="mt-2 list-disc space-y-1.5 pl-5 text-sm text-amber-50/90">
                {config.disclaimers.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
              {!apiOk ? (
                <p className="mt-3 text-xs text-amber-200/70">
                  If the API is slow to respond, the Render free tier may be cold-starting (often
                  30–60 seconds).
                </p>
              ) : null}
            </div>
          ) : null}
        </>
      ) : null}
    </section>
  );
}
