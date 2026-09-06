## Context

The repository contains only the initial project structure, so no API contract or backend implementation exists. See proposal.md for motivation and `specs/dice-api/spec.md` for the behavior contract. The backend target is Python and FastAPI.

## Goals / Non-Goals

**Goals:**
- Establish one typed request/response boundary usable by HTTP clients, the Web UI, and the CLI.
- Make every successful roll replayable through a returned seed.
- Bound parser and roll work before random values are generated.
- Leave room to evolve the RNG without silently invalidating replay claims.

**Non-Goals:**
- Multiple dice groups, arithmetic expressions, parentheses, keep/drop mechanics, advantage/disadvantage, or dice notation shortcuts.
- Authentication, persistence, roll history, rate limiting, or UI and CLI implementation.
- A cryptographic fairness or provability guarantee.

## Decisions

### Use `POST /roll` with an expression object
Accept `{ "expression": string, "seed": integer | absent }` rather than query parameters or separate `count`, `sides`, and `modifier` fields. A textual expression gives Web UI and CLI users a portable familiar input while one parser is the source of truth. `POST` avoids URL length and URL logging concerns as options expand.

Alternative: structured fields simplify initial validation but introduce a competing expression model once CLI notation is supported. `GET` is cache-friendly but exposes seed and expression in URLs and has less room for future request options.

### Start with one explicit dice group
Parse only `NdM`, optionally followed by signed integer modifier, after accepting and removing ASCII whitespace. Require both `N` and `M`; do not treat `d20` as `1d20`. Parse into a small internal roll model before executing it.

Alternative: support a general expression grammar now. It would enlarge validation, response grouping, limits, and test cases before a baseline public contract exists.

### Return an explainable normalized result
A success contains the canonical expression, seed, `rng_version`, one group with individual die values and subtotal, modifier, and total. The normalized expression removes accepted whitespace and represents the modifier consistently. This lets UI clients render dice while CLI clients consume the total.

Alternative: return only a total. That is smaller but prevents clients from explaining or replay-verifying individual rolls.

### Make seed generation and RNG version explicit
Use a documented deterministic pseudo-random generator for rolls with a supplied seed. Generate a seed from an operating-system entropy source for unseeded calls, then run the same deterministic generator with it. Include a stable `rng_version` such as `"v1"` in every success; a future algorithm change must use a new version rather than claim cross-version replay.

Alternative: use process-global randomness directly for unseeded rolls. It cannot reliably return a replay token and can make tests coupled to process state.

### Validate before execution and use a uniform error envelope
Decode JSON and content type first, validate request field types, parse the expression, and enforce numeric limits before constructing the RNG or dice-value array. Map known client failures to stable codes and reserve 500 errors for unexpected faults; never return parser internals or stack traces.

Alternative: rely on framework-default validation errors. They are useful internally but make the public error contract dependent on framework versions and mix expression failures with request-shape failures.

## Risks / Trade-offs

- [Seeded results differ after an RNG change] -> Include `rng_version`; preserve v1 behavior or make version selection explicit if historical replay becomes a product requirement.
- [Expression parsing accepts ambiguous input] -> Define a narrow grammar, normalize only ASCII whitespace, and use table-driven valid/invalid tests.
- [Large numeric values consume resources or overflow calculations] -> Enforce limits before rolling and use checked/appropriately wide integer calculations for subtotal and total.
- [The public API needs richer notation soon] -> Keep parsing and result construction separate so a later grammar can add roll groups without changing the baseline response envelope.

## Migration Plan

This is a new API with no deployed clients. Deploy `/health` and `/roll` together behind the initial service release. If a release fails, roll back the service version; no stored data or client migration is required. Additive response fields are preferred for compatible future extensions.
