# Comprehensive Manual of Prompt Engineering Frameworks

Software Lifecycle Implementation Guide.

## I. In-depth Analysis of Prompting Frameworks

### 1. I.c.I.o (Industrial Standard)

* **Components:** Instruction / Context / Input / Output
* **Source:** Official best practices from OpenAI/Anthropic.
* **Core Feature:** Structured operators. Minimalist and rigorous; eliminates fluff to ensure the most stable machine response.
* **Case Example:**
    (I) Optimize this SQL query;
    (c) Database is PostgreSQL with a user table of 10 million rows;
    (I) [Paste SQL code here];
    (o) Return the optimized code, execution plan explanation, and index suggestions in JSON format.

### 2. CRISPE (Creative All-rounder)

* **Components:** Capacity and Role / Insight / Statement / Personality / Experiment
* **Source:** Matt Mansion (AI Expert).
* **Core Feature:** Solution optimization. Focuses on multi-version comparison to stimulate deep model reasoning.
* **Case Example:**
    (CR) You are a senior marketing strategist;
    (I) Insight: Cloud platform ads are full of technical parameters but lack "business logic" that moves CEOs;
    (S) Write 3 slogans for a "Zero Downtime" cloud platform;
    (P) Tone: Minimalist, professional, with a touch of "sarcasm" toward mediocre products;
    (E) Provide a "Hardcore Tech" version and a "Business Value" version for comparison, briefly describing the psychological tactics behind each.

### 3. RISE (Process Benchmark)

* **Components:** Role / Input / Steps / Expectation
* **Source:** Rick Schneider (AI Community Contributor).
* **Core Feature:** Linear execution. Forces the model to output in logical order; provides a strong sense of workflow.
* **Case Example:**
    (R) Senior DevOps Engineer;
    (I) [A freshly formatted Linux server];
    (S) Steps: 1. Security hardening; 2. Docker installation; 3. Nginx configuration;
    (E) Produce a Markdown document that a beginner can execute directly.

### 4. BROKE (Management Loop)

* **Components:** Background / Role / Objectives / Key Result / Evolve
* **Source:** Fused from OKR philosophies of Intel/Google.
* **Core Feature:** Feedback loop. The only framework with an "Evolution" step for self-correction.
* **Case Example:**
    (B) Original login only supports passwords; now need to integrate QR code scanning;
    (R) Technical Lead;
    (O) Complete integration without delaying next week's launch;
    (K) Output API modification list and security analysis;
    (E) If completion by next week is impossible, provide a roadmap for "Beta launch first, then gradual migration."

### 5. ROSES (Deep Decision Making)

* **Components:** Role / Objective / Scenario / Solution / Steps
* **Source:** Derived from the McKinsey consulting model.
* **Core Feature:** Global decision-making. Focuses on weighing solutions in complex, multi-variable environments.
* **Case Example:**
    (R) Chief Architect;
    (O) Solve the pressure of 100,000 writes per second;
    (S) Limited budget and the team is unfamiliar with Golang;
    (S) Compare Redis vs. Message Queue solutions;
    (S) Provide implementation steps for the selected solution.

### 6. CARE (Teaching Assistant)

* **Components:** Context / Action / Result / Example
* **Source:** Evolved from the workplace STAR method.
* **Core Feature:** Illustrative logic. Enhances output readability through "Examples."
* **Case Example:**
    (C) New team members don't understand asynchronous locks;
    (A) Explain the difference between `lock` and `SemaphoreSlim`;
    (R) Goal: Help them understand how to prevent deadlocks;
    (E) Provide a simple thread-safe bank transfer code example.

### 7. COAST (Scenario Expert)

* **Components:** Context / Objective / Action / Scenario / Task
* **Source:** Product Hunt / UX Designer Community.
* **Core Feature:** Scenario-driven. Extremely focused on edge cases.
* **Case Example:**
    (C) User is in the payment flow;
    (O) Prevent duplicate charges;
    (A) Design logic;
    (S) Consider: Network disconnection, rapid double-clicking, and payment success with timeout;
    (T) Output corresponding copy and frontend logic.

### 8. RACE (General Template)

* **Components:** Role / Action / Context / Expectation
* **Source:** Coursera / DeepLearning.ai.
* **Core Feature:** Academic standard. Solid logical structure with the broadest versatility.
* **Case Example:**
    (R) Senior Programmer;
    (A) Summarize this week's progress;
    (C) Completed WPF converter refactoring, but encountered `CallerMemberName` errors;
    (E) Output a well-organized weekly report in Markdown.

### 9. TRACE (Communication Master)

* **Components:** Task / Request / Action / Context / Example
* **Source:** Prompt Engineering Guide (DAIR.AI).
* **Core Feature:** Communication details. Emphasizes the subtle difference between Request and Action.
* **Case Example:**
    (T) Apply for a server;
    (R) Polite but firm tone;
    (A) Draft an application email;
    (C) Existing cluster load has reached 90%;
    (E) Refer to a formal business application email template.

### 10. TAG (Atomic Instruction)

* **Components:** Task / Action / Goal
* **Source:** Derived from Agile Stand-up logic.
* **Core Feature:** Atomization. Minimalist structure suitable for automated AI Agents.
* **Case Example:**
    (T) Check this code for security;
    (A) Focus on auditing SQL injection vulnerabilities;
    (G) Ensure code meets security standards for production.

### 11. APE (Efficiency Driven)

* **Components:** Action / Purpose / Expectation
* **Source:** Kevin P. Nichols (Content Strategy Expert).
* **Core Feature:** Intent alignment. Emphasizes purpose to prevent model drift in long conversations.
* **Case Example:**
    (A) Write a Python crawler script;
    (P) Purpose is to monitor public e-commerce prices;
    (E) Expectation: Include error handling and follow standards.

### 12. ERA (Rapid Response)

* **Components:** Expectation / Role / Action
* **Source:** Early X (Twitter) Developer Community.
* **Core Feature:** Anchoring effect. Defines the result first, then works backward to execution.
* **Case Example:**
    (E) Undo last commit without deleting code changes;
    (R) Git Expert;
    (A) Provide a one-line command.

---

## II. Framework Selection for Software Development Scenarios

### 1. New Feature

* **Recommended Model:** CRISPE
* **Key Addition:** If the feature involves multi-module interaction, use (C) Role to output a "Module Decomposition List" first.
* **Reason:** Prevents the AI from losing context of Logic B while implementing Function A.

### 2. Change Requirement

* **Recommended Model:** BROKE
* **Key Addition:** Apply "Atomic" constraints to (B) Background. Suggested limit of 100 lines of logic per change.
* **Reason:** More complexity equals higher regression risk. Small evolutionary paths ensure system integrity.

### 3. Refactor Code

* **Recommended Model:** RISE
* **Key Addition:** Strictly follow (S) Small Steps. Each step must be a minimal unit that is compilable and testable.
* **Reason:** Prevents logic breaks caused by the AI rewriting too much at once.

### 4. Fix Bug

* **Recommended Model:** I.c.I.o
* **Key Addition:** Provide precise (I) Input. For multi-threading or complex async bugs, provide step-by-step debug logs first.
* **Reason:** Finer granularity leads to more accurate bug localization.
