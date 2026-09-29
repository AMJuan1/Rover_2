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

### 2026-09-29 10:20 — app — Protocol acknowledged
- Done: Pulled `2d1b772`, read CLAUDE.md changes and this log.
- Decided: Nothing new (no ADRs).
- Requests:
  1. re 2026-09-29 #1: Protocol accepted. From now on, the app runs `git pull` and reads this file when Jan says "refresh", and appends an entry before every push.
  2. @jan: The pending approvals in 2026-09-29 #3 are still open (ROS 2 Humble install, `~/rover_ws` workspace, package rename).
- Blocked on: nothing.

### 2026-09-29 10:30 — app — Approvals from Jan and new phase (hardware evaluation)
- Done: Added ADR-004 (package rename, accepted) and ADR-005 (hardware evaluation phase). Created `docs/research/hardware-tests.md` (device table + standard per-device test sequence).
- Decided: Jan approved all items of 2026-09-29 #3. Roadmap on hold; detailed rover hardware data (dimensions, mounting, wiring) is NOT to be requested in this phase.
- Requests:
  1. @code: Install ROS 2 Humble (desktop), colcon, rosdep; add Jan to `dialout` and `video` groups (tell him to log out/in).
  2. @code: Create workspace `~/rover_ws/src/Rover_2` as a symlink to the current clone; build.
  3. @code: Implement ADR-004 rename (`Rover_2` → `rover_2`) in `package.xml`, `CMakeLists.txt`, `launch/rsp.launch.py`, and update commands in `CLAUDE.md` / docs. Fix `package.xml` placeholders (maintainer Jan <juantony794@gmail.com>, Apache-2.0, deps). Build and verify `ros2 launch rover_2 rsp.launch.py`.
  4. @code: Update the CLAUDE.md "Current status" and "First session" sections to reflect ADR-005 (hardware evaluation phase; roadmap on hold).
  5. @code: Once Jan gives the LiDAR and depth camera models, run the test sequence in `docs/research/hardware-tests.md`; put driver configs/launch files under `tests/<device>/` and record results in that file.
  6. @jan: Give the models of the new LiDAR and depth camera (only the model names; nothing else needed now).
  7. @app: Research gimbal camera options compatible with ROS 2 Humble once Jan states requirements.
- Blocked on: device models (Jan).
