---
title: "曾鸣〈AI 发展第三阶段〉与开源 AI OS 生态对照"
source_type: article
source_url: "https://smartai.hupan.com/articles/3"
author: "曾鸣"
published: 2026-11-12
captured: 2026-11-12
tags: [ai-industry, agent, infra, method]
status: draft
---

# 曾鸣〈AI 发展第三阶段〉与开源 AI OS 生态对照

> 一句话结论：文章要的「任务操作系统」尚不存在，但它拆出的每层能力都有成熟开源件，缺口在跨系统调度这一层。

## 元信息

| 项 | 值 |
| --- | --- |
| 来源 | 湖畔智能 · 曾鸣《AI 发展第三阶段：智能体大爆发》（页面标题作「AI OS 的出现」） |
| 篇幅 | 约 3000 字，四个小节 |
| 整理方式 | 文章观点摘要 + 独立开源生态调研；项目数据为 GitHub REST API 实测，非二手搜索结果 |
| 数据快照 | 2026-11-12（star 数、`pushed_at` 均为当日快照，会变化） |
| 原始链接 | https://smartai.hupan.com/articles/3 |

> 原文页面未标注发布日期，`published` 按本次调研日登记，不代表文章发布时间。

## 核心框架

文章的推演链条是**浏览 → 搜索 → 直接表达任务**：第二阶段用户要「试 3 个智能体、改 5 次提示」，探索成本太高；第三阶段用户只说「我要什么结果」，系统自己拆解、组合、调度、执行。所以平台的核心能力**不再是信息排序，而是任务调度**。

调度区别于「选一个 Agent」的三个特征（原文）：

1. **是过程，不是瞬时决策** —— 贯穿任务执行全过程，按阶段状态持续调整。
2. **是组合，不是单点最优** —— 问题不是哪个能力最好，而是哪些能力组合起来更稳定。
3. **要处理不确定性** —— 执行中不断出现新信息和偏差，需动态调整路径仍达成整体目标。

当调度从单任务扩展到跨场景，就出现「统一组织方式」的需求：调度方式不一致 → 协同成本上升；上下文跨系统传递 → 信息损失；权限与身份缺统一机制 → 不确定性增加。这些收敛成 AI OS。

**最关键的断代判断**（原话）：传统 OS 面向确定性程序，管的是 CPU / 内存 / 文件系统 / 进程调度；「AI OS 面对的不再是确定性程序，而是大量持续运行、动态协同的智能体网络。这时候，系统真正需要管理的已经不只是算力，还有**任务流、上下文、能力协同与长期状态**。」

文章给的具象化案例是车企 CEO 的战略任务：多智能体持续跟踪政策、竞争、供应链、财务、消费者洞察，动态调整策略，并沉淀为「持续运行的组织记忆系统」—— 记住当前任务、过去的关键判断、方案为何被放弃、哪些假设已变化、哪些风险在上升。原文点破一句：**「传统组织之所以需要大量会议，本质上就是因为人类需要不断重新同步上下文。」**

作者自己留了边界：「今天的大多数讨论还处于早期阶段：标准如何形成？上下文如何长期持续？不同智能体之间如何稳定协同？……这些问题都有待深入研究。」

## 关键判断

> 以下 1 为原文作者判断，2–5 是**我在本次调研后的推论**，不是曾鸣的观点。

1. **（原作者）任务成为核心单位，交互逻辑反转** —— 「过去，人需要理解软件；未来，系统会越来越需要理解人的任务。」AI OS 不像单一工具，也不完全等同于传统平台，而是在用户入口、系统内调度、开发者接口三个层面同时起作用的基础系统。

2. **（我的推论）「AI OS」同名项目与文章定义存在粒度错位** —— `agiresearch/AIOS` 的 kernel 是「在 OS 内核之上做一层抽象，管理 LLM、memory、storage、tool 等**资源**」，本质是传统 OS 资源隐喻的平移（syscall 调度、context switch）；文章要的是**任务级**调度与组织记忆。名字一样，抽象层级差一层。

3. **（我的推论）生态已分化为四层，且成熟度和文章的价值排序相反** —— 越靠底层（算力资源、协议、编排）越成熟，越靠顶层（开放任务调度、组织记忆）越空白。这与首篇笔记的三阶段框架一致：基础设施先收官，入口与上层组织形态后到。

4. **（我的推论）现有「编排」仍是开发者预定义，不是系统自主调度** —— LangGraph / CrewAI / Dify / n8n 都是人先写 DAG 或工作流，系统按图执行；文章要求的是「系统自己决定调用哪些能力、如何组织流程」。DeerFlow 2.0 这类 long-horizon harness 把 sub-agent、memory、sandbox、skills 收进一个运行时，是目前最接近的形态，但能力集合仍由部署者预先装配，不是开放市场级发现与调度。

5. **（我的推论）「组织记忆」尚无通用实现** —— mem0 / Graphiti / cognee / Letta 解决的是单个 agent 的记忆存取与检索，而文章要的是跨多个 agent、跨数周数月、带「判断为何被推翻 / 假设何时失效」语义的共享状态。后者更接近决策日志 + 时序知识图谱 + 版本化假设，目前只见于产品设计讨论，没有开源共识实现。

## 事实与数据

全部取自 GitHub REST API `GET /repos/{owner}/{repo}`，2026-11-12 快照。`pushed_at` 为最近推送日期，用于判断活跃度。

### A. 多智能体编排 / long-horizon harness

| 项目 | star | 最近推送 | 许可 | 定位（官方描述摘要） |
| --- | ---: | --- | --- | --- |
| `n8n-io/n8n` | 210,220 | 2026-11-12 | fair-code | 工作流自动化，原生 AI 能力 |
| `langgenius/dify` | 160,996 | 2026-11-12 | NOASSERTION | Agentic workflow / RAG 平台 |
| `All-Hands-AI/OpenHands` | 93,255 | 2026-11-12 | MIT | AI 驱动开发 |
| `bytedance/deer-flow` | 85,255 | 2026-11-12 | MIT | long-horizon SuperAgent harness：编排 sub-agents + memory + sandboxes + extensible skills |
| `geekan/MetaGPT` | 71,252 | 2026-01-21 | MIT | 多智能体「软件公司」（近 10 个月未推送） |
| `microsoft/autogen` | 61,786 | 2026-10-28 | CC-BY-4.0 | agentic AI 编程框架 |
| `crewAIInc/crewAI` | 60,786 | 2026-11-11 | MIT | 角色扮演式自治 agent 编排 |
| `FlowiseAI/Flowise` | 55,567 | 2026-08-13 | NOASSERTION | 可视化搭 Agent |
| `langchain-ai/langgraph` | 44,817 | 2026-11-11 | MIT | 有状态 / 可恢复的 agent 图编排 |
| `modelscope/agentscope` | 35,819 | 2026-11-11 | Apache-2.0 | 可观测、可理解的 agent |
| `openai/openai-agents-python` | 30,621 | 2026-11-12 | MIT | 轻量多 agent 工作流 |
| `microsoft/semantic-kernel` | 28,758 | 2026-11-10 | MIT | 企业级 LLM 集成 |
| `google/adk-python` | 22,185 | 2026-11-11 | Apache-2.0 | code-first agent 开发工具 |
| `openai/swarm` | 22,125 | 2026-04-15 | MIT | 教学用实验框架，已被 openai-agents-python 取代 |
| `pydantic/pydantic-ai` | 21,149 | 2026-11-12 | MIT | 类型化 agent 框架 |
| `camel-ai/camel` | 18,026 | 2026-11-09 | Apache-2.0 | 多智能体研究框架 |
| `cloudwego/eino` | 13,620 | 2026-11-09 | Apache-2.0 | Go 语言 LLM / AI 应用开发框架 |
| `ag2ai/ag2` | 5,058 | 2026-11-10 | Apache-2.0 | AutoGen 社区分叉，自称 Open-Source AgentOS |

> `agentscope-ai/agentscope` 与 `modelscope/agentscope` 返回同一 star 数与推送时间，属同仓库迁移/重定向，不是两个项目。

### B. 自称 OS / 调度层

| 项目 | star | 最近推送 | 许可 | 实际定位 |
| --- | ---: | --- | --- | --- |
| `unicity-aos/aos-ce` | 8,458 | 2026-10-22 | Apache-2.0 | 本地共享环境：Wasm capsule、显式权限、审计轨迹、MCP 接口（偏工具/权限层） |
| `agiresearch/AIOS` | 6,555 | 2026-07-20 | NOASSERTION | AIOS kernel：LLM / memory / storage / tool 资源调度；配套 SDK `Cerebrum`（166 star） |
| `dimensionalOS/Dimos` | 4,741 | 2026-11-12 | NOASSERTION | 面向物理空间 / 机器人的 agentic OS |
| `deer-flow/llm-space` | 2,115 | 2026-11-09 | MIT | 桌面工具：原型 agent、逐步检视 harness、回放失败 |
| `agentlas-ai/Agentlas-OS` | 1,452 | 2026-11-09 | Apache-2.0 | 本地无 VM 运行时，独立 verifier 校验执行收据；偏个人桌面 |
| `Arvincreator/project-golem` | 642 | 2026-06-22 | NOASSERTION | OS 级自治 agent + 长期记忆 |
| `benz33/Liagent_OS_V0.1.2` | 7 | 2026-03-09 | MIT | 本地优先实验品 |
| `agiresearch/LiteCUA` | — | HTTP 404 | — | README 中引用的 computer-use 子项目，当前 slug 不可访问 |

AIOS 有正式论文支撑：arXiv 2403.16971（COLM 2025）、2312.03815（"LLM as OS, Agents as Apps"）、2503.11444（Cerebrum, NAACL 2025）、2502.12110（A-MEM）。

### C. 记忆 / 长期状态 / 可靠执行

| 项目 | star | 最近推送 | 定位 |
| --- | ---: | --- | --- |
| `mem0ai/mem0` | 68,832 | 2026-11-06 | agent 记忆层 |
| `langfuse/langfuse` | 37,319 | 2026-11-11 | AI 网关 / 可观测（属工程配套） |
| `topoteretes/cognee` | 33,255 | 2026-11-12 | 开源 agent 记忆平台 |
| `getzep/graphiti` | 32,759 | 2026-11-11 | 实时时序知识图谱 |
| `dapr/dapr` | 26,186 | 2026-11-12 | 分布式应用可移植运行时 |
| `letta-ai/letta` | 25,419 | 2026-10-18 | stateful agent / 记忆；**活跃代码已迁至 `letta-ai/letta-code`** |
| `temporalio/temporal` | 24,342 | 2026-11-11 | durable execution，失败重放与状态持续 |
| `inngest/inngest` | 6,033 | 2026-11-12 | 有状态步骤的工作流编排 |
| `restatedev/restate` | 4,690 | 2026-11-11 | 弹性应用 / 持久执行 |
| `agiresearch/A-mem` | 1,214 | 2025-12-12 | Agentic Memory 论文实现 |

### D. 协议与标准

| 项目 | star | 最近推送 | 定位 |
| --- | ---: | --- | --- |
| `modelcontextprotocol/servers` | 91,936 | 2026-11-11 | MCP 参考实现集合 |
| `a2aproject/A2A` | 26,495 | 2026-11-11 | Agent2Agent 通信协议，已归属 Agentic AI Foundation（aaif.io） |
| `modelcontextprotocol/modelcontextprotocol` | 9,672 | 2026-11-11 | MCP 规范与文档 |
| `i-am-bee/acp` | 1,020 | 2025-08-25 | 早期 agent 通信协议，近 15 个月未推送，实质被 A2A 吸收 |

## 可落地推论

- **对齐参考系**：`bytedance/deer-flow` 2.0 是 2026-02-28 的 GitHub Trending 榜首，且明确把 sub-agents / memory / sandboxes / **extensible skills** 收进一个 long-horizon harness。手上基于 `cloudwego/eino`（Go）做的类 DeerFlow 智能体，正落在这一层；优先对照它的 skill 装载方式、子 agent 边界与失败回放（`deer-flow/llm-space`），而不是再抽象一套编排 DSL。
- **补的不是编排，是状态**：文章说的「失败回退与状态持续」在工程上对应 durable execution（Temporal / Restate）而非又一个 agent 框架。若要把长任务做成可持续数周的系统，先把执行状态外置到可重放的 runtime，再谈智能调度。
- **组织记忆可拆成三件事实现**：时序知识图谱（Graphiti）存「什么变了」、决策日志记录「为何放弃某方案」、假设表做版本化与定期复核。三者都不需要新框架，但没有现成开源项目把它们缝在一起 —— 这是相对空白、且可与 `PREDICTIONS.md` 那套「留痕/复核」方法论直接复用的位置。
- **底层会被抽象掉**：K8s 化 vLLM + GPU 监控属于「算力资源管理」，正是文章认为 AI OS 之上不再需要用户关心的部分；按首篇笔记的三阶段框架，这层会寡头化、成熟但不高毛利。做平台工程经验可迁移，但不宜把它当成第三阶段的产品护城河。
- **选型避坑**：`openai/swarm` 已归档被取代、`letta-ai/letta` 主仓转为历史存档（活跃代码在 letta-code）、`i-am-bee/acp` 停更、`MetaGPT` 近 10 个月无推送、`AIOS` 近 4 个月无推送。搜索结果里的 star 数互相矛盾，用 API 实测比信二手榜单可靠。

## 存疑 / 待验证

> 本文是概念推演 + 生态调研，没有独立的可证伪预测，暂不新增 ID。文中「第三阶段会出现统一调度层」与 [P004](../PREDICTIONS.md)（三年内出现 Agent 入口）高度相关，若将来出现明确项目，直接在 P004 的复核记录里补证据，不重复登记。

- [ ] 命名污染严重：「AI OS」「Agent OS」在 2026 年被大量项目用作营销标签，AOS CE（权限运行时）、Dimos（机器人）、Agentlas OS（个人桌面）彼此几乎不相关。判断一个项目是否真在文章意义上，只能看它是否管理**跨系统任务流**，而不是看名字。
- [ ] 论证跳跃：文章从「人工编排效率低」直接推到「需要统一的高层收敛」，但也可能走向相反的分布式标准化（协议足够统一后，调度可以由各方各自实现，无需一个中心 OS）。MCP / A2A 的路线更接近后者。
- [ ] star 数是热度不是能力；本表未做功能评测，未验证任何项目的实际长任务成功率。
- [ ] 项目清单是人工候选集，可能遗漏；尤其未覆盖闭源产品与国内非 GitHub 托管项目。

## 延伸问题

- 如果调度真成为系统级能力，谁有动力提供它？模型厂商、云厂商还是终端入口？三者的激励都不完全匹配 —— 这可能是「方向清晰但没人做」的真实原因。
- 跨组织调度绕不开身份、授权、计费与责任归属。A2A 只解决通信，不解决「调用出错谁负责」。这是否意味着 AI OS 首先是个**制度/结算标准**，其次才是技术系统？
- 文章假设任务可以被系统可靠地拆解与验证。若任务本身无法自动验收（战略、研究、创意），「失败回退」的判据由谁给？这大概是组织记忆之外最难的一块。

## 原始资料

- [曾鸣《AI 发展第三阶段：智能体大爆发》](https://smartai.hupan.com/articles/3)
- [AIOS 论文 arXiv:2403.16971](https://arxiv.org/abs/2403.16971) · [LLM as OS, Agents as Apps arXiv:2312.03815](https://arxiv.org/abs/2312.03815)
- [AIOS 仓库](https://github.com/agiresearch/AIOS) · [Cerebrum](https://github.com/agiresearch/Cerebrum) · [DeerFlow](https://github.com/bytedance/deer-flow)
- [MCP](https://github.com/modelcontextprotocol/modelcontextprotocol) · [A2A](https://github.com/a2aproject/A2A) · [AOS CE](https://github.com/unicity-aos/aos-ce)
- 全部 star / 推送时间来自 GitHub REST API，2026-11-12 快照
- 本仓库首篇：[和曾鸣聊产业史观](2026-09-03-zengming-industrial-history.md)

---

*整理笔记，非原文转载。观点归原作者所有；标注「我的推论」的部分由整理者负责。*
