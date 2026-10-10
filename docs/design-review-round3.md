# 第三轮设计评审——六 skill × 四角度

- 日期：2026-10-10 · 基线：`autopilot/design-round3-upgrade`（源自 feat/design-round2 @ 78c69ab）
- 方法：6 个并行只读评审 agent（每 skill 一个，覆盖四角度）+ 主会话交叉层评审
  （README 路由、citation-core 实例化、CI 盲区、仓库卫生）。**每条 P0/P1 均由主会话
  在源码中二次验证**（追溯 file:line 或复现），P2 由评审 agent 自带实测/引用支撑，
  修复时逐条再验。
- 已知勿重复：第二轮（e8857d1）与实测批（78c69ab）已修项不重复上报；上轮已修项
  的**新回归面**（如 merge_wrapped_lines 对块元素）正常上报。

## 总览

| Skill | A1 科研严谨性 | A2 skill 设计 | A3 产出质量 | A4 代码 |
|---|---|---|---|---|
| lit-search | P0×1 P1×2 P2×4 | P2×5 | P2×2 | P2×4 |
| medical-imaging-review | P1×5 | P2×3 | 无发现（已查） | P1×1 P2×4 |
| paper-slide-deck | P2×2 | P2×3 | P2×3 | P1×1 P2×3 |
| research-paper | P0×1 P1×4 P2×1 | P2×1 | P1×1 P2×2 | P2×5 |
| research-proposal | P2×3 | P2×3 | P2×3 | P2×3 |
| scholar-slides | P1×2 P2×1 | P1×1 P2×1 | P1×2 P2×2 | P1×1 P2×1 |
| 交叉层（跨 skill） | P2×1 | — | P2×1 | P1×1 P2×3 |

**合计：P0×2 · P1×13+8=21 · P2×45。**

严重度定义：P0=会产出错误/不可回溯的结果、真实使用中崩溃或静默失败、可被踩中的
严谨性漏洞；P1=可靠性/可用性/可维护性明显受损、文档-行为缝隙、纪律只有文档没有
 enforcement；P2=打磨。

---

## P0（2 条）

### RP-01 [A1] research-paper：占位符门禁正则放走文档自己规定的冒号形旗标
- 位置：`research-paper/SKILL.md:101`、`research-paper/references/QUALITY_CHECKLIST.md:12` vs `references/CITATION_INTEGRITY.md:16`
- 证据：门禁 grep 为 `\[UNVERIFIED\]`（闭括号全词），而 Rule 3 规定的旗标格式是
  `[UNVERIFIED: …]`。实测对 `We compare against [UNVERIFIED: Smith et al. 2024] …`
  运行门禁 **0 命中（exit 1）**。严格按文档打旗标的未核验引用对 zero-hits 门禁完全
  隐形——披露纪律可被静默绕过且带"机械证据"。与 78c69ab 给 research-proposal 修掉
  的缺陷同型，本 skill 在同一 commit 里创建却继承了旧模式。
- 修法：两处 `\[UNVERIFIED\]` → `\[UNVERIFIED[^]]*\]`（POSIX 可移植的排除括号写法，
  与 research-proposal 的 canonical 版对齐。落地批注：初版用了 `[^\]]`——在
  Python re/ugrep 下正确、在 BSD/POSIX grep 下静默失配，codex 评审 CB-1 抓出后
  改为 `[^]]` 并让契约测试用真实 grep 执行）。

### LS-01 [A1] lit-search：`harvest --resume` 静默丢弃已提交阶段记录，却把阶段结局抄进新 manifest
- 位置：`src/litsearch/harvest.py:271-274`（对照同文件 :359-369 `read_all_records`）
- 证据：`carried` 只读主采集 `records.jsonl`；顶会/整卷/滚雪球阶段记录在
  `records_*.jsonl` 中，续跑后从语料消失；同时 :266-270 把旧 manifest 全部 complete
  结局（含阶段）追加进新 manifest → `find_gaps`（declared⊆executed）与
  `latest_degraded` 均不报警，PRISMA 识别数按记录文件统计而静默少算，滚雪球补回的
  文献在召回证据里凭空蒸发，退出码 0。评审 agent 以 respx 构造「openalex 成功 +
  europepmc 失败 + 2 条 stage3 记录」复现；主会话源码验证成立。
- 修法：`carried` 改用 `read_all_records(resume_from)`（`found_by ∩ retry_hashes`
  过滤天然只剔除重跑范围），补回归测试（含阶段 fixture 的 resume 用例）。

## P1（21 条）

### lit-search
- **LS-02** `lit reclassify` 漏更新 `canonical_records`，自产 run 过不了 `lit verify`
  | `cli.py:374-396` + `verify.py:53-61` | 只重建窗口状态计数，`counts = old | counts`
  不触碰 canonical_records；去重规则演进使 canonical 2→3 后 verify 报 corpus-count。
  修法：重判时同步写 `canonical_records`（顺带 `records_fetched`）+ 回归测试。
- **LS-03** `triage --auto-resolve` 可机器定谳撤稿记录，违反 SKILL.md:445 声明的
  不变量 | `cli_judge.py:578-629`、`screen_jev.py:412-450` | 撤稿强制人筛只在
  `finish_screening_round` 生效；`tiebreak_candidates` 四条入选条件均不查
  `is_retracted`。构造「通道分歧 + jev 0.95」的撤稿记录被机器裁定 include 并流入
  included.jsonl。修法：`tiebreak_candidates` 过滤 `record.is_retracted` + 回归测试。

### medical-imaging-review（审计器的六个洞）
- **MIR-01** 多指标 Markdown 表格/紧凑列表被并成单一 ambiguous 候选 → 永久
  critical | `checks_claims.py:39-49`（merge_wrapped_lines 仅以空行/标题为边界）、
  `:80-84`、`:449-458` | 按 TEMPLATES.md:689-694 自荐的 method/evidence table 放
  两行数据（Dice 0.85/AUC 0.91）端到端审计出 critical ambiguous_claim_segmentation。
  这是上轮硬换行修复的回归面：散文修好了，块元素被吞。修法：`|` 行与列表/引用
  标记行视为块边界（或表格按行产出候选）+ 回归测试。
- **MIR-02** 正文无内联 citekey 的量化主张可由指向任意来源的 ledger 行完成"三方"
  绑定 | `checks_claims.py:477`（`citation_ids or (None,)`）、`:434-436` | 手稿句
  `AUC was 0.85.`（零引用）+ citekey=smith2024 的 ledger 行 → findings=[]。三角链
  只剩两角。修法：无 citekey 的量化/方向类候选直接报 critical。
- **MIR-03** 「collection 开始后路由不可变」写在 TEMPLATES.md:128-130 的 Validation
  rules 里，但无任何校验器执行 | `checks_config.py:36-37` 只查 config.route == 请求
  路由 | 实测：init systematic 项目（人工 gate not_ready）→ 改 config 为 narrative →
  `--route narrative` 审计 **exit 0**。降级换皮即可躲过全部人工 gate。修法：审计
  交叉核对 PROTOCOL.md/search_log 记录的路由与 config，不一致且无 protocol_deviations
  记录时报 critical + 回归测试。
- **MIR-04** 前导点小数（.85/.9）逃过量化检测，以 factual 过审并跳过全部数值一致性
  检查 | `constants.py:514-523`（QUANTITATIVE_RE 各分支均要求前导 0）| 实测
  `AUC of .85` → kind=factual。修法：增加 `(?<!\w)\.\d+\b` 分支 + 回归测试。
- **MIR-05** 人工 gate 的反 AI 校验拦不住 gpt4/chatgpt/claude3 |
  `projectio.py:377-383`（token 后必须紧跟 `[-_:]` 或行尾）| 与 TEMPLATES.md:612 的
  承诺冲突。修法：词干匹配 `(gpt|chatgpt|claude|gemini|copilot|llm|bot)\w*` 一类
  + 边界用例。
- **MIR-06** 文档枚举的 claim_type=synthesis 在审计器不可满足 |
  `checks_claims.py:156-182`（candidates 永不产出 synthesis kind）、`:286-287`、
  `:478-491` vs `TEMPLATES.md:345` | 按文档合法填写 claim_type=synthesis → critical
  「claim_type does not cover the detected factual claim」。修法：synthesis 可覆盖
  factual 检测（或给 candidates 加综述信号）+ 回归测试。

### research-paper
- **RP-02** results_ledger 对账——本 skill 特有的防造假门禁——恰是唯一没有可粘贴
  命令的"机械门禁" | `references/QUALITY_CHECKLIST.md:3-19` | 文件头承诺 mechanical
  gates 贴输出为证，ledger 对账只有散文描述。修法：给一条可粘贴的对账命令。
- **RP-03** 对账范围仅 Abstract/Results，而 STRUCTURE_GUIDE 要求 Discussion 复述
  数字、Methods 承载 n=/超参 | `QUALITY_CHECKLIST.md:14` 等 | 凭空写 n=500 可通过
  全部门禁。修法：对账范围扩到全文自有数字。
- **RP-04** AI-tell 门禁覆盖小于自家禁用表 | `WRITING_STYLE.md:23-28` vs
  `SKILL.md:104` | 实测 "over the past **years**" 与 "众所周知" 均 0 命中。修法：
  正则补齐禁用表条目（并考虑与 research-proposal 的正则同步为共享家族）。
- **RP-05** STARD 在选择表有、在 Phase 1 路由表无——诊断准确性研究路由悬空 |
  `SKILL.md:33-39` vs `REPORTING_CHECKLISTS.md:15` | 修法：路由表补 Diagnostic
  accuracy → STARD 2015 行。
- **RP-06** CS/会议论文变体三处结构描述互相矛盾且无对应 scaffold | `SKILL.md:39`
  vs `STRUCTURE_GUIDE.md:17-19` vs `assets/` | 一等公民场景照 scaffold 起草会缺
  Related Work。修法：统一 CS 变体结构并补 conference scaffold 或明示改写规则。

### paper-slide-deck
- **PSD-01** `merge-to-pdf.ts:219` 用 `Bun.write`，node 运行时在全部图片 embed 完成后
  于最后一步崩溃（实测 "Error: Bun is not defined"，exit 1，PDF 未产出）| 与同文件
  :29 注释承诺的 node 兼容矛盾；文件第 1 行本就 import 了 writeFileSync。修法：改
  `writeFileSync(outputPath, Buffer.from(pdfBytes))` + 回归测试。

### scholar-slides
- **SS-01** 数字接地漏收 3 个会上屏的字段，公式常数可静默过闸 |
  `scripts/lib/qa.mjs:24-43` | collectFields 不含 `s.equations[].latex`、two-column
  `s.text`、`s.eyebrow`（三者均在 layouts.mjs 渲染上屏）。实测构造 deck（latex 含
  99.9、text 含 87.7、eyebrow 含 42）→ groundNumbers 0 条 finding。直接违背
  math.md:39「公式里的数字同任何数字一样接地」。修法：collectFields 增补三字段 +
  回归测试。
- **SS-02** 三份文档仍指向已退役的 PANDA 基准语料 | `benchmarks/README.md:48-50`、
  `benchmarks/eval/scorecard.md:41,53,66-67`、`references/aesthetics-review.md:105` |
  manifest.json 实为 attention/deepseek/glm5/xlstm 系列，无 PANDA。修法：引用改指
  现役条目。
- **SS-03** export_pptx 默认输出路径与 run_benchmark 期望错位：按文档重建后 parity
  门静默不跑 | `export_pptx.mjs:181`（默认 `out/<name>/deck.pptx`）vs
  `run_benchmark.mjs:56`（找 `<dir>/deck/deck.pptx`），benchmarks/README.md:18-20 的
  官方重建命令不带输出参数 | 实测基准行 `no-pptx`，parity.n=-1 不计入 hardFail，
  PPTX-parity 回归整体静默跳过。修法：exporter 默认写 `<dir>/deck/deck.pptx`（或
  修文档命令）+ 回归测试。
- **SS-04** 公式栅格化失败路径：逐条静默丢弃 + 汇总行虚报 | `export_pptx.mjs:48`
  （`if (!el || !box) continue;` 零警告）、`:185`（nEquationsRasterized 数收集数
  而非渲染数）| no-Chromium 路径先 WARN 后汇总仍打印 N rendered；parity 对 equation
  布局不期望图片，抓不住。修法：计数改 eqMap.size，每条 skip 打 WARN。
- **SS-05** install.sh 冒烟检查吞掉测试失败，坏安装以 0 退出 | `install.sh:38-39`
  （`cmd && echo OK`：失败只少打一行 echo，set -e 对 && 列表非末位命令不生效）|
  README.md:68 声称 install 用测试套件验证。修法：改 `|| { echo FAILED; exit 1; }`。
- **SS-06** 部署副本未同步：上一轮触发边界修复在仓库里、不在运行时 |
  repo `SKILL.md:6-11` vs `~/.claude/skills/scholar-slides/SKILL.md`、
  `~/.claude-gateway/skills/scholar-slides/SKILL.md` | 两处安装副本仍含「poster,
  or grant pitch」、缺 NOT 子句与 Learnings 节；其余文件逐字节一致。**处置：
  停机坪**（涉及仓库外文件，见运行记录）。

### 交叉层
- **XC-06** [P1·升级] CI 盲区：research-paper 与 research-proposal 零可执行检查，
  文档契约漂移无门禁 | 对照 medical 的 `test_document_contract.py` 模式（锁死路由
  声明、banned 短语、schema 版本）| 本轮 RP-01、RP-04 与 rprop 的正则/豁免/字数类
  P2 全部可被一个 doc-contract 测试拦住。修法：为两个纯文档 skill 各建
  `tests/test_document_contract.py` + 根级 citation-core 一致性检查进 CI。

## P2（45 条）

### lit-search
- **LS-04** SKILL.md:437 记载不存在的 `lit triage --limit`（实为
  `lit screen --model jev --limit`，cli_judge.py:339）——按文档校准阈值会撞死胡同。
- **LS-05** SKILL.md:418 引用不存在的 `zotero_add_by_doi`（本机 MCP 为
  `zotero_add_item`）。
- **LS-06** `references/jev-profile-template.yaml` 在 SKILL.md（Claude 实际加载的
  文件）内零入口，仅在 README.md:316 出现。
- **LS-07** `lit fulltext` 在 skill 内不可发现（SKILL.md:294 唯一出现处；工作流与
  产物表均无）。
- **LS-08** `lit deliver --ccf` 在缓存复用路径被静默忽略（cli.py:1491-1501 只在不
  复用分支调 `_load_ccf`），回显不提。
- **LS-09** ranked.csv 把「未评价」（None）与「否」（False）渲染成同一空串
  （rank.py:662-663），违背「未评价≠低」纪律。
- **LS-10** fulltext 三处 `except SourceError: return []` 把解析器故障静默折算成
  「暂无合法 OA」（fulltext.py:104,143,213），institutional_access.csv 混淆两者。
- **LS-11** `--sources` 拼错源名静默跳过（cli.py:268 + harvest.py:231-235），无校验
  无告警——正是本项目最不能接受的失败模式。
- **LS-12** snowball 轮次统计只在整条命令结束后落盘（cli.py:583,633-638），中途
  抛错则已完成轮次永久缺失，饱和曲线在残缺历史上判饱和。
- **LS-13** 上述四个已实证缺陷均无测试锁定（test_harvest_resume 无阶段 fixture、
  reclassify 只断言 exit 0、triage 用例无撤稿记录、deliver 复用用例不测 --ccf）。

### medical-imaging-review
- **MIR-07** 与 lit-search 的两阶段协作边界（README 讲了，SKILL.md/references 零
  落地：如何消费 dois.md、如何归一进 search/exports/）未落文档。
- **MIR-08** SKILL.md:21 与 frontmatter 承诺把 meta-analysis/umbrella 交给
  specialized methods workflow——该 workflow 不存在，代理可能虚构交接。
- **MIR-09** narrative/method-survey 禁用语（WORKFLOW.md:93）仅 title/abstract 的
  systematic review 触发检查，正文其余禁用语零检查。
- **MIR-10** 测试盲区：表格 claim 行为零用例、无 init→audit 往返用例、ai_like 无
  gpt4/chatgpt 边界用例。
- **MIR-11** 巨函数违反仓库自身 <50 行规约：validate_human_gate 约 495 行
  （checks_human.py:21-515）、complete_row 约 220 行——恰是严谨性规则最密集处。
- **MIR-12** ledger section 匹配约定（去编号、casefold、文首=preamble）未文档化，
  代理只能从报错反推（checks_claims.py:294、parsing.py:22-27）。
- **MIR-13** init 被硬杀遗留 `.initializing-*` 残骸且后续永不清理
  （init_review_project.py:581-602）。

### paper-slide-deck
- **PSD-02** 映射置信度表（>80%/50-80%）是无标定的伪量化
  （analysis-framework.md:273-276），全 skill 无机制计算这些百分比。
- **PSD-03** 断言两条生成路径"同一底层 Gemini 模型"无依据（SKILL.md:426），Web 端
  模型版本不受控。
- **PSD-04** content-rules.md:92-93 指向不存在的 "SKILL.md 风格画廊"（实在
  style-selection.md）。
- **PSD-05** skill 内部保留被 frontmatter 排除的 live-talk/答辩话语
  （academic-paper.md:3、analysis-framework.md:165,182-190、style-selection.md:35），
  三处互相矛盾。
- **PSD-06** 显式 `--style` 仍强制走 3 变体+确认（SKILL.md:164,183），与选项语义
  冲突。
- **PSD-07** API 失败路径：生成器退出码 0 + merge 间隙警告误诊为删除场景
  （generate-slides.py:303-310、merge-to-pptx.ts:181-184）。
- **PSD-08** 混合 deck 的 PDF 页面尺寸不一致（merge-to-pdf.ts:205-206：4K AI 页 vs
  1080p extract 页）。
- **PSD-09** Setup 未列 Pillow，而 webp→PNG 转换强依赖它（SKILL.md:37-41、
  generate-slides.py:91-96），新机器首跑全军覆没。
- **PSD-10** .txt prompt 在 PPTX 备注中被静默丢弃（merge-to-pptx.ts:107-108 只配对
  .md；生成器明确接受 .txt）。
- **PSD-11** 文档声称指数退避，实现是线性（SKILL.md:229 等 vs
  generate-slides.py:148 `5*(attempt+1)`）。
- **PSD-12** detect-figures.ts 纯函数零测试（决定抽哪张图哪一页的高杠杆模块）。

### research-paper
- **RP-07** 绑定报告清单的落盘产物（checklist_<name>.md）没有机械门禁。
- **RP-08** Reference Files 表的相位映射与文件实际需要矛盾（CITATION_INTEGRITY 标
  Phase 2/4 但含 Phase 5 gate；QUALITY_CHECKLIST 标 Phase 5 但 Phase 2 建 ledger
  要读 schema）。
- **RP-09** 中文摘要字数门禁用 `wc -w`，实测 19 字句计 2（QUALITY_CHECKLIST.md:23；
  zh 路径应 `wc -m`）。
- **RP-10** author–year 对账抽查 grep 只覆盖 et al. 形态（CITATION_INTEGRITY.md:43-44）。
- **RP-11** SUBMISSION_PACK 缺作者贡献（CRediT）条目而 SKILL.md:110 承诺了；
  "COflicts" 错字。
- **RP-12** paper_draft.md 从未被指定为草稿文件名却是两门禁扫描对象（Phase 4 不命名
  输出，门禁硬编码；改名则假阴性零命中）。
- **RP-13** zh scaffold 末行括号不闭合（paper_scaffold_zh.md:54）。
- **RP-14** "学号制期刊"为错词（STRUCTURE_GUIDE.md:56，应为国内期刊/学报类）。
- **RP-15** [PENDING] 旗标未登记进共享核心旗标分类（citation-integrity-core.md:36-42），
  违反核心自身的防漂移规则。
- **RP-16** learnings/ 链接悬空、目录不存在（SKILL.md:130）——与 XC-01 同源。
- **RP-17** ledger 链描述与 schema 列名不符（SKILL.md:73 的 claim_location 不在
  表头）。

### research-proposal
- **RPROP-01** GB/T 7714 数字号引用（中文默认制式）无对账检测正则
  （CITATION_INTEGRITY.md:75-89 只实例化著者-年份制）。
- **RPROP-02** 共享核心 Rule 2 的 venue 校验只部分实例化；派生标记弱于姊妹变体；
  Rule 5（secondary source）未登记进 core 的 extension 清单。
- **RPROP-03** allowed-tools 声明了不存在的 `zotero_search_notes`（SKILL.md:33）。
- **RPROP-04** Phase 1 无 headless 分支，Phase 2/3 却都有（SKILL.md:71,80）。
- **RPROP-05** 开题报告路由要求加权的 feasibility/existing-basis 节在结构文档中
  不存在（SKILL.md:63）。
- **RPROP-06** 消费 lit-search 产物点名了默认不生成的 references.bib（默认是
  references.md，SKILL.md:10-11、LITERATURE_WORKFLOW.md:25）。
- **RPROP-07** AI-tell 门禁覆盖小于自家禁用表（vital role/sheds light/paves the
  way/ever-evolving/over the past three decades 均 0 命中），且 DOMAIN_TEMPLATES:263
  的模板句仍推荐漏网变体。
- **RPROP-08** Phase 5 占位符豁免清单是英文专属（zh scaffold 表头字段按字面违规）。
- **RPROP-09** 节级字数区间与小节之和不吻合（STRUCTURE_GUIDE.md:89,152）。
- **RPROP-10** "单一权威正则"声明与库内三处复述不符；CI:30/:84 的 grep 目标
  proposal_draft.md 而工作流从不创建该文件。
- **RPROP-11** Timeline 格式示例表与同节标准相位表矛盾（STRUCTURE_GUIDE.md:283-289，
  上轮同病灶残留）。
- **RPROP-12** WSG 引用密度表引用了提案不存在的 Discussion 节
  （WRITING_STYLE_GUIDE.md:446）。

### scholar-slides
- **SS-07** README 压测数字仅部分可复现（figures 98.4% 可复算；"9 papers"与
  "~92% usable"无逐篇测量记录支撑，README.md:102）。
- **SS-08** SKILL.md 的 Node 测试命令少列 3 个测试文件（照 SKILL.md 跑=44 tests，
  全量=75，SKILL.md:107-108）。
- **SS-09** qa_report.json 落盘丢失 timing/aesthetics（数组属性上的非索引属性被
  JSON.stringify 丢弃，qa_report.mjs:103,142）。
- **SS-10** 导出器对缺失图文件静默跳过（export_pptx.mjs:111 无 else）。
- **SS-11** detect_figures 双处裸 `except Exception: pass`
  （detect_figures.py:371-372,383-384），排障信息为零。

### 交叉层
- **XC-01** `lit-search/research-paper/learnings/README.md` 是放错位置的文件
  （e8857d1 提交错位），应在 `research-paper/learnings/`——同时解除 RP-16 的悬空
  链接。修法：git mv（内容保全的重命名，非删除；决策已入运行记录）。
- **XC-02** README.md:27 "All four writing/rendering skills"——注册表现有五个
  变体（第二轮加了 research-paper 未更新此句）。
- **XC-03** lit-search/SKILL.md:8 引用不存在的 `literature-search/` 流水线路径
  （代码在 `src/litsearch`，CLI 是 `lit`）。
- **XC-04** citation 变体派生标记 3/5 缺失（research-proposal、scholar-slides、
  paper-slide-deck 无 "Derived from" 头），核心的防漂移约定未被一致执行。
- **XC-05** scholar-slides IMPLEMENTATION_PLAN.md "Editable PPTX & Beamer deferred"
  与已交付的 PPTX 导出矛盾（2026-06-29 锁定决策未随实现更新）。
- **XC-07** learnings/README.md 惯例只在 medical/rprop 有，lit-search（惯例发源地）
  与 scholar-slides 缺——一致性打磨。

## 无发现的格子（C1 证据）

- medical-imaging-review × A3 产出质量：**无发现**。检查了：init 四路由实测，生成
  文件清单与 TEMPLATES.md:47-52 逐项一致（common 10 文件+12 子目录，route-specific
  不多不少）；REVIEW_TYPES 清单被 test_document_contract.py:69-110 双向锁定；exit
  0/1/2 语义与 ARCHITECTURE.md:33 一致并有 CLI 子进程测试；失败路径良好（exit 2+
  单行 stderr+无半写文件，atomic staging 真原子）；报告含 gate_status/四级
  summary/finding 带 line 与 excerpt。
- 其余 23 个 skill×角度格子均有 ≥1 条发现（见上）。
- 正向核验（选摘）：lit-search 金标准召回可证伪、PRISMA 拒绝渲染语义真实、Chapman
  估计三重限定语全在代码里；mir 的 gate_status 永不 pass 有契约测试锁定；psd 的
  乱码告知/Step 6.5 校对/base-prompt 数据保真护栏如实；ss 的 grounding≠语义正确
  分工如实传达、flag 纪律端到端有效、依赖与 import 一致、仓库卫生良好（out/ 入库
  是 .gitignore 注释声明的耐久 spec 设计）。

## 处置计划

1. **批 1（P0）**：LS-01、RP-01 —— 每处带红→绿回归验证；首次 gate 运行包含一次
   故意破坏演示（C8）。
2. **批 2（P1 代码类）**：LS-02/03、MIR-01..06、PSD-01、SS-01/03/04/05——全部带
   回归测试。
3. **批 3（P1 文档类 + CI 升级）**：RP-02..06、XC-06（doc-contract 测试 ×2 +
   citation-core 一致性检查进 CI）。
4. **批 4（P2 高价值）**：rigor 相邻与文档-行为缝隙类（LS-04..07、11、12、
   MIR-08、09、12、RP-09..17、RPROP-01..08、PSD-04、07、09、10、SS-02、07、08、
   XC-01..05）。
5. **停机坪/ledger**：SS-06（仓库外文件）、MIR-11（大重构，风险>收益）、其余 P2
   逐条 minor-open 或顺手修。

> 本文档为 Stage 1 交付物；各 finding 的最终处置状态以运行记录
> `docs/autopilot/runs/2026-10-10-design-round3-upgrade.md` 的 ledger 为准。
