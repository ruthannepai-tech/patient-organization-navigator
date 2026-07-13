# Patient Organization Navigator

A specialist agent profile and three companion skills for **Claude Science**,
built to help patient advocates and leaders of patient-led organizations —
most often rare-disease nonprofits — understand where their disease area
stands, what has been done, where the gaps are, and where their funding and
capacity sit.

The Navigator is **discovery-first and user-led**. It never prescribes. It runs
a discovery interview before proposing anything, lets the leader choose which
directions to pursue, keeps an explicit ledger of every assumption it makes
(surfaced in-session and stamped on every deliverable), and frames all outputs
as **resources to review — not a roadmap or a prescription**. It is designed to
encourage organizations across the full maturity spectrum, from those years
away from a tractable therapeutic strategy to those already leading a program.

## What's in this repository

```
agent/
  profile.json        # picker metadata + settings (name, description, access)
  system_prompt.md    # the agent's identity / opening system prompt
skills/
  patient-org-capacity-engine/   # the conductor: discovery, branch menu,
                                  #   assumption ledger, checkpoint protocol
  disease-landscape-timeline/     # source-grounded visual timeline of a
                                  #   disease area (science -> regulatory ->
                                  #   infrastructure -> pipeline -> patient voice)
  capacity-gap-roadmap/           # patient-journey gap map + peer-org model
                                  #   bank + gaps x levers x horizon options
export_manifest.json  # index of exported files
```

Each skill directory contains a `SKILL.md` (the guidance the agent loads) and a
`kernel.py` (helper functions auto-loaded into the analysis kernel — e.g. the
figure renderers and the assumption-ledger functions).

## The three skills

| Skill | What it does |
|-------|--------------|
| **patient-org-capacity-engine** | The conductor. Runs the Stage 0 discovery interview (vision, mission, disease-area maturity, budget, personnel, current assets, and what the leader wants), presents a six-branch focus menu the leader chooses from, maintains the assumption ledger, and composes the other skills. Threads one `org_capacity_profile.json` as the source of truth. |
| **disease-landscape-timeline** | Renders a single figure answering "where has this field been, and where is it now?" across five tracks — Science, Regulatory, Natural history/infrastructure, Pipeline, Patient voice — with every milestone grounded in a retrieved source. |
| **capacity-gap-roadmap** | Builds a patient-journey gap inventory (seven stages), a peer-organization model bank scaled to the org's size, and a phased roadmap of options tiered by cost and sequenced low-cost-first, classified by posture (amplify / revive / connect / build-via-partner). |

## How to install it in Claude Science

You do **not** need to be technical to install this. Pick whichever route fits.

### Easiest — paste one prompt to your Claude Science agent

Open a Claude Science conversation and paste this, verbatim:

> Please install the Patient Organization Navigator from this GitHub repo:
> https://github.com/ruthannepai-tech/patient-organization-navigator
> Clone or download it, then run `install.py` from the repo root in the repl
> tool with `exec(open("install.py").read())`. It will create and publish the
> three skills and create the `PATIENT_ORG_NAVIGATOR` agent profile with full
> access. Then create its environment and offer to switch me to it.

Your agent handles the rest. When it finishes, the **Patient Organization
Navigator** appears in your agent picker.

### One command — if you already have the repo

From the root of this repository, in the Claude Science **repl** tool:

```python
exec(open("install.py").read())
```

`install.py` reads the definitions in this repo and installs everything —
publishing all three skills and creating the agent profile with full catalog +
connector access (so it can reach PubMed, ClinicalTrials.gov, human-genetics,
and the rest of the scientific data catalog). It is **idempotent**: safe to
re-run, and it updates in place if you already have an older version installed.

It finishes by printing the one optional tool call to set up the figure-render
environment:

```python
manage_environments(mode='create', name='patient-org-navigator',
    packages=['pandas','numpy','matplotlib','seaborn'], python_version='3.13')
```

and the command to switch your conversation to the new specialist:

```python
host.agents.switch('PATIENT_ORG_NAVIGATOR')
```

### Manual — if you prefer to do it by hand

The `SKILL.md` and `kernel.py` files are plain text and self-documenting, and
`agent/profile.json` + `agent/system_prompt.md` fully define the agent. Ask your
Claude Science agent to create a skill per folder under `skills/` (writing each
`SKILL.md` and `kernel.py` verbatim, then publishing), and to create an
unrestricted profile named `PATIENT_ORG_NAVIGATOR` from the `agent/` files.

## Design commitments (baked into the engine)

1. **Discovery before deliverables** — never propose directions before
   understanding the organization.
2. **The leader chooses the direction** — a branch menu, not a decision made
   for them.
3. **Assumptions are logged, surfaced, and resolvable** — every blank filled is
   flagged, in-session and in every deliverable, with a standing invitation to
   correct it.
4. **Encourage, don't gatekeep** — meet the organization where it is; a large
   gap map is a community not yet served, not a failure.
5. **Resources to review, never a roadmap** — options tiered by cost, sequenced
   low-cost-first, built on what the organization already has.

## Provenance

Distilled from a real end-to-end engagement with a rare-disease nonprofit
(a lipodystrophy patient organization): a therapeutic-program run, an
externally-led patient-focused drug development (EL-PFDD) toolkit, and a full
capacity/budget scoping with a gaps-and-options analysis. The skills generalize
the reusable methodology from that project so it can serve any patient-led
organization.

## License

Released under the MIT License. See [LICENSE](LICENSE).
