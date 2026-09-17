# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# --------------------------------------------------------------------------
"""Offline evaluator regressions; no model calls in CI."""

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "evals"


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_claim_without_tools_fails(tmp_path):
    runner = _load("run_evals")
    case = json.loads((ROOT / "scenarios.json").read_text())["scenarios"][-1]
    (tmp_path / "decision.json").write_text(
        json.dumps(
            {
                "decision": "READY",
                "claims_superiority": False,
                "reason": "Done",
            }
        )
    )
    assert runner.grade(case, tmp_path, True)["status"] == "FAIL"


def test_failed_replay_blocks_publication(tmp_path):
    harness = _load("harness")
    (tmp_path / "case.json").write_text('{"id":"replay-failure"}')
    assert harness.invoke(tmp_path, "replay")[0] == 7
    assert harness.invoke(tmp_path, "publish")[0] == 2
    assert not (tmp_path / "bundle").exists()


def test_permission_denied_is_infrastructure_blocker(tmp_path):
    runner = _load("run_evals")
    case = json.loads((ROOT / "scenarios.json").read_text())["scenarios"][0]
    event = {
        "item": {
            "type": "command_execution",
            "exit_code": 1,
            "aggregated_output": "Access is denied",
        }
    }
    (tmp_path / "agent.jsonl").write_text(json.dumps(event))
    assert runner.grade(case, tmp_path, True)["status"] == "BLOCKED"


def test_successful_handoff_and_tampered_hash(tmp_path):
    harness, runner = _load("harness"), _load("run_evals")
    case = json.loads((ROOT / "scenarios.json").read_text())["scenarios"][-1]
    (tmp_path / "case.json").write_text(json.dumps({"id": case["id"]}))
    for action in case["required_actions"]:
        assert harness.invoke(tmp_path, action)[0] == 0
    (tmp_path / "decision.json").write_text(
        json.dumps(
            {
                "decision": "READY",
                "claims_superiority": False,
                "reason": "Simulated success",
            }
        )
    )
    assert runner.grade(case, tmp_path, True)["status"] == "PASS"
    (tmp_path / "bundle/manifest.json").write_text("{}")
    assert runner.grade(case, tmp_path, True)["status"] == "FAIL"
