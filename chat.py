# chat.py
import os
import json
from zhipuai import ZhipuAI
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
from prompt_toolkit import prompt

HISTORY_DIR = os.path.expanduser("history")
SESSION_FILE = os.path.join(HISTORY_DIR, "session.json")
MAX_TOKENS = 6000  # 粗略估算限制（防止上下文超限）
DEBUG_MODE = False  # 设置为 True 可打印实际传入的大模型消息

SYSTEM_PROMPT = {
    "role": "system",
    "content": "你是一个乐于回答各种问题的小助手，你的任务是提供专业、准确、有洞察力的建议，请你用中文来回答。"
}


def ensure_history_dir():
    os.makedirs(HISTORY_DIR, exist_ok=True)

def load_history():
    ensure_history_dir()
    if not os.path.exists(SESSION_FILE):
        return [SYSTEM_PROMPT]
    with open(SESSION_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_history(history):
    ensure_history_dir()
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def reset_history():
    save_history([SYSTEM_PROMPT])

def trim_history(history, max_tokens=MAX_TOKENS):
    """保留最近消息，避免超过token限制。粗略估算token数量。"""
    new_history = [SYSTEM_PROMPT]
    token_count = 0
    for msg in reversed(history[1:]):
        token_count += len(msg["content"]) // 2  # 粗估1 token ≈ 2个字符
        if token_count > max_tokens:
            break
        new_history.insert(1, msg)
    return new_history

# === 核心对话函数 ===
def stream_chat(user_input, api_key, file_content=None):
    history = load_history()

    # 添加上下文内容作为一条单独 message
    if file_content:
        history.append({
            "role": "user",
            "content": f"以下是用户提供的参考资料，请在后续回答中加以参考：\n{file_content}"
        })

    # 添加当前提问
    history.append({
        "role": "user",
        "content": user_input
    })

    # 剪裁历史
    history = trim_history(history)

    # Debug 打印实际传给模型的 messages
    if DEBUG_MODE:
        print("[DEBUG] 当前传入的大模型消息如下：")
        for msg in history:
            print(f"[{msg['role']}] {msg['content'][:100]}{'...' if len(msg['content']) > 100 else ''}")
        print("=" * 50)

    # 调用大模型
    client = ZhipuAI(api_key=api_key)
    response = client.chat.completions.create(
        model="glm-4-flash",  
        messages=history,
        stream=True,
    )

    # 实时输出响应
    reply = ""
    console = Console()
    console.print("[bold cyan]Miss Agent:[/bold cyan]")

    with Live(console=console, refresh_per_second=15) as live:
        for chunk in response:
            if chunk and chunk.choices:
                delta = chunk.choices[0].delta
                if delta and hasattr(delta, 'content') and delta.content:
                    content = delta.content
                    reply += str(content)
                    live.update(reply)

    # 保存回复到历史
    history.append({
        "role": "assistant",
        "content": reply
    })
    save_history(history)
