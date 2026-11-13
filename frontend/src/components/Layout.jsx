import { useCallback, useEffect, useId, useRef, useState } from "react";
import { NavLink, Outlet, useLocation } from "react-router-dom";
import { api } from "../api/client.js";
import IconButton from "./ui/IconButton.jsx";
import {
  IconAbout,
  IconAuth,
  IconClose,
  IconLab,
  IconMenu,
  IconObservatory,
  IconOverview,
  IconPqc,
  IconStatusDot,
} from "./ui/Icons.jsx";

const links = [
  { to: "/", label: "Overview", end: true, icon: IconOverview },
  { to: "/lab", label: "Quantum Lab", icon: IconLab },
  { to: "/observatory", label: "Entropy Observatory", icon: IconObservatory },
  { to: "/authenticator", label: "Authenticator", icon: IconAuth },
  { to: "/pqc", label: "Post-Quantum", icon: IconPqc },
  { to: "/about", label: "About", icon: IconAbout },
];

function NavItems({ onNavigate }) {
  return (
    <nav className="flex flex-col gap-1" aria-label="Primary">
      {links.map((link) => {
        const Icon = link.icon;
        return (
          <NavLink
            key={link.to}
            to={link.to}
            end={link.end}
            onClick={onNavigate}
            className={({ isActive }) =>
              [
                "group relative flex min-h-[44px] items-center gap-3 rounded-md px-3 py-2 text-sm transition duration-fast",
                isActive
                  ? "bg-cyan/10 text-white"
                  : "text-slate-400 hover:bg-panel-elevated hover:text-slate-100",
              ].join(" ")
            }
          >
            {({ isActive }) => (
              <>
                <span
                  className={[
                    "absolute left-0 top-1/2 h-5 w-0.5 -translate-y-1/2 rounded-full transition",
                    isActive ? "bg-cyan" : "bg-transparent",
                  ].join(" ")}
                  aria-hidden="true"
                />
                <Icon className={isActive ? "text-cyan" : "text-slate-500 group-hover:text-slate-300"} />
                <span>{link.label}</span>
              </>
            )}
          </NavLink>
        );
      })}
    </nav>
  );
}

function ApiStatus({ status }) {
  const tone =
    status === "ok" ? "text-ok" : status === "waking" ? "text-warn" : "text-danger";
  const label =
    status === "ok"
      ? "API reachable"
      : status === "waking"
        ? "API waking…"
        : status === "error"
          ? "API unreachable"
          : "Checking API…";

  return (
    <div className="flex items-center gap-2 rounded-md border border-line/80 bg-ink/50 px-3 py-2.5">
      <IconStatusDot className={tone} />
      <div className="min-w-0">
        <p className="text-xs font-medium text-slate-200">{label}</p>
        <p className="truncate font-mono text-[10px] text-slate-500">/api/health</p>
      </div>
    </div>
  );
}

function BrandBlock({ compact = false }) {
  return (
    <div className={compact ? "" : "px-1"}>
      <p className="text-lg font-semibold tracking-tight text-white">QubitKey</p>
      {!compact ? (
        <p className="mt-1 font-mono text-[10px] leading-relaxed tracking-wide text-slate-500">
          Quantum Entropy. Stronger Digital Identity.
        </p>
      ) : null}
    </div>
  );
}

export default function Layout() {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [healthStatus, setHealthStatus] = useState("checking");
  const location = useLocation();
  const drawerId = useId();
  const closeBtnRef = useRef(null);

  const checkHealth = useCallback(async () => {
    setHealthStatus((prev) => (prev === "ok" ? "ok" : "checking"));
    try {
      await api.health();
      setHealthStatus("ok");
    } catch {
      // Render free tier may cold-start; surface waking then retry once
      setHealthStatus("waking");
      try {
        await new Promise((r) => setTimeout(r, 2500));
        await api.health();
        setHealthStatus("ok");
      } catch {
        setHealthStatus("error");
      }
    }
  }, []);

  useEffect(() => {
    checkHealth();
    const id = setInterval(checkHealth, 60000);
    return () => clearInterval(id);
  }, [checkHealth]);

  useEffect(() => {
    setDrawerOpen(false);
  }, [location.pathname]);

  useEffect(() => {
    if (!drawerOpen) return undefined;
    const onKey = (e) => {
      if (e.key === "Escape") setDrawerOpen(false);
    };
    document.addEventListener("keydown", onKey);
    document.body.style.overflow = "hidden";
    closeBtnRef.current?.focus();
    return () => {
      document.removeEventListener("keydown", onKey);
      document.body.style.overflow = "";
    };
  }, [drawerOpen]);

  const sidebarInner = (
    <>
      <div className="flex items-start justify-between gap-2">
        <BrandBlock />
        <div className="md:hidden">
          <IconButton
            ref={closeBtnRef}
            label="Close navigation"
            onClick={() => setDrawerOpen(false)}
          >
            <IconClose />
          </IconButton>
        </div>
      </div>

      <div className="mt-8 flex-1">
        <NavItems onNavigate={() => setDrawerOpen(false)} />
      </div>

      <div className="mt-6 space-y-3">
        <ApiStatus status={healthStatus} />
        <p className="text-[11px] leading-relaxed text-slate-500">
          Educational prototype — simulator output is not physical quantum entropy. TOTP is not
          quantum-resistant.
        </p>
      </div>
    </>
  );

  return (
    <div className="min-h-screen md:flex">
      {/* Desktop sidebar */}
      <aside className="sticky top-0 hidden h-screen w-60 shrink-0 flex-col border-r border-line/80 bg-ink/90 px-4 py-5 backdrop-blur-md md:flex lg:w-64">
        {sidebarInner}
      </aside>

      {/* Mobile drawer */}
      {drawerOpen ? (
        <div className="fixed inset-0 z-40 md:hidden" role="presentation">
          <button
            type="button"
            className="absolute inset-0 bg-black/60 animate-fade-in"
            aria-label="Close navigation overlay"
            onClick={() => setDrawerOpen(false)}
          />
          <aside
            id={drawerId}
            className="absolute inset-y-0 left-0 flex w-[min(18rem,88vw)] flex-col border-r border-line bg-ink px-4 py-5 shadow-panel animate-slide-in-left"
            role="dialog"
            aria-modal="true"
            aria-label="Navigation"
          >
            {sidebarInner}
          </aside>
        </div>
      ) : null}

      <div className="flex min-w-0 flex-1 flex-col">
        <header className="sticky top-0 z-30 flex items-center justify-between gap-3 border-b border-line/80 bg-ink/85 px-4 py-3 backdrop-blur-md md:hidden">
          <BrandBlock compact />
          <IconButton
            label="Open navigation"
            aria-expanded={drawerOpen}
            aria-controls={drawerId}
            onClick={() => setDrawerOpen(true)}
          >
            <IconMenu />
          </IconButton>
        </header>

        <main className="mx-auto w-full max-w-content flex-1 px-4 py-6 sm:px-6 sm:py-8 lg:px-8">
          <Outlet />
        </main>

        <footer className="border-t border-line/60 px-4 py-4 text-center text-[11px] text-slate-500 md:hidden">
          Educational prototype — simulator output is not physical quantum entropy. TOTP is not
          quantum-resistant.
        </footer>
      </div>
    </div>
  );
}
