export default function AboutPage() {
  return (
    <section className="animate-fade-up prose prose-invert max-w-3xl space-y-4 text-slate-300">
      <h2 className="text-2xl font-semibold text-white">About & methodology</h2>
      <p>
        QubitKey is an educational platform for exploring Hadamard-based quantum random number
        generation with Qiskit, comparing classical baselines, and demonstrating a standards-based
        TOTP authenticator flow.
      </p>
      <ul className="list-disc space-y-2 pl-5">
        <li>Qiskit Aer output is classical simulation — not physical quantum entropy.</li>
        <li>IBM QPU mode requires credentials and never silently falls back to the simulator.</li>
        <li>TOTP secrets come from the OS CSPRNG; TOTP is not quantum-resistant.</li>
        <li>Statistical diagnostics are educational and do not certify cryptographic security.</li>
        <li>ML-DSA (optional) is a post-quantum signature demo, separate from QRNG and TOTP.</li>
      </ul>
      <p>
        See <span className="font-mono">docs/EXPERIMENT_METHODOLOGY.md</span>,{" "}
        <span className="font-mono">docs/THREAT_MODEL.md</span>, and{" "}
        <span className="font-mono">docs/INTEGRATION_CONTRACTS.md</span> for details.
      </p>
    </section>
  );
}
