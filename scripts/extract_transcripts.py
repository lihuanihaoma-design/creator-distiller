"""
Extract transcripts from videos_details.json and output:
1. Individual .txt files per video
2. transcript_index.json
"""
import json
import os
import re
import sys

# Add project scripts to path for enhanced punctuation restoration
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))
from utils.punctuation_restorer import restore_punctuation_enhanced

DATA_DIR = r"D:\dachaoshuomei_data"
OUTPUT_DIR = r"D:\transcripts"

def safe_filename(text):
    """Remove chars unsafe for filenames"""
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    text = re.sub(r'[\\/*?:"<>|]', '', text)
    # Collapse multiple spaces
    text = re.sub(r' +', ' ', text)
    return text[:80].strip()

def main():
    # Find details file
    details_path = None
    for f in os.listdir(DATA_DIR):
        if 'details' in f.lower() and f.endswith('.json'):
            details_path = os.path.join(DATA_DIR, f)
            break
    
    if not details_path:
        print("ERROR: No details file found")
        sys.exit(1)
    
    print(f"Loading: {details_path}")
    with open(details_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    index_entries = []
    transcribed = 0
    
    for i, entry in enumerate(data, 1):
        video = entry.get('video', {})
        title = video.get('title', '') or entry.get('_title', 'Untitled')
        feed_id = entry.get('_feed_id', f'unknown_{i}')
        interacts = video.get('interactInfo', {})
        likes = interacts.get('likedCount', '0')
        comments = interacts.get('commentCount', '0')
        create_time = video.get('time', '')
        duration = video.get('duration', '')
        
        transcript = entry.get('transcript', {})
        has_text = bool(transcript and transcript.get('text', '').strip())
        
        if not has_text:
            err = entry.get('_transcript_error', 'no_transcript')
            print(f"[{i}] SKIP: {title[:50]} ({err})")
            # Still add to index with empty transcript
            index_entry = {
                "index": i,
                "video_id": feed_id,
                "title": title,
                "publish_date": create_time,
                "likes": str(likes),
                "comments": str(comments),
                "duration": str(duration),
                "transcript_file": None,
                "transcript_word_count": 0,
                "status": err,
            }
            index_entries.append(index_entry)
            continue
        
        # Create filename from title
        filename = safe_filename(title)
        if not filename:
            filename = feed_id
        filename = f"{i:03d}_{filename}.txt"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        # Apply punctuation restoration + trad→simp
        raw_text = transcript.get('text', '')
        clean_text = restore_punctuation_enhanced(raw_text)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(clean_text)
        
        transcribed += 1
        char_diff = f"{len(raw_text)}→{len(clean_text)}" if len(clean_text) != len(raw_text) else f"{len(clean_text)}"
        print(f"[{i}] OK: {filename} ({char_diff} chars)")
        
        index_entry = {
            "index": i,
            "video_id": feed_id,
            "title": title,
            "publish_date": create_time,
            "likes": str(likes),
            "comments": str(comments),
            "duration": str(duration),
            "transcript_file": os.path.join('transcripts', filename),
            "transcript_word_count": transcript.get('word_count', len(raw_text)),
            "transcript_duration_seconds": transcript.get('duration', 0),
            "status": "ok",
        }
        index_entries.append(index_entry)
    
    # Write index
    index_path = os.path.join(OUTPUT_DIR, 'transcript_index.json')
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index_entries, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*60}")
    print(f"Done! {transcribed} transcripts extracted.")
    print(f"Output: {OUTPUT_DIR}")
    print(f"  - {transcribed} .txt files")
    print(f"  - transcript_index.json ({len(index_entries)} entries)")

if __name__ == '__main__':
    main()
