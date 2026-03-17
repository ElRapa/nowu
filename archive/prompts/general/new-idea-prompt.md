# New Idea Capture Prompt

Use this when you have an idea, problem, or question that needs to be structured before acting on it.
Paste into Perplexity, Copilot chat, or `know capture`.

---

I have a new idea or observation for the nowu framework. Help me structure it.

**Raw idea:** [describe in your own words, no polish needed]

**Context:**
- Active project: [project name]
- Related module or component: [know / flow / bridge / soul / dash / unsure]

**Please:**
1. Determine which atom type this best fits: fact / concept / task / decision / lesson / reference / preference / ephemeral
2. Write a clean `title` (≤ 10 words) and `content` (2–4 sentences) for the atom
3. Suggest a project_scope value
4. If this is a task: suggest priority (low/medium/high/critical) and whether it belongs in v1 or v2
5. If this conflicts with an existing decision, flag it
6. Output the atom in this format:

```
Type: task
Title: Implement semantic search layer in know
Content: Add embedding-based search as the third search layer, after FTS5 keyword and exact match. Use sentence-transformers for embedding generation. Store embeddings in a separate SQLite table. Integrate into know.search() with a combined ranking function.
Project: know
Priority: medium
V1/V2: v2 (per V2_IDEAS.md)
```
