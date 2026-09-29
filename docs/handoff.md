# Hand-off log (Claude Code ⇄ Claude app)

Asynchronous message board between the two tools. Newest entry at the **bottom**. Never edit or delete past entries; append only.

## Protocol
1. **Before work:** `git pull`, read this file from your last entry down, act on any `@code` / `@app` items addressed to you.
2. **After work:** append one entry (template below), commit, push.
3. **Addressing:** `@code` = Claude Code on the Ubuntu machine; `@app` = Claude in the claude.ai app; `@jan` = needs Jan.
4. **Closing requests:** reply in a new entry referencing the item (e.g. `re 2026-09-29 #2: done in <commit>`).
5. **File ownership (avoids merge conflicts):**

| Path | Owner | Other side |
|---|---|---|
| Code, `launch/`, `config/`, `description/`, `CMakeLists.txt`, `package.xml` | Code | Request changes via this file |
| `docs/hardware.md`, `CLAUDE.md` Environment/Status sections | Code | Request changes via this file |
| `docs/research/` | App | Read only |
| `docs/decisions.md` | Both | Append-only; one ADR per commit |
| `docs/handoff.md` | Both | Append-only |

## Entry template
```
### YYYY-MM-DD HH:MM — <code|app> — <short title>
- Done: <what changed, commit hashes>
- Decided: <decisions, ADR refs>
- Requests: <@app / @code / @jan items, numbered>
- Blocked on: <or "nothing">
```

---

### 2026-09-29 — code — Environment detected, push access set up
- Done: Cloned repo on dev machine; git push over SSH working (remote `git@github.com:AMJuan1/Rover_2.git`, author `Jan`). Filled Environment section in `CLAUDE.md`. Created this hand-off log.
- Decided: Nothing new (no ADRs).
- Requests:
  1. @app: Read this protocol; follow it from your next session. Confirm with an entry here.
  2. @jan: Hardware details still pending (LiDAR, depth camera, IMU, motor driver, compute board, wheel/encoder dimensions). Paused by Jan for now.
  3. @jan: Pending approvals — install ROS 2 Humble on dev machine; workspace at `~/rover_ws/src/Rover_2` (symlink to current clone); rename package `Rover_2` → `rover_2` (REP-144, would be ADR-004).
- Blocked on: ROS 2 not installed on dev machine (no build possible yet).
