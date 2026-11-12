import { useState } from "react";
import { api } from "../api/client.js";
import { EmptyState, ErrorState, LoadingState } from "../components/StatusBlock.jsx";

export default function PqcPage() {
  const [session, setSession] = useState(null);
  const [challenge, setChallenge] = useState(null);
  const [verifyResult, setVerifyResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

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

  return (
    <section className="animate-fade-up space-y-6">
      <div>
        <h2 className="text-2xl font-semibold text-white">Post-Quantum Demo (experimental)</h2>
        <p className="mt-2 max-w-3xl text-sm text-slate-300">
          Isolated ML-DSA-65 challenge/signature flow. This is separate from QRNG and TOTP. Enable
          with <span className="font-mono">QUBITKEY_ENABLE_PQC=true</span> on the backend.
        </p>
      </div>

      <div className="flex flex-wrap gap-3">
        <button
          type="button"
          onClick={onKeygen}
          className="rounded-md bg-accent px-4 py-2 text-sm text-white hover:bg-blue-500"
          disabled={loading}
        >
          Generate ML-DSA key pair
        </button>
        <button
          type="button"
          onClick={onChallenge}
          className="rounded-md border border-line px-4 py-2 text-sm text-slate-100 hover:bg-panel"
          disabled={loading || !session}
        >
          Fresh challenge
        </button>
        <button
          type="button"
          onClick={onVerifyDemo}
          className="rounded-md border border-line px-4 py-2 text-sm text-slate-100 hover:bg-panel"
          disabled={loading || !session || !challenge}
        >
          Server demo sign + verify
        </button>
      </div>

      {loading ? <LoadingState /> : null}
      {error ? <ErrorState error={error} /> : null}
      {!session && !loading ? (
        <EmptyState message="Generate a key pair to begin the experimental demo." />
      ) : null}

      {session ? (
        <div className="space-y-3 rounded-md border border-line bg-panel/40 p-4 text-sm text-slate-300">
          <p>
            Algorithm: <span className="font-mono">{session.algorithm}</span>
          </p>
          <p>
            Fingerprint: <span className="font-mono">{session.public_key_fingerprint}</span>
          </p>
          {challenge ? (
            <p className="break-all">
              Challenge: <span className="font-mono text-xs">{challenge.challenge_b64}</span>
            </p>
          ) : null}
          {verifyResult ? (
            <p className={verifyResult.valid ? "text-emerald-300" : "text-rose-300"}>
              Verification: {verifyResult.valid ? "valid" : verifyResult.detail || "invalid"}
            </p>
          ) : null}
          <ul className="list-disc pl-5 text-xs text-amber-100">
            {(session.warnings || []).map((w) => (
              <li key={w}>{w}</li>
            ))}
          </ul>
        </div>
      ) : null}
    </section>
  );
}
