import { useEffect, useState } from "react";
import { api } from "../api/client.js";
import { EmptyState, ErrorState, LoadingState } from "../components/StatusBlock.jsx";
import Badge from "../components/ui/Badge.jsx";
import Button from "../components/ui/Button.jsx";
import Metric from "../components/ui/Metric.jsx";
import PageHeader from "../components/ui/PageHeader.jsx";
import Panel from "../components/ui/Panel.jsx";

export default function PqcPage() {
  const [pqcEnabled, setPqcEnabled] = useState(null);
  const [session, setSession] = useState(null);
  const [challenge, setChallenge] = useState(null);
  const [verifyResult, setVerifyResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [configLoading, setConfigLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const cfg = await api.config();
        if (!cancelled) setPqcEnabled(Boolean(cfg?.features?.pqc));
      } catch {
        // If config fails, leave null and allow attempt (backend will error honestly)
        if (!cancelled) setPqcEnabled(null);
      } finally {
        if (!cancelled) setConfigLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  async function onKeygen() {
    setLoading(true);
    setError(null);
    setChallenge(null);
    setVerifyResult(null);
    try {
      const data = await api.pqcKeygen();
      setSession(data);
    } catch (err) {
      setSession(null);
      setError(err);
    } finally {
      setLoading(false);
    }
  }

  async function onChallenge() {
    if (!session) return;
    setLoading(true);
    setError(null);
    try {
      const data = await api.pqcChallenge(session.session_id);
      setChallenge(data);
      setVerifyResult(null);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }

  async function onVerifyDemo() {
    if (!session) return;
    setLoading(true);
    setError(null);
    try {
      const data = await api.pqcVerify({
        session_id: session.session_id,
        signature_b64: "AA==",
        use_server_demo_sign: true,
      });
      setVerifyResult(data);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }

  const disabled = pqcEnabled === false;

  return (
    <section className="qk-page">
      <PageHeader
        eyebrow="Experimental"
        title="Post-Quantum Cryptography"
        description="Isolated ML-DSA-65 challenge/signature flow. ML-DSA is a post-quantum signature scheme — separate from QRNG and TOTP."
        actions={
          configLoading ? (
            <Badge tone="mute">Checking…</Badge>
          ) : disabled ? (
            <Badge tone="warn">Feature off</Badge>
          ) : (
            <Badge tone="violet">Experimental</Badge>
          )
        }
      />

      <div className="qk-callout-info">
        <p className="text-sm">
          QRNG generates randomness; PQC provides quantum-resistant signatures. They are not the
          same thing. This demo does not claim production security.
        </p>
      </div>

      {configLoading ? <LoadingState label="Checking feature flags…" /> : null}

      {disabled ? (
        <EmptyState
          title="PQC endpoints are disabled"
          message="Enable with QUBITKEY_ENABLE_PQC=true on the backend, then reload this page."
        />
      ) : (
        <>
          <Panel elevated>
            <p className="qk-label">Pipeline</p>
            <ol className="mt-3 flex flex-col gap-2 text-sm text-slate-400 sm:flex-row sm:items-center sm:gap-3">
              <li className={session ? "text-cyan" : ""}>1. Keygen</li>
              <li className="hidden text-slate-600 sm:inline" aria-hidden="true">
                →
              </li>
              <li className={challenge ? "text-cyan" : ""}>2. Challenge</li>
              <li className="hidden text-slate-600 sm:inline" aria-hidden="true">
                →
              </li>
              <li className={verifyResult ? "text-cyan" : ""}>3. Sign + verify</li>
            </ol>
            <div className="mt-5 flex flex-wrap gap-3">
              <Button type="button" onClick={onKeygen} disabled={loading}>
                Generate ML-DSA key pair
              </Button>
              <Button
                type="button"
                variant="secondary"
                onClick={onChallenge}
                disabled={loading || !session}
              >
                Fresh challenge
              </Button>
              <Button
                type="button"
                variant="secondary"
                onClick={onVerifyDemo}
                disabled={loading || !session || !challenge}
              >
                Server demo sign + verify
              </Button>
            </div>
          </Panel>

          {loading ? <LoadingState /> : null}
          {error ? <ErrorState error={error} /> : null}
          {!session && !loading ? (
            <EmptyState
              title="No session yet"
              message="Generate a key pair to begin the experimental demo."
            />
          ) : null}

          {session ? (
            <Panel className="animate-fade-up space-y-5">
              <dl className="grid gap-5 sm:grid-cols-2">
                <Metric label="Algorithm" value={session.algorithm || "—"} />
                <div>
                  <dt className="qk-label">Session</dt>
                  <dd className="mt-1 qk-mono-meta">{session.session_id}</dd>
                </div>
              </dl>
              <div>
                <p className="qk-label">Public key fingerprint</p>
                <p className="mt-1 qk-mono-meta">{session.public_key_fingerprint}</p>
              </div>
              {challenge ? (
                <div>
                  <p className="qk-label">Challenge (base64)</p>
                  <p className="mt-1 qk-mono-meta">{challenge.challenge_b64}</p>
                </div>
              ) : null}
              {verifyResult ? (
                <div
                  className={
                    verifyResult.valid
                      ? "rounded-md border border-emerald-500/30 bg-emerald-950/30 px-3 py-2 text-sm text-emerald-200"
                      : "rounded-md border border-rose-500/30 bg-rose-950/30 px-3 py-2 text-sm text-rose-200"
                  }
                  role="status"
                >
                  Verification: {verifyResult.valid ? "valid" : verifyResult.detail || "invalid"}
                </div>
              ) : null}
              {(session.warnings || []).length ? (
                <ul className="list-disc pl-5 text-xs text-amber-100">
                  {session.warnings.map((w) => (
                    <li key={w}>{w}</li>
                  ))}
                </ul>
              ) : null}
            </Panel>
          ) : null}
        </>
      )}
    </section>
  );
}
