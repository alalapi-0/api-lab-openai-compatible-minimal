# LEARNING — api-lab-openai-compatible-minimal

> 这份文件回答：「我跑完这个仓库，应该真的学到什么？」
> README 负责"怎么跑"，本文件负责"为什么跑、跑完该看什么、自己有没有真懂"。

## 你跑完应该能回答的问题

1. 「OpenAI-compatible」到底是协议还是某家厂商的产品？
2. 同一份 `main.py` 不改一行代码，为什么能切到 OpenRouter / DeepSeek / LM Studio / 公司内网代理这些完全不同的服务？
3. 当一个新模型供应商上线，你怎么**最快**判断它能不能复用这套代码？
4. 协议兼容到什么程度算"足够兼容"？哪些字段是必须严丝合缝的？

## 实操验证清单（务必动手）

> 本仓库的精髓是 **「同一份代码，多次切换 .env，跑出不同结果」**。如果你只跑一次，等于没学到。

### 阶段 A — 环境就绪
- [ ] `cp .env.example .env`
- [ ] `pip install -r requirements.txt`

### 阶段 B — 第一家：OpenRouter
- [ ] `.env` 填：
  ```
  AI_API_KEY=<你的 OpenRouter key>
  AI_BASE_URL=https://openrouter.ai/api/v1
  AI_MODEL=openai/gpt-4o-mini
  ```
- [ ] `python3 main.py` → 应成功
- [ ] 把 `output/result.json` 重命名保存为 `output/run-openrouter.json`（防止下一次被覆盖）

### 阶段 C — 第二家：DeepSeek（或任意一家便宜的兼容服务）
- [ ] `.env` 改成：
  ```
  AI_API_KEY=<你的 DeepSeek key>
  AI_BASE_URL=https://api.deepseek.com/v1
  AI_MODEL=deepseek-chat
  ```
- [ ] **不要改 main.py 一个字符**
- [ ] `python3 main.py` → 应该照样成功
- [ ] 保存为 `output/run-deepseek.json`

### 阶段 D — 第三家：本地（可选，配合 LM Studio 仓库）
- [ ] 启动 LM Studio 并 Start Server
- [ ] `.env` 改成：
  ```
  AI_API_KEY=lm-studio
  AI_BASE_URL=http://localhost:1234/v1
  AI_MODEL=<LM Studio 显示的模型名>
  ```
- [ ] `python3 main.py` → 应该照样成功
- [ ] 保存为 `output/run-lmstudio.json`

### 阶段 E — 关键观察
- [ ] 三份 `output/run-*.json` 的 `provider` / `base_url` / `model` 字段不同，**但 main.py 没改过一次**
- [ ] 比较三家回答的风格、长度、错别字、措辞 → 这是模型差异
- [ ] 比较三家的 `elapsed_seconds` → 这是网络 + 推理速度差异

## 自检题

1. 如果某家服务声称自己"OpenAI-compatible"，但响应里没有 `choices[0].message.content`，会发生什么？本仓库的代码会怎么报错？
2. 我能不能把 `AI_BASE_URL` 设成 `http://localhost:11434`（Ollama 的端口）然后跑这份 `main.py`？为什么不行？（提示：Ollama 默认走 `/api/chat`，路径不一样）
3. 如果某家服务**只**支持 `/v1/completions`（旧版 completion 接口）而不支持 `/v1/chat/completions`，本仓库能用吗？
4. 我把 `AI_BASE_URL` 末尾加了一个 `/`（变成 `https://api.deepseek.com/v1/`）会出问题吗？看一眼 `main.py` 怎么处理的。

## 与其它仓库的连接

| 关系 | 仓库 | 为什么去看 |
| --- | --- | --- |
| **协议同源** | `api-lab-openrouter-minimal` | 它是这套兼容协议的"网关式"用法 |
| **协议同源** | `api-lab-groq-minimal` | 多一个练手对象，附带"看耗时" |
| **协议同源** | `api-lab-deepseek-minimal` | 主打"低成本场景"的同款 |
| **协议同源** | `api-lab-lmstudio-local-minimal` | 把 base_url 指向本地，**这是协议化最强的证据** |
| **对比 — 不兼容协议** | `api-lab-anthropic-minimal` | 一看就懂为什么这套代码套不上 Anthropic |
| **对比 — 不兼容协议** | `api-lab-gemini-minimal` | 同上 |

## 你应该感受到的"啊哈"瞬间

- 当你只改 `.env`、不改 `.py`，第三次跑成功的那一刻——**你会真的相信「OpenAI-compatible 是个事实标准」这句话**。
- 当你看到不同供应商返回的 `usage` / `id` / `created` 字段格式略有差异，但 `choices[0].message.content` 永远一致——**这是协议化最有价值的部分**。
