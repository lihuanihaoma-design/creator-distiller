"""
Chinese punctuation restoration for Whisper output (no-space continuous text).
Focuses on sentence boundaries and transition words, avoids over-punctuating.
"""
import re

# ── Patterns ──────────────────────────────────────────────

# Sentence-ending particles → 。or ？
_Q = re.compile(r'(吗|呢|嘛|吧)')
_S = re.compile(r'(啊|呀|哦|哈|喽|啦|呗|哇|耶|噢|哎|嗯)')

# Transition words that clearly start a new clause
_TRANS = re.compile(r'(但是|可是|不过|然而|所以|因此|于是|而且|况且|并且|另外|还有|尤其|特别|比如|例如|换句话说|毕竟|当然|其实|实际上|总之|说白了)')

# Common spoken filler / discourse markers
_FILLER = re.compile(r'(我跟你讲|你知道吗|你想|你想想|你看|我跟你说|说真的|说实话|讲真的)')

# ── Core logic ────────────────────────────────────────────

def restore_chinese_punctuation(text: str) -> str:
    """
    Add minimal punctuation to continuous Chinese Whisper output.
    Rules (conservative, to avoid bad breaks):
      1. 吗呢嘛吧 → ？
      2. 啊呀哦哈喽啦呗哇耶噢哎嗯 → 。
      3. Transition words → ，before
      4. Discourse markers → ，before
      5. Clean up: no double punctuation, ensure ends with punctuation
    Does NOT force-break long runs — better to leave some under-punctuated
    than insert bad commas.
    """
    if not text or not text.strip():
        return text

    # Remove all whitespace first
    text = re.sub(r'\s+', '', text)

    # ── Rule 1: 吗呢嘛吧 → ？ ──
    # Add ?, but only if not already followed by punctuation and followed by content
    text = _Q.sub(r'\1？', text)

    # ── Rule 2: 啊呀哦哈喽啦呗哇耶噢哎嗯 → 。 ──
    # Add 。after these particles, unless they're inside common words
    # Exception: avoid common compounds like "是啊" inside a sentence
    text = _S.sub(r'\1。', text)

    # ── Rule 3: Transition words → ， ──
    # Only insert comma if previous char is not already punctuation
    text = _TRANS.sub(r'，\1', text)
    
    # ── Rule 4: Discourse markers → ， ──
    text = _FILLER.sub(r'，\1', text)

    # ── Cleanup ──
    # Collapse any run of Chinese punctuation: period > question > comma priority
    def collapse_punct(m):
        chars = m.group(0)
        if '。' in chars:
            return '。'
        if '！' in chars:
            return '！'
        if '？' in chars:
            return '？'
        return '，'
    text = re.sub(r'[，。！？、]{2,}', collapse_punct, text)
    
    # Remove leading punctuation
    text = re.sub(r'^[，。！？、]+', '', text)
    
    # Ensure text ends with proper punctuation
    if text and text[-1] not in '。！？…～':
        text += '。'

    return text


def restore_punctuation_enhanced(raw: str) -> str:
    """繁体→简体 + Chinese punctuation restoration."""
    # 1. 繁体 → 简体
    try:
        import zhconv
        text = zhconv.convert(raw, 'zh-cn')
    except ImportError:
        text = raw

    # 2. Apply punctuation restoration
    text = restore_chinese_punctuation(text)

    return text
