# -*- coding: utf-8 -*-
"""
Creator Distiller - Twitter/X 博主思想蒸馏引擎
使用 TikHub API，支持高级搜索切片提取、无感翻页、高清配图自动下载及深度评论归档。
"""

import asyncio
import json
import os
import sys
import urllib.request
from datetime import datetime, timedelta
from tikhub import AsyncTikHub

sys.stdout.reconfigure(encoding='utf-8')

# 自动定位 config 文件获取 TikHub Token
def get_tikhub_token():
    # 尝试从 ~/.xiaohongshu/tikhub_config.json 获取
    cfg_path = os.path.expanduser("~/.xiaohongshu/tikhub_config.json")
    if os.path.exists(cfg_path):
        try:
            with open(cfg_path, 'r', encoding='utf-8') as f:
                return json.load(f).get("tikhub_api_token")
        except Exception:
            pass
    # 备用：从环境变量获取
    return os.environ.get("TIKHUB_API_KEY")

API_KEY = get_tikhub_token()

def generate_date_ranges(start_date_str, end_date_str, step_days=15):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    ranges = []
    current_start = start_date
    while current_start < end_date:
        current_end = current_start + timedelta(days=step_days)
        if current_end > end_date:
            current_end = end_date
        ranges.append((current_start.strftime("%Y-%m-%d"), current_end.strftime("%Y-%m-%d")))
        current_start = current_end
    return list(reversed(ranges))

async def distill_twitter_creator(username, start_date="2025-01-01", end_date=None, output_dir="output"):
    if not API_KEY:
        print("❌ 错误: 未配置 TikHub API Token！")
        print("💡 请参考 README.md 配置 ~/.xiaohongshu/tikhub_config.json 或设置环境变量 TIKHUB_API_KEY。")
        return

    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")

    print(f"🛰️  [Creator Distiller] 正在加载博主: @{username}")
    print(f"📅  检索起止时间: {start_date} 至 {end_date}")

    base_dir = os.path.join(output_dir, f"{username}_twitter_kb")
    images_dir = os.path.join(base_dir, "images")
    os.makedirs(images_dir, exist_ok=True)

    tweets_dataset = []
    seen_ids = set()

    summary_json_path = os.path.join(base_dir, "all_tweets_summary.json")
    if os.path.exists(summary_json_path):
        try:
            with open(summary_json_path, 'r', encoding='utf-8') as f:
                tweets_dataset = json.load(f)
                for et in tweets_dataset:
                    seen_ids.add(et.get("tweet_id"))
            print(f"💾  载入本地缓存 checkpoint: 已恢复 {len(tweets_dataset)} 条记录。")
        except Exception:
            pass

    date_blocks = generate_date_ranges(start_date, end_date, step_days=15)

    async with AsyncTikHub(api_key=API_KEY) as client:
        for idx, (since_date, until_date) in enumerate(date_blocks):
            query = f"from:{username} since:{since_date} until:{until_date}"
            print(f"👉  ({idx+1}/{len(date_blocks)}) 执行周期检索: {query}")
            try:
                response = await client.twitter_web.fetch_search_timeline(keyword=query, search_type="Latest")
                if response and response.get("code") == 200:
                    data = response.get("data", {})
                    timeline = data.get("timeline", []) or []
                    
                    new_tweets = []
                    for t in timeline:
                        t_id = t.get("tweet_id")
                        if t_id and t_id not in seen_ids:
                            seen_ids.add(t_id)
                            tweets_dataset.append(t)
                            new_tweets.append(t)
                    
                    print(f"   📊 成功捕获新推文 {len(new_tweets)} 条 (累计已下载 {len(tweets_dataset)} 条)")
                    
                    for t_item in new_tweets:
                        await process_tweet(client, username, t_item, base_dir, images_dir)
                    
                    with open(summary_json_path, "w", encoding="utf-8") as f:
                        json.dump(tweets_dataset, f, ensure_ascii=False, indent=2)
                else:
                    print(f"   ⚠️ 接口提示: {response.get('message_zh', '未知限制')}")
                
                await asyncio.sleep(2.0)
            except Exception as e:
                print(f"   ❌ 查询异常: {e}")
                await asyncio.sleep(4)

    print(f"🎉  [@{username}] 思想蒸馏完成！成果输出在: {base_dir}/")

async def process_tweet(client, username, t, base_dir, images_dir):
    tweet_id = t.get("tweet_id")
    text = t.get("text", "")
    created_at = t.get("created_at", "")
    likes = t.get("favorites", 0)
    reposts = t.get("retweets", 0)
    replies_count = t.get("replies", 0)
    bookmarks = t.get("bookmarks", 0)
    views = t.get("views", "0")
    url = f"https://x.com/{username}/status/{tweet_id}"

    md_file_path = os.path.join(base_dir, f"{tweet_id}.md")
    if os.path.exists(md_file_path):
        return

    # 下载高清图
    local_image_paths = []
    media_obj = t.get("media", [])
    photo_list = []
    if isinstance(media_obj, dict):
        photo_list = media_obj.get("photo", [])
    elif isinstance(media_obj, list):
        photo_list = media_obj

    for img_idx, photo in enumerate(photo_list):
        img_url = photo.get("media_url_https")
        if img_url:
            local_img_name = f"{tweet_id}_{img_idx}.jpg"
            local_img_path = os.path.join(images_dir, local_img_name)
            try:
                clean_img_url = img_url.split('?')[0] if '?' in img_url else img_url
                urllib.request.urlretrieve(clean_img_url, local_img_path)
                local_image_paths.append(f"./images/{local_img_name}")
            except Exception:
                local_image_paths.append(img_url)

    # 提炼评论
    replies_list = []
    if replies_count > 0:
        try:
            comments_response = await client.twitter_web.fetch_post_comments(tweet_id=tweet_id)
            if comments_response and comments_response.get("code") == 200:
                comments_data = comments_response.get("data", {})
                thread = comments_data.get("thread", []) or []
                for reply in thread:
                    reply_text = reply.get("text", "") or reply.get("display_text", "")
                    reply_author = reply.get("author", {})
                    if reply_text:
                        replies_list.append({
                            'username': reply_author.get("screen_name", "未知"),
                            'name': reply_author.get("name", "未知"),
                            'text': reply_text,
                            'likes': reply.get("likes", 0)
                        })
            await asyncio.sleep(1.2)
        except Exception:
            pass

    # 写 Markdown 
    markdown_content = f"""---
id: "{tweet_id}"
url: "{url}"
created_at: "{created_at}"
likes: {likes}
reposts: {reposts}
replies_count: {replies_count}
bookmarks: {bookmarks}
views: "{views}"
---

# 推文正文
{text}

"""
    if local_image_paths:
        markdown_content += "## 关联图片\n"
        for img_path in local_image_paths:
            markdown_content += f"![图片]({img_path})\n"

    markdown_content += "\n## 推文下方读者热评\n"
    if replies_list:
        sorted_replies = sorted(replies_list, key=lambda x: x['likes'], reverse=True)
        for r in sorted_replies[:15]:
            markdown_content += f"- **@{r['username']}** ({r['name']}): {r['text']} (👍 {r['likes']})\n"
    else:
        markdown_content += "（暂无读者评论）\n"

    with open(md_file_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("💡 用法: python distill_twitter.py <博主用户名> [开始时间, YYYY-MM-DD]")
        sys.exit(1)
        
    user = sys.argv[1]
    start = sys.argv[2] if len(sys.argv) > 2 else "2025-01-01"
    
    asyncio.run(distill_twitter_creator(user, start_date=start))
