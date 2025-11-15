# BuildMate
An AI-accelerated compiler that keeps dependency lists razor-thin, built in 24 hours of sleep deprivation at DubHacks 2025.

## Overview
BuildMate is a VSCode plugin + Flask container that auto-fixes and builds embedded C projects with minimal dependencies. It runs code in Docker (MinGW for Windows compatability), attempts compilation, and—if it fails—lets an AI agent research, patch, and retry until it works.

Started as a joke about "AI-everything." Became a functional proof-of-concept.

**TLDR:** It compiles. It debloats. It learns.

[Presentation →](https://docs.google.com/presentation/d/1O6FQpgzIuRjXI7pAPp5VFMJ2p7l43DUGuFoBtTeZ6GM/edit?usp=sharing) | [Devpost →](https://devpost.com/software/buildmate-av7oj8)

## How It Works
1. Runs C code with `mingw` in Docker.
2. On compile failure:
   - Summarizes error + code context.
   - Generates search query via RAG.
   - Uses Brave Search for docs/examples.
   - Synthesizes a fix and recompiles.
3. Repeats until success or timeout.

Powered by Gemini API + lightweight web retrieval.

## What's Next
- Async multi-agent architecture.
- Vector database for deeper context.
- FSM-based decision-making.
- Modular microservice design.

## Hackathon Notes
Built overnight, out of country, and 5 Redbulls deep. Despite the chaos, it genuinely compiles, debloats, and teaches a lot about agentic AI workflows.

---
