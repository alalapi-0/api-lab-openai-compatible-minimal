# RUN_RESULT

| 字段 | 值 |
| --- | --- |
| 真实 API 运行 | 否 |
| 离线契约验证 | 通过（2026-08-12） |
| 验证 base_url | `https://provider.invalid/v1`（保留测试域名） |
| 验证模型占位名 | `test-model` |
| 真实请求耗时 | — |
| 未运行原因 | 未读取或配置凭据，也未选择一个获准调用的真实供应商 |

## 验证范围

在一次性的 `git archive` 副本中，以内存桩替代 `requests` 和 `python-dotenv`，验证了：

- 缺少三个必填配置时返回退出码 2，且不发起请求；
- base URL 规范化、Bearer 头、模型、消息、`max_tokens` 与超时参数符合兼容协议；
- 成功响应会生成预期的 `output/result.json`；
- HTTP 401 与畸形成功响应均返回退出码 1；
- `main.py` 通过 Python 语法编译检查。

验证结束后已移除一次性副本。桩响应不能证明任何真实供应商、模型、凭据或网络链路可用。
