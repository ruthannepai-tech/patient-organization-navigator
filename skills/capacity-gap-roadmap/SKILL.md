---
name: capacity-gap-roadmap
description: Build a patient-journey gap analysis and a capacity-building options roadmap for a patient-led organization. Inventories gaps across the full patient journey (disease understanding, diagnosis, research infrastructure, therapeutic development, regulatory/patient-voice, access, lived experience), tagged by community and severity; assembles a peer-organization model bank (how comparable nonprofits created leverage and the scaled-down first move); and crosses gaps against the org's levers to produce options tiered by cost/effort and sequenced by horizon, grounded in what the org already has. Renders two hero figures: a gap map (severity by journey stage, colored by how directly the org can act) and a phased roadmap (options by horizon, framed amplify/revive/connect/build). Use inside a capacity-building engagement, or when a leader asks where the gaps are and where their organization can move the needle. Output is options to review, tiered and sequenced, never a prescription. Ground facts in retrieved sources.
---

# Capacity Gap & Roadmap

Two connected deliverables that answer, for a patient organization: **where are
the gaps across the patient journey, and — given what we already have, our
levers, our budget, and our capacity — what options do we have and in what
order?** The answer is always framed as options tiered by cost and sequenced
low-cost-first, built on the organization's existing assets. Never a
prescription.

## The seven patient-journey stages

Every gap is placed in exactly one:

1. **Disease understanding** — basic biology, mechanism, genotype→phenotype.
2. **Diagnosis** — odyssey, misdiagnosis, case-finding, testing access.
3. **Research infrastructure** — registry, natural history, biobank, models.
4. **Therapeutic development** — targets, endpoints, trial-readiness, pipeline.
5. **Regulatory / patient voice** — PFDD, orphan, surrogate endpoints, COA/PRO.
6. **Access** — approval, reimbursement, expanded/off-label, global equity.
7. **Lived experience** — psychosocial, QoL, caregiver burden.

## The five lever types

Recommendations map to how a patient organization actually creates leverage:
**advocacy**; **fundraising/funding** (incl. venture philanthropy, seed grants);
**research infrastructure**; **partnership**; **organizational capacity-building**.

## The four postures (build on what exists)

Classify each option by its posture toward the org's current work — this is the
core discipline that keeps the roadmap grounded and non-prescriptive:

- **Amplify** — scale something the org already does well.
- **Revive** — restart a dormant asset (e.g. a lapsed registry).
- **Connect** — plug the org into an existing external effort rather than
  duplicating it.
- **Build-via-partner** — create a new asset through an academic/industry
  partner; the org recruits/consents/coordinates, the partner runs the lab.

Prefer amplify/revive/connect before build. A tiny organization's durable
leverage is usually to own the patient-facing shared assets and connect them to
the science that already exists — not to run wet-lab work in-house.

## Workflow

1. **Inventory the gaps (grounded).** For each of the seven stages, enumerate
   the real gaps for this disease area, grounded in retrieved sources and any
   prior landscape/dossier work. Tag each: `communities_hit_hardest`,
   `severity_1to5`, `grounding` (the source). Save `gap_inventory.csv` with
   columns `pathway_stage, gap_id, gap, communities_hit_hardest, severity_1to5,
   grounding`.
2. **Assemble the peer-model bank.** Pick comparable organizations chosen for
   *transferability* to this org's size — lead with the closest disease/size
   analog. For each: why relevant, the leverage mechanism, what it took, and the
   scaled-down first move this org could realistically start. Save
   `peer_models.csv` (`organization, most_relevant_because, leverage_mechanism,
   what_it_took, scaled_down_start_move, lever_type`).
3. **Inventory current assets.** What the org already has, per domain, with
   status — the foundation every option builds on. Save `current_assets.csv`.
4. **Cross gaps × levers → options by horizon.** For high-priority gaps, name
   the concrete play, the posture, what it builds on, the lever, cost/effort
   (Low/Med/High), horizon (H1 0–12mo / H2 1–3yr / H3 3–5yr+), and the peer
   model it echoes. Save `recommendations_matrix.csv`.
5. **Render the two hero figures** (kernel helpers below), then **verify**
   (open the PNGs, check no label overlaps, legends beside their marks).
6. **Write it up** — a report that opens with the assumption block (from the
   capacity engine) and the framing line: prepared for the leader's review,
   options tiered by cost, sequenced low-cost-first, a first draft to cut and
   reorder — not a prescription.

## Kernel helpers (auto-loaded)

- `render_gap_map(stages, out_path="fig_gap_map.png", title=..., subtitle=...)` —
  `stages` is a list of dicts: `{stage, mean_severity, n_gaps, leverage
  ('High'|'Med'|'Low'), org_active (bool)}`. Bar height = mean severity, color =
  how directly the org can act, "already active" flag = existing footprint.
- `gap_map_from_inventory(gap_csv, leverage_map, active_map, ...)` — convenience:
  computes per-stage mean severity and counts straight from a gap_inventory.csv,
  given `leverage_map` and `active_map` keyed by stage name.
- `render_roadmap(horizons, cards, backbone=None, out_path="fig_roadmap.png",
  title=...)` — `horizons` is a list of `(title, subtitle)`; `cards` is a dict
  keyed by horizon index → list of `(id, label, cost, posture)`; `backbone` is
  an optional dict of horizon index → caption for the capacity-backbone band.
- `COST_COLORS`, `POSTURE_COLORS`, `LEVERAGE_COLORS` — the palettes, so report
  text and captions match the figures.

## Honesty & framing rules

- Every gap and every disease fact traces to a retrieved source (the `grounding`
  column); do not invent severity or dates.
- Right-size every option to the stated budget and staffing. A play a
  three-person volunteer org cannot resource is not an "option" — reframe it as
  a later-horizon build-via-partner with named prerequisites.
- Sparse data is a finding, not a gap in your work. If the field is early, say
  so plainly and let that shape the roadmap toward foundational moves.
- The roadmap is options to review. Sequence and tier them; never present them
  as the required path.
