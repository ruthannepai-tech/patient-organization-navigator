---
name: disease-landscape-timeline
description: Build a source-grounded visual timeline of research, infrastructure, and clinical development in a disease area — the arc from foundational science through gene/mechanism discovery, first therapies and regulatory milestones, natural-history studies and research infrastructure, the current clinical pipeline, and patient-voice/PFDD events. Each milestone is categorized, dated, and tagged with a confidence/source note so the reader sees at a glance where the field has been and where it is now. Use when a patient advocate, organization leader, or program strategist wants a map of "what has happened and what is happening" in their disease area, or as the flagship figure inside a capacity-building or landscape engagement. Produces a milestones CSV and a publication-grade timeline PNG. Ground every milestone in a retrieved source (clinical-trials, pubmed, drug-regulatory); never invent a date.
---

# Disease Landscape Timeline

A single figure that answers "where has this field been, and where is it now?"
for a disease area — the visual backbone of a landscape or capacity engagement.
It plots dated milestones across five tracks so a patient leader, funder, or
partner sees the whole arc at a glance.

## The five tracks

Categorize every milestone into exactly one:

- **Science** — foundational biology, gene/mechanism discovery, key
  proof-of-concept findings.
- **Regulatory** — drug approvals, orphan designations, guidance, PFDD program
  milestones with a regulatory footprint.
- **Natural history** — natural-history studies, registries, biobanks, and
  other research-infrastructure launches.
- **Pipeline** — clinical trials and programs currently in development.
- **Patient voice** — PFDD / EL-PFDD meetings, Voice-of-the-Patient reports,
  patient-generated evidence efforts.

## Workflow

1. **Gather milestones, grounded.** Use the research connectors to retrieve
   real events — `clinical-trials` for trials/NH studies (capture the NCT id and
   start date), `pubmed`/`literature` for discovery papers (capture PMID/year),
   `drug-regulatory` for approvals (capture the label/BLA). Do NOT rely on
   memory for dates; every row needs a source string. For undated or
   approximate events, still record them but set `confirmed` to a hedge
   ("approximate", "planned") — never a bare guess presented as fact.
2. **Assemble the table.** One row per milestone with columns:
   `year, label, detail, category, confirmed`. `category` must be one of the
   five track names (case-insensitive). `label` is the short on-figure text;
   `detail` is the tooltip/caption sentence; `confirmed` is the source/confidence
   note (e.g. "ClinicalTrials.gov confirmed (start 2018-02-27)",
   "FDA label confirmed", "planned", "established fact"). Save as a CSV.
3. **Render.** Call `render_timeline(csv_path, out_path, title=..., subtitle=...)`
   from the kernel. It loads `figure-style` conventions, alternates labels
   above/below the axis to avoid collisions, colors by category, rings the most
   significant events (first approval, upcoming patient-voice milestone), and
   writes a publication-grade PNG. Returns the output path.
4. **Verify then caption.** Open the PNG, check no labels overlap and every
   milestone is legible. Write a caption that states the arc in one line
   ("gene discovery -> first approved therapy -> today's pipeline & patient
   voice") and notes that dates are source-confirmed where tagged.

## Kernel helpers (auto-loaded)

- `render_timeline(csv_path, out_path="research_timeline.png", title=None,
  subtitle=None, figsize=(15, 7))` — render the timeline PNG from a milestones
  CSV. Returns `out_path`.
- `TRACK_COLORS` (dict) — the category→color map, so captions and companion
  figures can match.
- `blank_milestones_csv(path)` — write an empty template CSV with the right
  header to fill in.

## Honesty rules

- Every dated milestone traces to a retrieved source; tag it in `confirmed`.
- Planned/future events (e.g. an upcoming EL-PFDD meeting) are allowed but must
  be visibly tagged as planned, not asserted as having happened.
- If a disease area is data-poor and the timeline is sparse, that sparseness is
  itself the finding — present it plainly ("the field has few milestones; the
  research base is early") rather than padding with weak entries.
