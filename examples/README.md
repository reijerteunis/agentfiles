# Examples

Made-up inputs for the demos in the README. Each one contains a planted problem that a guarantee has to catch. `just demo` runs them all and shows the output; `just validate` and CI run the same checks and fail if any of them stops catching its problem.

| Example | Planted problem | Caught by |
|---|---|---|
| `cv/tailored-cv.md` | A job title upgraded, a number inflated from 7 to 12, a bullet with no source | `check_claims.py` from the `cv-tailor` skill |
| `landing/page.md` | "The fastest checkout … trusted by 200 brands" with no proof | `proof_check.py` from the `messaging` skill |
