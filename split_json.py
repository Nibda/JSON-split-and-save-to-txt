import json
import re
import os

INPUT_FILE = "result.json"
MAX_WORDS = 400_000
OUTPUT_DIR = "."

print("Завантаження файлу...")
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

header = {k: v for k, v in data.items() if k != "messages"}
messages = data["messages"]

print(f"Всього повідомлень: {len(messages)}")

def count_words(obj):
    text = json.dumps(obj, ensure_ascii=False)
    return len(re.findall(r'\S+', text))

parts = []
current_chunk = []
current_words = 0

for i, msg in enumerate(messages):
    w = count_words(msg)
    if current_words + w > MAX_WORDS and current_chunk:
        parts.append(current_chunk)
        current_chunk = [msg]
        current_words = w
    else:
        current_chunk.append(msg)
        current_words += w

    if (i + 1) % 10000 == 0:
        print(f"  Оброблено {i+1}/{len(messages)} повідомлень, частин: {len(parts)+1}")

if current_chunk:
    parts.append(current_chunk)

print(f"\nВсього частин: {len(parts)}")

for idx, chunk in enumerate(parts, 1):
    out = dict(header)
    out["messages"] = chunk
    filename = os.path.join(OUTPUT_DIR, f"result_part{idx:02d}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    word_count = count_words(out)
    print(f"  {filename}: {len(chunk)} повідомлень, ~{word_count:,} слів")

print("\nГотово!")
