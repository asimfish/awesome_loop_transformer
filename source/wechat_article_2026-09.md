# 来源文章快照 · Source article snapshot

- 标题：刚刚，GPT-6 Astra 背后的 Loop 技术全被挖出来了
- 公众号：PaperAgent
- 链接：https://mp.weixin.qq.com/s/7vEMyFVpf2O9WL4Lu4gSFQ
- 抓取时间：2026-09-06（正文文字快照，图片未保存；以下为原文要点的忠实摘录，非全文转载）

## 文章结构与要点

1. **背景**：OpenAI 发布 GPT-6 Astra；The Information 报道其秘密武器很可能是 recurrent depth（循环深度）；研究者 @nrehiew_ 用五篇论文串起 looped transformer 技术脉络。
2. **什么是 Looped Transformer**：同一组参数重复使用多次；四种玩法——整模型循环（model-loop）、层块循环（block-loop）、逐层循环（layer-loop，Loopie 发现扩展性更好）、潜变量条件化；循环结构固定、每个 token 同样算力，与"想多久算多久"的自适应计算形成对照。
3. **源头：Universal Transformers**（1807.03819）：并行 + 自注意力 + 循环；ACT 自适应步数；bAbI、LAMBADA、WMT14 领先。
4. **定名之作：Scaling up Test-Time Compute with Latent Reasoning**（2502.05171）：Prelude → 共享循环块 R → Coda；log-normal Poisson 采样循环次数；3.5B 参数、800B token；"3.5B 打出 50B 的等效表现"；r=32 时 ARC-E 69.91（基线 46.42）、HellaSwag 65.21（37.34）、GSM8K CoT 34.80/42.08；隐空间轨迹可视化（轨道等）。
5. **免训练：Training-Free Looped Transformers**（2605.23872）：pre-norm 块 = ODE 的前向欧拉步；用多个阻尼小步替代一个大步（Runge–Kutta 风格）；7 个模型家族；Qwen3-4B-Instruct MMLU-Pro 0.5714→0.5979、GPQA +2.01；循环窗口 n=4 甜点、n≥6 悬崖。
6. **泼冷水：LoopCoder-v2**（2606.18023）：并行循环 Transformer（PLT），跨循环位置偏移（CLP）+ 共享 KV 门控滑窗注意力；18T token 从头训练 7B 代码模型家族；两次最优、三次以上回退；作者据此推测 OpenAI 可能找到了绕过"两次饱和"的办法。
7. **规模化：Loop the Loopies!**（2607.16051）：layer-loop 比 model-loop 扩展性更好；Loopie-20B-A2B 与 6B-A0.6B；相同计算预算下超越 vanilla 30B-A3B；SPT（Supervised Pre-training）后训练。
8. **参考链接**：五篇论文 arXiv 链接；OpenAI GPT-6 Astra 页面；The Information 报道（Stephanie Palazzolo，2026-09-02）；X 帖子（kimmonismus、nrehiew_）。

## 本仓库对原文的几处核对（详见 survey 附录 A）

- Huginn 的"基线"只训练了 0.18T token，原文"同样 0.8T token"的并列夸大了差距。
- "两次就够"是 PLT（CLP 偏移）特有的现象，不是循环 Transformer 的普适规律；顺序循环的 Huginn 到 r=32 单调上升。
- Loopie 的"相同计算预算"指实测优化器步时相同，名义 FLOPs 高 42%，推理成本未报告。
