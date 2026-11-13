import PageHeader from "../components/ui/PageHeader.jsx";
import Panel from "../components/ui/Panel.jsx";

const CAVEATS = [
  "Qiskit Aer output is classical simulation — not physical quantum entropy.",
  "IBM QPU mode requires credentials and never silently falls back to the simulator.",
  "TOTP secrets come from the OS CSPRNG; TOTP is not quantum-resistant.",
  "Statistical diagnostics are educational and do not certify cryptographic security.",
  "ML-DSA (optional) is a post-quantum signature demo, separate from QRNG and TOTP.",
];

const DOCS = [
  {
    path: "docs/EXPERIMENT_METHODOLOGY.md",
    href: "https://github.com/Isomkevin/QubitKey/blob/main/docs/EXPERIMENT_METHODOLOGY.md",
    blurb: "How experiments are constructed and interpreted.",
  },
  {
    path: "docs/THREAT_MODEL.md",
    href: "https://github.com/Isomkevin/QubitKey/blob/main/docs/THREAT_MODEL.md",
    blurb: "Security boundaries and what this prototype does not claim.",
  },
  {
    path: "docs/INTEGRATION_CONTRACTS.md",
    href: "https://github.com/Isomkevin/QubitKey/blob/main/docs/INTEGRATION_CONTRACTS.md",
    blurb: "API contracts, provenance statements, and client rules.",
  },
];

export default function AboutPage() {
  return (
    <section className="qk-page max-w-3xl">
      <PageHeader
        eyebrow="Methodology"
        title="About & methodology"
        description="QubitKey is an educational platform for exploring Hadamard-based quantum random number generation with Qiskit, comparing classical baselines, and demonstrating a standards-based TOTP authenticator flow."
      />

      <Panel elevated>
        <h2 className="text-sm font-medium text-white">Scientific honesty</h2>
        <ul className="mt-4 space-y-3">
          {CAVEATS.map((item) => (
            <li
              key={item}
              className="flex gap-3 text-sm leading-relaxed text-slate-300 before:mt-2 before:h-1.5 before:w-1.5 before:shrink-0 before:rounded-full before:bg-cyan before:content-['']"
            >
              {item}
            </li>
          ))}
        </ul>
      </Panel>

      <div className="qk-callout-warn">
        <p className="text-sm font-medium text-amber-100">Not a certification product</p>
        <p className="mt-1.5 text-sm text-amber-50/90">
          Passing statistical tests does not prove cryptographic security or entropy certification.
          Hardware results require real IBM backend execution and verifiable job metadata.
        </p>
      </div>

      <div>
        <h2 className="text-sm font-medium text-white">Documentation</h2>
        <ul className="mt-3 space-y-2">
          {DOCS.map((doc) => (
            <li key={doc.path}>
              <a
                href={doc.href}
                target="_blank"
                rel="noreferrer"
                className="qk-panel flex flex-col gap-1 px-4 py-3 transition hover:border-cyan/35"
              >
                <span className="font-mono text-xs text-cyan">{doc.path}</span>
                <span className="text-sm text-slate-400">{doc.blurb}</span>
              </a>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
