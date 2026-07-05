<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h1>🫗 博主万能蒸馏器</h1>
  <h3>Creator Distiller</h3>
  <p>
    一键蒸馏任意抖音 / 小红书 / YouTube 博主<br/>
    从视频到逐字稿，从口播到结构化文本<br/>
    <strong>零成本起步，一个 pip install 就开干</strong>
  </p>
  <br />
  <p>
    <a href="#-能干什么">能干什么</a>
    ·
    <a href="#-两分钟上手">两分钟上手</a>
    ·
    <a href="#-管道详解">管道详解</a>
    ·
    <a href="#-输出物">输出物</a>
  </p>
</div>

---

## 🧠 一句话

> 给一个博主名字，还你 100 条高质量中文逐字稿。**不花一分钱。**

## 🎯 能干什么

| 你扔进来 | 它还给你 |
|-----------|----------|
| 抖音博主链接 / ID | `{标题}.txt` × N，标点完整、繁转简 |
| 小红书博主主页 | 同上 + 小红书笔记正文 |
| Twitter/X 账号用户名 | 全量推文、高清图片及高赞评论归档的带 YAML Metadata 的 Markdown 知识库 |
| YouTube 频道 | 同上（计划中） |
| `--max-videos 200` | 200 条口播逐字稿，带点赞/评论/时长索引 |

**核心场景：**
- 研究某个博主的"话术体系"——他翻来覆去到底在说什么
- 批量分析内容打法——标题、选题、情绪曲线
- LLM 二次加工——摘要、分类、情感分析、风格模仿

## ⚡ 两分钟上手

> **默认路径：纯免费。** yt-dlp 直接下载 + Whisper 转写，不注册任何平台。

```bash
# 1. 克隆 + 安装
git clone https://github.com/lihuanihaoma-design/creator-distiller.git
cd creator-distiller
pip install openai-whisper zhconv yt-dlp python-docx

# ffmpeg 也要装
# macOS:  brew install ffmpeg
# Windows: winget install Gyan.FFmpeg
# Linux:  apt install ffmpeg

# 2. 跑！
python scripts/transcribe_douyin.py "https://www.douyin.com/user/xxx" \
  --max-videos 100 \
  -o ./output
```

**30 分钟后**，`./output/` 里全是逐字稿。100 条视频，零元。

> 💡 **进阶：需要标题、点赞、评论等结构化元数据？** 见下方 [Layer 1——元数据增强](#layer-1--元数据增强tikhub-可选)。

---

## 🔧 管道详解

```
┌──────────────────────┐    ┌─────────────────┐    ┌──────────────────┐
│       yt-dlp         │───▶│     Whisper      │───▶│   Punctuation    │
│   音频下载（主路径）   │    │   语音转文字      │    │   标点 + 繁简     │
│   免费 ∞ 永不过期     │    │   免费 (CPU)      │    │   免费            │
└──────────────────────┘    └─────────────────┘    └──────────────────┘
         │                                                    │
         │  🆙 可选增强                                        │
         ▼                                                    ▼
┌──────────────────────┐                         ┌──────────────────────┐
│     TikHub API       │                         │     ./output/        │
│  元数据（标题/点赞/    │                         │  ├── 001_xxx.txt     │
│  评论/发布时间）      │                         │  ├── 002_xxx.txt     │
│  ¥0.03/条（可选）    │                         │  └── index.json      │
└──────────────────────┘                         └──────────────────────┘
```

### Layer 1——音频下载（yt-dlp）⭐ 主路径

**这是默认推荐路径。免费、稳定、不需要任何 API Key。**

> ⚠️ **为什么不推荐 TikHub 的视频直链？**  
> TikTok CDN 链接 30 分钟过期。100 条视频转写要跑 1 小时，后半段全部 404。  
> **yt-dlp 每次实时解析抖音页面**，永不过期，零费用。

- 从 Douyin / 小红书网页提取真实视频地址
- 只下载音频轨道（`-x --audio-format mp3`）
- 逐条下载 → 转写 → 删 mp3，磁盘零残留
- 支持：抖音、小红书、YouTube、B站……yt-dlp 支持的都行

```python
# 核心就这两行
import yt_dlp
yt_dlp.YoutubeDL({'-x': True, '--audio-format': 'mp3'}).download([url])
```

### Layer 1½——元数据增强（TikHub）🆙 可选

> 不需要也可以跑完全流程。需要标题/点赞/评论时才开。

- 自动搜索博主 → 模糊匹配 → 获取 `sec_uid`
- 翻页拉取全部视频列表（标题、点赞、评论数、video ID）
- 拉取每条视频详情 + 前 20 条热门评论
- 端点自动探测：哪个端点能用就用哪个，自动降级
- 注册：https://user.tikhub.io（免费注册，按量付费，¥5 够采 100 条）

### Layer 2——语音转文字（Whisper）

- 模型：`small`（CPU 可用，中文准确率 ~85%，~30s/条）
- 逐条转写 + 每条存盘 → 崩溃零丢失
- 超过 10 分钟的视频自动跳过（抖音口播很少超）

### Layer 3——中文后处理

Whisper 输出是连续汉字，没有标点。这一层做：

| 输入 | 输出 |
|------|------|
| `男女审美真的是不一样啊只是建议啊没别的意思` | `男女审美真的是不一样啊。只是建议啊。没别的意思。` |
| `但是你别和夜场女生风格一样` | `，但是你别和夜场女生风格一样。` |
| `明白我啥意思吗男生还是喜欢牛仔裤` | `明白我啥意思吗？男生还是喜欢牛仔裤。` |
| `發現一個現象` | `发现一个现象`（繁体 → 简体）|

## 📦 输出物

```
output/
├── 001_穿衣自由没毛病就当我胡说八道了.txt
├── 002_在婚姻这一块男生从来不慕强.txt
├── ...
├── 100_杭州第四场活动.txt
└── transcript_index.json
```

**`transcript_index.json`** 每条记录（元数据需开启 TikHub）：

```json
{
  "index": 1,
  "title": "穿衣自由没毛病，就当我胡说八道了",
  "video_id": "7578007750...",
  "publish_date": "2025-03-15",
  "likes": "14834",
  "comments": "326",
  "duration": "93",
  "transcript_file": "output/001_穿衣自由没毛病.txt",
  "transcript_word_count": 353,
  "status": "ok"
}
```

## 🧪 实战数据

| 博主 | 平台 | 视频数 | 转写成功率 | 总字数 | 花费 |
|------|------|--------|-----------|--------|------|
| 大超说媒（主号） | 抖音 | 19 | 95% | ~6,000 | ¥0 |
| 大超说媒 2 号 | 抖音 | 101 | 100% | ~24,000 | ¥0 |
| **合计** | | **120** | **99.2%** | **~30,000** | **¥0** |

> 💸 纯 yt-dlp 路径：零元。开了 TikHub 元数据：¥5 够采 100 条。

## 📂 文件结构

```
creator-distiller/
├── README.md                          ← 你在看的
├── SKILL.md                           ← Agent 可复用的技能定义
├── scripts/
│   ├── distill_twitter.py             ← Twitter/X 极速高级搜索时间切片蒸馏脚本（TikHub）
│   ├── extract_transcripts.py         ← 从 JSON 提取逐字稿 + 标点恢复 + 生成索引
│   ├── retry_ytdlp.py                 ← yt-dlp 下载音频 + Whisper 转写（崩溃可恢复）
│   └── utils/
│       ├── punctuation_restorer.py    ← 中文标点自动注入 + 繁转简
│       └── transcript.py             ← Whisper 集成（需从 blogger-distiller 获取）
└── requirements.txt
```

> **依赖说明**：`transcript.py` 来自 [otter1101/blogger-distiller](https://github.com/otter1101/blogger-distiller)，提供 Whisper 模型加载、ffmpeg 音频提取、转写调度。本仓库是它的上层封装。

## 🚧 路线图

- [x] yt-dlp 音频下载（主路径，免费）
- [x] TikHub 元数据增强（可选）
- [x] Whisper 语音转文字
- [x] 中文标点恢复 + 繁转简
- [x] 增量存盘（崩溃恢复）
- [x] Twitter/X 博主深度提炼（包含高清图、高赞评论）
- [ ] 一键纯 yt-dlp 脚本（零依赖 blogger-distiller）
- [ ] YouTube 频道支持
- [ ] 小红书笔记正文提取
- [ ] 一键 Docker 部署
- [ ] GPU 加速（faster-whisper CTranslate2）

## ⚖️ License

MIT — 随便用，标注出处即可。

---

<p align="center">
  <sub>built with ☕ and a lot of 抖音口播</sub>
</p>
