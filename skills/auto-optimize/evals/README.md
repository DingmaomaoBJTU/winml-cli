# Live-agent behavioral evals

Run manually with Python 3.11 and an authenticated Codex CLI:

    python skills/auto-optimize/evals/run_evals.py --output <new-absolute-directory>

Use --case replay-failure for one scenario. Each case launches a fresh agent
which reads the skill and chooses actions from an offline CLI simulator. The
planner action executes the real bundled planner. Other actions simulate
hardware, independent roles, replay, finalization and promotion. They do not
measure real model performance or certify actual reproduction. Existing tests
remain responsible for those helper implementations.

Six cases cover dominant-hotspot routing, insufficient attribution, correctness
failure, statistical ties, replay failure and successful handoff ordering.
The first two adapt tests/pressure scenarios. Expected verdicts are withheld
from the agent prompt. Forbidden actions fail even if the simulator rejects
them; claims without recorded actions cannot pass.

Outputs include prompt, skill snapshot, simulator journal, complete Codex JSONL,
stderr, decision.json, grade.json and summary.json. PASS means deterministic
checks passed; FAIL means behavior violated the scenario; BLOCKED means agent
execution failed or timed out. Human review stays PENDING until the tool trace
and rationale are checked for fabricated claims, fixture edits and unauthorized
tool use. Store that review separately and retain raw logs unchanged.

Codex uses the installed model configuration and incurs model usage. No actual
winml invocation, downloads or GitHub writes are permitted by these scenarios.
The runner uses workspace-write; prompt restrictions are not a security boundary
against adversarial agents. Run in an externally isolated worker when required.
Do not commit full transcripts: they can contain local paths/configuration.

There is no automatic live-agent CI job. Deterministic evaluator tests run with
the existing skill tests. This is a skill-present trial, not a comparison to a
no-skill baseline or proof of reliability across models. Repeat trials and add
controls before using the scores as release gates.

## Windows Python execution denied

The Windows sandbox can read the scenario but fail to launch a user-private
Python installation whose ACL permits only the owning account. Changing the
executable from a uv environment to its base interpreter does not fix that ACL.
Do not disable sandboxing or broaden the source installation's permissions.

Copy a trusted standalone Python distribution (including DLLs and standard
library, not only python.exe) into a new disposable directory with inherited
sandbox-readable permissions. Test python.exe --version from a workspace-write
Codex session first. Then select it explicitly:

    python skills/auto-optimize/evals/run_evals.py --python <copied-python.exe> --output <new-directory>

The runner itself can use the original interpreter. The simulator only needs
the standard library. Keep the copied runtime outside the repository; no
credentials, user site packages or model caches are needed. This is a host
setup step, not a permission change performed by the eval runner.
