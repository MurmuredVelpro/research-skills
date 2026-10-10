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
| C1 | 六个 skill（lit-search / medical-imaging-review / paper-slide-deck / research-paper / research-proposal / scholar-slides）每个在四个角度（A1 科研严谨性 / A2 skill 设计 / A3 产出质量 / A4 代码）各有 ≥1 条带 `file:line` 证据的评审记录，或明确写出「无发现」及检查了什么 | 评审文档 `docs/design-review-round3.md` 的 skill×角度矩阵 | open | |
| C2 | 评审产出的每条 finding 分级（P0/P1/P2）并在 ledger 中有处置状态（fixed / minor-open / rejected+反证 / parked），无静默丢弃 | 本记录 Ledger「Review findings」表 | open | |
| C3 | 全部确认成立的 P0（破坏严谨性 / 错误产出 / 代码缺陷）在最终 commit 前修复，每处修复带一个「会失败的验证」（回归测试或可重复的破坏性检查，红→绿证据） | 修复 diff + 测试/gate 证据 | open | |
| C4 | 全部确认成立的 P1：修复，或 ledger 为 minor-open 并写明理由 | 本记录 Ledger | open | |
| C5 | 四条测试链（lit-search pytest+ruff；scholar-slides pytest+node；medical pytest；paper-slide-deck pytest+node）在最终 commit、干净工作树上全绿 | 最终 machine gate 证据文件 | open | |
| C6 | 升级后 `README.md` 与各 `SKILL.md` 的行为级声明同实际行为一致——凡本 run 改动过行为的声明逐条核对 | 文档核对清单 + 证据 | open | |
| C7 | 落地 review gate 两名评审（codex 对手 + acceptance auditor，全程 base→HEAD）的每条 finding 在本记录有处置行 | Ledger 表 | open | |
| C8 | machine gate 本身被证明「会失败」：至少一次故意破坏使某条 gate 命令变红，随后复原变绿 | 红运行 + 绿运行的 gate 证据对比 | open | |

`status` is `open`, `proven` or `parked`.

## Stages

1. [ ] 四维评审 — 6 skill × 4 角度并行评审 + 交叉验证 + 分级 ledger，产出
   `docs/design-review-round3.md` — owns C1, C2
2. [ ] 升级批 1 — P0 修复（每处带红→绿验证 + learnings）；首次 gate 运行包含一次
   故意破坏演示（证明 gate 会红） — owns C3, C8
3. [ ] 升级批 2 — P1 修复或 minor-open ledger（按 skill 分批提交，沿用 repo 的
   批次惯例） — owns C4
4. [ ] 升级批 3（如需）— P2 打磨 + README/SKILL.md 文档-行为同步核对 — owns C6
5. [ ] 落地 — 最终 machine gate + 全程 review gate（codex + auditor）+ 本记录完结 +
   验收走查 — owns C5, C7

## Ledger

### Decisions

| id | stage | chose | rejected | wrong if |
|---|---|---|---|---|

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
