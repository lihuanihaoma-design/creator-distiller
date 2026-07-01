"""
Retry failed transcriptions using yt-dlp to download video audio,
then Whisper to transcribe. Saves after each success.
"""
import json, os, sys, time, subprocess, tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))
from utils.transcript import get_whisper_model, transcribe_from_url, _ensure_ffmpeg_in_path

DATA_FILE = r"D:\yuelaodachao_data\大超说媒2号（6.21北京端午节大集）_videos_details.json"
AUDIO_DIR = r"D:\yuelaodachao_audio"

def save():
    tmp = DATA_FILE + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, DATA_FILE)

def download_audio(video_id: str) -> str | None:
    """Download Douyin video audio via yt-dlp. Returns mp3 path or None."""
    url = f"https://www.douyin.com/video/{video_id}"
    out_tmpl = os.path.join(AUDIO_DIR, f"%(id)s.%(ext)s")
    os.makedirs(AUDIO_DIR, exist_ok=True)
    
    try:
        subprocess.run([
            sys.executable, "-m", "yt_dlp",
            "-x", "--audio-format", "mp3",
            "-o", out_tmpl,
            "--no-playlist",
            "--socket-timeout", "15",
            "--retries", "2",
            url,
        ], capture_output=True, timeout=45, check=True)
        mp3_path = os.path.join(AUDIO_DIR, f"{video_id}.mp3")
        if os.path.isfile(mp3_path) and os.path.getsize(mp3_path) > 1000:
            return mp3_path
    except Exception as e:
        print(f"    yt-dlp error: {str(e)[:80]}")
    return None

# ── Main ──
print(f"Loading: {DATA_FILE}")
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find entries that need retry (download_failed)
retry = [(i, e) for i, e in enumerate(data) 
         if e.get('_transcript_error') == 'download_failed' and not e.get('transcript')]
print(f"Failed entries to retry: {len(retry)}")

if not retry:
    print("Nothing to retry!")
    sys.exit(0)

if not _ensure_ffmpeg_in_path():
    print("ERROR: ffmpeg not found")
    sys.exit(1)

model = get_whisper_model()
if not model:
    print("ERROR: Whisper not loaded")
    sys.exit(1)

new_ok = 0
new_fail = 0
t0_total = time.time()

for idx, (i, entry) in enumerate(retry, 1):
    n = i + 1
    vid = entry.get('_feed_id', '')
    title = entry.get('video', {}).get('title', '')[:45]
    
    print(f"[{idx}/{len(retry)}] (global #{n}) 🎬 {title}")
    
    # Download
    mp3 = download_audio(vid)
    if not mp3:
        entry['_transcript_error'] = 'ytdlp_download_failed'
        new_fail += 1
        save()
        continue
    
    # Transcribe
    try:
        print(f"    🎙 transcribing...", end='', flush=True)
        t0 = time.time()
        result = transcribe_from_url(mp3, model=model)
        elapsed = time.time() - t0
        
        if result and result.get('text', '').strip():
            wc = result['word_count']
            print(f" ✅ ({elapsed:.0f}s, {wc} chars)")
            entry['transcript'] = result
            del entry['_transcript_error']
            new_ok += 1
        else:
            print(f" ⚠️ empty")
            entry['_transcript_error'] = 'ytdlp_transcribe_empty'
            new_fail += 1
    except Exception as e:
        print(f" ❌ {str(e)[:50]}")
        entry['_transcript_error'] = f'ytdlp_exception:{str(e)[:60]}'
        new_fail += 1
    finally:
        # Clean up mp3
        if mp3 and os.path.isfile(mp3):
            try:
                os.unlink(mp3)
            except:
                pass
        save()
    
    if (new_ok + new_fail) % 10 == 0:
        elapsed_total = time.time() - t0_total
        eta = elapsed_total / (new_ok + new_fail) * (len(retry) - new_ok - new_fail) if (new_ok + new_fail) > 0 else 0
        print(f"  --- progress: {new_ok}✅ {new_fail}❌ | {elapsed_total:.0f}s elapsed | ~{eta:.0f}s remaining ---")

total_elapsed = time.time() - t0_total
print(f"\n{'='*60}")
print(f"Retry done! New OK: {new_ok}, New Fail: {new_fail}")
print(f"Total: {total_elapsed:.0f}s ({total_elapsed/60:.1f}min)")
save()
print(f"Saved: {DATA_FILE}")
