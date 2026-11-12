import { useState } from "react";
import { api } from "../api/client.js";
import { EmptyState, ErrorState, LoadingState } from "../components/StatusBlock.jsx";

export default function AuthenticatorPage() {
  const [accountLabel, setAccountLabel] = useState("demo@local");
  const [issuer, setIssuer] = useState("QubitKey");
  const [enrollment, setEnrollment] = useState(null);
  const [showSecret, setShowSecret] = useState(false);
  const [otp, setOtp] = useState("");
  const [verifyResult, setVerifyResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function onEnroll(event) {
    event.preventDefault();
    setLoading(true);
    setError(null);
    setVerifyResult(null);
    try {
      const data = await api.totpEnroll({
        account_label: accountLabel,
        issuer,
      });
      setEnrollment(data);
      setShowSecret(false);
    } catch (err) {
      setEnrollment(null);
      setError(err);
    } finally {
      setLoading(false);
    }
  }

  async function onVerify(event) {
    event.preventDefault();
    if (!enrollment) return;
    setLoading(true);
    setError(null);
    try {
      const data = await api.totpVerify({
        enrollment_id: enrollment.enrollment_id,
        otp,
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
        <h2 className="text-2xl font-semibold text-white">Authenticator demo</h2>
        <p className="mt-2 max-w-3xl text-sm text-slate-300">
          TOTP secrets are generated with the OS CSPRNG. This is not a quantum-resistant protocol,
          and secrets are not stored in browser localStorage.
        </p>
      </div>

      <form
        onSubmit={onEnroll}
        className="grid gap-4 rounded-md border border-line bg-panel/40 p-4 md:grid-cols-3"
      >
        <label className="text-sm text-slate-300">
          Account label
          <input
            className="mt-1 w-full rounded-md border border-line bg-ink px-2 py-2"
            value={accountLabel}
            onChange={(e) => setAccountLabel(e.target.value)}
            required
          />
        </label>
        <label className="text-sm text-slate-300">
          Issuer
          <input
            className="mt-1 w-full rounded-md border border-line bg-ink px-2 py-2"
            value={issuer}
            onChange={(e) => setIssuer(e.target.value)}
            required
          />
        </label>
        <div className="flex items-end">
          <button
            type="submit"
            className="rounded-md bg-accent px-4 py-2 text-sm font-medium text-white hover:bg-blue-500 disabled:opacity-60"
            disabled={loading}
          >
            Enroll
          </button>
        </div>
      </form>

      {loading ? <LoadingState /> : null}
      {error ? <ErrorState error={error} /> : null}
      {!enrollment && !loading ? (
        <EmptyState message="Enroll to receive a one-time QR and manual setup key." />
      ) : null}

      {enrollment ? (
        <div className="grid gap-4 lg:grid-cols-2">
          <div className="rounded-md border border-line bg-panel/40 p-4">
            <h3 className="text-sm font-medium text-white">Provisioning QR</h3>
            <img
              className="mt-3 max-w-xs rounded-md bg-white p-2"
              alt="TOTP enrollment QR code"
              src={`data:image/png;base64,${enrollment.qr_png_base64}`}
            />
            <button
              type="button"
              className="mt-3 text-sm text-accent underline"
              onClick={() => setShowSecret((v) => !v)}
            >
              {showSecret ? "Hide manual key" : "Reveal manual key"}
            </button>
            {showSecret ? (
              <p className="mt-2 break-all font-mono text-xs text-slate-200">
                {enrollment.secret_base32}
              </p>
            ) : null}
            <ul className="mt-4 list-disc space-y-1 pl-5 text-xs text-amber-100">
              {(enrollment.warnings || []).map((w) => (
                <li key={w}>{w}</li>
              ))}
            </ul>
          </div>

          <form
            onSubmit={onVerify}
            className="rounded-md border border-line bg-panel/40 p-4 space-y-3"
          >
            <h3 className="text-sm font-medium text-white">Verify OTP</h3>
            <label className="block text-sm text-slate-300">
              Current code
              <input
                className="mt-1 w-full rounded-md border border-line bg-ink px-2 py-2 font-mono"
                value={otp}
                onChange={(e) => setOtp(e.target.value)}
                inputMode="numeric"
                autoComplete="one-time-code"
                minLength={6}
                maxLength={8}
                required
              />
            </label>
            <button
              type="submit"
              className="rounded-md border border-line px-4 py-2 text-sm text-white hover:bg-ink"
              disabled={loading}
            >
              Verify
            </button>
            {verifyResult ? (
              <p
                className={
                  verifyResult.valid ? "text-sm text-emerald-300" : "text-sm text-rose-300"
                }
              >
                {verifyResult.valid ? "Valid code" : "Invalid code"}
              </p>
            ) : null}
          </form>
        </div>
      ) : null}
    </section>
  );
}
