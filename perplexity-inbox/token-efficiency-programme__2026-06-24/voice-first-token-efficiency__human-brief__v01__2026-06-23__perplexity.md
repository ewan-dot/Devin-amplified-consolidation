---
title: "Keep Talking, Spend Less — your voice-first loop, costed (human brief)"
document_type: "readable_research_conclusion"
artifact_id: "voice-first-token-efficiency__human-brief__v01__2026-06-23__perplexity"
date_utc: "2026-06-23T20:40:00Z"
project: "Amplified Partners"
author: "Perplexity Computer"
stage: "synthesis"
audience: "Ewan"
purpose: "Plain-English answer: how to keep talking the way you do, but make it token-efficient and organisationally useful."
source_refs: ["companion agent doc same date", "Methodology Synthesis Part XVI + Appendix G (your Mac)", "research_voice_first_efficiency.md"]
attribution: "Your architecture (Amplified). External numbers cited in the agent doc. Synthesis by Perplexity Computer."
epistemic_tier: "STRUCTURED"
epistemic_role: "clarity"
tier_reason: "Published pattern numbers + a design mapped onto your existing pipe; not yet measured on your estate."
confidence_plain_english: "High on the mechanism — and most of it you've already designed. Not yet measured on our own spend."
open_questions:
  - "Which Mac runs local speech-to-text, and is it whisper.cpp or MacWhisper?"
  - "Does the pipe's curator already auto-harvest breakthroughs, or is that still manual?"
companion_agent_doc: "voice-first-token-efficiency__research-conclusion__agent-doc__v01__2026-06-23__perplexity"
system_of_record: "Drive"
machine_action_allowed: "recommend"
next_human_decision: "Approve the 5-step loop and let me wire the two fastest wins (local capture + cheap cleanup)."
outcome:
  class: "methodology_candidate"
  plain_english_reason: "A reusable way to keep your talking style while cutting spend, built on your own pipe."
---

# Keep talking. The fix isn't your mouth — it's what happens after you speak.

You asked three things. Short answers first, then the loop.

- **Would routing through your research pipe cut spend?** Yes — a lot. Pulling the right bits from your Brain instead of dumping everything into the chat keeps the context small; for most questions that's **20–200× cheaper** and gives the same answer.
- **Would idealising the prompt cut spend?** Yes — every turn after. A sharpened prompt is smaller and stays out of the bloat; compression research shows **2–20× fewer tokens**, and one study cut cost **94%** while *improving* quality.
- **Both together?** That's the loop below. Frontier models can do 95% of the quality while only handling ~14% of the calls if you route well.

## The one idea
Your talking is **divergent** — exploring, rambling, finding the pudding. That phase must stay free and messy; you can't pre-structure discovery (the Pudding Technique itself came out of a ramble with Grok — it's in your own Appendix G). So make that phase cost **£0** by capturing it locally.

Then there's the **convergent** phase — turning the ramble into something precise and acting on it. That's where the expensive model earns its keep, so you hand it a tight, sharpened, reusable brief — never the raw ramble.

The good news: **you already designed this.** Your Epistemic Pipe already insists on a "sharpened question," applies the Five Rods, and refuses to fire an expensive external search until it's tried locally twice. We're just putting a price tag on it and adding a free front door.

## Your loop, and the better version of each step
1. **You talk** → capture it on your Mac with local speech-to-text. **£0 in tokens.** Keeps the raw audio and every tangent, exactly as you like.
2. **Clean it up** → a cheap (or local) model fixes the wrong words and tidies it. The expensive model never has to read the mess.
3. **Sharpen it** → your neutral-brief skill turns it into a tight prompt. Because it's now stable, it can be cached (90% off on reuse) — something a fresh ramble can never be.
4. **Route it** → pipe/Brain for discovery, cheap model for mechanical work, the frontier model **only** for real judgment on the sharpened question.
5. **Harvest it** → pull the keepers into your Brain. This is the sneaky one: it's free, and it stops you paying to rediscover the same insight next month.

## Why this is also organisationally efficient
Step 5 is where the two goals become one. Every breakthrough you file makes the next search hit your own Brain instead of an expensive model. Cheaper *and* more organised, from the same action.

## What I'd wire first
The two fastest wins need no new infrastructure: **local capture (Step 1)** and **cheap cleanup (Step 2)**. That alone stops the frontier model paying to wade through raw speech. Say go and I'll set them up — I just need to know which Mac you want doing the listening.
