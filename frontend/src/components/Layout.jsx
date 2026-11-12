import { NavLink, Outlet } from "react-router-dom";

const links = [
  { to: "/", label: "Overview", end: true },
  { to: "/lab", label: "Quantum Lab" },
  { to: "/observatory", label: "Entropy Observatory" },
  { to: "/authenticator", label: "Authenticator" },
  { to: "/pqc", label: "Post-Quantum" },
  { to: "/about", label: "About" },
];

export default function Layout() {
  return (
    <div className="min-h-screen">
      <header className="border-b border-line/80 bg-ink/80 backdrop-blur">
        <div className="mx-auto flex max-w-6xl flex-col gap-4 px-4 py-5 md:flex-row md:items-center md:justify-between">
          <div className="animate-fade-up">
            <p className="font-mono text-xs uppercase tracking-[0.24em] text-accent">QubitKey</p>
            <h1 className="mt-1 text-2xl font-semibold tracking-tight text-white md:text-3xl">
              Quantum Entropy Laboratory
            </h1>
          </div>
          <nav className="flex flex-wrap gap-2" aria-label="Primary">
            {links.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                end={link.end}
                className={({ isActive }) =>
                  [
                    "rounded-md px-3 py-1.5 text-sm transition",
                    isActive
                      ? "bg-accent/20 text-white ring-1 ring-accent/50"
                      : "text-slate-300 hover:bg-panel hover:text-white",
                  ].join(" ")
                }
              >
                {link.label}
              </NavLink>
            ))}
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-4 py-8">
        <Outlet />
      </main>
      <footer className="border-t border-line/60 px-4 py-6 text-center text-xs text-slate-400">
        Educational prototype — simulator output is not physical quantum entropy. TOTP is not
        quantum-resistant.
      </footer>
    </div>
  );
}
