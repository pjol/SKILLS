---
name: time-accounting
description: "Measure how long work actually took, from session-transcript timestamps clustered into sittings, and write the figure down honestly. Use whenever hours are being reported — branch scopes, work logs, status notes, estimates, invoices — or when an existing figure needs auditing. Replaces guessing time from diff size, which inflates."
---

# Time Accounting

## Purpose

Report hours that are **measured**, not inferred.

This skill exists because of a specific, expensive failure. On one branch, hours
were written up from diff volume and "the shape of the work" — a
plausible-sounding method that estimates how long the work would have taken a
person to type. The clock was never consulted. The branch was reported at
**11.5 hours against a measured 2.5**: an inflation of **4.7x**, discovered only
because the person paying attention said the number was obviously untrue.

## The rule

> **Hours are measured wall-clock time. They are never an estimate of how long
> the work would have taken to do by hand.**

A thousand-line component written in forty minutes took forty minutes. Reporting
it as a day because that is how long a person would have needed is a false
statement, not a generous one. The record says what happened, not what a
counterfactual human would have needed.

**If the clock was not consulted, do not report hours at all.** Report the
volume and say the time was not measured.

## When to use this skill

- Writing or updating anything that carries hours: branch scopes, work logs,
  status reports, retrospectives, estimates, invoices.
- Auditing a figure that looks wrong, or that was written before this skill.
- Any time the phrase "roughly" or "about" is reaching for an hours number.

## Method

### 1. Prefer the live stamps

A `UserPromptSubmit` hook can stamp every message with its local time, putting
elapsed time directly in the conversation. When it is installed, the first and
last stamp of a sitting is the whole measurement — no parsing needed.

Install it globally in `~/.claude/settings.json`:

```json
{ "hooks": { "UserPromptSubmit": [ { "hooks": [ {
  "type": "command",
  "command": "printf '{\"hookSpecificOutput\":{\"hookEventName\":\"UserPromptSubmit\",\"additionalContext\":\"Message sent at %s.\"}}' \"$(date '+%Y-%m-%d %H:%M:%S %Z')\"",
  "timeout": 5
} ] } ] } }
```

### 2. Otherwise, measure from the transcript

Session transcripts carry a timestamp on every message, so working time is
recoverable exactly after the fact:

```sh
python3 scripts/measure_sittings.py                 # newest transcript for $PWD
python3 scripts/measure_sittings.py --gap 30        # custom sitting gap, minutes
python3 scripts/measure_sittings.py --project /path/to/repo
```

It clusters timestamps into **sittings**, splitting on any gap longer than **30
minutes**, and sums each sitting's span.

Why 30 minutes: a shorter gap is somebody reading a diff, thinking, or fetching
coffee — that is working time. A longer one is somebody who left.

### 3. Corroborate against file mtimes

The files touched should fall inside the sittings. If they do not, the
measurement is describing the wrong session.

```sh
git status --porcelain | awk '{print $NF}' \
  | while read f; do [ -f "$f" ] && stat -f "%Sm %N" -t "%Y-%m-%d %H:%M" "$f"; done | sort
```

### 4. Split a sitting across features

The sitting total is the truth; the per-feature split is an apportionment of it.

Apportion by **when files were touched**, not by how large they are — mtimes
bracket each feature within the sitting, and the brackets must sum to the
measured total. Where two features interleave, say so and split the overlap
evenly rather than inventing a boundary. Say plainly that the split is
approximate; do not let it contradict the total.

## What each source is good for

| Source | Measures | Use it for |
|---|---|---|
| Live prompt stamps | When each message arrived | **The total, when the hook is installed** |
| Transcript timestamps | When work actually happened | **The total, otherwise** |
| File mtimes | When each file was last written | Splitting a sitting; corroborating the total |
| Commit timestamps | When work *landed* | Establishing which round work belongs to. Nothing else |
| Diff size | How much changed | The volume line only. **Never hours** |

**Commit timestamps are not working time.** Work committed days after it was
written clusters into the length of the commit session, which is neither the
doing nor an estimate of it. Use commits only to decide which round work belongs
to.

## Writing the figure down

State the method in one line wherever a figure appears, and name its weakness if
it has one.

Honest:

- *"1.6h, measured from transcript timestamps (Aug 28 12:18–13:53), corroborated
  by file mtimes."*
- *"0.9h measured; the split across five features is apportioned by file mtime
  and is approximate below 0.1h."*
- *"~2,100 lines across 22 files. Time not measured."*

Not honest:

- *"Derived from volume and the shape of the work."* A guess wearing the
  vocabulary of a measurement.
- Any hours figure produced without opening a clock.

Round to 0.1h. Where a measured total and an itemised split disagree, **the
measured total wins** and the split is adjusted to it.

## Correcting a figure already published

State the correction; do not silently restate the number. A reader who saw the
old figure needs to know it moved and why. Put the old value, the new value, the
ratio, and the reason in the document itself — the correction is part of the
record.

## Maintenance

- Keep the hook snippet here in step with the one actually installed.
- If a project keeps its own copy of this method (e.g. `docs/TIME_ESTIMATION.md`),
  that copy points here; do not let the two drift.
