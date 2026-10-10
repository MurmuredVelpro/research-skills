# 第三轮设计评审 × 全 skill 起飞升级

- status: flying
- workspace: autopilot/design-round3-upgrade
- base: 78c69ab (feat/design-round2 HEAD, unmerged — chosen so the upgrade builds on the
  skills' current state; human confirms at takeoff)
- contract: docs/autopilot.md

## Goal

用户原话：「这是一个科研skills库，请你从科研严谨性、skill设计、产出结果质量、以及代码四个角度review各个skill。然后根据你的review结果对全部skill进行起飞升级。」

## Acceptance criteria

Frozen at takeoff. A run changes `status` and `evidence`, never the criterion.

| id | criterion | proven by | status | evidence |
|---|---|---|---|---|
| C1 | 六个 skill（lit-search / medical-imaging-review / paper-slide-deck / research-paper / research-proposal / scholar-slides）每个在四个角度（A1 科研严谨性 / A2 skill 设计 / A3 产出质量 / A4 代码）各有 ≥1 条带 `file:line` 证据的评审记录，或明确写出「无发现」及检查了什么 | 评审文档 `docs/design-review-round3.md` 的 skill×角度矩阵 | proven | docs/design-review-round3.md @ 922d3f7 |
| C2 | 评审产出的每条 finding 分级（P0/P1/P2）并在 ledger 中有处置状态（fixed / minor-open / rejected+反证 / parked），无静默丢弃 | 本记录 Ledger「Review findings」表 | proven | 本记录 Ledger（随批次更新至全部处置） |
| C3 | 全部确认成立的 P0（破坏严谨性 / 错误产出 / 代码缺陷）在最终 commit 前修复，每处修复带一个「会失败的验证」（回归测试或可重复的破坏性检查，红→绿证据） | 修复 diff + 测试/gate 证据 | proven | LS-01/RP-01 修复 @ efc2af2：两条新回归测试均在缺陷形态下红（resume 测试 exit 1 见 stage2-c8；doc-contract 2 subtest FAILED 见运行输出）、修复后绿 |
| C4 | 全部确认成立的 P1：修复，或 ledger 为 minor-open 并写明理由 | 本记录 Ledger | open | |
| C5 | 四条测试链（lit-search pytest+ruff；scholar-slides pytest+node；medical pytest；paper-slide-deck pytest+node）在最终 commit、干净工作树上全绿 | 最终 machine gate 证据文件 | open | |
| C6 | 升级后 `README.md` 与各 `SKILL.md` 的行为级声明同实际行为一致——凡本 run 改动过行为的声明逐条核对 | 文档核对清单 + 证据 | open | |
| C7 | 落地 review gate 两名评审（codex 对手 + acceptance auditor，全程 base→HEAD）的每条 finding 在本记录有处置行 | Ledger 表 | open | |
| C8 | machine gate 本身被证明「会失败」：至少一次故意破坏使某条 gate 命令变红，随后复原变绿 | 红运行 + 绿运行的 gate 证据对比 | proven | docs/autopilot/evidence/stage2-c8-break-proof.txt（回退 LS-01 修复 → pytest exit 1 → 恢复 → exit 0） |

`status` is `open`, `proven` or `parked`.

## Stages

1. [x] 四维评审 — 6 skill × 4 角度并行评审 + 交叉验证 + 分级 ledger，产出
   `docs/design-review-round3.md` — owns C1, C2 ✅ 922d3f7（docs-only，跳过
   review gate；机器 gate 7/7 绿）
2. [x] 升级批 1 — P0 修复（每处带红→绿验证）；首次 gate 运行包含一次
   故意破坏演示（证明 gate 会红） — owns C3, C8 ✅ efc2af2（gate 8/8 绿）
3. [ ] 升级批 2 — P1 代码修复（LS-02/03、MIR-01..06、PSD-01、SS-01/03/04/05，
   全部带回归测试）+ P1 文档修复（RP-02..06、XC-06 doc-contract 测试与 CI） —
   owns C4
4. [ ] 升级批 3 — P2 高价值修复 + README/SKILL.md 文档-行为同步核对 — owns C6
5. [ ] 落地 — 最终 machine gate + 全程 review gate（codex + auditor）+ 本记录完结 +
   验收走查 — owns C5, C7

## Ledger

### Decisions

| id | stage | chose | rejected | wrong if |
|---|---|---|---|---|
| D1 | 1 | 基线取 feat/design-round2@78c69ab（人为起飞确认） | main（会评审到不含第二轮升级的旧状态） | 人类在落地时想基于 main 重放 |
| D2 | 2 | XC-01 用 `git mv`（内容保全的重命名）执行 | 视为「删除跟踪文件」红线而停机坪 | 用户认为任何路径消失都算删除需事先确认 |
| D3 | 1 | 评审 agent 上报的发现先在源码亲验再定级（P0/P1 全部亲验，P2 修复时逐条再验） | 照单全收 | 验证发现误读源码（未发生：0 条被驳回） |

### Review findings

| id | round | reviewer | finding | status | note |
|---|---|---|---|---|---|

`status` is `blocking-fixed`, `minor-fixed`, `minor-open`, `fixed-unreviewed`, `parked`,
`rejected` or `dispute`. The note holds the commit that fixed it or the evidence that
refutes it; a dispute states both positions.

### Parked

In the order the human should do them.

| id | needs | exact action | unblocks | verify afterward |
|---|---|---|---|---|

### Not verified

Everything the run did not or could not check, and why.

## Acceptance walk

Riskiest first.

| # | where | do | should see |
|---|---|---|---|
