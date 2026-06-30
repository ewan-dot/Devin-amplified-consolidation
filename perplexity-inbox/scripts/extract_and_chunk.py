#!/usr/bin/env python3
import os
import json
import re
from pathlib import Path

# Chronological order of the last 15 parent user sessions (oldest first)
CONVERSATIONS = [
    "b7f781c8-d937-46b5-ac20-06ae91f64f9d", # 15
    "57358f82-35b1-4179-b78f-4499cfafd088", # 14
    "25bc9838-275b-4c2c-b54e-cf7454a2ba63", # 13
    "e07b0a40-f62a-426f-9c1b-a7da8e348fad", # 12
    "20407f71-3240-4b0a-9112-a6b41db67234", # 11
    "621629b6-569d-4248-ac9f-f44c1c03cbb6", # 10
    "a3fb2a4c-0b97-48a0-81af-8ee11c0ee103", # 9
    "f6cdf6bf-27aa-411d-86ef-71104756b25c", # 8
    "b7553b84-08b8-43ed-8fb9-f43c201ca9e3", # 7
    "615d6e08-74f2-49ce-8cd8-7b43679bfa42", # 6
    "4803d293-5f46-4c93-98b5-c01cca39a54f", # 5
    "3ed1b0b1-2c97-41c6-94de-b62385ec4a87", # 4
    "b96f63ef-daab-428e-9fbe-ae02f02eb504", # 3
    "6ff55ae9-48dc-4d0c-a6ff-ef549fe0bb9c", # 2
    "b3c6cad8-d782-4797-9d9d-51ed1b80c200"  # 1 (Current)
]

BRAIN_DIR = Path("/Users/ewansair/.gemini/antigravity/brain")
TARGET_DIR = Path("/Users/ewansair/ingestion-to-research-pipe/backward_consolidation_2026-06-30")
RAW_CHUNKS_DIR = TARGET_DIR / "raw_chunks"

def clean_content(text: str) -> str:
    """Removes user request tags, system prompts, or metadata headers."""
    text = re.sub(r"<USER_REQUEST>\s*", "", text)
    text = re.sub(r"\s*</USER_REQUEST>", "", text)
    text = re.sub(r"<ADDITIONAL_METADATA>.*?</ADDITIONAL_METADATA>", "", text, flags=re.DOTALL)
    text = re.sub(r"<USER_SETTINGS_CHANGE>.*?</USER_SETTINGS_CHANGE>", "", text, flags=re.DOTALL)
    return text.strip()

def extract_dialogue_blocks(conv_id: str) -> list:
    """Reads transcript logs and extracts individual dialogue blocks chronologically."""
    log_dir = BRAIN_DIR / conv_id / ".system_generated" / "logs"
    jsonl_path = log_dir / "transcript_full.jsonl"
    if not jsonl_path.exists():
        jsonl_path = log_dir / "transcript.jsonl"
    
    if not jsonl_path.exists():
        print(f"[WARN] Transcript files not found for {conv_id}")
        return []
        
    print(f"[EXTRACT] Parsing session: {conv_id}...")
    blocks = []
    
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
                step_type = data.get("type")
                source = data.get("source")
                content = data.get("content", "")
                
                if step_type == "USER_INPUT":
                    cleaned = clean_content(content)
                    if cleaned:
                        blocks.append(f"### USER (Session {conv_id[:8]})\n{cleaned}")
                elif source == "MODEL" and step_type == "PLANNER_RESPONSE":
                    cleaned = clean_content(content)
                    if cleaned:
                        blocks.append(f"### ASSISTANT (Session {conv_id[:8]})\n{cleaned}")
            except Exception as e:
                print(f"[ERROR] Error parsing line in {conv_id}: {e}")
                
    return blocks

def main():
    RAW_CHUNKS_DIR.mkdir(parents=True, exist_ok=True)
    
    all_blocks = []
    for conv_id in CONVERSATIONS:
        blocks = extract_dialogue_blocks(conv_id)
        if blocks:
            # Insert a marker indicating the boundary of a session
            all_blocks.append(f"<!-- SESSION_START: {conv_id} -->")
            all_blocks.extend(blocks)
            all_blocks.append(f"<!-- SESSION_END: {conv_id} -->")
            
    if not all_blocks:
        print("[ERROR] No dialogue blocks extracted. Exiting.")
        return
        
    print(f"[INFO] Total dialogue blocks extracted: {len(all_blocks)}")
    
    # Target chunk character length: 12000 characters
    # Target overlap percentage: 15% (approx 1800 characters)
    target_size = 12000
    overlap_pct = 0.15
    
    chunks = []
    start_idx = 0
    num_blocks = len(all_blocks)
    
    while start_idx < num_blocks:
        # Accumulate blocks until we exceed target_size
        current_len = 0
        end_idx = start_idx
        
        while end_idx < num_blocks:
            block_content = all_blocks[end_idx]
            block_len = len(block_content)
            current_len += block_len
            end_idx += 1
            
            # Semantic Dialog Turn Splitting:
            # Only split if we have met the size threshold and the NEXT block starts a new dialog turn (USER)
            # This ensures each chunk ends on an ASSISTANT response, containing complete turns.
            if current_len >= target_size:
                if end_idx < num_blocks:
                    next_block = all_blocks[end_idx]
                    if next_block.startswith("### USER") or next_block.startswith("<!-- SESSION_START"):
                        break
        
        # Capture the chunk content
        chunk_content = "\n\n".join(all_blocks[start_idx:end_idx])
        chunks.append({
            "content": chunk_content,
            "length": len(chunk_content)
        })
        
        if end_idx >= num_blocks:
            break
            
        # Determine the 15% sliding window overlap starting index for the next chunk
        overlap_target_len = int(len(chunk_content) * overlap_pct)
        
        # Traverse backward to find a USER block or SESSION_START block that meets the overlap target length
        next_start_idx = end_idx - 1
        acc_overlap_len = 0
        found_overlap_start = False
        
        while next_start_idx > start_idx:
            acc_overlap_len += len(all_blocks[next_start_idx])
            # The next chunk should start with a USER block or SESSION_START block, and satisfy overlap length
            is_valid_start = (
                all_blocks[next_start_idx].startswith("### USER") or 
                all_blocks[next_start_idx].startswith("<!-- SESSION_START")
            )
            if is_valid_start and acc_overlap_len >= overlap_target_len:
                found_overlap_start = True
                break
            next_start_idx -= 1
            
        if found_overlap_start:
            start_idx = next_start_idx
        else:
            # Fallback: find the closest USER block going backward
            fallback_found = False
            for fallback_idx in range(end_idx - 1, start_idx, -1):
                if all_blocks[fallback_idx].startswith("### USER") or all_blocks[fallback_idx].startswith("<!-- SESSION_START"):
                    start_idx = fallback_idx
                    fallback_found = True
                    break
            if not fallback_found:
                start_idx = end_idx  # No overlap if no boundary found
                
    total_chunks = len(chunks)
    print(f"[INFO] Generated {total_chunks} chunks.")
    
    for idx, ch in enumerate(chunks, 1):
        chunk_filename = f"chunk_{idx:02d}.txt"
        chunk_path = RAW_CHUNKS_DIR / chunk_filename
        
        prev_chunk = f"chunk_{idx-1:02d}.txt" if idx > 1 else "null"
        next_chunk = f"chunk_{idx+1:02d}.txt" if idx < total_chunks else "null"
        
        header = (
            "---\n"
            f"chunk_index: {idx}\n"
            f"total_chunks: {total_chunks}\n"
            f"previous_chunk: \"{prev_chunk}\"\n"
            f"next_chunk: \"{next_chunk}\"\n"
            f"content_length: {ch['length']}\n"
            "---\n\n"
        )
        
        with open(chunk_path, "w", encoding="utf-8") as f_out:
            f_out.write(header + ch["content"])
            
    print(f"[SUCCESS] Wrote {total_chunks} chunks to {RAW_CHUNKS_DIR}")

if __name__ == "__main__":
    main()

