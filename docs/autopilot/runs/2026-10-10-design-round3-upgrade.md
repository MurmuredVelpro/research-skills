# 第三轮设计评审 × 全 skill 起飞升级

- status: flying <!-- landing: 最终 gate 复跑 + 双评审处置完毕后置 landed -->
- workspace: autopilot/design-round3-upgrade
- base: 78c69ab (feat/design-round2 HEAD, unmerged — human confirmed at takeoff)
- contract: docs/autopilot.md
- head (review pin): d73a425（其后另有 cc30766 一行文档修复 XC-03，见 D5）

## Goal

用户原话：「这是一个科研skills库，请你从科研严谨性、skill设计、产出结果质量、以及代码四个角度review各个skill。然后根据你的review结果对全部skill进行起飞升级。」

## Acceptance criteria

Frozen at takeoff. A run changes `status` and `evidence`, never the criterion.

| id | criterion | proven by | status | evidence |
|---|---|---|---|---|
| C1 | 六个 skill 每个在四个角度各有 ≥1 条带 `file:line` 证据的评审记录，或明确「无发现」 | `docs/design-review-round3.md` 的 skill×角度矩阵 | proven | 922d3f7（24 格全满：23 格有发现，mir×A3 无发现+检查清单） |
| C2 | 每条 finding 分级并有处置状态，无静默丢弃 | 本记录 Ledger | proven | 本记录（68 条全部处置） |
| C3 | 全部确认的 P0 修复且带红→绿验证 | 修复 diff + 证据 | proven | LS-01/RP-01 @ efc2af2；resume 测试红（stage2-c8 证据）→绿；doc-contract 2 subtest FAILED→passed |
| C4 | 全部确认的 P1：修复或 minor-open 写明理由 | 本记录 Ledger | proven | 21 条 P1：20 修复 + 1 parked（SS-06，仓库外文件） |
| C5 | 四条测试链（现为十条 gate 命令）在最终 commit 干净树上全绿 | 最终 machine gate 证据 | open | d73a425 上 10/10 绿（final-gate.txt）；cc30766 后复跑见 final-gate-2.txt |
| C6 | 本 run 改动过行为的 README/SKILL.md 声明逐条核对一致 | 文档核对清单 | proven | d73a425：顶层 README 两处（ss 压测口径、references.bib 条件）+ 五个变体声明同步；repo-contract 测试锁数量声明 |
| C7 | 落地 review gate 两名评审每条 finding 有处置行 | 本记录 Ledger | open | 见「Review findings」R 轮 |
| C8 | machine gate 被证明会失败（故意破坏红→复原绿） | 红/绿证据对比 | proven | stage2-c8-break-proof.txt（回退 LS-01 修复 → pytest exit 1 → 恢复 → exit 0） |

## Stages

1. [x] 四维评审 — owns C1, C2 ✅ 922d3f7（6 agent + 交叉层；docs-only 跳过 review gate）
2. [x] P0 修复批 — owns C3, C8 ✅ efc2af2
3. [x] P1 修复批（代码 5 skill + 文档 + CI 契约基座）— owns C4 ✅ 782ad1f/86b7192/0b40c23/f7be5f0/3cddac7
4. [x] P2 清扫 + learnings + README 同步 — owns C6 ✅ 5fb1000/e65d45e/16b578b/d73a425/cc30766
5. [ ] 落地 — 最终 gate + 双评审 + 本记录完结 — owns C5, C7（进行中）

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

### Review findings（第三轮评审 68 条的处置）

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

In the order the human should do them.

| id | needs | exact action | unblocks | verify afterward |
|---|---|---|---|---|
| P1 (SS-06) | 仓库外文件写入未预授权 | 同步部署副本（两处）：<br>`cp research-paper/../scholar-slides/SKILL.md ~/.claude/skills/scholar-slides/SKILL.md`（即仓库内 scholar-slides/SKILL.md）<br>`cp scholar-slides/SKILL.md ~/.claude-gateway/skills/scholar-slides/SKILL.md`<br>或改为 symlink 指向仓库 | 上一轮+本轮的触发边界修复（NOT 子句、poster/grant-pitch 移除）对真实触发生效 | `diff scholar-slides/SKILL.md ~/.claude/skills/scholar-slides/SKILL.md` 为空；新会话里问「poster 幻灯」不再触发 scholar-slides |
| P2 (落地) | 合并未预授权 | 人工决定：`git checkout main && git merge --no-ff feat/design-round2 && git merge --no-ff autopilot/design-round3-upgrade && git push`（或按需重排/review） | 三个分支上的全部成果进入 main | `gh run watch`（CI 十一个 job）全绿 |

### Not verified

- **SS-06 部署副本**：本 run 不写仓库外文件——两处安装副本的陈旧程度由评审 agent diff 证实，修复停机坪。
- **CI 全链**：本地跑的是与 ci.yml 逐条等价的命令；GitHub Actions 上的 11 个 job（含新增 research-proposal/repo-contract）未实际触发（不推分支是红线）。
- **外部端到端**：lit-search 真实网络采集、paper-slide-deck 真实 Gemini 生成、scholar-slides Playwright 截图/aesthetics 评分环——按合同离线执行，未验证。
- **CLAIM/STARD/TRIPOD 等外部命名的年份与时效**（评审 agent 亦声明离线不可核）。
- **scholar-slides python 套件 1 例环境性 skip**（out/deepseek_conf 未构建的 parity 用例，基线同款 skip）。
- **round-2 双评审 pin 于 d73a425**：其后仅 cc30766 一行文档改动（D5），无行为变更。

## Landing review

（双评审结论到达后填入）

## Acceptance walk

Riskiest first.

| # | where | do | should see |
|---|---|---|---|
| 1 | 仓库根 | `python3 -m pytest tests/ -q && cd research-paper && python3 -m pytest tests/ -q` | 全绿——新增的跨 skill 契约层（注册表↔变体↔README、旗标分类）在跑 |
| 2 | lit-search/ | `uv run pytest tests/test_harvest_resume.py -q` | 5 例含「续跑携带阶段记录」——把 harvest.py 的 carried 临时改回只读主文件，此测试应变红（C8 同款自证） |
| 3 | medical-imaging-review/ | `python3 -m pytest tests/test_audit_manuscript.py -q` | 117 例含 Round3AuditHardeningTests 五锁 |
| 4 | scholar-slides/ | `node --test tests/*.test.mjs` | 79 例；`node scripts/export_pptx.mjs out/attention/deck.json` 后 `ls out/attention/deck/deck.pptx` 存在（parity 门可跑） |
| 5 | paper-slide-deck/ | `node scripts/merge-to-pdf.ts <任一图片目录>`（纯 node） | PDF 真实产出（不再 "Bun is not defined"） |
| 6 | docs/design-review-round3.md | 通读 | 68 条发现与你看到的代码现状对得上；处置与本记录 Ledger 一致 |
| 7 | 停机坪 P1 | 执行 Parked 表两条 cp 后 diff 验证 | 部署副本与仓库一致 |
