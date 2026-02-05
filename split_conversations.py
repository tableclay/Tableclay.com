"""
Run this on your local machine to split conversations.json into <25MB chunks
for GitHub upload.

Usage:
    python split_conversations.py

Expects conversations.json in the same folder (or your Downloads folder).
Outputs: conversations_part1.json, conversations_part2.json, etc.
"""

import json
import os
import sys

# Try to find conversations.json
paths_to_try = [
    "conversations.json",
    os.path.expanduser("~/Downloads/conversations.json"),
]

input_path = None
for p in paths_to_try:
    if os.path.exists(p):
        input_path = p
        break

if not input_path:
    print("Could not find conversations.json. Place it in the same folder as this script or in ~/Downloads/")
    sys.exit(1)

print(f"Found: {input_path}")
print("Loading...")

with open(input_path, "r", encoding="utf-8") as f:
    conversations = json.load(f)

print(f"Total conversations: {len(conversations)}")

# Split into chunks that stay under 24 MB each (leave buffer)
MAX_BYTES = 24 * 1024 * 1024  # 24 MB
output_dir = os.path.dirname(input_path) if os.path.dirname(input_path) else "."

chunk = []
chunk_num = 1
chunk_size = 0

for convo in conversations:
    convo_json = json.dumps(convo)
    convo_size = len(convo_json.encode("utf-8"))

    if chunk and (chunk_size + convo_size > MAX_BYTES):
        out_path = os.path.join(output_dir, f"conversations_part{chunk_num}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(chunk, f)
        size_mb = os.path.getsize(out_path) / (1024 * 1024)
        print(f"  Wrote {out_path} ({len(chunk)} convos, {size_mb:.1f} MB)")
        chunk = []
        chunk_size = 0
        chunk_num += 1

    chunk.append(convo)
    chunk_size += convo_size

# Write remaining
if chunk:
    out_path = os.path.join(output_dir, f"conversations_part{chunk_num}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(chunk, f)
    size_mb = os.path.getsize(out_path) / (1024 * 1024)
    print(f"  Wrote {out_path} ({len(chunk)} convos, {size_mb:.1f} MB)")

print(f"\nDone! {chunk_num} files created. Upload them all to GitHub.")
