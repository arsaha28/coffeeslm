# Coffee SLM — Tasks

Rule: every step changes ≤ 20 lines and has one check.
Status: ⬜ todo · 🔄 in progress · ✅ done

## Decisions
- General English corpus: **TinyStories** (fluent simple English; story-style tone accepted)
- Curriculum: TinyStories → coffee text (+10–20% TinyStories replay) → coffee Q&A
- Architecture: **GPT-2 style** (learned positions, LayerNorm, GELU MLP) → exportable to Hugging Face
- Tokenizer: **byte-level BPE** (GPT-2 style), written by us, exported as `vocab.json` + `merges.txt`

## Phase 0 — Setup
| Step | Task | Check | Status |
|---|---|---|---|
| 0.1 | Create Python 3.13 virtual env `.venv` | `python --version` → 3.13 | ✅ |
| 0.2 | `requirements.txt` with torch + pytest, install | `pip list` shows both | ✅ |
| 0.3 | Package folders `src/coffee_slm/` + `pytest.ini` | `import coffee_slm` works | ✅ |
| 0.4 | `device.py`: pick MPS or CPU | prints `mps` | ✅ |
| 0.5 | First test for `device.py` | `pytest` passes | ✅ |
| 0.6 | `git init` + `.gitignore` | `git status` clean of `.venv` | ✅ |

## Phase 1 — Data
| Step | Task | Check | Status |
|---|---|---|---|
| 1.1 | Fetch one Wikipedia page ("Coffee") as plain text | print first 200 chars | ⬜ |
| 1.2 | Save raw text to `data/raw/` | file exists | ⬜ |
| 1.3 | List of coffee page titles in config | load + print list | ⬜ |
| 1.4 | Fetch all pages in list | count files in `data/raw/` | ⬜ |
| 1.5 | Fetch Gutenberg book *All About Coffee* | print size | ⬜ |
| 1.6 | Strip Gutenberg header/footer | test on sample | ⬜ |
| 1.7 | Clean text (whitespace, references) | test on sample | ⬜ |
| 1.8 | Deduplicate paragraphs | test on sample | ⬜ |
| 1.9 | Train/val split, write `data/clean/` | print sizes | ⬜ |
| 1.10 | General English corpus (TinyStories sample) | print size | ⬜ |

## Phase 2 — Tokenizer
| Step | Task | Check | Status |
|---|---|---|---|
| 2.1 | Byte-level tokenizer (text ↔ bytes 0–255) | round-trip test | ⬜ |
| 2.2 | Count adjacent token pairs | test on tiny string | ⬜ |
| 2.3 | Merge one pair | test on tiny string | ⬜ |
| 2.4 | BPE training loop | learns merges on sample | ⬜ |
| 2.5 | BPE encode / decode | round-trip test | ⬜ |
| 2.6 | Save / load tokenizer | reload gives same ids | ⬜ |
| 2.7 | Train on coffee corpus, inspect "cappuccino" | print tokens | ⬜ |

## Phase 3 — Dataset & Bigram baseline
| Step | Task | Check | Status |
|---|---|---|---|
| 3.1 | Encode corpus to token-id file | print token count | ⬜ |
| 3.2 | Random batch sampler (x, y shifted by 1) | shape test | ⬜ |
| 3.3 | Bigram model | forward shape test | ⬜ |
| 3.4 | Loss computation | loss ≈ ln(vocab) at init | ⬜ |
| 3.5 | Minimal training loop | loss goes down | ⬜ |
| 3.6 | Sampling / generate | prints text | ⬜ |

## Phase 4 — Transformer
| Step | Task | Check | Status |
|---|---|---|---|
| 4.1 | Config dataclass (dims, layers, heads) | instantiate | ⬜ |
| 4.2 | Token + position embeddings | shape test | ⬜ |
| 4.3 | Single attention head | shape test | ⬜ |
| 4.4 | Causal mask | future positions = 0 | ⬜ |
| 4.5 | Multi-head attention | shape test | ⬜ |
| 4.6 | MLP | shape test | ⬜ |
| 4.7 | Transformer block (residual + LayerNorm) | shape test | ⬜ |
| 4.8 | Full GPT model | logits shape test | ⬜ |
| 4.9 | Parameter count | print ~15M | ⬜ |

## Phase 5 — Pretraining (general English)
| Step | Task | Check | Status |
|---|---|---|---|
| 5.1 | YAML config loader | prints config | ⬜ |
| 5.2 | Optimizer setup (AdamW) | test | ⬜ |
| 5.3 | LR schedule (warmup + cosine) | plot/print values | ⬜ |
| 5.4 | Train step function | loss is a number | ⬜ |
| 5.5 | Validation loss | runs on val set | ⬜ |
| 5.6 | Checkpoint save / load | reload equal | ⬜ |
| 5.7 | Logging loss to CSV | file grows | ⬜ |
| 5.8 | Full pretraining run | val loss decreasing | ⬜ |

## Phase 6 — Coffee domain adaptation
| Step | Task | Check | Status |
|---|---|---|---|
| 6.1 | Data mixer: coffee + 10–20% TinyStories replay | ratio test | ⬜ |
| 6.2 | Resume from checkpoint on mixed data | loss continues | ⬜ |
| 6.3 | Compare samples before / after | read samples | ⬜ |

## Phase 7 — Instruction tuning
| Step | Task | Check | Status |
|---|---|---|---|
| 7.1 | Chat template (`<q>` … `<a>`) | format test | ⬜ |
| 7.2 | Create coffee Q&A dataset (JSONL) | count pairs | ⬜ |
| 7.3 | Loss mask (answer tokens only) | mask test | ⬜ |
| 7.4 | SFT training run | loss decreasing | ⬜ |

## Phase 8 — Evaluation
| Step | Task | Check | Status |
|---|---|---|---|
| 8.1 | Eval question set (~100) | count | ⬜ |
| 8.2 | Run model on eval set | answers file | ⬜ |
| 8.3 | Score + compare across phases | table | ⬜ |

## Phase 9 — Chat
| Step | Task | Check | Status |
|---|---|---|---|
| 9.1 | Temperature + top-k sampling | test | ⬜ |
| 9.2 | CLI chat script | ask a coffee question | ⬜ |

## Phase 10 — Export & Integrate
| Step | Task | Check | Status |
|---|---|---|---|
| 10.1 | Export tokenizer to HF format | HF tokenizer gives same ids | ⬜ |
| 10.2 | Map our weights → `GPT2LMHeadModel` | loads without errors | ⬜ |
| 10.3 | Compare HF vs our model outputs | logits match | ⬜ |
| 10.4 | (Optional) Push to Hugging Face Hub | model page visible | ⬜ |
| 10.5 | LangChain example via `HuggingFacePipeline` | answers a coffee question | ⬜ |
| 10.6 | (Optional) Convert to GGUF, run in Ollama | `ollama run` works | ⬜ |
