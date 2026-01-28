# MirrorDNA Governance Charter

**Version:** 1.0
**Effective Date:** 2026-01-29
**Author:** Paul Desai, N1 Intelligence

---

## Purpose

This charter establishes binding governance principles for the MirrorDNA ecosystem. It exists to **prevent drift, capture, and erosion of core values** as the project grows.

**Key principle:** Loosening constraints must be harder than maintaining them.

---

## Core Invariants (Cannot Be Changed)

These principles are immutable. They cannot be modified by any contributor, maintainer, or future owner:

### 1. User Sovereignty

- Users own their data. Always.
- No silent data collection.
- No data sales, ever.
- Export must always be possible.
- Deletion must be provable.

### 2. Reflection Over Prediction

- MirrorDNA reflects, it does not predict.
- No behavioral scoring.
- No outcome predictions about users.
- No "optimization" of human behavior.
- No engagement maximization.

### 3. Local-First Architecture

- Core functionality must work offline.
- Cloud is optional enhancement, not requirement.
- No hard dependency on any single vendor.
- Users can self-host everything.

### 4. Transparency

- All governance rules must be public.
- No hidden policies.
- No secret algorithms.
- Audit trails must be accessible.

### 5. No Harm

- Crisis resources, not crisis exploitation.
- No dark patterns.
- No dependency creation.
- No manipulation.

---

## Governance Rules (Can Be Amended)

These rules guide operation but can be modified through the amendment process:

### Policy Changes

1. **Minor changes** (bug fixes, clarifications): Maintainer approval
2. **Moderate changes** (new features, policy additions): RFC + 7-day review
3. **Major changes** (architectural shifts): RFC + 30-day review + community vote

### Constraint Modifications

To loosen any safety constraint:

1. Written RFC explaining rationale
2. 30-day public comment period
3. Security review
4. Supermajority (75%) approval from maintainers
5. 90-day trial period with monitoring
6. Final confirmation vote

To tighten any safety constraint:

1. Written RFC
2. 7-day review
3. Simple majority approval

**Asymmetry is intentional.** Loosening must be harder than tightening.

---

## Prohibited Actions

The following actions are permanently prohibited:

1. **Selling user data** to any party for any reason
2. **Training on user content** without explicit opt-in consent
3. **Creating psychological profiles** for targeting or manipulation
4. **Implementing addiction mechanics** (streaks, variable rewards, etc.)
5. **Dark patterns** in consent flows
6. **Vendor lock-in** by design
7. **Weaponizing the protocol** for surveillance or control

Violation of prohibitions triggers immediate review and potential removal of contributor access.

---

## Crisis Protocol

If MirrorDNA detects crisis content (suicide, self-harm, etc.):

1. **MUST** provide appropriate crisis resources
2. **MUST NOT** attempt therapy or counseling
3. **MUST NOT** lecture, moralize, or guilt
4. **MUST NOT** create dependency ("I'm always here for you")
5. **MUST** offer to help with something else
6. **MUST** log crisis routing (anonymized) for safety auditing

---

## Enforcement

### Maintainer Responsibilities

- Uphold this charter in all decisions
- Block PRs that violate invariants
- Report violations publicly
- Recuse from decisions with conflicts of interest

### Community Rights

- Anyone can file a governance violation report
- All reports must receive public response within 7 days
- Repeated violations trigger maintainer review

### Succession

If the original author (Paul Desai) is unable to maintain the project:

1. Maintainership transfers to designated successors
2. This charter remains binding
3. Core invariants cannot be modified by successors
4. Community fork rights are preserved

---

## Amendment Process

To amend this charter (except Core Invariants):

1. Submit amendment RFC
2. 60-day public comment period
3. Security and ethics review
4. 80% supermajority approval
5. 6-month observation period
6. Final ratification vote

Core Invariants (Section 2) cannot be amended. They can only be added to.

---

## Signatures

This charter is effective as of the date above.

**Author:**
Paul Desai
Founder, N1 Intelligence
paul@n1intelligence.com

---

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-01-29 | 1.0 | Initial charter |

---

*"The purpose of governance is to make good outcomes likely and bad outcomes unlikely, even when no one is watching."*

⟡ MirrorDNA — Reflection over prediction
