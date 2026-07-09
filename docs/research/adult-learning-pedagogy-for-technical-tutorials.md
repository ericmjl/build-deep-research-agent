# Adult Learning & Pedagogy for Technical Tutorials (SciPy 2026)

**Purpose:** Research base for the AI reviewer agent that checks tutorial notebook
content (programming / data science / AI-ML) against evidence-based pedagogy
principles for adult professional learners (scientists, engineers, researchers).

**Method:** All principles below were extracted from webfetch-accessible sources
(Wikipedia, Learning Scientists). Each finding carries its source URL and a
one-line rationale for *why it matters for this audience*. Epistemically honest
labels are applied: sourced, heuristic (defensible inference from sourced
principles), or gap (could not verify this session).

**Audience calibration — SciPy 2026:** working professionals, not novices. Most
are domain experts (science/engineering) but *novices in the specific tutorial
topic* (deep-research agents). This split — **expert-in-domain, novice-in-topic**
— is the single most important fact for the reviewer. It triggers the
expertise-reversal effect (Section B) and the curse-of-knowledge trap (Section F)
simultaneously.

---

## Source-access audit (epistemic honesty)

| Source requested | Status | Note |
|---|---|---|
| `pmc.ncbi.nlm.nih.gov/articles/PMC11157198/` | **WRONG ARTICLE** | Resolves to a *cancer* paper ("time from primary diagnosis to brain metastasis in lung and breast cancer"), NOT adult learning. The PMC ID is unrelated to andragogy. Do NOT use. |
| `cft.vanderbilt.edu/guides-sub-pages/adult-learning/` | **DEAD/REDIRECTED** | Old CFT guides URL now 302-redirects to Vanderbilt's generic "AdvancED" institute landing page. The specific adult-learning guide content is gone from that URL. |
| `poorvucenter.yale.edu/AdultLearning` | **404** | Dead link. |
| `en.wikipedia.org/wiki/Andragogy` | OK | Full content retrieved. |
| `en.wikipedia.org/wiki/Cognitive_load` | OK | Full content retrieved. |
| `en.wikipedia.org/wiki/Worked-example_effect` | OK | Full content retrieved. |
| `en.wikipedia.org/wiki/Cognitive_apprenticeship` | OK | Full content retrieved. |
| `en.wikipedia.org/wiki/Desirable_difficulty` | OK | Full content retrieved. |
| `en.wikipedia.org/wiki/Curse_of_knowledge` | OK | Full content retrieved. |
| `en.wikipedia.org/wiki/Instructional_scaffolding` | OK | (Correct title; `Scaffolding_(teaching)` is a 404.) |
| `en.wikipedia.org/wiki/Subgoal_labeling` | OK | Full content retrieved. |
| `en.wikipedia.org/wiki/Gradual_release_of_responsibility` | OK | Full content retrieved. |
| `en.wikipedia.org/wiki/Expertise_reversal_effect` | OK | Full content retrieved. |
| `learningscientists.org` (+ spaced-practice post) | OK | Landing + one strategy post retrieved. |
| Mark Guzdial's computing-education blog | **NOT DIRECTLY FETCHED** | Captured his key contribution (subgoal labeling) via the Wikipedia Subgoal labeling article, which cites Margulieux, Guzdial & Catrambone (2012). Direct blog fetch not attempted this session. |

**Gaps to flag:** No peer-reviewed medical-education / CME source was successfully
retrieved this session (the PMC ID was wrong). The andragogy material therefore
rests on Wikipedia (which itself cites Knowles, Merriam, TEAL Center fact sheets)
rather than a primary NCBI/PMC article. Treat the Knowles principles as
well-established in the field but secondary-sourced here.

---

## A) Core andragogy principles (what makes adult learners different)

Source: https://en.wikipedia.org/wiki/Andragogy

### A1. Knowles' six assumptions about adult learners
Malcolm Knowles' andragogy rests on six assumptions that distinguish adults from
child learners (pedagogy). Each maps to a checkable notebook property.

| # | Assumption | Checkable implication for notebook content |
|---|---|---|
| 1 | **Need to know** — adults need to understand *why* something is worth learning before investing effort. | Each major section / new concept should open with a one- to two-sentence "why this matters" tied to the learner's professional context. |
| 2 | **Self-concept** — adults are self-directing and want involvement in planning/evaluating their learning. | Provide optional depth, "try it yourself" prompts, and self-check moments; don't gate everything on the instructor. |
| 3 | **Experience** — prior experience is the richest resource (and a liability when it is wrong). | Explicitly invite learners to connect new content to their existing workflows; surface and correct likely misconceptions. |
| 4 | **Readiness** — adults learn best when the topic has *immediate relevance* to work/life. | Sequence content so each unit is usable on Monday at work, not "you'll need this in chapter 9." |
| 5 | **Orientation** — adult learning is **problem-centered**, not content-/subject-centered. | Organize around a real problem the learner has (e.g. "build a research agent"), not a feature tour of a library. |
| 6 | **Motivation** — internal motivators (self-confidence, growth, recognition) outweigh external ones (grades, certs). | Frame exercises around autonomy/mastery/purpose, not completion badges. |

*Why it matters:* SciPy attendees are volunteers paying attention in 90-minute
blocks; they disengage the instant content feels academic-without-payoff. Every
assumption above is a retention predictor.

### A2. Seven consolidated principles of adult learning
Source: https://en.wikipedia.org/wiki/Andragogy#Principles (citing literacy.ca and the TEAL Center Fact Sheet No. 11)

- Adults must **want** to learn (inner motivation sustains it).
- Adults must **feel they need** to learn — they ask "how does this help me right now?"
- Adults **learn by doing** (active practice integrates component skills).
- Adult learning is **problem-solving-centered** (start from a problem, find the solution).
- **Experience affects learning** — prior knowledge is an asset *and* a liability ("if prior knowledge is inaccurate, incomplete, or immature, it can interfere with or distort the integration of incoming information").
- Adults learn best in **informal, collaborative** situations (not rigid curriculum delivery).
- Adults want **guidance as equal partners**, not to be told what to do.

*Why it matters:* The "experience as liability" point is the most underused in
technical tutorials — instructors rarely audit for *misconceptions the audience
already holds* (e.g. "RAG just means ChatGPT + search").

### A3. The pedagogy → andragogy → heutagogy continuum
Source: https://en.wikipedia.org/wiki/Andragogy#Differences_in_learning

- **Pedagogy:** teacher-directed, didactic, external motivation, standardized curriculum.
- **Andragogy:** self-directed, problem-solving/discussion-based, internal motivation, application-based.
- **Heutagogy:** self-determined — the learner also decides *what* to learn and whether objectives were met.

*Checkable implication:* A SciPy tutorial sits in the **andragogy** band —
learners want to be led through a structured problem, but they expect agency and
expect the instructor to respect their expertise. Heutagogy (fully self-determined)
is the *aspirational end-state* the tutorial should move learners toward by the
final exercise ("now go define your own agent").

---

## B) Cognitive load theory applied to technical content

Source: https://en.wikipedia.org/wiki/Cognitive_load

### B1. The three load types (Sweller)
Working memory is severely limited in capacity and duration; learning requires
moving information through it into long-term memory schemas. Three load types:

- **Intrinsic load** — inherent difficulty of the topic (e.g. 2+2 vs. a differential equation). Cannot be eliminated, but can be **managed by breaking schemas into "subschemas" taught in isolation, then recombined**.
- **Extraneous load** — load imposed by *how* material is presented. **Fully under the instructor's/designer's control.** This is the lever tutorials pull most often (badly).
- **Germane load** — the productive effort the learner puts into schema construction. The goal is to **minimize extraneous so germane can rise**.

*Why it matters:* DS/AI tutorials are intrinsically high-load (many interacting
concepts: tokens, embeddings, retrieval, prompts, tools, graphs). Every
extraneous load addition (unexplained jargon, split attention, decorative detail)
directly subtracts from learning.

### B2. The split-attention effect (Chandler & Sweller)
Source: https://en.wikipedia.org/wiki/Cognitive_load + https://en.wikipedia.org/wiki/Worked-example_effect

When related information sources are separated in space/time (e.g. code in one
cell, explanation in another far above; text describing a diagram placed apart
from the diagram), the learner burns working memory *integrating* them.
**Fix:** physically integrate text with the thing it describes; place explanation
adjacent to the code/figure it explains.

### B3. Miller's 7±2 and chunking (Simon & Chase)
Source: https://en.wikipedia.org/wiki/Cognitive_load

Working memory holds roughly **seven plus or minus two** units. "Chunking" —
organizing information into schema-level units — raises effective capacity.
**Pedagogical implication:** present 3–5 new items per chunk, name them
(subgoal labeling, Section D), and let the names act as the chunk handles.

### B4. The expertise reversal effect (Kalyuga)
Sources: https://en.wikipedia.org/wiki/Expertise_reversal_effect + https://en.wikipedia.org/wiki/Worked-example_effect

This is the **single most important effect for the SciPy audience.**

- Guidance that is *essential for novices* (worked examples, heavy scaffolding, redundant explanation) becomes **redundant or harmful for higher-knowledge learners** because they must expend working memory reconciling external guidance with schemas they already have.
- "Instructional guidance, which may be essential for novices, may have negative consequences for more experienced learners." (Kalyuga)
- **Implication for SciPy:** your learners are experts *in Python/science* but novices *in agents*. You must calibrate guidance **per-concept, not per-learner**: heavy scaffolding on the new agent concepts; minimal scaffolding on the Python they already know. Over-explaining `def` or `pip install` to this audience triggers expertise reversal.

*Why it matters:* A reviewer agent can check whether the notebook is
over-scaffolding familiar material (insulting + harmful) or under-scaffolding
novel material (overwhelming).

---

## C) Teaching programming specifically (worked examples, live coding, scaffolding)

### C1. The worked-example effect (Sweller; Renkl)
Source: https://en.wikipedia.org/wiki/Worked-example_effect

A **worked example** is a step-by-step demonstration of how to perform a task or
solve a problem. The worked-example effect is "the best known and most widely
studied of the cognitive load effects" (Sweller).

Key findings a reviewer can check:

- **Worked examples beat problem-solving and discovery learning for novices** during initial skill acquisition. They reduce extraneous load and free germane load for schema construction.
- **Use example–problem *pairs*, not isolated examples** (Sweller & Cooper): a worked example followed by an isomorphic problem to solve is the canonical pattern. Maps directly to "I do / we do / you do."
- **"At least add a second example"** (Reed & Bolstad) — one example is rarely enough to induce a transferable schema; a second, more-complex example significantly improves transfer.
- **Faded worked examples** (Renkl & Atkinson): progressively remove solution steps so the learner fills them in — this transitions the learner from studying examples to solving problems *without* an expertise-reversal cliff.
- **Self-explanation prompts** matter: most learners are "passive and superficial self-explainers." Worked examples only deliver deep understanding when learners are **guided to actively self-explain** each step.

### C2. Renkl's five criteria for effective worked examples
Source: https://en.wikipedia.org/wiki/Worked-example_effect#Developing_effective_worked_examples

A worked example gives deep understanding only when it:

1. Is **self-explanatory** (the steps speak for themselves).
2. Provides **principle-based, minimalist, example-relation instructional explanations** as help (note: *minimalist* — not exhaustive prose).
3. **Shows relations between different representations** (e.g. code ↔ diagram ↔ natural language).
4. **Highlights structural features** relevant to selecting the correct solution (vs. surface features the learner might wrongly key on).
5. **Isolates meaningful building blocks** (chunks / subgoals — see Section D).

*Reviewer check:* for each code block, does the notebook satisfy these five?

### C3. Subgoal labeling (Margulieux, Catrambone, Guzdial) — *the* programming-specific technique
Source: https://en.wikipedia.org/wiki/Subgoal_labeling

**This is the most directly applicable finding for a programming tutorial.**
(Research specifically on teaching programming with App Inventor and similar.)

- **Subgoal labeling** = giving a *name* to a group of steps in a worked example, where the name describes the function that group achieves.
- It helps learners **separate structural/domain information from incidental information** — novices struggle precisely because they cannot tell which details matter.
- It **reduces cognitive load during problem solving** because the learner has fewer candidate next-steps to consider at each point.
- It supplies a **mental-model framework**: learners who were given subgoal labels *used those labels* when later explaining their own solutions, showing the labels became their organizing schema.
- **Pairing subgoal-labeled instructional text with subgoal-labeled worked examples** improves performance and transfer *even without a live instructor* (directly relevant to notebooks).

*Reviewer check:* code blocks should be annotated with **named functional groups**
(e.g. `# 1. Load and chunk the corpus`, `# 2. Embed chunks`, `# 3. Build the
retriever`) rather than uncommented or line-by-line commented.

### C4. Cognitive apprenticeship — Collins, Brown, Newman
Source: https://en.wikipedia.org/wiki/Cognitive_apprenticeship

Cognitive apprenticeship exists to fix the core problem that **masters fail to
surface the tacit processes** experts use. Six methods:

1. **Modeling** — expert makes the process visible (writes code aloud, explains heuristics).
2. **Coaching** — observes the novice and gives feedback/hints.
3. **Scaffolding** — provides supports the learner can't yet provide themselves; **fades** over time.
4. **Articulation** — gets the learner to verbalize their reasoning ("think-aloud").
5. **Reflection** — learner compares their process to an expert's.
6. **Exploration** — teacher withdraws; learner frames and solves their own problems.

*Why it matters:* A notebook can implement modeling (annotated worked examples),
scaffolding (starter code, partial solutions), articulation (prompts asking the
learner to predict/explain), and exploration (open-ended final exercise).
Coaching and reflection need the live instructor.

### C5. Gradual release of responsibility — the "I do / we do / you do" model
Source: https://en.wikipedia.org/wiki/Gradual_release_of_responsibility

Fisher & Frey's four phases:

| Phase | Tag | Who acts | Notebook analog |
|---|---|---|---|
| Focused lesson | "I do it" | Teacher models | Annotated reference solution cell |
| Guided instruction | "We do it" | Teacher + learner, needs-based groups | Fill-in-the-blank exercise with hints |
| Collaborative | "You do it together" | Learners in pairs/groups | Pair exercise / discussion prompt |
| Independent | "You do it alone" | Learner solo | Open-ended exercise / "your own agent" |

**Fisher & Frey's modeling pattern** (7 steps) is itself a checkable template:

1. **Name** the strategy/skill/task.
2. **State the purpose**.
3. **Explain when** it is used.
4. **Use analogies to link prior knowledge to new learning.**  ← directly supports Section D
5. **Demonstrate** how it is done.
6. **Alert learners about errors to avoid.**
7. **Assess** use of the new skill.

*Reviewer check:* does each new technique introduction follow roughly this shape?

### C6. Instructional scaffolding — the three essential features
Source: https://en.wikipedia.org/wiki/Instructional_scaffolding

1. **Collaboration** between learner and expert (not one-way delivery).
2. Work in the **Zone of Proximal Development** — slightly beyond what the learner can do alone. Requires the instructor to **know the learner's current level**.
3. **Fading** — supports are gradually removed as proficiency grows.

Effective scaffolding additionally requires:
- **Selection of an appropriate task** (neither too hard nor too easy; engaging).
- **Anticipation of errors** the learner is likely to make.
- **Consideration of emotional issues** — managing frustration, sustaining interest.

*Why it matters:* The "anticipation of errors" check is highly actionable: a
good notebook *names the bug the learner is about to hit* before they hit it.

### C7. Two scaffolding types: soft vs. hard
- **Soft / contingent scaffolding:** improvised in the moment (instructor walking the room).
- **Hard / embedded scaffolding:** pre-planned supports for known-hard points (hints, partial code, callout boxes).

A notebook can only ship **hard scaffolding** — so the author must pre-identify
every hard point and embed a support there.

---

## D) Vocabulary & jargon introduction (the most important section for this use case)

This section synthesizes principles from cognitive load theory (B), curse of
knowledge (F), subgoal labeling (C3), and Renkl's worked-example criteria (C2).
Each rule is **checkable**.

### The core problem (from the literature)
- Every undefined technical term is **extraneous cognitive load** (https://en.wikipedia.org/wiki/Cognitive_load). The learner must pause, hold the unknown term in working memory, and keep reading — burning the 7±2 slots needed for the actual concept.
- **Novices cannot distinguish domain-essential information from incidental detail** (https://en.wikipedia.org/wiki/Subgoal_labeling) — so they treat every new term as equally important, which multiplies the load.
- The **curse of knowledge** (https://en.wikipedia.org/wiki/Curse_of_knowledge) means the expert author literally *cannot reconstruct* which terms are jargon to a newcomer — "telling people about the bias does not reduce it." Authorial introspection is insufficient; **student-verified framing** is required (Wieman 2007, cited in Curse of knowledge).

### D1. Define-before-first-use (checkable)
**Rule:** Every domain-specific term must be defined (inline gloss or link) **on or before its first use**, not after.

- *Heuristic from Miller 7±2:* if a reader hits a paragraph with ≥3 undefined jargon terms, they have no working-memory budget left for the concept.
- Source anchor: extraneous load is "under the control of instructional designers" (https://en.wikipedia.org/wiki/Cognitive_load).

### D2. Cap new terms per section (checkable, with a heuristic threshold)
**Rule:** Introduce **no more than ~3 new technical terms per pedagogical chunk** (a chunk = one notebook section or one subgoal-labeled code block).

- This threshold is a **heuristic**, not a hard empirical constant — it follows from working-memory capacity (7±2) minus the slots needed for the actual concept (https://en.wikipedia.org/wiki/Cognitive_load). Flag as heuristic, not sourced fact.
- If a section needs more, **split it** or move definitions to an appendix/glossary and reference rather than teach.

### D3. Use analogies grounded in the learner's existing domain (checkable)
**Rule:** When introducing a novel concept, anchor it with an analogy to something the *specific audience* already knows.

- For SciPy: scientists/engineers. Good anchors = lab protocols, statistical estimation, signal processing, software-engineering patterns they use daily.
- **Avoid analogies from domains your audience doesn't share** (e.g. explaining embedding similarity via a music-theory analogy to a bioinformatics crowd).
- Source: Fisher & Frey modeling step 4 "Use analogies to link prior knowledge to new learning" (https://en.wikipedia.org/wiki/Gradual_release_of_responsibility); Knowles assumption 3 (experience is the basis for learning, https://en.wikipedia.org/wiki/Andragogy).

### D4. Prefer "just-in-time" over "just-in-case" vocabulary (checkable, with caveat)
**Rule:** Introduce a term **when the learner first needs it to make progress**, not in a front-loaded glossary dump.

- **Just-in-time** respects cognitive load: a term is taught at the moment the learner has a "need to know" (https://en.wikipedia.org/wiki/Instructional_scaffolding — worked examples as "need to know").
- **Just-in-case** front-loading imposes extraneous load with no schema to attach to — terms are forgotten before they're used.
- *Caveat / nuance:* a **short reference glossary at the back** is fine and helpful for lookup; what fails is *teaching* the glossary up front as if it were content. (Heuristic synthesis, not a single sourced rule.)

### D5. Name functional groups (subgoal labeling) instead of line-by-line commenting (checkable)
**Rule:** Annotate code with **named functional chunks**, not per-line comments.

- Source: https://en.wikipedia.org/wiki/Subgoal_labeling (Margulieux, Catrambone, Guzdial).
- Example of compliance:
  ```python
  # ── 1. Ingest: load papers into a document store ──
  ...
  # ── 2. Retrieve: top-k similarity search ──
  ...
  # ── 3. Synthesize: prompt the LLM with retrieved context ──
  ```
- Example of violation: `# increment i`, `# call the API`, `# parse JSON`.

### D6. Explicitly flag prerequisite knowledge (checkable)
**Rule:** State upfront which concepts/skills the tutorial assumes (Python level, specific libraries, domain knowledge).

- Reason: expertise reversal (Section B4) — if you over-scaffold assumed knowledge you harm the experts; if you under-scaffold it you lose the genuinely-novice tail. **The only resolution is to declare the assumed baseline explicitly** so learners can self-select and self-remediate.
- Source: derived from expertise-reversal framework (https://en.wikipedia.org/wiki/Expertise_reversal_effect) + Knowles self-concept assumption.

### D7. Surface and correct likely misconceptions proactively (checkable)
**Rule:** Where the audience is likely to hold an inaccurate prior model, **name it and correct it explicitly** before teaching the accurate model.

- Reason: Knowles assumption 3 / principle 5 — "if prior knowledge is inaccurate, incomplete, or immature, it can interfere with or distort the integration of incoming information" (https://en.wikipedia.org/wiki/Andragogy#Principles).
- Example: "You may have heard RAG described as 'ChatGPT plus a search box.' That's misleading because…"

### D8. Reuse terms consistently; avoid synonym drift (checkable)
**Rule:** Once a term is introduced for a concept, use *that exact term* everywhere. Don't rotate synonyms ("agent" / "assistant" / "bot" / "model" for the same thing).

- Reason: every synonym forces the learner to disambiguate (extraneous load) and undermines the schema they're building. (Heuristic, from cognitive-load first principles.)

### D9. Renkl's "minimalist explanation" rule (checkable)
**Rule:** Inline explanations should be **principle-based and minimalist** — enough to connect the step to the underlying principle, not an exhaustive treatise.

- Source: https://en.wikipedia.org/wiki/Worked-example_effect#Developing_effective_worked_examples (Renkl criterion 2).
- The trap: over-explaining *also* adds extraneous load (the expertise-reversal trap for any audience member who already gets it).

### D10. Connect representations explicitly (checkable)
**Rule:** When the same idea appears in code, in prose, and in a diagram, **state the correspondence** ("the `retrieve()` call on line 12 is the arrow labeled 'fetch' in the diagram above").

- Source: Renkl criterion 3 (https://en.wikipedia.org/wiki/Worked-example_effect).
- This is the direct antidote to the split-attention effect (B2).

---

## E) Pacing, chunking, and motivation

### E1. Chunk content; cap new load per chunk
- Apply Miller's 7±2 (https://en.wikipedia.org/wiki/Cognitive_load): a pedagogical chunk should introduce ≤ ~3–5 new idea-units. Beyond that, split.
- Use **subgoal labels as chunk boundaries** (Section D5) — they double as a table of contents and a cognitive-rest point.

### E2. Segment multimedia/long material
- Segmentation (breaking animations/long-form into segments with processing breaks) reduces cognitive load and aids low-knowledge learners specifically (https://en.wikipedia.org/wiki/Expertise_reversal_effect — segmentation example).
- Notebook analog: **short cells with run-and-observe checkpoints**, not one 200-line mega-cell.

### E3. Build in desirable difficulty (Bjork) — but only at the right level
Source: https://en.wikipedia.org/wiki/Desirable_difficulty

- **Desirable difficulty** = effort that slows initial learning but improves long-term retention and transfer (retrieval practice, spacing, interleaving).
- **The difficulty must be *achievable*.** "Too difficult a task may dissuade the learner and prevent full processing." A difficulty is only desirable if the learner can complete it.
- Distinguish **learning vs. performance**: conditions that look worse in the short run (lower immediate performance) often produce better long-term learning. Don't optimize the tutorial for "feels easy right now."
- **Optimal Challenge Point** (Guadagnoli & Lee, via the framework): the difficulty level that maximizes learning *for this learner's current ability*.
- *Concrete techniques a reviewer can look for:* retrieval prompts ("without scrolling up, write down what `retrieve()` does"), interleaved exercise types, spaced review of earlier concepts in later exercises.

### E4. Motivate via immediate professional relevance (Knowles)
- Open each section with the *problem the learner has at work*, not the *feature the library has*. (Andragogy assumptions 1, 4, 5 — https://en.wikipedia.org/wiki/Andragogy.)
- State the payoff in the learner's vocabulary: "by the end of this cell you'll have a working literature-search agent you can point at your own papers."

### E5. The 6 evidence-based learning strategies (Learning Scientists)
Source: https://www.learningscientists.org (+ spaced-practice post at /blog/2016/7/21-1)

The six strategies the Learning Scientists promote (a practitioner-facing
distillation of cognitive-science research):

1. **Spaced practice** — distribute study over time rather than cramming.
2. **Retrieval practice** — recall from memory beats re-reading.
3. **Interleaving** — mix problem types rather than blocking by type.
4. **Elaboration** — ask "how/why" and connect to prior knowledge.
5. **Concrete examples** — pair abstract principles with specific instances.
6. **Dual coding** — combine words and visuals.

*Reviewer check:* the notebook should **embed** these where feasible — e.g.
elaboration prompts, concrete worked examples + abstract statement pairs, words
+ diagrams (dual coding). A single-shot tutorial can't space over weeks, but it
*can* interleave and retrieve.

---

## F) Common failure modes to check AGAINST

### F1. The curse of knowledge / curse of expertise
Source: https://en.wikipedia.org/wiki/Curse_of_knowledge

- Definition: a cognitive bias where someone with specialized knowledge **assumes others share it** and **cannot accurately reconstruct the less-knowledgeable state of mind** (Camerer, Loewenstein, Weber 1989; Fischhoff 1975 hindsight-basis).
- Classic demonstration: Newton's tappers-and-listeners study — tappers vastly overestimated how often listeners would recognize tapped songs (the tune was "playing in their head").
- **Education implication (Wieman 2007):** "it could be potentially ineffective, if not harmful, to think about how students are viewing and learning material by asking the perspective of the teacher as opposed to what has been verified by students." Authorial intuition is *not* a valid proxy for novice difficulty.
- **The bias resists correction:** telling people about it, or asking them to take the other's perspective, does *not* reduce it; nor do financial incentives. So **structural mitigations** are required (usability-test content on a target learner; apply the checkable rules in Section D).
- **Mitigation — "Decoding the Disciplines":** make the expert's tacit knowledge explicit step-by-step so students can master the mental actions required.

*Reviewer check:* flag any passage whose only justification is "the author
understands it" — i.e. undefined terms, skipped inferential steps, assumed
conventions. These are the curse-of-knowledge fingerprint.

### F2. Jargon walls
- A paragraph or cell dense with undefined terms (violates D1, D2). Detectable: count undefined domain terms per chunk.
- Especially harmful combined with the curse of knowledge: the author literally doesn't see the wall.

### F3. Unexplained inferential leaps
- The author skips 2–3 reasoning steps that are obvious to them but opaque to the learner. (Curse of knowledge + missing scaffolding.)
- *Reviewer check:* each new code construct or concept should be reachable from the *previous* cell's content by ≤ one inferential step.

### F4. Missing prerequisites
- The tutorial silently assumes a library/concept the learner may not have. Violates D6 and triggers either expertise reversal (if over-explained) or drop-off (if under-explained).
- *Reviewer check:* an explicit "you should already be comfortable with…" block at the top.

### F5. Over-scaffolding the familiar (expertise reversal in reverse)
- Explaining Python basics or `pip install` to a SciPy audience is not just patronizing — it is **measurably harmful** to their learning of the new material (https://en.wikipedia.org/wiki/Expertise_reversal_effect).
- *Reviewer check:* flag redundant explanation of assumed-baseline content.

### F6. Under-scaffolding the novel
- Conversely, treating the *new* topic (agents, retrieval, tool-use) as if a short paragraph is enough. Low-knowledge learners "resort to inefficient problem-solving strategies that overwhelm working memory" (https://en.wikipedia.org/wiki/Expertise_reversal_effect).
- *Reviewer check:* novel concepts need worked examples, subgoal labels, and an example–problem pair.

### F7. Split attention
- Code and its explanation separated; diagram and its legend far apart. Violates B2.
- *Reviewer check:* explanation adjacent to the thing explained.

### F8. Surface-feature fixation
- Worked examples that key on incidental details (variable names, specific dataset) rather than the structural features that generalize (https://en.wikipedia.org/wiki/Worked-example_effect — Renkl criterion 4).
- *Reviewer check:* does the example highlight *why this approach fits this problem class*, not just *what code to type*?

### F9. "Just-in-case" front-loaded glossaries taught as content
- Teaching 40 terms up front before the learner has any schema to hang them on. Violates D4.

### F10. Single-example transfer failure
- One worked example rarely induces a transferable schema (Reed & Bolstad — https://en.wikipedia.org/wiki/Worked-example_effect). At least two examples, the second more complex, are needed for transfer.

### F11. Performance-theater instead of learning
- Tutorial optimized to *look* smooth and impressive (runs first time, no errors shown) rather than to produce retention. Desirable-difficulty research (https://en.wikipedia.org/wiki/Desirable_difficulty) shows smoother-feeling instruction often produces *worse* long-term learning.

---

## Consolidated reviewer checklist (quick reference for the agent)

Below is a distilled, checkable list the AI reviewer can implement directly. Each
item is tagged with its evidence anchor above.

**Structure & release**
- [ ] Each major section opens with a "why this matters to your work" hook. **(A1)**
- [ ] Content is organized around a real problem the learner has, not a feature tour. **(A1, A2)**
- [ ] Sequencing follows an "I do → we do → you do" shape with worked + faded + open exercises. **(C1, C5)**
- [ ] The tutorial moves toward learner autonomy by the final exercise. **(A3)**

**Cognitive load**
- [ ] No more than ~3–5 new idea-units per chunk; chunks split when exceeded. **(B3, E1) — heuristic**
- [ ] Explanations are physically adjacent to the code/diagram they describe. **(B2, F7)**
- [ ] Code is annotated with **named functional subgoals**, not per-line comments. **(C3, D5)**
- [ ] Worked examples are paired with an isomorphic problem to solve. **(C1)**
- [ ] At least two examples per concept (second one harder). **(C1, F10)**
- [ ] Self-explanation prompts accompany worked examples. **(C1)**

**Vocabulary & jargon (Section D — highest weight)**
- [ ] Every domain term is defined on or before first use. **(D1)**
- [ ] ≤ ~3 new technical terms per chunk. **(D2) — heuristic**
- [ ] Novel concepts carry an analogy to the audience's existing domain. **(D3)**
- [ ] Terms are taught just-in-time, not front-loaded as a glossary lecture. **(D4)**
- [ ] Prerequisites are stated explicitly up front. **(D6, F4)**
- [ ] Likely misconceptions are named and corrected before the accurate model. **(D7)**
- [ ] Terminology is consistent — no synonym drift. **(D8)**
- [ ] Inline explanations are minimalist and principle-based. **(D9)**
- [ ] Correspondences between code/prose/diagram are stated explicitly. **(D10)**

**Calibration to expertise**
- [ ] Assumed-baseline content (Python, pip) is NOT over-explained. **(B4, F5)**
- [ ] Novel content (agents, retrieval, tools) IS heavily scaffolded. **(B4, F6)**
- [ ] Hard points have pre-embedded "hard scaffolding" (hints, partial code). **(C7)**

**Pacing & motivation**
- [ ] Short cells with run-and-observe checkpoints, not mega-cells. **(E2)**
- [ ] Exercises include desirable difficulty (retrieval, interleaving) but are achievable. **(E3)**
- [ ] Embeds elaboration prompts, concrete + abstract pairs, words + diagrams. **(E5)**

**Failure-mode sweep**
- [ ] No jargon walls (undefined-term density check per chunk). **(F2)**
- [ ] No inferential leaps > 1 step between adjacent cells. **(F3)**
- [ ] Examples highlight structural (not surface) features. **(F8)**
- [ ] Content has been (or should be) validated on a real target learner — authorial intuition alone is insufficient. **(F1)**

---

## What was NOT verified this session (gaps)

- **No primary peer-reviewed medical-education/CME source** was retrieved (the PMC ID provided was a cancer paper). Knowles' principles rest on Wikipedia secondary sourcing.
- **Mark Guzdial's blog** was not directly fetched; his programming-education contribution is captured via the secondary Wikipedia Subgoal labeling article.
- **Live-coding-specific empirical research** (e.g. studies on live-coded vs. pre-written examples) was not retrieved; the worked-example and cognitive-apprenticeship literatures are the closest well-sourced proxies.
- **Specific numeric thresholds** (e.g. "exactly 3 terms per section") are **heuristics** synthesized from cognitive-load first principles, not empirically derived constants. They should be presented to the agent as tunable defaults, not laws.
- The **"just-in-time vs. just-in-case" debate** is referenced widely in practitioner literature but the specific framing was not located in a single authoritative webfetch-accessible source this session; it is treated here as a heuristic synthesis from scaffolding + cognitive-load principles (D4).
