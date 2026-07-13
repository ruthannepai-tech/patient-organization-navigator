"""Kernel helpers for patient-org-capacity-engine.

Threads one org_capacity_profile.json through a user-led, non-prescriptive
capacity-building engagement. See SKILL.md for the workflow.
"""
import json
import os
import datetime

SCHEMA_VERSION = "1.0"

BRANCHES = {
    "A_landscape": "Disease landscape & research-gap mapping",
    "B_readiness": "Research readiness & infrastructure (registry, biobank, natural history, models)",
    "C_pipeline": "Therapeutic strategy & pipeline (incl. CRISPR-led / genetic medicine)",
    "D_patientvoice": "Regulatory & patient voice (PFDD / EL-PFDD, Voice of the Patient)",
    "E_access": "Access & care navigation (diagnosis, expanded access, centers of care, payer/HTA)",
    "F_capacity": "Organizational capacity & funding (gap map, peer models, options by cost/horizon)",
}

MATURITY_TIERS = [
    "No tractable therapeutic strategy identified yet",
    "Building disease understanding & community",
    "Early research infrastructure (registry / natural history forming)",
    "Research-ready (assets exist; supporting external programs)",
    "Supporting or co-driving a therapeutic program",
    "Leading a therapeutic program in-house",
]

DISCOVERY_FIELDS = [
    "vision", "mission", "disease_area", "communities_served", "maturity",
    "budget_band", "staffing", "filing_type", "key_personnel",
    "current_assets", "risk_appetite", "constraints", "wants",
]


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def init_profile(org_name, disease_area, path="org_capacity_profile.json"):
    """Create the source-of-truth profile and write it to disk. Returns dict."""
    profile = {
        "schema_version": SCHEMA_VERSION,
        "created_at": now_iso(),
        "org_name": org_name,
        "disease_area": disease_area,
        "discovery": {},
        "branches_selected": [],
        "stages": {},
        "assumptions": [],
        "checkpoints": [],
    }
    save_profile(profile, path)
    return profile


def load_profile(path="org_capacity_profile.json"):
    with open(path) as fh:
        return json.load(fh)


def save_profile(profile, path="org_capacity_profile.json"):
    profile["updated_at"] = now_iso()
    with open(path, "w") as fh:
        json.dump(profile, fh, indent=2)
    return path


def record_discovery(profile, path="org_capacity_profile.json", **fields):
    """Store discovery-interview answers. Unknown keys are kept but flagged."""
    unknown = [k for k in fields if k not in DISCOVERY_FIELDS]
    profile.setdefault("discovery", {}).update(fields)
    if unknown:
        profile["discovery"]["_extra_fields"] = sorted(
            set(profile["discovery"].get("_extra_fields", []) + unknown))
    save_profile(profile, path)
    return profile["discovery"]


def select_branches(profile, branch_ids, path="org_capacity_profile.json"):
    """Record the leader's chosen focus branches (validated against BRANCHES)."""
    if isinstance(branch_ids, str):
        branch_ids = [branch_ids]
    bad = [b for b in branch_ids if b not in BRANCHES]
    if bad:
        raise ValueError("Unknown branch id(s): %s. Valid: %s"
                         % (bad, list(BRANCHES)))
    profile["branches_selected"] = list(branch_ids)
    save_profile(profile, path)
    return [(b, BRANCHES[b]) for b in branch_ids]


def log_assumption(profile, statement, basis, how_to_resolve, stage=None,
                   path="org_capacity_profile.json"):
    """Append an assumption to the ledger. Do this every time you fill a blank.

    statement       - the assumption in one plain sentence
    basis           - why it was assumed (what was missing)
    how_to_resolve  - the single thing the leader could share to retire it
    """
    entry = {
        "index": len(profile.setdefault("assumptions", [])),
        "statement": statement,
        "basis": basis,
        "how_to_resolve": how_to_resolve,
        "stage": stage,
        "status": "open",
        "logged_at": now_iso(),
    }
    profile["assumptions"].append(entry)
    save_profile(profile, path)
    return entry


def resolve_assumption(profile, index, resolution,
                       path="org_capacity_profile.json"):
    """Mark an assumption resolved with the leader's real input."""
    for a in profile.get("assumptions", []):
        if a["index"] == index:
            a["status"] = "resolved"
            a["resolution"] = resolution
            a["resolved_at"] = now_iso()
            save_profile(profile, path)
            return a
    raise KeyError("No assumption with index %s" % index)


def pending_assumptions(profile):
    """The still-open assumptions to surface with the leader now."""
    return [a for a in profile.get("assumptions", []) if a["status"] == "open"]


def set_checkpoint(profile, stage, question, options=None,
                   path="org_capacity_profile.json"):
    """Record that you paused here for the leader. Pair with an ask_user call."""
    entry = {
        "stage": stage,
        "question": question,
        "options": options or [],
        "at": now_iso(),
    }
    profile.setdefault("checkpoints", []).append(entry)
    save_profile(profile, path)
    return entry


def update_stage(profile, stage, status, outputs=None, notes=None,
                 path="org_capacity_profile.json"):
    """Track progress and deliverables for a stage."""
    profile.setdefault("stages", {})[stage] = {
        "status": status,
        "outputs": outputs or [],
        "notes": notes,
        "at": now_iso(),
    }
    save_profile(profile, path)
    return profile["stages"][stage]


def assumptions_markdown(profile, include_resolved=False):
    """Render the ledger as a Markdown block for the top of a deliverable."""
    items = profile.get("assumptions", [])
    if not include_resolved:
        items = [a for a in items if a["status"] == "open"]
    lines = ["> **Assumptions this document rests on.** These are our best "
             "reading of gaps in what we were told; please correct any of them "
             "— each carries the one thing you could share to replace it.", ""]
    if not items:
        lines.append("> _No open assumptions — the inputs below were confirmed "
                     "with the organization._")
        return "\n".join(lines)
    for a in items:
        tag = "" if a["status"] == "open" else " _(resolved)_"
        lines.append("> - **%s**%s  \n>   _Why assumed:_ %s  \n>   _To resolve, "
                     "share:_ %s" % (a["statement"], tag, a["basis"],
                                     a["how_to_resolve"]))
    return "\n".join(lines)


def build_manifest(profile, path="capacity_manifest.json"):
    """Collect stages, outputs, branches, and open assumptions into a manifest."""
    manifest = {
        "org_name": profile.get("org_name"),
        "disease_area": profile.get("disease_area"),
        "branches": [(b, BRANCHES.get(b, b))
                     for b in profile.get("branches_selected", [])],
        "stages": profile.get("stages", {}),
        "deliverables": sorted({o for s in profile.get("stages", {}).values()
                                for o in s.get("outputs", [])}),
        "open_assumptions": pending_assumptions(profile),
        "n_checkpoints": len(profile.get("checkpoints", [])),
        "built_at": now_iso(),
    }
    with open(path, "w") as fh:
        json.dump(manifest, fh, indent=2)
    return manifest
