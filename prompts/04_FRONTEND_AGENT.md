# Frontend Agent Prompt

Build the QubitKey web interface in `frontend/` only. Read the product and architecture docs first.

Stack: React + Vite, JavaScript preferred, Tailwind, Recharts. Use the agreed API client and schemas; do not invent mock metrics as if they were real. If API work is not ready, use clearly labelled fixtures behind a development-only flag.

Pages:
- Overview
- Quantum Lab
- Entropy Observatory
- Authenticator
- Experimental Post-Quantum Demo
- About / Methodology

Design: sophisticated quantum-security laboratory, deep navy, restrained blue/violet accents, excellent readability, clean charts, responsive and accessible. Avoid generic neon sci-fi clutter.

Must include:
- Circuit diagram from actual circuit data or an honest circuit rendering.
- Source provenance badges.
- Run parameters and loading/error/empty states.
- Side-by-side comparisons with sample sizes.
- Statistical caveats.
- TOTP enrollment QR display and reveal/hide manual key.
- No secrets in localStorage, logs or console.
- Keyboard navigation and meaningful labels.

Run the app, inspect it in a browser, fix console/network errors, and provide screenshots or a visual QA report. Do not claim a visual review if none was performed.
