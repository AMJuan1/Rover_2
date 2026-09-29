# Decisions log (ADR)

Record each design decision before implementing it. Newest at the bottom.

## Template

```
## ADR-NNN: <title>
- Date: YYYY-MM-DD
- Status: Proposed | Accepted | Superseded by ADR-NNN
- Context: <problem and constraints>
- Options: <A / B / C with key trade-offs>
- Decision: <chosen option>
- Consequences: <what changes, what to watch>
```

---

## ADR-001: Repository and workflow structure
- Date: 2026-09-28
- Status: Accepted
- Context: Project combines hardware-bound ROS 2 development with research and documentation.
- Options: (A) single tool for everything; (B) Claude Code on the Ubuntu machine for code + Claude web/app for research and docs, sharing this repository.
- Decision: B. This repository is the single source of truth; decisions and research are recorded in `docs/`.
- Consequences: Every research conclusion must be committed to `docs/` so Claude Code sees it.

## ADR-002: Visualization tooling
- Date: 2026-09-28
- Status: Proposed
- Context: RViz currently used for testing and visualization; evaluating more professional alternatives.
- Options: TODO (e.g., RViz2, Foxglove, others — research in `docs/research/visualization.md`)
- Decision: Pending.
- Consequences: Pending.

## ADR-003: Keep single-package template layout
- Date: 2026-09-28
- Status: Accepted
- Context: Repository was created from a single-package ROS 2 robot template (`description/`, `launch/`, `config/`, `worlds/` at the root).
- Options: (A) keep single package; (B) restructure into multiple packages now.
- Decision: A. Split into separate packages only when a subsystem justifies it, with its own ADR.
- Consequences: New directories must be registered in `CMakeLists.txt` `install(DIRECTORY ...)`.
