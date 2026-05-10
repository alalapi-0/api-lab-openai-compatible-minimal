# api-lab-openai-compatible-minimal

> 通用「OpenAI-compatible」最小壳子。一套代码，靠 `.env` 切换不同供应商。

## 它在做什么

很多大模型服务商都支持 OpenAI 风格的 `/chat/completions` 接口，包括但不限于：

- OpenRouter
- DeepSeek
- LM Studio（本地）
- 各家国内/海外兼容服务
- 公司内部代理接口

只要它们：

- 接受 POST `{base_url}/chat/completions`
- 接受 `Authorization: Bearer {api_key}`
- 接受 `{"model": ..., "messages": [...]}`
- 返回 `{"choices":[{"message":{"content": "..."}}]}`

那么这个脚本一行不改，就能切。

## 为什么这件事很重要

理解了「OpenAI-compatible」之后，你看任何一家新模型的官网，第一眼就能判断：

- 它是不是 OpenAI 兼容？
- 我的代码要不要改？
- 我能不能用 OpenRouter 这类网关一次调多家？

## 运行步骤

```bash
cd api-lab-openai-compatible-minimal
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# 编辑 .env，填三件事：
#   AI_API_KEY  = 你的 key
#   AI_BASE_URL = 服务商兼容接口的 v1 根路径，例如 https://api.deepseek.com/v1
#   AI_MODEL    = 该供应商可用的模型名

python3 main.py
cat output/result.json
```

## 几个示范配置（仅示例，请用你账户实际可用的模型名）

DeepSeek：

```
AI_BASE_URL=https://api.deepseek.com/v1
AI_MODEL=deepseek-chat
```

OpenRouter：

```
AI_BASE_URL=https://openrouter.ai/api/v1
AI_MODEL=openai/gpt-4o-mini
```

LM Studio 本地：

```
AI_API_KEY=lm-studio
AI_BASE_URL=http://localhost:1234/v1
AI_MODEL=（看 LM Studio 当前加载的模型名）
```

## 常见报错

| 终端打印 | 可能原因 | 怎么处理 |
| --- | --- | --- |
| `.env 缺少以下变量` | 三个变量没都填 | 全部填好再跑 |
| `HTTP 401` | key 错或没传 | 检查 `AI_API_KEY` |
| `HTTP 404` | 路径或模型名错 | 注意 `base_url` 末尾不要带 `/chat/completions`，脚本会自动拼 |
| `HTTP 422` / 模型不存在 | 该模型在你账户不可用 | 换一个该供应商列表里你能用的模型 |
| `响应结构不符合 OpenAI-compatible` | 服务商其实不是兼容接口 | 换合适的仓库（例如 Anthropic、Gemini 仓库） |

## .env.example

```
AI_API_KEY=填入你的API Key
AI_BASE_URL=https://example.com/v1
AI_MODEL=填入模型名
```

## 不会做的事

- 不会自动重试
- 不会打印 API Key
- 不会下载额外模型
