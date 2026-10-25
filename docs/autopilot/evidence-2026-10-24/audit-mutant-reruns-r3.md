c5-backup-severity: cmd=[cd scholar-slides && node --test tests/deck_type.test.mjs] exit=1 signature-matched=yes
c5-jc-guard: cmd=[cd scholar-slides && node --test tests/deck_type.test.mjs] exit=1 signature-matched=yes
c5-limits-guard: cmd=[cd scholar-slides && node --test tests/deck_type.test.mjs] exit=1 signature-matched=yes
c6-allow-ignored: cmd=[cd paper-slide-deck && node --test tests/proofread.test.mjs] exit=1 signature-matched=yes
c6-mark-sha: cmd=[cd paper-slide-deck && node --test tests/proofread.test.mjs] exit=1 signature-matched=yes
c6-no-entry-ok: cmd=[cd paper-slide-deck && node --test tests/proofread.test.mjs] exit=1 signature-matched=yes
c1-fullwidth-percent: cmd=[cd research-paper && python3 -B -m pytest tests/ -q -p no:cacheprovider] exit=1 signature-matched=yes
c1-fullwidth-equals: cmd=[cd research-paper && python3 -B -m pytest tests/ -q -p no:cacheprovider] exit=1 signature-matched=yes
c1-ledger-leading-dot: cmd=[cd research-paper && python3 -B -m pytest tests/ -q -p no:cacheprovider] exit=1 signature-matched=yes
c7-symlink-guard: cmd=[cd medical-imaging-review && python3 -B -m pytest tests/ -q -p no:cacheprovider] exit=1 signature-matched=yes
