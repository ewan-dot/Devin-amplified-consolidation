# Mac Automation Trio: Hazel + Shortcuts + launchd
## A Deterministic Automation Layer for Multi-Agent AI Dev on macOS Tahoe 26

> **Purpose:** Design a deterministic "floor" automation layer for a Mac mini running isolated AI-agent containers. This layer moves files, triggers pipeline steps, and runs scheduled jobs with no LLM in the loop. Research covers real-world rule patterns, CLI integration, scheduling primitives, tool hand-offs, and known failure modes.

---

## Table of Contents

1. [Hazel — File-Event Automation](#1-hazel)
2. [Shortcuts — CLI-Triggered Orchestration](#2-shortcuts)
3. [launchd — Scheduler and Daemon Supervisor](#3-launchd)
4. [Combination Architecture](#4-combination-architecture)
5. [Critical Gotchas](#5-critical-gotchas)
6. [Which Tool Owns What — Decision Table](#6-which-tool-owns-what)
7. [Verdict: Can `shortcuts run` Work Headless?](#7-verdict)

---

## 1. Hazel

**What it is:** A macOS preference pane / standalone app (current: Hazel 5) that watches folders with filesystem events and fires rules when conditions match. Rules are if-then logic chains: one or more conditions, one or more sequential actions. ([Noodlesoft official manual](https://www.noodlesoft.com/manual/hazel/attributes-actions/using-shell-scripts/), no date; [Macworld review](https://www.macworld.com/article/632990/hazel-review-watches-folders-and-takes-automatic-action.html), Apr 2022)

### 1.1 Architecture

Hazel runs as a persistent LaunchAgent under the logged-in user. It uses FSEvents (the same kernel API as Spotlight) to watch folders without polling. This means near-zero CPU cost until a change occurs. It can watch any local folder, smart folders, and the Trash. Hazel 5 added Shortcuts integration (macOS 12+) and JavaScript scripting alongside shell scripts and AppleScript. ([Asian Efficiency, Feb 2026](https://www.asianefficiency.com/technology/hazel-intro/))

### 1.2 Rule Conditions — What You Can Match

| Condition axis | Examples |
|---|---|
| **Name/Extension** | name matches pattern `IMG_*.jpg`, extension is `pdf` |
| **Date attributes** | date added > 4 weeks, date last modified < 1 day |
| **Tags** | tagged "inbox", tagged "processed" |
| **Contents** | PDF text contains "invoice", file encoding |
| **Size** | file size > 100MB |
| **Custom shell script** | exit 0 = match, any other exit = no match |
| **Custom attributes** | user-defined text, date, list, or table attributes |

For **pattern matching**, Hazel supports token-based patterns (`IMG_` + digits + `.jpg`), regex-style wildcards, and table-matching (import a CSV of strings, match file names against it). ([Macworld review](https://www.macworld.com/article/632990/hazel-review-watches-folders-and-takes-automatic-action.html), Apr 2022)

**Watch subfolders:** A rule applied to a folder can be set to recurse into subfolders by enabling "Include subfolders" on the watched folder. This is per-folder, not per-rule. ([Automators Talk thread](https://talk.automators.fm/t/hazel-rule-to-run-any-time-files-are-added-to-a-folder-or-sub-folder/17163), Jan 2024)

### 1.3 Actions — Move, Not Delete

For an auditable pipeline, the safe action pattern is **move to a staging folder**, never delete directly. Hazel supports:

- **Move to folder** — moves matched file to a destination, preserving or flattening folder structure
- **Rename** — rename with token patterns (date, counter, matched groups)
- **Add tag** — tag files for downstream visibility
- **Run shell script** — call any shell script or program
- **Run Shortcut** — trigger a named Shortcut (Hazel 5.1+, requires logged-in GUI session)
- **Run Automator workflow** / **Run AppleScript** / **Run JavaScript**

For a move-not-delete discipline: set up a `_processed/` subfolder as move target and a second rule that archives files from `_processed/` to cold storage after N days. This gives a two-stage recoverable pipeline.

### 1.4 Shell Script Integration — The Core Mechanism

This is the most important Hazel capability for agent integration.

**The file path variable:** Hazel passes `$1` as the full absolute path of the matched file to any shell script. ([Noodlesoft manual](https://www.noodlesoft.com/manual/hazel/attributes-actions/using-shell-scripts/))

```bash
#!/bin/zsh
# $1 = full path to the matched file, e.g. /Users/agent/inbox/job_42.json
FILE_PATH="$1"
# Always quote $1 — paths can contain spaces
/usr/local/bin/my-agent-trigger --input "$FILE_PATH"
```

**Embedded vs. external scripts:**

- **Embedded:** Script is stored inside the Hazel rule (pasted into the rule UI). Portable when rules are exported/synced. No separate file to manage.
- **External:** Hazel calls a standalone script file on disk. Must be `chmod +x` and have a `#!` shebang. Use external scripts when the logic is complex, version-controlled, or shared across rules.

**Script execution environment:** Hazel runs scripts in a non-interactive subshell. Your `.zshrc` / `.bash_profile` PATH customizations are **not** loaded. Always use absolute paths to binaries. If you need a custom PATH, set it explicitly at the top of the script:

```bash
#!/bin/zsh
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
```

This is a documented pitfall — the Noodlesoft forums confirm PATH issues appear after macOS updates that remove system Python or change binary locations. ([Noodlesoft forums](https://www.noodlesoft.com/forums/viewtopic.php?f=4&t=14264), Mar 2022)

**Exit codes in conditions:** When a shell script is used as a **condition**, exit 0 = match, any other exit = no match. Use this to do arbitrary file inspection (grep content, parse JSON, call an API) to gate whether a rule fires.

**Chaining actions:** Hazel executes the action list sequentially within a single rule. You can have multiple actions in order:

1. Run shell script (invoke agent trigger)
2. Add tag "processed"
3. Move to `_processed/` folder
4. Send notification

Between rules, Hazel re-evaluates the file after each rule runs, so Rule A can produce output that Rule B on the same folder immediately picks up.

### 1.5 Logging and Auditability

Hazel does not have a native structured log output, but you have several options:

1. **Notification action:** Hazel can fire a macOS notification for each matched file. Good for real-time visibility.
2. **Status panel:** In the Hazel UI, click the "Status" button on any folder to see which files had rules applied and when. This is an interactive audit trail.
3. **Pause/Play per folder:** Suspend a folder's rules without removing them — useful for safe testing.
4. **Log from your script:** Since rules call shell scripts, redirect output to a log file:

```bash
#!/bin/zsh
LOG="/var/log/hazel-pipeline.log"
echo "$(date -Iseconds) | HAZEL | processed: $1" >> "$LOG"
```

5. **Dry-run pattern:** There is no native dry-run, but you can create a test rule that only logs (no move/rename) and run it on a copy of files to verify logic before activating the real rule.

6. **Disable rule without deleting:** Uncheck a rule in the UI to keep it defined but inactive.

---

## 2. Shortcuts

**What it is:** Apple's first-party automation app, available on Mac since macOS Monterey (12, 2021). Shortcuts are visual workflows of "actions" — app intents, shell scripts, AppleScript blocks, HTTP calls, file operations, and more. They sync via iCloud. ([Apple Shortcuts Mac CLI guide](https://support.apple.com/guide/shortcuts-mac/run-shortcuts-from-the-command-line-apd455c82f02/mac))

### 2.1 CLI Triggering — `shortcuts run`

```bash
# Basic invocation
shortcuts run "Shortcut Name"

# Pass a file as input
shortcuts run "ProcessJob" --input-path /path/to/job.json

# Capture text output
shortcuts run "GetStatus" | cat

# Write output to a file
shortcuts run "GenerateReport" -o ~/Desktop/report.pdf

# Pipe output to another command
shortcuts run "ExtractMetadata" --output-type public.plain-text | jq .
```

The `shortcuts` binary is at `/usr/bin/shortcuts`. It exits 0 on success, 1 on error. ([Apple Shortcuts CLI guide](https://support.apple.com/guide/shortcuts-mac/run-shortcuts-from-the-command-line-apd455c82f02/mac); [OS X Daily](https://osxdaily.com/2022/02/28/run-shortcuts-from-the-command-line-on-mac/), Feb 2022)

**Passing output to other processes:**
```bash
shortcuts run "songtitle" | bbedit
shortcuts run "songtitle" | cat
shortcuts run "songtitle" -o ~/songtitle.txt
```
([Six Colors](https://sixcolors.com/post/2021/12/run-shortcuts-from-the-mac-command-line/), Dec 2021)

**List available shortcuts:**
```bash
shortcuts list
shortcuts list -f "FolderName"
shortcuts list --folders
```

**From AppleScript (alternative to CLI):**
```applescript
tell application "Shortcuts Events"
    set theResult to run shortcut "MyShortcut" with input "some text"
end tell
```
`Shortcuts Events` is a background helper that runs Shortcuts without opening the Shortcuts.app UI — this is the preferred AppleScript integration path. ([Six Colors](https://sixcolors.com/post/2021/12/run-shortcuts-from-the-mac-command-line/), Dec 2021)

### 2.2 Shell Scripts and AppleScript Inside Shortcuts

A Shortcut can contain a **Run Shell Script** action. This lets a Shortcut call arbitrary shell code:

```
[Receive Input] → [Run Shell Script: /bin/zsh -c "..."] → [Output result]
```

The shell script receives Shortcut input via stdin or via a magic variable, and its stdout becomes the next action's input. ([MacScripter forum](https://www.macscripter.net/t/running-a-shell-script-in-a-shortcut/77069), Apr 2025; [Six Colors](https://sixcolors.com/post/2022/01/shortcuts-applescript-terminal-working-around-automation-roadblocks/), Jan 2022)

A Shortcut can also contain a **Run AppleScript** action for app control.

### 2.3 Cross-Device Sync via iCloud

Shortcuts sync automatically across all devices signed into the same Apple ID via iCloud. A Shortcut created on Mac is available on iPhone and iPad. Running `shortcuts run "name"` on Mac triggers the Mac-local copy; the iPhone copy is separate. Cross-device *invocation* (Mac triggering an iPhone Shortcut remotely) is not a CLI feature — it requires the Shortcuts URL scheme or a shared Shortcut that calls another device via Siri Shortcuts intents. ([Apple Shortcuts What's New](https://support.apple.com/en-us/125148), Mar 2026)

### 2.4 macOS Tahoe 26 Shortcuts Improvements

macOS 26 introduced the biggest Shortcuts upgrade for Mac:

- **Personal Automations on Mac** — Shortcuts can now trigger automatically based on: Time of Day, Alarm, Email received, Message received, Folder (files added to folder), File modified, External Drive connected, Wi-Fi joined, Bluetooth device connected. These are the same automation triggers iOS has had for years, now coming to Mac. ([Apple Shortcuts What's New](https://support.apple.com/en-us/125148), Mar 2026; [macOS Tahoe newsroom](https://www.apple.com/newsroom/2025/06/macos-tahoe-26-makes-the-mac-more-capable-productive-and-intelligent-than-ever/), Jun 2025)
- **Natural language shortcut creation** (AI-assisted)
- **Apple Intelligence integration** — `Use Model` action taps on-device LLM, Private Cloud Compute, or ChatGPT
- **Spotlight integration** — shortcuts can receive selected text from Spotlight
- **Quick Keys** — keyboard shortcuts to invoke Shortcuts instantly

The **Folder trigger** is directly relevant: a Shortcut can now fire when files are added to a specified folder. This is macOS Tahoe's native version of what Hazel does, but with less flexibility in condition matching. ([Tom's Guide](https://www.tomsguide.com/computing/software/apples-shortcuts-app-is-getting-a-huge-upgrade-in-ios-26-and-macos-26-heres-how-it-will-help-you), Jun 2025; [macOS 26 Tahoe Shortcuts](https://macdownload.informer.com/Mac-Stories/macos-26-tahoe-the-shortcuts-app-improvements.html), Oct 2025)

### 2.5 Session Requirements — The Critical Limitation

**`shortcuts run` requires a logged-in GUI session (Aqua session).** This is not documented explicitly by Apple but is confirmed by:

1. The `shortcuts` binary is a Cocoa/AppKit app front-end that communicates with the `Shortcuts Events` helper. Both require a windowing environment.
2. OS X Daily explicitly notes: "with the exception of 'list', they will all launch the Shortcuts app in the GUI on the Mac." ([OS X Daily](https://osxdaily.com/2022/02/28/run-shortcuts-from-the-command-line-on-mac/), Feb 2022)
3. `tell application "Shortcuts Events"` — the agent is named "Events" precisely because it runs in the user's event-dispatch session.

See [Section 7](#7-verdict) for the full verdict.

---

## 3. launchd

**What it is:** PID 1 on macOS since 10.4 Tiger. Everything on the system either descends from launchd or is launched by it. It replaces cron, inetd, and rc.d. ([Apple Developer: Creating Launch Daemons and Agents](https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html), 2016; [launchd.info](https://launchd.info/))

### 3.1 Daemon vs. Agent — The Critical Distinction

| | LaunchDaemon | LaunchAgent |
|---|---|---|
| **Runs as** | root (or `UserName` key) | logged-in user |
| **Starts when** | system boot | user login |
| **Runs without GUI** | Yes | No (requires Aqua session) |
| **Has GUI access** | No | Yes |
| **Can run `shortcuts run`** | **No** | Yes |
| **plist location** | `/Library/LaunchDaemons/` | `~/Library/LaunchAgents/` or `/Library/LaunchAgents/` |
| **TCC behavior (Tahoe)** | Bypasses user-space TCC | Subject to user TCC |

([Sweep for Mac guide](https://www.sweepformac.com/guides/mac-launch-agents-vs-daemons/), Dec 2025; [launchd.info](https://launchd.info/); [Apple Developer docs](https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html))

### 3.2 Plist Key Reference for This Use Case

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
    "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- === IDENTITY === -->
    <key>Label</key>
    <string>com.agentpipeline.job-processor</string>

    <!-- === WHAT TO RUN === -->
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/agent-job-processor.sh</string>
    </array>

    <!-- === RUN AS SPECIFIC USER (daemon only) === -->
    <key>UserName</key>
    <string>agentuser</string>

    <!-- === SCHEDULED TRIGGER (cron-style) === -->
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>   <integer>2</integer>
        <key>Minute</key> <integer>0</integer>
    </dict>
    <!-- Or for every-N-seconds interval: -->
    <!-- <key>StartInterval</key> <integer>300</integer> -->

    <!-- === WATCH-PATH TRIGGER === -->
    <key>WatchPaths</key>
    <array>
        <string>/var/agent/inbox</string>
    </array>
    <!-- QueueDirectories: fire when dir is non-empty, re-fire if still non-empty after job exits -->
    <!-- <key>QueueDirectories</key>
    <array>
        <string>/var/agent/queue</string>
    </array> -->

    <!-- === SCHEDULING BEHAVIOR === -->
    <key>RunAtLoad</key>
    <false/>  <!-- Don't fire immediately on launchctl load -->

    <!-- === LOGGING === -->
    <key>StandardOutPath</key>
    <string>/var/log/agentpipeline/processor.log</string>
    <key>StandardErrorPath</key>
    <string>/var/log/agentpipeline/processor.err</string>

    <!-- === LOW-PRIORITY IO === -->
    <key>LowPriorityIO</key>
    <true/>
    <key>Nice</key>
    <integer>10</integer>   <!-- 0=normal, 20=lowest -->

    <!-- === WORKING DIRECTORY === -->
    <key>WorkingDirectory</key>
    <string>/var/agent</string>

    <!-- === ENVIRONMENT === -->
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
    </dict>

    <!-- === RESTART BEHAVIOR === -->
    <key>ThrottleInterval</key>
    <integer>30</integer>  <!-- min seconds between restarts on failure -->
</dict>
</plist>
```

### 3.3 StartCalendarInterval — Scheduling Patterns

`StartCalendarInterval` uses cron-like dictionaries. Omitted keys are treated as wildcards (`*`).

```xml
<!-- Every day at 02:00 -->
<key>StartCalendarInterval</key>
<dict>
    <key>Hour</key>   <integer>2</integer>
    <key>Minute</key> <integer>0</integer>
</dict>

<!-- Every Monday at 08:30 -->
<key>StartCalendarInterval</key>
<dict>
    <key>Weekday</key> <integer>1</integer>
    <key>Hour</key>    <integer>8</integer>
    <key>Minute</key>  <integer>30</integer>
</dict>

<!-- Multiple times: use an ARRAY of dicts -->
<key>StartCalendarInterval</key>
<array>
    <dict><key>Hour</key><integer>8</integer><key>Minute</key><integer>0</integer></dict>
    <dict><key>Hour</key><integer>18</integer><key>Minute</key><integer>0</integer></dict>
</array>
```

**Important:** `StartCalendarInterval` fires a missed job when the Mac wakes from sleep (unlike cron, which skips missed jobs). ([launchd.info](https://launchd.info/); [John Dturn's launchd gist](https://gist.github.com/johndturn/09a5c055e6a56ab61212204607940fa0), Jul 2023)

### 3.4 WatchPaths vs. QueueDirectories

Both trigger a job when filesystem changes occur, but they behave differently:

**`WatchPaths`:**
- Fires when any file in the specified path is created, modified, or deleted
- Fires once per batch of changes (debounced), not once per file
- Your script must enumerate the directory contents itself
- Will also fire on disk mounts/unmounts at that path

**`QueueDirectories`:**
- Like WatchPaths, but with re-fire semantics: if the directory is still non-empty when the job exits, launchd re-fires the job after `ThrottleInterval`
- This makes it a natural "drain the queue" trigger
- Caveat: if the job never empties the directory (e.g., it processes one file and leaves others), it will re-fire repeatedly. Always drain all files or move them out before exiting.

([Notes on Apple's launchd gist by dabrahams](https://gist.github.com/dabrahams/4092951), 2019; [Apple Developer docs](https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html))

### 3.5 Running as a Non-Login System User

For a daemon serving containerized agents, run it as a dedicated non-login user, not root:

```xml
<key>UserName</key>
<string>agentrunner</string>
<key>GroupName</key>
<string>staff</string>
```

This gives the daemon access to files owned by `agentrunner` while limiting its privileges. The `UserName` key is only valid in a LaunchDaemon (plist in `/Library/LaunchDaemons/`). ([launchd.plist man page](https://www.manpagez.com/man/5/launchd.plist/); [Tahoe TCC dev.to post](https://dev.to/linou518/when-macos-26-tahoe-blocked-python-socket-connections-and-how-launchdaemon-fixed-it-3j2i), Mar 2026)

### 3.6 Logging

launchd does not integrate with the macOS unified logging system (OSLog) automatically, but:
- `StandardOutPath` / `StandardErrorPath` redirect a job's stdout/stderr to files
- For rotation-safe logging, write to files with timestamps or use `syslog(3)` from your script
- `log show --predicate 'process == "launchd"'` surfaces launchd-level events in Console.app
- `launchctl list | grep com.yourjob` confirms whether a job is loaded and its last exit code

([Debugging launchd plist jobs — mobeets](https://mobeets.github.io/blog/launchd/), Jan 2016; [Stack Overflow — launchd log rotation](https://stackoverflow.com/questions/71832882/macos-launchd-fails-to-redirect-stdout-to-the-file-after-log-rotation), Apr 2022)

### 3.7 Loading and Managing Jobs

```bash
# Modern approach (macOS 10.11+) — use bootstrap/bootout
sudo launchctl bootstrap system /Library/LaunchDaemons/com.agentpipeline.plist
sudo launchctl bootout system/com.agentpipeline

# For LaunchAgents (user context)
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.myagent.plist
launchctl bootout gui/$(id -u)/com.myagent

# Legacy approach (still works, deprecated)
sudo launchctl load /Library/LaunchDaemons/com.agentpipeline.plist
sudo launchctl unload /Library/LaunchDaemons/com.agentpipeline.plist

# Manually trigger (ignore schedule/watch conditions)
launchctl start com.agentpipeline
launchctl stop com.agentpipeline

# Check status
launchctl list | grep com.agentpipeline
```

---

## 4. Combination Architecture

### 4.1 Conceptual Layer Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│  FILESYSTEM                                                      │
│  /var/agent/inbox/   /var/agent/queue/   /var/agent/processed/  │
└────────┬──────────────────┬───────────────────────┬─────────────┘
         │ FSEvents         │ WatchPaths/Queue       │ output
         ▼                  ▼                        │
┌────────────────┐  ┌───────────────────┐            │
│   HAZEL        │  │   LAUNCHD         │            │
│  (LaunchAgent) │  │  (LaunchDaemon)   │            │
│                │  │                  │            │
│ • Complex file │  │ • Cron-scheduled │            │
│   condition    │  │   batch jobs     │            │
│   matching     │  │ • Headless, no   │            │
│ • Pattern/age/ │  │   GUI needed     │            │
│   tag/content  │  │ • System-level   │            │
│ • Move files   │  │   services       │            │
│ • Call shell   │  │ • Run as any     │            │
│   scripts ($1) │  │   user           │            │
└───────┬────────┘  └────────┬──────────┘            │
        │ $1=path            │ shell script           │
        ▼                    ▼                        │
┌───────────────────────────────────────────────────┐ │
│   SHELL SCRIPTS (the universal hand-off medium)   │ │
│   /usr/local/bin/*.sh                             │ │
└───────────┬───────────────────────────────────────┘ │
            │ (optional, GUI session only)             │
            ▼                                          │
┌───────────────────────────────────────────────────┐ │
│   SHORTCUTS (LaunchAgent, GUI session required)   │◄┘
│   /usr/bin/shortcuts run "name"                   │
│   • Cross-app orchestration (Mail, Calendar, etc.)│
│   • Cross-device triggers (iPhone ↔ Mac)          │
│   • Apple Intelligence actions                    │
└───────────────────────────────────────────────────┘
```

### 4.2 Hand-off Patterns

**Pattern A: Hazel → shell script → agent container**

The most important and reliable pattern. Hazel detects a new file, calls an embedded/external shell script with `$1`, the script enqueues the job to a container's API, and moves the file to `_processed/`.

```bash
#!/bin/zsh
# hazel-trigger-agent.sh — called by Hazel with $1 = matched file path
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
FILE="$1"
LOG="/var/log/hazel-pipeline.log"
echo "$(date -Iseconds) | hazel-trigger | file=$FILE" >> "$LOG"

# Drop a trigger file into the agent queue
cp "$FILE" /var/agent/queue/
echo "$(date -Iseconds) | hazel-trigger | queued: $FILE" >> "$LOG"

# Signal completion — Hazel will then run next action (e.g., move to processed/)
exit 0
```

**Pattern B: launchd → shell script → agent container (scheduled)**

A LaunchDaemon fires on schedule or when a watch path changes. The shell script enumerates the queue directory, processes jobs, and logs results. Runs headlessly, no user session needed.

```bash
#!/bin/zsh
# agent-batch-runner.sh — called by launchd LaunchDaemon
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
QUEUE="/var/agent/queue"
DONE="/var/agent/processed"
LOG="/var/log/agentpipeline/runner.log"

for f in "$QUEUE"/*.json; do
    [[ -f "$f" ]] || continue
    echo "$(date -Iseconds) | runner | processing: $f" >> "$LOG"
    /usr/local/bin/agent-runner --input "$f" >> "$LOG" 2>&1
    STATUS=$?
    if [[ $STATUS -eq 0 ]]; then
        mv "$f" "$DONE/"
        echo "$(date -Iseconds) | runner | done: $f" >> "$LOG"
    else
        echo "$(date -Iseconds) | runner | FAILED ($STATUS): $f" >> "$LOG"
    fi
done
```

**Pattern C: launchd → `shortcuts run` → Shortcut (GUI session required)**

Use this only for event-driven orchestration that needs app-level Mac automation (controlling apps, calendar, cross-device triggers). This pattern requires a LaunchAgent (not LaunchDaemon) because `shortcuts run` needs the Aqua session.

```xml
<!-- ~/Library/LaunchAgents/com.agentpipeline.shortcuts-trigger.plist -->
<key>ProgramArguments</key>
<array>
    <string>/usr/bin/shortcuts</string>
    <string>run</string>
    <string>AgentNotify</string>
</array>
<key>StartCalendarInterval</key>
<dict>
    <key>Hour</key><integer>9</integer>
    <key>Minute</key><integer>0</integer>
</dict>
```

([Periodic Execution of Apple Shortcuts with launchd — ileif.de](https://en.ileif.de/2024/05/16/periodic-execution-of-apple-shortcuts-with-launchd/), May 2024)

**Pattern D: Hazel → Run Shortcut action**

Hazel 5.1+ has a native "Run Shortcut" action. Behind the scenes it calls `shortcuts run`. This is convenient but carries the same GUI session requirement. For a headless Mac mini, **prefer calling a shell script from Hazel instead**, and reserve `Run Shortcut` for user-facing actions.

**Pattern E: Shell script → `shortcuts run` (agent-triggered)**

An AI agent inside a container can SSH or write a trigger file. A LaunchAgent watching that trigger file (via WatchPaths) can then call `shortcuts run`. This gives agents the ability to trigger Mac-native automation — but only when a user is logged in.

### 4.3 Hazel vs. launchd on the Same Folder

Both can watch the same folder simultaneously without conflict — they use independent FSEvents subscriptions. However, be careful about:

1. **Race conditions:** If launchd's WatchPaths and Hazel both fire on the same file creation event, both scripts may run near-simultaneously. Design one to be the authoritative mover (move file to a different folder), so the second tool sees an empty directory.
2. **Recommended pattern:** Hazel owns the human-facing inbox (Downloads, Desktop). launchd owns machine-facing queue directories (`/var/agent/queue`). Never let both watch the same directory with write actions on the same files.
3. **Log timestamps** from both to detect unexpected parallelism.

---

## 5. Critical Gotchas

### 5.1 `shortcuts run` from a LaunchDaemon — DOES NOT WORK

**This is the most important gotcha for headless automation.**

`shortcuts run` (and `tell application "Shortcuts Events"`) requires an Aqua GUI session. LaunchDaemons run before any user logs in, as root, with no windowing server connection. Attempting `shortcuts run` from a LaunchDaemon will either:

- Silently hang (waiting for a session that never arrives)
- Return exit code 1 with no useful error
- Crash `Shortcuts Events` with an AppKit/CoreGraphics assertion

Evidence:

1. Apple's Quinn "The Eskimo" (DTS): "a LaunchAgent only runs if a user logs into a GUI session. The `launchd.plist` default for agents is session type `Aqua`." The doc also confirms daemons have no GUI context at all. ([Apple Developer Forums](https://developer.apple.com/forums/thread/696859), Jan 2022)
2. Chris Paynter (Medium): "Daemons are run as the root user, but the root user does not have a GUI session. Daemons are typically loaded by the root user before the GUI is even loaded. There's no way for it to trigger the TCC prompt." ([Medium — macOS daemon TCC](https://chrispaynter.medium.com/what-to-do-when-your-macos-daemon-gets-blocked-by-tcc-dialogues-d3a1b991151f), Feb 2021)
3. OS X Daily (2022): "with the exception of 'list', they will all launch the Shortcuts app in the GUI on the Mac." — meaning `shortcuts run` is inherently GUI-coupled. ([OS X Daily](https://osxdaily.com/2022/02/28/run-shortcuts-from-the-command-line-on-mac/))

**Workaround if you need Shortcuts from a headless context:** Write a trigger file to a path that a LaunchAgent (running in the GUI session) is watching. The LaunchDaemon writes the trigger; the LaunchAgent picks it up and calls `shortcuts run`. This adds a one-step delay but maintains headless operation.

### 5.2 Hazel Requires a Logged-In User

Hazel itself runs as a LaunchAgent under the logged-in user. If no user is logged in, Hazel's rules do not run. For a Mac mini used as a headless server:

- Enable **automatic login** in System Settings > Users & Groups (or use MDM)
- Alternatively, use `caffeinate -dimsu` via a LaunchDaemon to keep the system awake, and ensure a GUI session is always running

([Headless Mac setup — Harshit Chawla, Medium](https://chawlaharshit.medium.com/how-i-turned-my-mac-into-a-headless-server-my-always-on-setup-for-ai-monitoring-and-automation-aa9a8ff9aeff), Oct 2025)

### 5.3 TCC — Full Disk Access Requirements

On macOS Tahoe 26, TCC has been significantly tightened:

**Hazel:** Requires Full Disk Access to read/move files outside the user's standard folders. Must be granted in System Settings → Privacy & Security → Full Disk Access. Without it, rules silently skip files in restricted locations. ([Retrospect macOS Tahoe FDA docs](https://docs.retrospect.com/docs/macos-sequoia-application-data-privacy-full-disk-access), Sep 2024)

**`shortcuts run` / Shortcuts.app:** Requires Full Disk Access when the shortcut includes a Run Shell Script action that touches restricted folders. If triggered from Finder Quick Actions or the menu bar, Finder itself may need FDA. ([Apple Community thread](https://discussions.apple.com/thread/255210852), Oct 2023)

**LaunchDaemons:** Running as root bypasses most user-space TCC checks. Third-party runtimes (Homebrew Python, Node.js) launched via LaunchAgent are subject to TCC, but the same runtimes launched via LaunchDaemon (root) are not. This is documented in a real-world Tahoe case where Homebrew Python socket connections failed as a LaunchAgent but succeeded as a LaunchDaemon. ([dev.to / macOS 26 TCC](https://dev.to/linou518/when-macos-26-tahoe-blocked-python-socket-connections-and-how-launchdaemon-fixed-it-3j2i), Mar 2026)

**Tahoe 26 enhanced permissions:** macOS 26 reorganized the Privacy & Security panel. Apps now appear automatically when they first request access. For scripts and CLI tools, you may need to add the **interpreter** (e.g., `/bin/zsh`, `/opt/homebrew/bin/python3`) to the Full Disk Access list rather than the script itself. ([allthings.how — macOS 26 App Permissions](https://allthings.how/use-the-enhanced-app-permissions-in-macos-26-tahoe/), Jun 2025)

**TCC summary for this use case:**

| Component | TCC requirement |
|---|---|
| Hazel | Full Disk Access if watching system/app folders |
| `shortcuts run` from terminal | Full Disk Access for shell script in shortcut |
| Hazel calling shell script | None beyond Hazel's own FDA grant |
| LaunchDaemon (root) | Bypasses user-space TCC |
| LaunchAgent + Homebrew binary | May hit TCC on Tahoe; use LaunchDaemon or grant FDA to interpreter |

### 5.4 PATH Environment in All Three Tools

None of the three tools load your shell profile:
- **Hazel scripts:** Set `PATH` explicitly at top of script
- **launchd jobs:** Use `EnvironmentVariables` key in plist
- **Shortcuts Run Shell Script:** Runs with a minimal `/bin/zsh` environment

Always use absolute paths to binaries. `/opt/homebrew/bin` and `/usr/local/bin` are not on the default PATH in non-interactive shells.

### 5.5 Shortcuts Automations (New in Tahoe 26) vs. Hazel

macOS 26 introduced Folder-trigger Automations in Shortcuts — a shortcut can fire when files are added to a specified folder. This seems to overlap with Hazel, but:

- Hazel conditions are far richer (age, pattern, content, tag, custom script conditions)
- Hazel can match by PDF text content, regex patterns, file attributes
- Shortcuts automations lack multi-condition logic and move/rename actions
- Shortcuts automations are useful for cross-app chaining; Hazel is better for file hygiene

Use both if needed: Hazel does the file matching and moving; a Shortcuts automation handles downstream app-level actions.

### 5.6 Conflict: Hazel and launchd WatchPaths on the Same Folder

Confirmed safe to co-exist at the FSEvents level. The conflict is logical, not technical. Design rule: **one tool owns one inbox, files move out before the other tool could act on them.**

### 5.7 `shortcuts run` Headless Workaround — ShortKit

A community workaround exists: [ShortKit](https://gist.github.com/yazanzaid00/34593dced357648d29708b10d39a0cbb) (May 2025) is an AppleScript app with `LSBackgroundOnly=true` that registers a custom `shortkit://` URL scheme. It calls `tell application "Shortcuts Events"` which still requires a GUI session, but it runs without opening the Shortcuts.app UI. This reduces visible disruption but does **not** remove the GUI session requirement.

---

## 6. Which Tool Owns What — Decision Table

| Job type | Owner tool | Reason |
|---|---|---|
| Watch an inbox folder for new files by name/pattern/age/tag | **Hazel** | Richest condition matching, no polling, FSEvents-native |
| Match file by content (PDF text, JSON key) | **Hazel** (shell script condition) | Use embedded shell script as condition gate |
| Move/rename matched file to pipeline stage | **Hazel** | Native move/rename with token patterns |
| Call agent trigger script when file arrives | **Hazel** (Run Shell Script, `$1`) | Direct, synchronous, file path passed in |
| Scheduled batch job (cron-style, runs headless) | **launchd LaunchDaemon** | No GUI needed, runs at boot, any user |
| Watch a machine queue directory, drain it | **launchd LaunchDaemon** (QueueDirectories) | Automatic re-fire until queue empty |
| Long-running background service for agents | **launchd LaunchDaemon** | Persistent, restart on crash, root-level |
| Restart a crashed service | **launchd** (KeepAlive) | Native supervisor behavior |
| Run a pipeline step that controls Mac apps (Mail, Calendar, Reminders) | **Shortcuts** (LaunchAgent) | Cross-app intent access |
| Cross-device trigger (notify iPhone, run iPhone shortcut from Mac) | **Shortcuts** | Only tool with cross-device reach |
| Human-invoked multi-step workflow with I/O | **Shortcuts** | Best developer experience for GUI-adjacent flows |
| Headless scheduled system maintenance (disk cleanup, backup) | **launchd LaunchDaemon** | Zero GUI dependency |
| Logging/auditing file operations | **Shell scripts** (called by all three) | Central log file, timestamp each operation |
| Dry-run / preview before live rules | **Hazel** (disable rule, check status pane) | Built-in per-folder pause and status view |

---

## 7. Verdict: Can `shortcuts run` Work Headless?

**No, not in a pure LaunchDaemon / no-GUI-session context.**

The `shortcuts run` CLI and `tell application "Shortcuts Events"` both require an Aqua GUI session (a logged-in user with a windowing server). This is inherent to how Shortcuts is implemented — it uses AppKit and communicates through the user's session. Running it from a LaunchDaemon (which boots before login and runs as root with no windowing context) will fail silently or hang.

**What works:**

| Invocation context | Works? | Notes |
|---|---|---|
| Terminal (logged-in user) | ✅ Yes | Nominal use case |
| LaunchAgent (user logged in, Aqua) | ✅ Yes | Standard approach, see ileif.de blog |
| SSH session (user logged in) | ✅ Yes (usually) | May need `launchctl asuser $(id -u) /usr/bin/shortcuts run ...` on some macOS versions |
| Hazel rule action (user logged in) | ✅ Yes | Hazel is a LaunchAgent; same session |
| LaunchDaemon (no GUI session) | ❌ No | No windowing environment |
| SSH session (no GUI session / headless) | ❌ Unreliable | No Aqua session to attach to |
| `shortcuts run` via `su` / `sudo` as root | ❌ No | Root has no GUI session |

**Practical consequence for agent automation on a Mac mini:**

- Use a **LaunchDaemon** for all headless, always-on pipeline work (file processing, scheduled jobs, container orchestration)
- Use a **LaunchAgent** only for jobs that need GUI (Shortcuts, Hazel)
- Ensure the Mac mini has **automatic login** enabled so Hazel and Shortcuts LaunchAgents always have a session
- If you need a headless job to trigger Shortcuts: write a trigger file from the daemon → LaunchAgent watches for that file → LaunchAgent calls `shortcuts run`
- For purely headless automation (zero GUI dependency), **replace any `shortcuts run` calls with direct shell scripts** — anything you'd do in a Shortcut can be replicated in a shell script or Python script running under launchd

**The architectural bottom line:** Shortcuts is the human-facing orchestration layer — good for things that interact with Apple apps and devices. Shell scripts + launchd are the headless backbone. Hazel is the file-event intelligence layer that sits between the filesystem and both of the other tools. Trying to use Shortcuts as the headless glue is the most common failure mode in Mac automation for server-style deployments.

---

## Source Index

| Source | URL | Date |
|---|---|---|
| Noodlesoft — Using Shell Scripts | https://www.noodlesoft.com/manual/hazel/attributes-actions/using-shell-scripts/ | (undated, current) |
| Noodlesoft — Attributes & Actions | https://www.noodlesoft.com/manual/hazel/attributes-actions/ | (undated, current) |
| Noodlesoft forums — PATH in embedded scripts | https://www.noodlesoft.com/forums/viewtopic.php?f=4&t=14264 | Mar 2022 |
| Macworld — Hazel review | https://www.macworld.com/article/632990/hazel-review-watches-folders-and-takes-automatic-action.html | Apr 2022 |
| Asian Efficiency — Hazel 2026 guide | https://www.asianefficiency.com/technology/hazel-intro/ | Feb 2026 |
| Automators Talk — Hazel subfolder rule | https://talk.automators.fm/t/hazel-rule-to-run-any-time-files-are-added-to-a-folder-or-sub-folder/17163 | Jan 2024 |
| Apple — Shortcuts CLI guide | https://support.apple.com/guide/shortcuts-mac/run-shortcuts-from-the-command-line-apd455c82f02/mac | (current) |
| Apple — What's New in Shortcuts | https://support.apple.com/en-us/125148 | Mar 2026 |
| Apple — macOS Tahoe 26 newsroom | https://www.apple.com/newsroom/2025/06/macos-tahoe-26-makes-the-mac-more-capable-productive-and-intelligent-than-ever/ | Jun 2025 |
| OS X Daily — shortcuts CLI | https://osxdaily.com/2022/02/28/run-shortcuts-from-the-command-line-on-mac/ | Feb 2022 |
| Six Colors — shortcuts CLI | https://sixcolors.com/post/2021/12/run-shortcuts-from-the-mac-command-line/ | Dec 2021 |
| Six Colors — Shortcuts AppleScript workarounds | https://sixcolors.com/post/2022/01/shortcuts-applescript-terminal-working-around-automation-roadblocks/ | Jan 2022 |
| Tom's Guide — Shortcuts in macOS 26 | https://www.tomsguide.com/computing/software/apples-shortcuts-app-is-getting-a-huge-upgrade-in-ios-26-and-macos-26-heres-how-it-will-help-you | Jun 2025 |
| macOS 26 Tahoe Shortcuts improvements | https://macdownload.informer.com/Mac-Stories/macos-26-tahoe-the-shortcuts-app-improvements.html | Oct 2025 |
| Apple Developer — Creating Launch Daemons and Agents | https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html | 2016 |
| launchd.info primer | https://launchd.info/ | (current) |
| launchd.plist man page | https://www.manpagez.com/man/5/launchd.plist/ | (current) |
| Sweep for Mac — LaunchAgent vs LaunchDaemon | https://www.sweepformac.com/guides/mac-launch-agents-vs-daemons/ | Dec 2025 |
| Apple Developer Forums — LaunchAgent without GUI | https://developer.apple.com/forums/thread/696859 | Jan 2022 |
| Periodic Execution of Shortcuts with launchd — ileif.de | https://en.ileif.de/2024/05/16/periodic-execution-of-apple-shortcuts-with-launchd/ | May 2024 |
| John Dturn — launchd gist | https://gist.github.com/johndturn/09a5c055e6a56ab61212204607940fa0 | Jul 2023 |
| dabrahams — Notes on Apple's launchd | https://gist.github.com/dabrahams/4092951 | 2019 |
| Stack Overflow — launchd log rotation | https://stackoverflow.com/questions/71832882/macos-launchd-fails-to-redirect-stdout-to-the-file-after-log-rotation | Apr 2022 |
| Chris Paynter — macOS daemon TCC | https://chrispaynter.medium.com/what-to-do-when-your-macos-daemon-gets-blocked-by-tcc-dialogues-d3a1b991151f | Feb 2021 |
| dev.to — macOS 26 Tahoe TCC and LaunchDaemon | https://dev.to/linou518/when-macos-26-tahoe-blocked-python-socket-connections-and-how-launchdaemon-fixed-it-3j2i | Mar 2026 |
| allthings.how — macOS 26 App Permissions | https://allthings.how/use-the-enhanced-app-permissions-in-macos-26-tahoe/ | Jun 2025 |
| Apple Discussions — Shortcuts "Operation not permitted" | https://discussions.apple.com/thread/255210852 | Oct 2023 |
| Retrospect — macOS Sequoia/Tahoe Full Disk Access | https://docs.retrospect.com/docs/macos-sequoia-application-data-privacy-full-disk-access | Sep 2024 |
| ShortKit — headless Shortcuts launcher gist | https://gist.github.com/yazanzaid00/34593dced357648d29708b10d39a0cbb | May 2025 |
| Headless Mac server setup — Harshit Chawla | https://chawlaharshit.medium.com/how-i-turned-my-mac-into-a-headless-server-my-always-on-setup-for-ai-monitoring-and-automation-aa9a8ff9aeff | Oct 2025 |
| Apple — What's new in macOS Tahoe 26 updates | https://support.apple.com/en-us/122868 | Jun 2026 |
