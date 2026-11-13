import { useState } from "react";
import { api } from "../api/client.js";
import { EmptyState, ErrorState, LoadingState } from "../components/StatusBlock.jsx";
import Badge from "../components/ui/Badge.jsx";
import Button from "../components/ui/Button.jsx";
import Field from "../components/ui/Field.jsx";
import PageHeader from "../components/ui/PageHeader.jsx";
import Panel from "../components/ui/Panel.jsx";

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
    <section className="qk-page">
      <PageHeader
        eyebrow="Identity"
        title="Authenticator"
        description="TOTP secrets are generated with the OS CSPRNG. This is not a quantum-resistant protocol, and secrets are not stored in browser localStorage."
        actions={
          enrollment ? <Badge tone="ok">Enrolled</Badge> : <Badge tone="mute">Not enrolled</Badge>
        }
      />

      <div className="qk-callout-info">
        <p className="text-sm text-slate-200">
          Educational demonstration only. TOTP is{" "}
          <strong className="font-medium text-white">not quantum-resistant</strong>. Secrets remain
          in memory for this session and are never written to localStorage.
        </p>
      </div>

      <Panel as="form" onSubmit={onEnroll} elevated>
        <p className="qk-label">Step 1 · Enroll</p>
        <div className="mt-4 grid gap-4 md:grid-cols-3">
          <Field label="Account label" htmlFor="totp-account">
            <input
              id="totp-account"
              className="qk-input"
              value={accountLabel}
              onChange={(e) => setAccountLabel(e.target.value)}
              required
            />
          </Field>
          <Field label="Issuer" htmlFor="totp-issuer">
            <input
              id="totp-issuer"
              className="qk-input"
              value={issuer}
              onChange={(e) => setIssuer(e.target.value)}
              required
            />
          </Field>
          <div className="flex items-end">
            <Button type="submit" className="w-full md:w-auto" disabled={loading}>
              Enroll
            </Button>
          </div>
        </div>
      </Panel>

      {loading && !enrollment ? <LoadingState label="Enrolling…" /> : null}
      {error ? <ErrorState error={error} /> : null}
      {!enrollment && !loading ? (
        <EmptyState
          title="Awaiting enrollment"
          message="Enroll to receive a one-time QR and manual setup key."
        />
      ) : null}

      {enrollment ? (
        <div className="animate-fade-up grid gap-4 lg:grid-cols-2">
          <Panel elevated className="space-y-4">
            <div className="flex items-center justify-between gap-2">
              <h2 className="text-sm font-medium text-white">Step 2 · Provision</h2>
              <Badge tone="cyan">QR</Badge>
            </div>
            <div className="inline-block rounded-lg bg-white p-3 shadow-panel">
              <img
                className="max-w-[220px]"
                alt="TOTP enrollment QR code"
                src={`data:image/png;base64,${enrollment.qr_png_base64}`}
              />
            </div>
            <div>
              <Button
                type="button"
                variant="secondary"
                size="sm"
                onClick={() => setShowSecret((v) => !v)}
              >
                {showSecret ? "Hide manual key" : "Reveal manual key"}
              </Button>
              {showSecret ? (
                <p className="mt-3 break-all rounded-md border border-line bg-ink px-3 py-2 font-mono text-xs text-slate-200">
                  {enrollment.secret_base32}
                </p>
              ) : (
                <p className="mt-2 text-xs text-slate-500">
                  Manual key is hidden until you choose to reveal it.
                </p>
              )}
            </div>
            {(enrollment.warnings || []).length ? (
              <ul className="list-disc space-y-1 pl-5 text-xs text-amber-100">
                {enrollment.warnings.map((w) => (
                  <li key={w}>{w}</li>
                ))}
              </ul>
            ) : null}
            <p className="qk-mono-meta text-slate-500">
              enrollment_id · {enrollment.enrollment_id}
            </p>
          </Panel>

          <Panel as="form" onSubmit={onVerify} className="space-y-4">
            <h2 className="text-sm font-medium text-white">Step 3 · Verify</h2>
            <Field
              label="Current code"
              htmlFor="totp-otp"
              hint="Enter the 6-digit code from your authenticator app."
            >
              <input
                id="totp-otp"
                className="qk-input font-mono text-2xl tracking-[0.35em] text-center"
                value={otp}
                onChange={(e) => setOtp(e.target.value.replace(/\D/g, "").slice(0, 8))}
                inputMode="numeric"
                autoComplete="one-time-code"
                minLength={6}
                maxLength={8}
                placeholder="••••••"
                required
              />
            </Field>
            <Button type="submit" variant="secondary" disabled={loading}>
              {loading ? "Verifying…" : "Verify OTP"}
            </Button>
            {verifyResult ? (
              <div
                className={
                  verifyResult.valid
                    ? "rounded-md border border-emerald-500/30 bg-emerald-950/30 px-3 py-2 text-sm text-emerald-200"
                    : "rounded-md border border-rose-500/30 bg-rose-950/30 px-3 py-2 text-sm text-rose-200"
                }
                role="status"
              >
                {verifyResult.valid ? "Valid code" : "Invalid code"}
              </div>
            ) : null}
          </Panel>
        </div>
      ) : null}
    </section>
  );
}
