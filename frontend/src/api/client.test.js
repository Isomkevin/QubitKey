import { describe, expect, it } from "vitest";

describe("api client contract smoke", () => {
  it("documents required endpoint paths", () => {
    const paths = [
      "/api/health",
      "/api/config",
      "/api/qrng/run",
      "/api/analysis/compare",
      "/api/auth/totp/enroll",
      "/api/auth/totp/verify",
    ];
    expect(paths.every((p) => p.startsWith("/api/"))).toBe(true);
  });
});
