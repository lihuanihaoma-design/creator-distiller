<div align="center">

# 🫗 博主万能蒸馏器 (Blogger Distiller)

> *「别让博主只留在屏幕里，一键把他们‘吸干’成你的本地 AI 知识库，零成本提取博主的认知操作系统」*

简体中文 | [English](README_EN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![RAG-Ready](https://img.shields.io/badge/RAG-Ready-green.svg)](#-能干什么)
[![Local-First](https://img.shields.io/badge/Local-First-blue.svg)](#-安装与使用)
[![Zero-Cookie](https://img.shields.io/badge/Zero--Cookie-Twitter/X-orange.svg)](#-为什么它极其牛逼)

<br>

**博主是时代的思想放大器，而「Blogger Distiller」则是帮你捕获博主认知资产的超强物理抽水机。**

无需配置任何 Cookie，也不需要承担被推特风控封号的风险。只需输入一个博主名字，自动在后台“抽干”他们所有的历史推文、视频逐字稿、高清配图、以及最精华的读者评论，瞬间为你构建出一座高保真的本地 RAG 知识库与专属数字分身。

[效果演示](#⚡-效果演示) · [为什么它极其牛逼](#🔥-为什么它极其牛逼) · [安装与使用](#⚡-安装与使用) · [大超说媒实战](#⚡-经典实战案例大超说媒) · [路线图](#🚧-路线图)

<br>

[![Star History Chart](https://api.star-history.com/svg?repos=lihuanihaoma-design/creator-distiller&type=Date)](https://star-history.com/#lihuanihaoma-design/creator-distiller&Date)

</div>

---

## ⚡ 效果演示

这不是机械复读语录，这是当你把「Blogger Distiller」所提取的高保真 Markdown 知识库喂给本地大模型后，他们用自己独特的认知系统、表达DNA和口吻帮你在本地解答问题的场景：

```
用户 ❯ 大超，帮我看看这一对合适不？女生30岁英语老师杭州本地中产家庭，男生31岁程序员农村出身，大厂35万带房贷。

大超 ❯ 大兄弟，你年薪35万如果回家不会和姑娘说话，那就是一堆废纸。合上你的破电脑，带上钱包陪她去旅游，教她怎么理解程序员的踏实。
        
        姑娘，也别太死卡男生的农村出身和不解风情。这个男生能一个人在杭州白手起家买房，靠的是绝对的靠谱。
        
        合婚率 75%，这是一个绝对值得调教、值得成婚的潜力组合，互相向下兼容，这一对，有得做！
```

再来一个干货博主 `@dontbesilent` 的知识蒸馏对话：

```
用户 ❯ 我写了好多关于大模型的硬核技术干货，但为什么就是不涨粉，也没有人买单？

dontbesilent ❯ 你完全分不清什么是“问题”，什么是“痛感”。
               
               类似“大模型的参数、Transformer 架构”——这是 Question。
               用户的痛感是“焦虑，感觉现在干的工作没有未来”。
               
               不要死啃算法和堆砌技术，要思考怎么去敲开这扇紧闭的大门。
               每个武装完整的大脑，底层都是通过痛苦来认识你的，而不是通过幸福。
               让你的内容去帮他们解脱痛苦，而不是去帮他们幸福，懂我意思吗？
```

---

## 🎯 能干什么

| 你扔进来 | 它还给你 | 本机优势 |
|-----------|----------|----------|
| **Twitter/X 用户名** | 全量推文、高清图片及高赞评论归档的带 YAML Metadata 的 Markdown | 💡 **100% 零 Cookie、免登录、抗风控**，直接秒杀传统接口 |
| **抖音博主 ID / 昵称** | `{标题}.txt` × N，标点完整、繁转简的视频高精度口播逐字稿 | 💡 **纯免费。** 实时解析音频，磁盘零残留，崩溃自动恢复 |
| **小红书博主主页** | 包含笔记正文、多图本地保存、标签整理的格式化知识包 | 💡 高保真度保留视觉与文案排版 |
| **YouTube 渠道** | 音频自动提取 + 本地 Whisper 转写文档（计划中） | 💡 真正的一键流式提取 |

---

## 🔥 为什么它极其牛逼？

目前在 GitHub 上，绝大多数 Twitter 爬虫和媒体下载工具都面临着**频繁触发 400 Bad Request、以及 Cookie 泄露被封号**的死局。而我们彻底重写了这套架构，实现了以下革命性的技术突破：

### 1. 高级搜索日期切片 (Zero-Cookie / Zero-Browser) 🛡本地优先
不再依赖极易被推特防火墙阻断的 `next_cursor` 游标翻页。我们将时间线科学切割为 **37个 15天日期微区间**，通过 `from:username since:YYYY-MM-DD until:YYYY-MM-DD` 组合语法执行定向 Latest 检索。
* **效果**：实现 100% 稳定的高频免登录、免 Cookie 抓取，彻底告别 400 错误。

### 2. 多模态流式落盘与断点续传 (Streaming & Checkpoint) 💾
不把数据压在 Python 内存中，而是采用**流式实时存储**。每当抓取并解析完一条推文，Markdown、高清配图就会**瞬间 flush 写入硬盘**。
* **效果**：即便中途网络抖动，重启脚本会毫秒级识别本地已有 MD，**直接跳过已完成部分继续往下爬，为你节省 100% 的 TikHub API 计费额度**。

### 3. 高赞读者神评深度提取 (Reply Harvesting) 💬
许多博主在正文中字数受限，最精华的见解、反向提问以及与行业大咖的深度辩论其实都在评论区中。我们不仅提取推文，还会自动调用 TikHub 接口**爬取下方的精选高赞评论，作为上下文一并拼入 Markdown 归档**。
* **效果**：大模型读取后能自动获取完整的社会化语境反响，认知广度翻倍。

---

## ⚡ 安装与使用

### 1. 快速安装
```bash
# 克隆
git clone https://github.com/lihuanihaoma-design/creator-distiller.git
cd creator-distiller

# 安装依赖
pip install -r requirements.txt

# 确保安装 ffmpeg（Whisper/yt-dlp 必要依赖）
# macOS: brew install ffmpeg  |  Windows: winget install Gyan.FFmpeg
```

### 2. 配置 TikHub API Token (仅需¥5即可采集上百条)
1. 访问 [https://user.tikhub.io](https://user.tikhub.io) 免费注册。
2. 在左侧面板生成你的 API Token。
3. 将 Token 写入系统配置中：
   ```bash
   python -c "
   import json, os
   cfg = os.path.join(os.path.expanduser('~'), '.xiaohongshu', 'tikhub_config.json')
   os.makedirs(os.path.dirname(cfg), exist_ok=True)
   json.dump({'tikhub_api_token': '你的TOKEN'}, open(cfg, 'w'))
   "
   ```

### 3. 一键运行！
```bash
# 1. 蒸馏 Twitter/X 博主（例如 dontbesilent）
python scripts/distill_twitter.py dontbesilent

# 2. 蒸馏 抖音 博主（例如 视频链接）
python scripts/retry_ytdlp.py "抖音博主主页或视频链接"
```

你将直接在本地获得一个完美的、包含 YAML Front-Matter 标签的 Markdown 文件夹！

---

## 🔧 工作原理

Blogger Distiller 分为两条核心流水线，完全针对大语言模型（LLM）的结构偏好进行设计：

### 📺 视频转写流水线 (抖音/小红书)
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌──────────────┐
│  TikHub API  │───▶│   yt-dlp    │───▶│   Whisper    │───▶│  Punctuation  │
│  元数据采集   │    │  音频流提取  │    │  语音转文字   │    │  标点自动恢复 │
└─────────────┘    └─────────────┘    └─────────────┘    └──────────────┘
```
* **yt-dlp 实时解析**：拒绝过期的 CDN 直链链接，每次均实时解析音轨，零费用、永不过期。
* **自动繁转简 + 标点恢复**：Whisper 转换后缺失标点，我们通过算法自动补齐逗号、句号、问号，实现完美的阅读排版。

### 🐦 推文采集流水线 (Twitter/X)
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌──────────────┐
│ 15天日期切片 │───▶│  定向检索    │───▶│  配图本地化  │───▶│ 读者神评合并  │
│ 规避400游标  │    │ 最新时间线   │    │ 高清大图下载 │    │ 作为上下文 RAG│
└─────────────┘    └─────────────┘    └─────────────┘    └──────────────┘
```
* **高清图片本地化**：去除 Twitter 缩略图限制，下载原始高分辨率 `.jpg`，并在 Markdown 中自动建立本地引用路径。
* **高赞热评深度合成**：自动捕获推文下方热度排名前 15 的追问和反思，连同点赞数一并写入，打造拥有“群体智慧辩论”的深度知识库。

---

## 📂 文件结构

```
blogger-distiller/
├── README.md                          ← 你正在看的
├── README_EN.md                       ← English Version
├── SKILL.md                           ← Agent 可复用的技能定义
├── scripts/
│   ├── distill_twitter.py             ← Twitter/X 极速高级搜索时间切片蒸馏脚本（TikHub）
│   ├── extract_transcripts.py         ← 从 JSON 提取逐字稿 + 标点恢复 + 生成索引
│   ├── retry_ytdlp.py                 ← yt-dlp 下载音频 + Whisper 转写（崩溃可恢复）
│   └── utils/
│       ├── punctuation_restorer.py    ← 中文标点自动注入 + 繁转简
│       └── transcript.py             ← Whisper 集成调度器
└── requirements.txt
```

---

## ⚡ 经典实战案例：“大超说媒”

<details>
<summary>点击展开 ➡️ 如何利用大超的逐字稿打造一个真实的“相亲评估 AI Agent”</summary>

### 1. 蒸馏得到的知识库样例
本项目工具会自动将大超的历史点评逐字稿整合为带本地配图和读者回复的 Markdown：
```markdown
---
id: "2058011944897097845"
created_at: "Sat May 23 02:27:38"
likes: 53
reposts: 3
bookmarks: 29
---
# 推文正文
大厂IT程序员（外地，年薪35w，有房贷） vs 本地女教师（中产，本地人，年入12w）...
...
## 读者热评
- @stometaverse: 确实，目标用户相似这个洞察挺准的。(👍 3)
```

### 2. “数字大超” 提示词构建
直接复制以下 Prompts，并附带你通过本项目生成的 Markdown 切片文件，丢给任意 LLM 即可创建一个无懈可击、极具大超风味的情感导师：
```markdown
系统角色：你是“数字人大超”（数字大超说媒），抖音上最接地气的相亲和情感诊断专家。请根据提供的 [上下文参考案例] 中的逻辑口吻、实用主义标准（卡本地户籍、职业稳定性、程序员情绪价值、年龄硬伤等）对新男女进行深度适配度诊断。

行话与吨调：
1. 婚姻是合伙，不能光谈风花雪月。
2. 说话直接犀利、幽默接地气，拒绝画饼。
3. 常用词：“向下兼容”、“相亲市场香饽饽”、“情绪价值”、“天花板”、“有得做”。
```

### 3. 评测输出示例
* **输入新情侣条件**：男方31岁外地资深程序员，杭房有贷，年薪35万，内向；女方30岁杭州公立高中教师，中产本地家庭，年薪12万，爱精致生活。
* **数字大超输出**：
  > “大兄弟，你的35万年薪如果回家不会和姑娘说话，那就是一堆废纸。合上你的破电脑，带上钱包陪她出去旅游，教她怎么理解程序员的踏实。
  > 姑娘，也别太死卡男生的农村出身。这男生靠自己在大厂买房，靠谱！
  > 最终成婚推荐指数：75%。互相向下兼容，这一对，有得做！”

</details>

---

## 🚧 路线图

- [x] 抖音元数据采集与音频一键流式转写
- [x] Twitter/X 高级搜索时间分片免 Cookie 蒸馏引擎（含高清图、高赞评论）
- [x] 本地增量断点续传（100% 避免重复请求计费）
- [ ] YouTube 视频自动音频转写管线
- [ ] 小红书正文与美图本地一键下载
- [ ] 容器化 Docker 一键部署

---

## ⚖️ License

MIT — 随便用，随便改，觉得好用请点击右上角点个 **Star ⭐️** 支持一下！

<div align="center">
<sub>built with ☕ and a lot of 🚀 Blogger Distiller</sub>
</div>
