"""api-lab-openai-compatible-minimal

通用 OpenAI-compatible 最小壳子。
只要某个供应商提供 /chat/completions 兼容接口，
你就能通过修改 .env 中的 AI_API_KEY / AI_BASE_URL / AI_MODEL 复用本脚本：
- OpenRouter
- DeepSeek
- LM Studio (本地)
- 公司内部兼容接口
等等。
"""

import json
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

PROMPT = "请用通俗语言解释 base_url、api_key、model 三者的关系。"
TIMEOUT_SECONDS = 30
MAX_TOKENS = 100


def main() -> int:
    load_dotenv()

    api_key = os.getenv("AI_API_KEY", "").strip()
    base_url = os.getenv("AI_BASE_URL", "").strip().rstrip("/")
    model = os.getenv("AI_MODEL", "").strip()

    missing = [k for k, v in {
        "AI_API_KEY": api_key,
        "AI_BASE_URL": base_url,
        "AI_MODEL": model,
    }.items() if not v]
    if missing:
        print(f"[错误] .env 缺少以下变量: {', '.join(missing)}")
        print("       请运行: cp .env.example .env，然后填好后再运行。")
        return 2

    url = f"{base_url}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": PROMPT}],
        "max_tokens": MAX_TOKENS,
    }

    print(f"[信息] endpoint = {url}")
    print(f"[信息] model    = {model}")
    print(f"[信息] prompt   = {PROMPT}")

    started = time.time()
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT_SECONDS)
    except requests.exceptions.Timeout:
        print(f"[失败] 请求超时（{TIMEOUT_SECONDS}s）。")
        return 1
    except requests.exceptions.RequestException as exc:
        print(f"[失败] 网络请求异常: {exc}")
        print("        如果 base_url 指向本地服务，请先确认服务已启动并能 curl 通。")
        return 1
    elapsed = time.time() - started

    if resp.status_code != 200:
        print(f"[失败] HTTP {resp.status_code}")
        print(f"        响应片段: {resp.text[:300]}")
        print("        常见原因: API Key 错 / base_url 拼写错 / 模型名错 / 服务商不兼容 OpenAI 协议。")
        return 1

    try:
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
    except (ValueError, KeyError, IndexError, TypeError):
        print("[失败] 响应结构不符合 OpenAI-compatible /chat/completions 预期。")
        print(f"        原始响应片段: {resp.text[:300]}")
        return 1

    print()
    print("[成功] 模型返回内容：")
    print(content)
    print()
    print(f"[信息] 耗时 {elapsed:.2f}s")

    out_dir = Path(__file__).parent / "output"
    out_dir.mkdir(exist_ok=True)
    result = {
        "provider": "openai-compatible",
        "base_url": base_url,
        "model": model,
        "prompt": PROMPT,
        "elapsed_seconds": round(elapsed, 3),
        "content": content,
    }
    out_file = out_dir / "result.json"
    out_file.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[信息] 已写入 {out_file}（不会被 git 提交）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
