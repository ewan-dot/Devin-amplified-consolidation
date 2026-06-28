#!/usr/bin/env python3
"""Single-pass Inbox Chunker (designed for Hazel or launchd integration).

Accepts a single file path argument, chunks it, prepends YAML headers, 
archives the original, and exits. Zero background memory footprint.
"""
import sys
from pathlib import Path

# Add parent directory to path
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

from inbox_watcher import chunk_file, load_state, save_state, check_beast_database


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 inbox_watcher_single_pass.py <filepath>", file=sys.stderr)
        sys.exit(1)

    target_path = Path(sys.argv[1]).resolve()
    if not target_path.exists():
        print(f"[SINGLE PASS] Error: File does not exist: {target_path}", file=sys.stderr)
        sys.exit(1)

    print(f"[SINGLE PASS] Initiating chunking execution for: {target_path.name}", file=sys.stderr)
    
    # Run pre-flight check (gracefully logs warnings if DB tunnel is closed)
    check_beast_database()

    # Process file using the shared chunking engine
    state = load_state()
    archived_path = chunk_file(target_path, state)
    
    if archived_path:
        save_state(state)
        print("[SINGLE PASS] ✓ Chunking complete.", file=sys.stderr)
        
        # 2. Trigger the debiasing pipeline on the archived file
        debias_script = Path("/Users/ewansair/debias/run.py")
        if debias_script.exists():
            print(f"[SINGLE PASS] -> Triggering debiasing pipeline on: {archived_path.name}...", file=sys.stderr)
            import subprocess
            try:
                # Run the debias script using the same virtualenv interpreter
                python_bin = sys.executable
                subprocess.run(
                    [python_bin, str(debias_script), str(archived_path)],
                    check=True,
                    cwd="/Users/ewansair/debias"  # Cwd so internal imports resolve
                )
                print("[SINGLE PASS] ✓ Debiasing pipeline executed successfully.", file=sys.stderr)
            except Exception as e:
                print(f"[SINGLE PASS] Warning: Debiasing pipeline failed: {e}", file=sys.stderr)
        else:
            print("[SINGLE PASS] Warning: Debias script '/Users/ewansair/debias/run.py' not found. Skipping.", file=sys.stderr)
            
        print("[SINGLE PASS] ✓ Execution complete.", file=sys.stderr)
        sys.exit(0)
    else:
        print("[SINGLE PASS] ❌ Execution failed.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
