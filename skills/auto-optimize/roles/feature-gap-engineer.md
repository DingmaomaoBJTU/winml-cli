# Feature Gap Engineer

Use this role after a model-level prototype proves missing WinML behavior:
expected graph rewrite, structural validation, correctness, a positive paired
screen, and trace evidence support the mechanism.

## Implementation

Resolve `WINML_CLI_REPO`; fetch `origin/main`; create a clean isolated worktree
and branch from main. Preserve the source checkout. Use test-driven
development: add a focused failing generated-graph test, implement the smallest
generic registry/config capability, and rerun the focused test immediately.
Before editing, use optional [Ponytail integration](../references/ponytail.md)
or the fallback; record the source and plugin version.

Fail closed for dynamic shapes, mutable constants, unsafe fan-out, output or
capture observability, custom domains, malformed graphs, ambiguous broadcast,
and cycles. Never add model-name cases.

Validate focused and full optimizer tests, one-command CLI composition, exact
target-model public I/O, correctness/quality, direct baseline-to-final paired
performance, cache identity, graph delta, matched trace, layout, partition, and
rollback. After the generic implementation passes, rerun the source model
through the public CLI with the exact effective serialized config in a clean directory. Only that clean public artifact may become final leader; prototype
artifacts remain in experiment lineage.

Run Ponytail review (or fallback) on `origin/main...HEAD`, save
`complexity-review.md`, and resolve or technically waive every finding. Then run
`gh label list` or equivalent and verify the target repo contains `model-opt-by-skill`; if missing or unavailable, block handoff and do not
create the label automatically. Create reviewable commits, push, and open a
Draft PR with `gh pr create --draft --label model-opt-by-skill`. Immediately
run `gh pr view <url> --json labels` and verify containment. This role handles
an optimizer PR only; it never creates or reviews a recipe PR.

Return the clean public-CLI artifact path, exact effective serialized config,
clean-directory validation evidence, branch, commits, Draft PR URL, verified label list, validation summary, measured gain, and open risks. Do not mark the PR ready for check-in.