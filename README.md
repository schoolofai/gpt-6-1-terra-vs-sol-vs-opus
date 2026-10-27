# GPT-6.1 Terra vs GPT-6.1 Sol vs Claude Opus 5.5: 11 coding tests

Everything behind the ProAI Clips video **"Is the Cheap AI Model Enough for Hard Coding? 11 Tests, One Surprise"**.

Video: https://youtu.be/e7F0hUp1FQA

Terra and Sol ran in Codex CLI, Opus 5.5 ran in Claude Code. Each run got the same prompt word for word, in a fresh empty folder, with no follow-ups. Cost = the token counts each tool reported × the official list price (the Codex runs were on a subscription, so these are API-equivalent costs). One run per model per round, 27 Oct 2026.

## Results

Easy rounds (R1–R7, all passed, 0 interventions)

| | Terra | Sol | Opus 5.5 |
|---|---|---|---|
| 7 runs total | $0.25 · 6.0 min | $0.84 · 18.3 min | $2.69 · 13.4 min |

Tough rounds

| Round | Terra | Sol | Opus 5.5 |
|---|---|---|---|
| R9 3D windmill from 2 reference images (/8) | 8/8 · 153 s · $0.107 | 8/8 · 282 s · $0.198 | 8/8 · 549 s · $1.384 |
| R10 Dungeon crawler (5 automated checks) | 5/5 · 108 s · $0.062 | 5/5 · 205 s · $0.135 | 5/5 · 255 s · $0.574 |
| R11 Planted-bug hunt (10 hidden bug tests) | high: 10/10, 0 regressions · 97 s · $0.107 | 9/10 · 565 s · $0.564 | 9/10 · 212 s · $0.852 |
| R11, Terra at max effort | 10/10, **1 regression** · 1,107 s · $1.021 | – | – |

R8 (Terra only): Codex app Computer Use on a real Mac filled an invoice form from a PDF, all fields correct, 66 s, about $0.09 at list price.

Harness note: the Codex runs had their Playwright browser tool switched off; Claude Code still had one, and in R9 Opus used it to check its own render.

## What's here

- `prompts/` the exact prompts (R1, R4, R5, R6, R7, R8_cu, R9, R10, R11)
- `r11-ledgerly/buggy/` the bug-hunt repo exactly as the models got it (7 visible tests, all pass)
- `r11-ledgerly/hidden-tests/` the hidden grader: 10 bug tests + 9 regression tests
- `r11-ledgerly/reference-fix/` my fixed version (passes 19/19)
- `r11-ledgerly/BUGS_KEY.md` the answer key (spoilers)
- `assets/` R9 reference images, R8 invoice + form, R6 ShopLite repo, R7 tool stubs
- `graders/` the R6, R9 and R10 checkers (they expect a `runs/` or `runs_tough/` folder of model outputs; edit the paths at the top)
- `results/` raw metrics (tokens, times, costs) and result boards

## Run the hidden tests on your own model's fix

```bash
cp -r r11-ledgerly/buggy my-attempt   # give my-attempt/ and prompts/R11.md to your agent
LEDGERLY_ROOT=$PWD/my-attempt node --test r11-ledgerly/hidden-tests/bugs.test.js r11-ledgerly/hidden-tests/regression.test.js
```

Node 20+, no dependencies. The buggy repo scores 9 pass / 10 fail (all regression tests pass, every bug test fails).

## Caveats

One run each. The R11 repo is about 1,000 lines with 10 bugs, far smaller than Pawel Huryn's 105-bug test, so treat these as spot checks, not a benchmark.

MIT licence for the code in this repo. The R9 reference images are AI-generated pictures of a generic windmill.
