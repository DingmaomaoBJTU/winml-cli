# QNN NPU Decisions

Use these as questions for the current graph, not universal preferences.

- Normalize constants and infer static shapes before attribution. Raw ONNX
  node count, file size, and initializer count are not latency evidence.
- Planning router: at 70 percent dominant accelerator time or higher with valid provider attribution and no larger fallback, partition, or transfer explanation, the fast lane is priority only, schedules at most two probes, does not prune other candidates, and keeps the normal correctness and paired performance gates. Write `hotspot_evidence.json`, run `python scripts/plan_hotspot.py hotspot_evidence.json --output hotspot_plan.json`, and adopt that JSON as the current plan. If mode is `dominant-hotspot-fast-lane`, execute only its steps and exit instruction before loading cases or proposing normal-loop hypotheses. If mode is `normal-hypothesis-loop`, continue normally. For quantized graphs, the second bounded step is qdq-boundary placement.
- Treat static Split and complete sibling Slice partitions as competing
  representations. Measure both directions when relevant. A representation may
  matter mainly because it exposes a downstream fusion.
- Preserve QNN-friendly rank and layout. If a smaller graph adds Transpose or
  other layout work, inspect the matched trace before keeping it.
- Audit partition count, residual CPU graph, and fallback. One partition proves
  coverage, not speed; fragmentation can erase a valid local fusion.
- Use matched traces to explain removed operators and accelerator time. Never
  compare profiled wall latency with non-profiled latency.
- Bind compile/cache identity to model hash, effective graph, provider options,
  runtime/provider/SDK versions, and profiling mode. Use a fresh stem when any
  identity component changes.
- Run correctness before performance. Screen in alternating A/B and B/A order;
  confirm the final challenger with paired evidence above noise.
- Preserve contrary results. A direction confirmed for one model, shape, or
  provider version only raises priority elsewhere.