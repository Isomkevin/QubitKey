# QubitKey Product & Technical Specification

## Product goal
A local-first, open-source quantum entropy learning platform with a practical TOTP authenticator demonstration.

## MVP scope
1. Qiskit Hadamard-based QRNG on local simulator.
2. Quantum circuit visualization and measurement counts.
3. Fair comparison against Python `random` and `secrets`.
4. Statistical observatory with honest caveats.
5. TOTP enrollment/verification using OS CSPRNG-generated secrets.
6. Runnable Jupyter notebook.
7. Responsive React dashboard and FastAPI backend.
8. Reproducible setup, tests, CI and documentation.

## Out of scope for MVP
- Production QRNG certification.
- Production entropy service.
- Cloud user accounts or multi-tenant storage.
- Custom cryptographic primitives.
- Claiming TOTP is post-quantum.
- Feeding simulator output directly into cryptographic key generation.
- Blockchain identity or tokenization.

## Key user stories
- As a beginner, I can see a Hadamard circuit and understand why measurement yields a bit.
- As a learner, I can run many shots and inspect counts.
- As an investigator, I can compare simulator, PRNG and CSPRNG outputs using equal sample sizes.
- As a user, I can enroll a TOTP account and verify an OTP.
- As a judge, I can run the demo without IBM credentials.
- As a reviewer, I can verify source provenance and reproduce reported statistics.

## Acceptance
- Clean install and one-command startup documented.
- Notebook executes top-to-bottom without hardware credentials.
- Simulator is never represented as physical quantum entropy.
- TOTP uses OS CSPRNG and a maintained RFC 6238 library.
- No secrets are logged or stored in browser localStorage.
- Statistical tests have documented limitations.
- All core paths have tests.
- Eight-slide presentation uses real experimental results or clearly marked placeholders.
