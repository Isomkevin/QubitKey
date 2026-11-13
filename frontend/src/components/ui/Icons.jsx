export function IconOverview(props) {
  return (
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" width="18" height="18" {...props}>
      <path
        d="M4 4h7v7H4V4Zm9 0h7v7h-7V4ZM4 13h7v7H4v-7Zm9 0h7v7h-7v-7Z"
        stroke="currentColor"
        strokeWidth="1.6"
      />
    </svg>
  );
}

export function IconLab(props) {
  return (
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" width="18" height="18" {...props}>
      <path
        d="M9 3v6l-4.5 9A2 2 0 0 0 6.3 21h11.4a2 2 0 0 0 1.8-3L15 9V3"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path d="M8 3h8" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
    </svg>
  );
}

export function IconObservatory(props) {
  return (
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" width="18" height="18" {...props}>
      <path
        d="M4 19V5m0 14h16M8 16V10m4 6V7m4 9v-4"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function IconAuth(props) {
  return (
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" width="18" height="18" {...props}>
      <rect
        x="5"
        y="10"
        width="14"
        height="10"
        rx="2"
        stroke="currentColor"
        strokeWidth="1.6"
      />
      <path
        d="M8 10V7a4 4 0 0 1 8 0v3"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinecap="round"
      />
    </svg>
  );
}

export function IconPqc(props) {
  return (
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" width="18" height="18" {...props}>
      <path
        d="M12 3 4 7v5c0 5 3.4 8.4 8 9 4.6-.6 8-4 8-9V7l-8-4Z"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinejoin="round"
      />
      <path d="M9 12h6M12 9v6" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
    </svg>
  );
}

export function IconAbout(props) {
  return (
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" width="18" height="18" {...props}>
      <circle cx="12" cy="12" r="8.2" stroke="currentColor" strokeWidth="1.6" />
      <path d="M12 11v5" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
      <circle cx="12" cy="8" r="0.9" fill="currentColor" />
    </svg>
  );
}

export function IconNotebook(props) {
  return (
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" width="18" height="18" {...props}>
      <path
        d="M7 4h10a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2Z"
        stroke="currentColor"
        strokeWidth="1.6"
      />
      <path d="M9 8h6M9 12h6M9 16h3" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
    </svg>
  );
}

export function IconExternal(props) {
  return (
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" width="14" height="14" {...props}>
      <path
        d="M14 5h5v5M19 5l-9 9M10 6H6a1 1 0 0 0-1 1v11a1 1 0 0 0 1 1h11a1 1 0 0 0 1-1v-4"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function IconMenu(props) {
  return (
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" width="20" height="20" {...props}>
      <path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
    </svg>
  );
}

export function IconClose(props) {
  return (
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" width="20" height="20" {...props}>
      <path d="M6 6l12 12M18 6 6 18" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
    </svg>
  );
}

export function IconStatusDot({ className = "text-ok", ...props }) {
  return (
    <svg viewBox="0 0 8 8" width="8" height="8" aria-hidden="true" className={className} {...props}>
      <circle cx="4" cy="4" r="3.5" fill="currentColor" />
    </svg>
  );
}
