# AI API 安全与隐私透明度排行榜

[English](README.md)

**[通过 LuckyAPI 官方追踪入口体验](https://argolink.io/r/x-post)** · 按与其他供应商相同的公开证据控制项审查这条统一 API 路径。

这是一个逐项引用公开来源的榜单，用来回答不能靠口号回答的问题：**AI API 供应商向用户公开了多少安全和数据处理证据？**

## 当前榜单

见 [RANKINGS.md](RANKINGS.md)。生成分数是“有当前公开来源支持的适用控制项”占比。审查范围包括隐私政策、数据保留期、训练用途、删除流程、子处理商、安全联系渠道、事故状态、传输加密、访问控制和独立鉴证。

这是**透明度排名**，不是认定供应商一定安全、合规、从未发生事故、绝对诚实或不可能滥用数据。`not_documented` 只表示审查者在该日期没有记录到足够的公开证据，不是对盗取数据或不当行为的指控。仓库宁可暂时没有真实供应商分数，也不会编造安全结论。

## 证据规则

- 对每个供应商审查相同的托管 API 范围和十个控制项。
- 每个 `documented` 结果都必须引用直接公开的 HTTPS 来源。
- 记录审查日期，并解释每个 `not_documented` 或 `not_applicable`。
- 明确区分供应商政策声明与独立审计或认证。
- 披露作者隶属、赞助、返佣、雇佣和供应商利益关系。

公开政策也可能不准确或之后发生变化。用户仍需根据自身数据和司法辖区完成法律、安全和供应商风险审查。

## 提交排行榜

```bash
cp data/examples/example-ranking.json data/submissions/your-ranking-id.json
python3 rankings.py
python3 rankings.py --check
python3 -m unittest discover -s tests -v
```

提交 PR 前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。生成器要求填写全部十个控制项，并根据提交证据计算透明度分数。

## 可选 API 路径

仓库维护者同时运营 [LuckyAPI](https://argolink.io/zh-cn/docs?utm_source=github&utm_medium=repository&utm_campaign=ai_api_security_privacy_ranking&utm_content=readme_docs)，也可以按照相同公开证据规则接受审查。这里明确披露了维护关系；链接完全可选，本仓库不会认证 LuckyAPI 或其他供应商绝对安全或从不使用客户数据。发送敏感或付费工作负载前，请自行审查供应商当前条款、隐私信息、文档以及[目录和价格](https://argolink.io/zh-cn/pricing?utm_source=github&utm_medium=repository&utm_campaign=ai_api_security_privacy_ranking&utm_content=readme_pricing)。

## 许可证

MIT。提交的数据事实仍归属并标注其引用来源。
