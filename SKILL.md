---
name: douyin-transcriber
description: Use when needing to batch-download Douyin videos from a blogger account, transcribe speech to text via Whisper, restore Chinese punctuation, and export clean .txt transcripts with metadata index
---

# Douyin Video Transcription Pipeline

## Overview

End-to-end pipeline: crawl Douyin video metadata → download audio → Whisper transcription → Chinese punctuation restoration → export clean transcripts.

**Core insight:** TikHub API for metadata + yt-dlp for audio (CDN links expire). Never use TikHub's
`videoUrl` for batch transcription — URLs die after ~30 minutes.

## Prerequisites

**Repo dependency:** Clone `https://github.com/otter1101/blogger-distiller` first. All scripts
live under its `scripts/` and root directory.

```bash
git clone https://github.com/otter1101/blogger-distiller.git
cd blogger-distiller
pip install openai-whisper zhconv yt-dlp python-docx
```

**ffmpeg** must be on PATH. On Windows: `winget install Gyan.FFmpeg`.

**TikHub API token** required for metadata collection. Register at https://user.tikhub.io, top up
pay-as-you-go (~¥5 per 100 videos), generate token.

## Pipeline Steps

### Step 1: Collect Metadata (TikHub)

Use `blogger-distiller/scripts/crawl_douyin.py`. Save token first:

```python
import json, os
cfg_path = os.path.join(os.path.expanduser('~'), '.xiaohongshu', 'tikhub_config.json')
os.makedirs(os.path.dirname(cfg_path), exist_ok=True)
with open(cfg_path, 'w') as f:
    json.dump({'tikhub_api_token': 'YOUR_TOKEN'}, f)
```

Run without `--transcript` (collect metadata only, fast):

```bash
python scripts/crawl_douyin.py "博主名" \
  --user-id "MS4wLjAB..." \
  --max-videos 200 \
  -o "D:/output_dir"
```

Output: `{name}_videos_details.json` (titles, likes, comments, video IDs, CDN URLs).

**Find `--user-id`:** search returns candidates; use the `sec_uid` from `_profile.json`. Or run
once without `--user-id` and copy from the printed output.

### Step 2: Download Audio + Transcribe (yt-dlp + Whisper)

Use `retry_ytdlp.py` pattern — yt-dlp downloads from Douyin by video ID, no expiry:

```python
import subprocess, sys

def download_audio(video_id: str, output_dir: str) -> str | None:
    url = f"https://www.douyin.com/video/{video_id}"
    out_tmpl = os.path.join(output_dir, "%(id)s.%(ext)s")
    subprocess.run([
        sys.executable, "-m", "yt_dlp",
        "-x", "--audio-format", "mp3",
        "-o", out_tmpl,
        "--no-playlist",
        "--socket-timeout", "15",
        "--retries", "2",
        url,
    ], capture_output=True, timeout=45, check=True)
    mp3_path = os.path.join(output_dir, f"{video_id}.mp3")
    return mp3_path if os.path.isfile(mp3_path) else None
```

Then transcribe with Whisper (save after EACH video to survive crashes):

```python
from utils.transcript import get_whisper_model, transcribe_from_url

model = get_whisper_model()  # uses model from config, default 'small'
result = transcribe_from_url(mp3_path, model=model)
entry['transcript'] = result
save_json(data_file, data)  # save immediately
```

**Key practices:**
- Model: `small` (CPU-safe, ~30s/video, ~85% accurate for Mandarin)
- Process one video at a time, save after each — crash recovery free
- Delete mp3 after transcription to save disk
- No consecutive-failure abort — yt-dlp is reliable

### Step 3: Restore Punctuation

Whisper outputs continuous text without punctuation. Use `scripts/utils/punctuation_restorer.py`:

```python
from utils.punctuation_restorer import restore_punctuation_enhanced

raw = entry['transcript']['text']
clean = restore_punctuation_enhanced(raw)  # trad→simp + 。？， injection
```

What it does:
1. Traditional Chinese → Simplified (zhconv)
2. 吗/呢/嘛/吧 → ？
3. 啊/呀/哦/哈/啦 → 。
4. 但是/所以/不过/当然/其实 → ，
5. Collapse duplicate punctuation (。，→ 。)
6. Ensure text ends with punctuation

### Step 4: Export Transcripts

Write each video's transcript to a `.txt` file, generate `transcript_index.json`:

```python
# Filename: {index:03d}_{safe_title}.txt
filename = f"{i:03d}_{safe_title}.txt"

# Index entry per video:
{
    "index": i,
    "title": "...",
    "video_id": "...",
    "publish_date": "...",
    "likes": "1234",
    "comments": "56",
    "duration": "45",
    "transcript_file": "output_dir/001_title.txt",
    "transcript_word_count": 350,
    "status": "ok"
}
```

## Environment Config

`~/.xiaohongshu/tikhub_config.json`:

```json
{
  "tikhub_api_token": "...",
  "whisper_available": true,
  "whisper_model": "small",
  "ffmpeg_path": "C:/path/to/ffmpeg.exe"
}
```

## Quick Reference

| Tool | Role | Cost |
|------|------|------|
| TikHub API | Video metadata (title/likes/comments/IDs) | ¥0.03-0.05/video |
| yt-dlp | Download audio from Douyin | Free |
| openai-whisper | Speech-to-text (small model) | Free (local CPU) |
| zhconv | Traditional→Simplified | Free |
| ffmpeg | Audio extraction/format conversion | Free |

## Common Mistakes

1. **Using TikHub CDN URLs for transcription** — they expire in ~30 min. Always use yt-dlp.
2. **Not saving after each video** — crash loses all in-memory transcripts. Save incrementally.
3. **medium model on CPU** — segfault on longer videos. Stick to `small` for CPU.
4. **Skipping punctuation restoration** — raw Whisper output is unreadable continuous text.
5. **Not handling newlines in titles** — `\n` in titles break filenames. Strip them.

## Recovery

If crash mid-transcription:
- Load `_videos_details.json`, find entries with `_transcript_error` but no `transcript`
- Re-run yt-dlp + Whisper on just those entries
- The save-after-each pattern means completed entries are safe

## Scripts Reference

All in `blogger-distiller/`:
- `scripts/crawl_douyin.py` — metadata collection (requires TikTokHub)
- `retry_ytdlp.py` — yt-dlp + Whisper batch transcription
- `extract_transcripts.py` — export .txt + index.json with punctuation restoration
- `scripts/utils/punctuation_restorer.py` — Chinese punctuation injection module
- `scripts/utils/transcript.py` — Whisper integration (ffmpeg, download, transcribe)
