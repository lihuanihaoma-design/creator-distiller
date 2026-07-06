<div align="center">

# 🫗 Blogger Distiller (博主万能蒸馏器)

> *"Stop wasting time scrolling. Distill any Douyin, Xiaohongshu, or Twitter/X creator into your local LLM and extract their cognitive OS in seconds."*

[简体中文](README.md) | English

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![RAG-Ready](https://img.shields.io/badge/RAG-Ready-green.svg)](#-capabilities)
[![Local-First](https://img.shields.io/badge/Local-First-blue.svg)](#⚡-installation--usage)
[![Zero-Cookie](https://img.shields.io/badge/Zero--Cookie-Twitter/X-orange.svg)](#-why-it-is-insanely-great)

<br>

**Creators are the cognitive amplifiers of our generation. 「Blogger Distiller」 is the high-power suction pump that extracts their mental assets directly to your machine.**

No Cookies or login sessions are required, and there's absolutely no risk of account bans. Simply input any creator's username, and watch the pipeline automatically, stealthily, and silently "drain" their entire historical posts, video transcripts, high-resolution media, and reader hot-takes into highly structured Markdown files. Build your high-fidelity local RAG knowledge base in minutes.

[Live Examples](#⚡-live-rag-examples) · [Why It's Insanely Great](#🔥-why-it-is-insanely-great) · [Installation & Usage](#⚡-installation--usage) · [Featured Case Study](#⚡-featured-case-study-dachao-matchmaker) · [Roadmap](#🚧-roadmap)

<br>

[![Star History Chart](https://api.star-history.com/svg?repos=lihuanihaoma-design/creator-distiller&type=Date)](https://star-history.com/#lihuanihaoma-design/creator-distiller&Date)

</div>

---

## ⚡ Live RAG Examples

This is not simple role-playing or a quote-reciter. This is what happens when you feed Blogger Distiller's raw Markdown output to your local LLM (such as GPT-4o or Claude 3.5), allowing them to use their genuine cognitive frameworks and expression DNA to solve your real problems:

```
User      ❯ DaChao, evaluate this match: Female 30, English teacher, Hangzhou local, middle-class. Male 31, Software Engineer, humble village background, owns apartment with mortgage.

DaChao    ❯ My brother, your ¥350k salary is useless if you don't talk to her. Close your laptop and go travel with her. 
            
            And girl, don't look down on his village roots. This guy didn't buy a Hangzhou apartment by slacking off; he is reliable. 
            
            Match rating: 75%. This is a high-potential combination worth fighting for. Mutual accommodation! Go for it!
```

Or a marketing/SaaS consultation with distilled influencer `@dontbesilent`:

```
User      ❯ I wrote a lot of deep technical articles about LLMs, but why am I not getting any followers or sales?

dontbesilent ❯ You completely fail to distinguish between a "Question" and a "Pain Point."
               
               Writing about "LLM parameters, Transformer architecture" — that is just a Question.
               Your user's actual pain point is "Anxiety, feeling that their current job has no future."
               
               Stop hammering on code and tech; think about how to knock on their closed doors. 
               The human brain gets to know you through pain, not through happiness. 
               Let your content relieve their pain, rather than teach them how to be happy. Got it?
```

---

## 🎯 Capabilities

| You Input | It Delivers | Key Breakthrough |
|-----------|----------|------------------|
| **Twitter/X Username** | High-fidelity Markdown posts with YAML Metadata + local images + sorted replies thread | 💡 **100% Zero-Cookie, No-Login, Stealth-Slicing**, completely bypasses modern anti-bot blocks |
| **Douyin (抖音) Creator ID** | `{Title}.txt` × N high-precision, punctuated, simplified Chinese transcripts | 💡 **100% Free.** Directly extracts audio streams with zero disk residues, auto-resumes on crashes |
| **Xiaohongshu (小红书) URL** | Full note bodies + multi-image local downloads + tag organization | 💡 Preserves original layout and visual fidelity |
| **YouTube Channel** | Automated audio ripping + local Whisper transcription pipelines (Planned) | 💡 Smooth one-click processing |

---

## 🔥 Why It Is Insanely Great?

In 2026, almost every public Twitter/X scraper and archiver on GitHub has run into a dead-end: **session bans, rate-limits, and frequent HTTP 400 Bad Request errors**. We solved this by completely rewriting the collection architecture:

### 1. Advanced Search Date Slicing (Zero-Cookie / Zero-Browser) 🛡️
No longer relying on fragile `next_cursor` tokens that get immediately flagged. We divide the historical timeline into **37 precise 15-day intervals**, utilizing targeted `from:username since:YYYY-MM-DD until:YYYY-MM-DD` queries.
* **Result**: Achieves 100% stable, un-throttled, un-authenticated crawling. No more 400 errors.

### 2. Multi-Modal Streaming Sync & Checkpoints 💾
We don't cache datasets in Python memory. Each time a tweet is parsed, the Markdown and high-res images are **instantly flushed to disk**.
* **Result**: If the network hiccups, restarting the script immediately scans the folder, identifies completed MD files, and **skips them in milliseconds — saving you 100% of your TikHub API credits**.

### 3. High-Value Reader Reply Harvesting 💬
Most creators are restricted by character limits. The most valuable debates, critiques, and follow-up ideas actually live in their comment sections. We automatically crawl and **sort the top 15 high-engagement replies, appending them as valuable contextual groundings in the Markdown**.
* **Result**: Provides the LLM with full social context and surrounding debates, doubling the cognitive depth of the resulting RAG agent.

---

## ⚡ Installation & Usage

### 1. Installation
```bash
# Clone
git clone https://github.com/lihuanihaoma-design/creator-distiller.git
cd creator-distiller

# Install dependencies
pip install -r requirements.txt

# Install ffmpeg on your system (mandatory)
# macOS: brew install ffmpeg  |  Windows: winget install Gyan.FFmpeg
```

### 2. Configure TikHub API Token
1. Go to [https://user.tikhub.io](https://user.tikhub.io) and register for free.
2. Copy your API Token from the dashboard.
3. Write it into the system configuration:
   ```bash
   python -c "
   import json, os
   cfg = os.path.join(os.path.expanduser('~'), '.xiaohongshu', 'tikhub_config.json')
   os.makedirs(os.path.dirname(cfg), exist_ok=True)
   json.dump({'tikhub_api_token': 'YOUR_TOKEN'}, open(cfg, 'w'))
   "
   ```

### 3. Run It!
```bash
# 1. Distill Twitter/X Creator (e.g., dontbesilent)
python scripts/distill_twitter.py dontbesilent

# 2. Distill Douyin Creator (e.g., Creator Page URL)
python scripts/retry_ytdlp.py "Douyin creator page link or video URL"
```
You will immediately get a beautifully organized, multi-modal local Markdown knowledge folder.

---

## 🔧 How It Works

Blogger Distiller is split into two specialized pipeline architectures tailored directly for Large Language Models (LLM):

### 📺 Video Transcription Pipeline (Douyin/Xiaohongshu)
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌──────────────┐
│  TikHub API  │───▶│   yt-dlp    │───▶│   Whisper    │───▶│  Punctuation  │
│  Metadata   │    │  Audio Ripping│    │  Speech-2-Text│    │  Restoration  │
└─────────────┘    └─────────────┘    └─────────────┘    └──────────────┘
```
* **yt-dlp Real-Time Parsing**: Completely avoids expired CDN link traps. Directly streams the audio tracks locally on-the-fly, forever free.
* **Simplified Conversion & Punctuation Restoration**: Whisper's output lacks proper breaks. Our custom restorer injects standard commas, periods, and question marks into the text flow.

### 🐦 Tweet Harvesting Pipeline (Twitter/X)
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌──────────────┐
│ 15-Day Date │───▶│  Stealth     │───▶│  Media      │───▶│ Comments Sync│
│ Slicing     │    │  Querying    │    │ Localizer   │    │ and Merge    │
└─────────────┘    └─────────────┘    └─────────────┘    └──────────────┘
```
* **Full-Resolution Media Downloads**: Automatically grabs high-res `.jpg` files without Twitter's thumbnail limits, embedding local relative links inside the Markdown output.
* **Interactive Thread Merging**: Crawls the top 15 replies/comments including their likes, giving your RAG model valuable crowd context.

---

## 📂 File Structure

```
blogger-distiller/
├── README.md                          ← Chinese Version
├── README_EN.md                       ← You are here
├── SKILL.md                           ← Agent Skill Definition
├── scripts/
│   ├── distill_twitter.py             ← Twitter/X Date-Sliced Advanced Search Engine (TikHub)
│   ├── extract_transcripts.py         ← Metadata extraction + Punctuation Restorer
│   ├── retry_ytdlp.py                 ← yt-dlp audio downloader + Whisper engine
│   └── utils/
│       ├── punctuation_restorer.py    ← Chinese punctuation injection
│       └── transcript.py             ← Whisper integration wrapper
└── requirements.txt
```

---

## ⚡ Featured Case Study: "DaChao Matchmaker"

<details>
<summary>Click to Expand ➡️ How to use the distilled transcripts to build a real-world Matchmaking AI Agent</summary>

### 1. Distilled Knowledge Sample
Our tool automatically converts history transcripts into clean Markdown:
```markdown
---
id: "2058011944897097845"
created_at: "Sat May 23 02:27:38"
likes: 53
reposts: 3
bookmarks: 29
---
# Tweet Body
IT programmer (village-rooted, ¥350k, mortgage) vs local teacher (middle-class, local, ¥120k)...
...
## Top Replies
- @stometaverse: Spot on! Serving similar users is the core heuristic.(👍 3)
```

### 2. Building the "Digital DaChao" Prompt
Feed this prompt and your generated Markdown folder into any LLM:
```markdown
System Prompt: You are "Digital DaChao" (数字大超), the matchmaking expert. Based on the [Context Cases] provided, evaluate the matchmaking compatibility of Couples with your real-world pragmatic logic, age/location standards, and direct-yet-constructive humor.

Tone & Style:
1. Marriage is a team partnership of assets, not romance.
2. Be extremely blunt, practical, and funny. No sugarcoating.
3. Use local keywords: "向下兼容" (marrying down), "相亲市场香饽饽" (highly sought-after), "情绪价值" (emotional value).
```

### 3. Output Example
* **Couple Input**: Male 31, Senior Engineer, non-local, ¥350k, owned condo with mortgage, introverted; Female 30, high school teacher, local middle-class, ¥120K, outgoing.
* **AI Agent Output**:
  > "My brother, your ¥350k salary is useless if you don't talk to her. Close your laptop, buy a ticket, and go travel with her. 
  > And girl, do not look down on his village roots. He bought an apartment in Hangzhou by himself; he is reliable. 
  > Match Rating: 75%. An excellent pragmatic match, highly worth fighting for!"

</details>

---

## 🚧 Roadmap

- [x] Douyin metadata collection and high-fidelity video transcripts pipeline
- [x] Twitter/X advanced search date-sliced engine (with images and reply threads)
- [x] Local incremental backup (100% duplicate-billing prevention)
- [ ] YouTube video-to-transcript automated pipelines
- [ ] Xiaohongshu note extraction and local image downloads
- [ ] One-click Dockerized containerization

---

## ⚖️ License

MIT License — feel free to use, modify, and distribute. If you find this project insanely great, please give us a **Star ⭐️**!

<div align="center">
<sub>built with ☕ and a lot of 🚀 Blogger Distiller</sub>
</div>
