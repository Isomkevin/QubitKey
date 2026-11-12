# QubitKey Demo Script (~8 minutes)

## Preconditions

- Backend: `cd backend && .venv\Scripts\activate && uvicorn app.main:app --reload --port 8000`
- Frontend: `cd frontend && npm install && npm run dev`
- Browser at `http://localhost:5173`
- No IBM credentials required for the core demo

## Script

1. **Overview (1 min)**  
   Show source availability and disclaimers. State: simulator ≠ physical quantum entropy; TOTP ≠ quantum-resistant.

2. **Quantum Lab (2 min)**  
   Run `qiskit_simulator`, 4 qubits, 256 shots, seed 7. Show circuit drawing, counts chart, provenance badge.

3. **Entropy Observatory (2 min)**  
   Compare simulator / PRNG / CSPRNG at equal sample size. Point at caveats: stats ≠ crypto proof.

4. **Authenticator (2 min)**  
   Enroll `demo@local`. Scan QR with an authenticator app (or reveal manual key). Verify OTP. Emphasize OS CSPRNG secret and no localStorage.

5. **Optional hardware / PQC (1 min)**  
   If IBM configured: show availability and that failures do not fake QPU. If PQC enabled: show ML-DSA is separate from QRNG/TOTP.

## Closing line

QubitKey is a scientifically honest educational lab connecting quantum measurement experiments to a practical authentication demo — without overclaiming.
