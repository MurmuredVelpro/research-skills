# audit r3 gate rerun at b00e709 snapshot (bwrap --unshare-net)
$ cd lit-search && /home/ubuntu/jason/research/.autopilot-deps/lit-venv/bin/python -B -m pytest -p no:cacheprovider -o pythonpath=src -q
........................................................................ [ 80%]
........................................................................ [ 88%]
........................................................................ [ 96%]
........................sss.........                                     [100%]
exit 0

$ cd lit-search && /home/ubuntu/jason/research/.autopilot-deps/lit-venv/bin/ruff check --no-cache .
All checks passed!
exit 0

$ cd scholar-slides && /home/ubuntu/jason/research/.autopilot-deps/ss-venv/bin/python -B -m pytest -p no:warnings -p no:cacheprovider -q
..........s.......................................s......sss............ [ 76%]
.............sss......                                                   [100%]
exit 0

$ cd scholar-slides && node --test tests/*.test.mjs 2>&1 | grep -E '^# (pass|fail)'
# pass 97
# fail 0
exit 0

$ cd medical-imaging-review && python3 -B -m pytest tests/ -q -p no:cacheprovider
........................................................................ [ 51%]
....................................................................     [100%]
140 passed in 1.47s
exit 0

$ cd paper-slide-deck && python3 -B -m pytest tests/ -q -p no:cacheprovider
...............                                                          [100%]
15 passed in 0.14s
exit 0

$ cd paper-slide-deck && node --test tests/*.mjs 2>&1 | grep -E '^# (pass|fail)'
# pass 32
# fail 0
exit 0

$ cd research-paper && python3 -B -m pytest tests/ -q -p no:cacheprovider
....................................                                     [100%]
36 passed in 0.12s
exit 0

$ cd research-proposal && python3 -B -m pytest tests/ -q -p no:cacheprovider
..........................................                               [100%]
42 passed in 0.13s
exit 0

$ python3 -B -m pytest tests/ -q -p no:cacheprovider
........                                                                 [100%]
8 passed in 0.04s
exit 0

885 passed, 15 skipped in 13.87s
exit 0
86 passed, 8 skipped in 1.18s
exit 0
