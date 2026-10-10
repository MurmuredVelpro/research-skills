# 第三轮设计评审 × 全 skill 起飞升级

- status: landed
- workspace: autopilot/design-round3-upgrade
- base: 78c69ab (feat/design-round2 HEAD, unmerged — human confirmed at takeoff)
- contract: docs/autopilot.md
- review pin: d73a425（第一轮全程序评审）；最终 HEAD: 0be4989
- 落地时间：2026-10-10

## Goal

用户原话：「这是一个科研skills库，请你从科研严谨性、skill设计、产出结果质量、以及代码四个角度review各个skill。然后根据你的review结果对全部skill进行起飞升级。」

## Acceptance criteria

Frozen at takeoff. A run changes `status` and `evidence`, never the criterion.

| id | criterion | proven by | status | evidence |
|---|---|---|---|---|
| C1 | 六个 skill 每个在四个角度各有 ≥1 条带 `file:line` 证据的评审记录，或明确「无发现」 | `docs/design-review-round3.md` 的 skill×角度矩阵 | proven | 922d3f7（24 格全满：23 格有发现，mir×A3 无发现+检查清单） |
| C2 | 每条 finding 分级并有处置状态，无静默丢弃 | 本记录 Ledger | proven | 本记录（85 条全部处置——审计员逐 ID 展开核对无静默丢弃） |
| C3 | 全部确认的 P0 修复且带红→绿验证 | 修复 diff + 证据 | proven | LS-01：stage2-c8-break-proof.txt；RP-01：rp01-red-green-retroactive.txt（审计员指出原始红跑未落盘后，以真实 grep 引擎追溯补录，exit 1→0） |
| C4 | 全部确认的 P1：修复或 minor-open 写明理由 | 本记录 Ledger | proven | 21 条 P1：20 修复 + 1 parked（SS-06，仓库外文件） |
| C5 | 四条测试链（现为十条 gate 命令）在最终 commit 干净树上全绿 | 最终 machine gate 证据 | proven | final-gate-2.txt @ 6fcbc35 前置、round2-fixes-gate.txt、round2b-gate.txt @ 0be4989（最终）均 10/10 exit 0；审计员独立复跑亦全绿 |
| C6 | 本 run 改动过行为的 README/SKILL.md 声明逐条核对一致 | 文档核对清单 | proven | d73a425：顶层 README 两处（ss 压测口径、references.bib 条件）+ 五个变体声明同步；repo-contract 测试锁数量声明 |
| C7 | 落地 review gate 两名评审每条 finding 有处置行 | 本记录 Ledger | proven | codex 5 条 + auditor 6 条全部处置（见「Landing review」）；codex 二轮 2 条异议成立并重修（fixed-unreviewed） |
| C8 | machine gate 被证明会失败（故意破坏红→复原绿） | 红/绿证据对比 | proven | stage2-c8-break-proof.txt（回退 LS-01 修复 → pytest exit 1 → 恢复 → exit 0） |

## Stages

1. [x] 四维评审 — owns C1, C2 ✅ 922d3f7（6 agent + 交叉层；docs-only 跳过 review gate）
2. [x] P0 修复批 — owns C3, C8 ✅ efc2af2
3. [x] P1 修复批（代码 5 skill + 文档 + CI 契约基座）— owns C4 ✅ 782ad1f/86b7192/0b40c23/f7be5f0/3cddac7
4. [x] P2 清扫 + learnings + README 同步 — owns C6 ✅ 5fb1000/e65d45e/16b578b/d73a425/cc30766
5. [x] 落地 — 最终 gate + 双评审 + 本记录完结 — owns C5, C7 ✅ 0be4989（gate 10/10；codex 两轮 + 验收审计全部处置）

## 批次与 commit 对照

| commit | 内容 |
|---|---|
| 2920f58 | 合同生效 + 运行记录 |
| 922d3f7 | 评审文档（Stage 1 交付物） |
| efc2af2 | P0：LS-01 + RP-01（含 doc-contract 测试基座与 CI research-paper job） |
| 782ad1f | lit-search 批 1：LS-02/03 |
| 86b7192 | mir 批 2：MIR-01..06 + Round3AuditHardeningTests |
| 0b40c23 | psd 批 3：PSD-01 |
| f7be5f0 | ss 批 4：SS-01..05、SS-08 |
| 3cddac7 | rp/rprop/xc 批 5：RP-02..06/08/11..17、RPROP-07/08、XC-01/02/04/06、RP-15/16 |
| 5fb1000 | lit-search 批 6：LS-04..12 |
| e65d45e | ss/psd 批 7：SS-02/07/09/10/11、PSD-02..07/09/10/11 |
| 16b578b | mir/rp/rprop/learnings 批 8：MIR-07..09/12/13、RP-07/09/10、RPROP-01..06/09..12、XC-07 |
| d73a425 | C6 README 同步 + 证据 |
| cc30766 | XC-03 一行文档修复（评审 pin 之后） |

## Ledger

### Decisions

| id | stage | chose | rejected | wrong if |
|---|---|---|---|---|
| D1 | 1 | 基线取 feat/design-round2@78c69ab（人为确认） | main（评审到旧状态） | 人类落地时想基于 main 重放 |
| D2 | 4 | XC-01 用 `git mv`（内容保全重命名）+ 清走搬空目录 | 视为删除红线停机坪 | 用户认为任何路径消失都需事先确认 |
| D3 | 1 | 评审发现先亲验再定级（P0/P1 全部亲验） | 照单全收 | 验证时发现误读（未发生） |
| D4 | 3 | MIR-02 使无 citekey 实质主张直接 critical，两个编码旧宽松契约的测试随新契约更新 | 保持宽松以不动测试 | 用户认为既有测试即契约不可更新 |
| D5 | 5 | cc30766（XC-03）落在评审 pin d73a425 之后——一行文档修复，最终 gate 在其后复跑覆盖 | 为评审纯净度回滚重做 | 评审期间该行又被改动 |
| D6 | 4 | SS-07/README 压测数字改为「可复算口径」（60/61≈98.4%） | 保留原数字（无逐篇记录支撑） | 人类有 9 篇测量记录可出示 |

### Review findings（第三轮评审 85 条的处置）

| id | round | reviewer | finding | status | note |
|---|---|---|---|---|---|
| LS-01 | 1 | review-lit-search | --resume 丢阶段记录 | blocking-fixed | efc2af2 + 回归（红→绿） |
| LS-02/03 | 1 | review-lit-search | reclassify 计数 / triage 撤稿 | blocking-fixed | 782ad1f + 两例回归 |
| LS-04..07 | 1 | review-lit-search | 文档指针×4 | minor-fixed | 5fb1000 |
| LS-08..12 | 1 | review-lit-search | --ccf 忽略/三态/折叠/轮次/拼错源 | minor-fixed | 5fb1000（08/11/12 带测试；09 带测试；10 带测试） |
| LS-13 | 1 | review-lit-search | 四缺陷无测试锁定 | minor-fixed（部分） | 01/02/03 已各带回归；deliver --ccf 用例未写 → minor-open（低风险：现为黄字显形） |
| MIR-01..06 | 1 | review-mir | 审计器六洞 | blocking-fixed | 86b7192 + 六回归锁 |
| MIR-07/08/12 | 1 | review-mir | 协作边界/虚构交接/约定未文档 | minor-fixed | 16b578b |
| MIR-09/13 | 1 | review-mir | 禁用语扫描/staging 残骸 | minor-fixed | 16b578b + 各带测试 |
| MIR-10 | 1 | review-mir | 测试盲区 | minor-fixed（部分） | 表格行为+ai_like 边界已锁；init→audit 往返用例 → minor-open |
| MIR-11 | 1 | review-mir | 巨函数 ~495 行 | minor-open | 拆分是高风险重构，本轮以六洞修复+新测试优先；下轮单独做 |
| PSD-01 | 1 | review-psd | Bun.write 崩溃 | blocking-fixed | 0b40c23 + merge-pdf.test（红→绿） |
| PSD-02..07/09/10/11 | 1 | review-psd | 伪量化/模型断言/指针/话语/变体/退出码/Pillow/.txt/退避 | minor-fixed | e65d45e（07/10 带测试） |
| PSD-08 | 1 | review-psd | PDF 页面尺寸不一致 | minor-open | 统一版面需视觉验证（渲染几何变更），停给下轮带截图验证做 |
| PSD-12 | 1 | review-psd | detect-figures 零测试 | minor-open | 行为与文档一致（评审实测），补测试下轮 |
| RP-01 | 1 | review-rp | 门禁正则放走冒号旗标 | blocking-fixed | efc2af2 + doc-contract（红→绿） |
| RP-02..06 | 1 | review-rp | 对账命令/范围/AI-tell/STARD/CS 结构 | blocking-fixed | 3cddac7（04 另有契约测试锁） |
| RP-07/09/10 | 1 | review-rp | checklist 门禁/wc -m/抽查正则 | minor-fixed | 16b578b |
| RP-08/11..17 | 1 | review-rp | 相位映射/CRediT/文件名/括号/错词/列名等 | minor-fixed | 3cddac7 |
| RP-15/16 | 1 | review-rp | [PENDING] 进核心 / learnings 悬空 | minor-fixed | 3cddac7（16 经 XC-01 归位） |
| RPROP-01..06/09..12 | 1 | review-rprop | 数字制正则/venue/工具名/headless/落点/产物/字数/正则声明/timeline/WSG | minor-fixed | 3cddac7 + 16b578b（07/08 进契约测试） |
| SS-01..05 | 1 | review-ss | 接地盲区/PANDA/parity 路径/公式计数/install 门 | blocking-fixed | f7be5f0 + 四例回归（SS-03 红→绿验证） |
| SS-06 | 1 | review-ss | 部署副本未同步 | parked | 见「Parked」P1 |
| SS-07..11 | 1 | review-ss | 数字口径/测试命令/json 形状/缺图/裸 except | minor-fixed | e65d45e + f7be5f0 |
| XC-01..05 | 0 | 主会话交叉层 | 混入文件/four→five/陈旧路径/派生标记/impl plan | minor-fixed | 3cddac7 + cc30766（XC-03） |
| XC-06 | 0 | 主会话交叉层 | CI 盲区 | blocking-fixed | 3cddac7：两 skill 契约测试 + 根级 repo-contract + CI 三 job |
| XC-07 | 0 | 主会话交叉层 | learnings README 不一致 | minor-fixed | 16b578b |

<!-- 落地双评审（round 2）的处置行在「Landing review」小节追加 -->

### Parked

落地时的人工决定（2026-10-10 已全部裁决执行）：

| id | needs | exact action | unblocks | 状态 |
|---|---|---|---|---|
| P1 (SS-06) | 仓库外文件写入未预授权 | 实测后同步部署副本 | 触发边界修复对真实触发生效 | **done**：实测全链（build 12 slides→PDF→PPTX 落新默认路径→parity 真跑→qa json 带 timing）；抢救部署副本独有的 learning（380009a）后 rsync 两处副本，SKILL.md/qa.mjs diff 为空 |
| P2 (落地) | 合并未预授权 | 合并两分支进 main 并 push | 全部成果进 main | **done**：见下方合并记录 |
| P3 (AU-4) | 合同为你所有 | gate 三条新命令写进合同 | 合同与实际 gate 一致 | **done**：2a66962 |
| P4 (AU-5/D2) | 追认或否决 D2 | 追认则无动作 | XC-01 最终性 | **done**：人为追认，git mv 维持 |

### Not verified

- **SS-06 部署副本**：本 run 不写仓库外文件——两处安装副本的陈旧程度由评审 agent diff 证实，修复停机坪。
- **CI 全链**：本地跑的是与 ci.yml 逐条等价的命令；GitHub Actions 上的 11 个 job（含新增 research-proposal/repo-contract）未实际触发（不推分支是红线）。
- **外部端到端**：lit-search 真实网络采集、paper-slide-deck 真实 Gemini 生成、scholar-slides Playwright 截图/aesthetics 评分环——按合同离线执行，未验证。
- **CLAIM/STARD/TRIPOD 等外部命名的年份与时效**（评审 agent 亦声明离线不可核）。
- **scholar-slides python 套件 1 例环境性 skip**（out/deepseek_conf 未构建的 parity 用例，基线同款 skip）。
- **round-2 双评审 pin 于 d73a425**：其后仅 cc30766 一行文档改动（D5），无行为变更。

## Landing review

**第一轮（全程 78c69ab→d73a425，pin）**

codex 对手（verdict: needs-attention，5 blocking）：

| id | finding | status | note |
|---|---|---|---|
| CB-1 | `[^\]]` 在 BSD/POSIX grep 下静默失配（我方当场用 /usr/bin/grep 复现确认；ugrep/Python re 下正确——初版验证用错了引擎） | blocking-fixed | 四处正则改 POSIX 可移植 `[^]]`；两 skill 契约测试改 subprocess 跑真实 grep（红→绿：坏模式 2 failed）@ 0be4989 前身 |
| CB-2 | init staging 清理会删并发实例的工作；且新测试缩进在 `__main__` 后未被收集（117→118 证实） | blocking-fixed | 先加 15 分钟年龄守卫；codex 二轮指出 mtime 不能证明实例退出 → 终版改为**只报告不删除** @ 0be4989 |
| CB-3 | merge-pdf.test.mjs 依赖的 pdf-lib 在干净 CI 必缺（psd job 无 npm 步骤） | blocking-fixed | ci.yml 加 scripts/npm ci 步骤 |
| CB-4 | checklist 门禁 `\[ \]\s*$` 只拦行尾空复选框 | blocking-fixed | 先改项首匹配；codex 二轮指出规范自荐产物是两列表 → 终版改为粘贴命令解析表格行（实测三失败形态 exit 1/干净表 exit 0）@ 0be4989 |
| CB-5 | C2 在 pin 处账本为空却标 proven | fixed-by-subsequent-commit | 总账 8a98eaf 在 pin 后落地（与 D5 同因）；审计员逐 ID 验证内容为真 |

验收审计（verdict: needs-work，窄口径——代码实质全部证实）：

| id | finding | status | note |
|---|---|---|---|
| AU-1 | 运行记录在 7155420→d73a425 间停更（stages 未勾/ledger 空/C2 凭空 proven） | fixed-by-subsequent-commit + 披露 | 过程失误如实记录：总账补齐在 pin 后；内容经审计逐 ID 验证。**这是本 run 的程序瑕疵，非内容问题** |
| AU-2 | 计数错：实有 85 条（2 P0+21 P1+62 P2），headline 68/P2×45 三处误 | minor-fixed | 三处更正 + 评审文档加落地批注 |
| AU-3 | RP-01 红跑证据未落盘 | minor-fixed | rp01-red-green-retroactive.txt（真实 grep 引擎，标注追溯补录） |
| AU-4 | gate 由合同 7 条扩至 10 条（只紧不松），合同未刷新 | parked→P3 | 合同为人所有；落地时请刷新 |
| AU-5 | D2（XC-01 git mv 使旧路径消失）需人工追认 | parked→P4 | 见 Parked 表 |
| AU-6 | 红线未越（未 push/未并 main/无外部写） | confirmed | — |

**第二轮（修复差量，最后一轮）**

codex 二轮（verdict: needs-attention，2 blocking；同时确认 CB-1 修复实测通过、计数更正正确）：

| id | finding | status | note |
|---|---|---|---|
| CB2-R2 | 15 分钟阈值不能证明并发实例退出（暂停超阈值的实例仍活着） | fixed-unreviewed | 异议成立：改报告不删除 @ 0be4989；测试改「残骸保留+init 成功」 |
| CB4-R2 | 门禁仍放行规范要求的两列表格（复选框门禁查错形状） | fixed-unreviewed | 异议成立：粘贴命令解析表格行 @ 0be4989；三失败形态/干净表双向实测 |

按协议，第二轮为最后一轮：其后的两条修复**无评审者过目**（fixed-unreviewed），
已在验收走查第 3/6 项给出人工复核入口。

**评审分歧记录**：无 dispute——codex 两轮全部异议经复现或事实核对后均成立并采纳。

## 争议与追认请求

- **P4（AU-5/D2）**：XC-01 的 `git mv lit-search/research-paper/learnings/README.md
  research-paper/learnings/README.md` 使旧路径从树中消失。本 run 将「内容保全的
  重命名」不视为删除红线（D2），请你在落地时追认或否决。
- **P3（AU-4）**：机器 gate 从合同 7 条扩到 10 条（新增 research-paper /
  research-proposal / 根级 repo-contract 三条命令，只紧不松）。合同为你所有，
  未动；请决定是否把新命令写进合同。

## Acceptance walk

Riskiest first.

| # | where | do | should see |
|---|---|---|---|
| 1 | 仓库根 | `python3 -m pytest tests/ -q && cd research-paper && python3 -m pytest tests/ -q` | 全绿——新增的跨 skill 契约层（注册表↔变体↔README、旗标分类）在跑 |
| 2 | lit-search/ | `uv run pytest tests/test_harvest_resume.py -q` | 5 例含「续跑携带阶段记录」——把 harvest.py 的 carried 临时改回只读主文件，此测试应变红（C8 同款自证） |
| 3 | medical-imaging-review/ | `python3 -m pytest tests/ -q` | 118 例含 Round3AuditHardeningTests 与「残骸只报告不删除」（fixed-unreviewed 的人工复核入口） |
| 4 | scholar-slides/ | `node --test tests/*.test.mjs` | 79 例；`node scripts/export_pptx.mjs out/attention/deck.json` 后 `ls out/attention/deck/deck.pptx` 存在（parity 门可跑） |
| 5 | paper-slide-deck/ | `node scripts/merge-to-pdf.ts <任一图片目录>`（纯 node） | PDF 真实产出（不再 "Bun is not defined"） |
| 6 | research-paper/ | 在临时目录建 `checklist_x.md` 两列表（一行空处置）跑 QUALITY_CHECKLIST 的粘贴命令 | 空处置行被点名、exit 1（fixed-unreviewed 的人工复核入口） |
| 7 | docs/design-review-round3.md | 通读 | 85 条发现与你看到的代码现状对得上；处置与本记录 Ledger 一致 |
| 8 | 停机坪 P1 | 执行 Parked 表两条 cp 后 diff 验证 | 部署副本与仓库一致 |
