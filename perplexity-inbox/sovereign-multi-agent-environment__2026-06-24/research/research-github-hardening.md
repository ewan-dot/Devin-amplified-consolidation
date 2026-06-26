# GitHub Repository & Organisation Hardening: Deep-Dive Reference

**Organisation:** Amplified-Partners (37 repos, prefixes: `fleet-` · `estate-` · `brain-` · `lab-` · `pipe-` · `product-` · `shared-`)  
**Context:** Multi-AI-agent environment (Claude Code, Cursor, Devin, Antigravity); agents open PRs autonomously.  
**Baseline already fixed:** Workflow CODEOWNER held by agent / auto-merge self-approval loop / `enforce_admins: false` / unsigned commits / no last-push-approval.  
**Date:** June 2026  

> **Frame:** "A repo is not GitHub — it is just something GitHub monitors. We can do anything with the repo. Make it more secure."

---

## Table of Contents

1. [Threat Model: Multi-Agent Environment](#1-threat-model-multi-agent-environment)
2. [Org-Level Rulesets (Modern Branch Protection Replacement)](#2-org-level-rulesets)
3. [Supply-Chain & Actions Hardening](#3-supply-chain--actions-hardening)
4. [Agent-Specific Threat Mitigations](#4-agent-specific-threat-mitigations)
5. [Commit Integrity: Signed Commits & Immutable Tags](#5-commit-integrity)
6. [Secrets Architecture: Eliminate Static Credentials](#6-secrets-architecture)
7. [What's New 2025–2026 (Feature Reference)](#7-whats-new-20252026)
8. [Prioritised Hardening Checklist](#8-prioritised-hardening-checklist)
9. [Copy-Ready YAML Patterns](#9-copy-ready-yaml-patterns)

---

## 1. Threat Model: Multi-Agent Environment

The Cloud Security Alliance published in May 2026 that AI coding agents — Claude Code, GitHub Copilot Coding Agent, Gemini CLI — are now embedded in GitHub Actions workflows and process untrusted repository content (PR titles, issue bodies, code comments, branch names) while holding **elevated privileges including write access and configured pipeline secrets** ([CSA, May 2026](https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/05/CSA_research_note_ai_github_actions_security_20260503-csa-styled.pdf)).

### Specific threats for Amplified-Partners

| Threat | Vector | Impact |
|--------|--------|--------|
| **Prompt injection / Comment-and-Control** | Malicious content in PR title, issue body, commit message instructs the agent to exfiltrate secrets | Secrets posted to public Actions logs or issue threads — zero maintainer interaction required |
| **Self-approval loop** | Agent opens PR, then agent's Actions token approves it, then auto-merge fires | Malicious code lands on `main` without any human review |
| **`.github/` write access** | Agent pushes changes to `.github/workflows/` or `CODEOWNERS`, re-wiring its own gates | Agent grants itself broader permissions or removes required checks |
| **Privilege escalation via Actions** | Workflow triggered by agent has `contents: write` and no `permissions:` ceiling | Agent's GITHUB_TOKEN becomes a write key to the entire repo |
| **Secret exfiltration** | `pull_request_target` + agent checks out fork code in privileged context | Long-lived API keys / ANTHROPIC_API_KEY exit via network or logs |
| **OIDC trust misconfiguration** | AWS/GCP IAM policy with no `sub` constraint lets *any* GitHub repo assume the role | Cloud account compromise from a forked or untrusted repo |
| **Supply-chain action compromise** | Floating version tag (e.g. `uses: actions/checkout@v4`) retroactively moved to malicious commit | All jobs run attacker code (see tj-actions/changed-files incident, March 2025) |
| **Tag mutability** | Agent force-pushes a tag used in a release pipeline | Downstream consumers receive malicious artifact |
| **PromptPwnd / clinejection** | Concealed instructions in a GitHub issue compel agent to execute arbitrary commands | Secrets exfiltrated into issue thread ([Aikido Security, 2025](https://www.aikido.dev/)) |

---

## 2. Org-Level Rulesets

### Rulesets vs. Legacy Branch Protection Rules

| Dimension | Legacy Branch Protection | Rulesets (Modern) |
|-----------|--------------------------|-------------------|
| Scope | Per-repo only | Per-repo **or org-wide** targeting multiple repos by pattern |
| Visibility | Admin-only | **Anyone with read access** can view active rulesets |
| Multiple rules | One rule per branch | Multiple rulesets layer; most-restrictive wins |
| Status management | Delete to disable | `Active` / `Disabled` statuses — disable without deleting |
| Targeting | Exact branch name | `fnmatch` glob patterns (e.g., `releases/**`) |
| Required workflows | Not supported | **Supported** — org-wide required CI workflows |
| Push rules | Not supported | Block by file path, extension, size, path length |
| Enforce admins | Separate toggle, often forgotten | Controlled via bypass list — grant bypass to specific app/team/role only |

Sources: [GitHub Docs — About Rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets); [GitHub Changelog — Org Rulesets for Team Plans, June 2025](https://github.blog/changelog/2025-06-16-organization-rulesets-now-available-for-github-team-plans/)

### How Rulesets Layer

> Multiple rulesets targeting the same branch are **aggregated**. Where the same rule appears in different forms, the **most restrictive version wins**. A repo-level ruleset requiring 2 reviews + an org-level ruleset requiring 3 reviews = 3 reviews required. ([GitHub Docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets))

### Org Ruleset: Branch Target Strategy for Amplified-Partners

The 37 repos with 6 prefixes allow a tiered approach:

```
Ruleset: "AP-Universal"  →  target: all repos (pattern: *)
Ruleset: "AP-Production" →  target: fleet-*, estate-*, product-*  (higher scrutiny)
Ruleset: "AP-Lab"        →  target: lab-*  (relaxed, no deploy gates)
```

Each org-level ruleset can be managed via UI, REST API, or GraphQL API and can be imported/exported as JSON (see `github/ruleset-recipes`).

### Break-Glass Bypass Pattern

**Never use "Repository Administrator" as a blanket bypass.** Instead:

1. Create a dedicated GitHub App called `amplified-break-glass` with the narrowest possible permissions.
2. Add it to the bypass list as **"For pull requests only"** — this forces even break-glass actors to open a PR, creating an audit trail.
3. Protect the break-glass app's private key in Azure Key Vault or AWS Secrets Manager (never as a repo secret).
4. Require a separate human to install/approve any new installation of the break-glass app.
5. Alert on every use: configure audit log streaming → SIEM and create an alert on `ruleset_bypass` events.

```
Bypass list entry:
  Actor: amplified-break-glass [GitHub App]
  Mode:  For pull requests only  (not "Always allow")
```

### Org Ruleset Settings: What to Enable

| Rule | Setting | Reason |
|------|---------|--------|
| Require a pull request before merging | ✅ Required reviewers: **2** (dismiss stale on new push) | Prevents direct push to default/release branches |
| Require last-push approval | ✅ Enabled | Forces fresh human approval after any push — critical for AI agents |
| Dismiss stale reviews on new push | ✅ Enabled | Agent pushing a commit to its own PR invalidates prior approvals |
| Require status checks to pass | ✅ Specific app as source | Prevents a rogue actor from faking status checks |
| Require signed commits | ✅ Enabled (see §5) | Cryptographic chain of custody for every commit |
| Block force pushes | ✅ Enabled | Prevents agents rewriting history |
| Restrict deletions | ✅ Enabled | Agents cannot delete protected branches |
| Require linear history | ✅ Enabled | Immutable, auditable history |
| Required workflows | ✅ security-audit.yml from `shared-security` repo | Org-wide gating CI that agents cannot bypass |
| Restrict file paths `.github/**` | ✅ Push ruleset | Block any push touching `.github/` without bypass |
| Restrict file paths `CODEOWNERS` | ✅ Push ruleset | Agents cannot modify their own gates |

### Push Ruleset: Protect `.github/` Universally

```json
{
  "name": "AP-Protect-DotGithub",
  "target": "push",
  "enforcement": "active",
  "rules": [
    {
      "type": "file_path_restriction",
      "parameters": {
        "restricted_file_paths": [
          ".github/**/*",
          "CODEOWNERS",
          ".github/CODEOWNERS"
        ]
      }
    }
  ],
  "bypass_actors": [
    {
      "actor_type": "App",
      "actor_id": "<break-glass-app-id>",
      "bypass_mode": "pull_request"
    }
  ]
}
```

The org-level push ruleset applies to the **entire fork network**, ensuring every entry point is protected. ([GitHub Docs — Available Rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets))

---

## 3. Supply-Chain & Actions Hardening

### 3.1 Pin All Actions to Full Commit SHA

> "Pinning to a full length commit SHA is currently the only way to use an action as an immutable release." — [GitHub Docs — Security Hardening for GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)

The tj-actions/changed-files compromise (March 2025) retroactively moved **all** version tags to point to a payload that printed secrets to public logs. A pinned SHA is immune to this attack class. ([CSA, May 2026](https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/05/CSA_research_note_ai_github_actions_security_20260503-csa-styled.pdf))

```yaml
# BAD — floating tag, vulnerable to tag-hijacking
- uses: actions/checkout@v4

# GOOD — pinned to immutable SHA
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
```

**Automation:** Use [StepSecurity's Secure Workflow tool](https://app.stepsecurity.io/secureworkflow) or OpenSSF Scorecard to convert all unpinned references across the org's 37 repos in bulk. [OpenSSF Scorecard](https://github.com/ossf/scorecard) also flags risky supply-chain practices and integrates with code scanning.

**Cooldown for Dependabot/Renovate:** Add a delay before adopting new action versions — Dependabot has a `cooldown` flag; Renovate has `minimumReleaseAge`. This prevents same-day compromise propagation. ([OWASP GitHub Actions Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/GitHub_Actions_Security_Cheat_Sheet.html))

### 3.2 `permissions:` — Least-Privilege in Every Workflow

> "Set the default permission for the GITHUB_TOKEN to read access only for repository contents." — [GitHub Docs — Security Hardening for GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)

```yaml
# REQUIRED: Org-level default setting
# Settings → Actions → General → Workflow permissions → Read repository contents and packages

# REQUIRED: Every workflow file must declare permissions at workflow level
permissions: {}   # deny-all at workflow level

jobs:
  build:
    permissions:
      contents: read       # minimal read
      id-token: write      # only if OIDC needed

  deploy:
    permissions:
      id-token: write
      contents: read
      # NOT: pull-requests: write (unless explicitly needed)
```

**Org-level enforcement:** Disable "Allow GitHub Actions to create and approve pull requests" at org level: Settings → Actions → General → Workflow permissions → **uncheck** "Allow GitHub Actions to create and approve pull requests". This is the single most important setting to prevent the self-approval loop.

### 3.3 Prevent Poisoned Pipeline Execution (PPE)

The three PPE sub-variants (Direct, Indirect, Public) are codified as MITRE ATT&CK T1677. ([CSA, May 2026](https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/05/CSA_research_note_ai_github_actions_security_20260503-csa-styled.pdf))

**The danger trigger: `pull_request_target`**

```yaml
# DANGEROUS — checks out fork code in privileged context with access to secrets
on: pull_request_target
jobs:
  review:
    steps:
      - uses: actions/checkout@... # This checks out the PR's code with secrets available
        with:
          ref: ${{ github.event.pull_request.head.sha }}  # ← attacker-controlled

# SAFE pattern — if you must use pull_request_target:
# Secret-using jobs must only run AFTER explicit CODEOWNER approval on the base branch
on: pull_request_target
jobs:
  # Job 1: runs immediately, NO secrets, checks out BASE only
  lint:
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@<SHA>  # Checkout BASE branch, not fork

  # Job 2: gated by environment requiring human approval
  deploy-preview:
    needs: lint
    environment: staging-preview  # ← Human must approve before this job runs
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@<SHA>
        with:
          ref: ${{ github.event.pull_request.base.sha }}  # ← Base branch only
```

**Safer alternative for most use-cases:**

```yaml
# Use pull_request (not pull_request_target) for fork PRs
# This has read-only permissions and NO access to secrets
on: pull_request
```

### 3.4 GITHUB_TOKEN: Prevent PR Creation and Approval by Actions

This combination is the exact mechanism behind the auto-merge self-approval loop:

**Org-level:** Settings → Actions → General → Workflow permissions:
- Set to "Read repository contents and packages permissions" (read-only default)
- Uncheck "Allow GitHub Actions to create and approve pull requests"

Note (2025): GitHub [merged these two settings](https://github.com/orgs/community/discussions/177800) into a single toggle — "Allow GitHub Actions to create and approve pull requests" — which controls both capabilities.

### 3.5 Artifact Attestations & SLSA Build Provenance

GitHub uses Sigstore to generate artifact attestations, providing **SLSA v1.0 Build Level 2** out-of-the-box. Using a reusable workflow for builds achieves **SLSA v1.0 Build Level 3**. ([GitHub Docs — Artifact Attestations](https://docs.github.com/en/actions/security-for-github-actions/using-artifact-attestations/using-artifact-attestations-to-establish-provenance-for-builds))

```yaml
# In the build job of every release workflow:
permissions:
  id-token: write      # Required for Sigstore/OIDC
  contents: read
  attestations: write  # Required to write attestation

steps:
  - name: Build artifact
    run: make build -o dist/app

  - name: Generate artifact attestation
    uses: actions/attest-build-provenance@v2
    with:
      subject-path: 'dist/app'

  # For container images:
  - name: Generate container attestation
    uses: actions/attest-build-provenance@v2
    with:
      subject-name: ghcr.io/amplified-partners/myapp
      subject-digest: ${{ steps.build.outputs.digest }}
      push-to-registry: true
```

**Verify attestation in a downstream workflow or deployment gate:**

```bash
gh attestation verify dist/app -R amplified-partners/fleet-api
gh attestation verify oci://ghcr.io/amplified-partners/fleet-api:latest \
  -R amplified-partners/fleet-api
```

### 3.6 Dependency Review as Required Workflow

```yaml
# .github/workflows/dependency-review.yml (in shared-security repo)
name: Dependency Review
on: [pull_request]
permissions:
  contents: read
  pull-requests: write
jobs:
  dependency-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<SHA>
      - uses: actions/dependency-review-action@<SHA>
        with:
          fail-on-severity: high
          deny-licenses: GPL-2.0, AGPL-3.0
```

Add this as a **required workflow** in the org-level ruleset so it applies across all repos. ([GitHub Docs — Dependency Review](https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/about-dependency-review))

### 3.7 CodeQL with Actions Language Support

```yaml
# .github/workflows/codeql.yml
name: CodeQL Analysis
on:
  pull_request:
  schedule:
    - cron: '0 2 * * 1'  # Weekly full scan
permissions:
  security-events: write
  contents: read
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<SHA>
      - uses: github/codeql-action/init@<SHA>
        with:
          languages: javascript, python, actions  # 'actions' scans workflow files
      - uses: github/codeql-action/autobuild@<SHA>
      - uses: github/codeql-action/analyze@<SHA>
```

Enable `language: actions` to detect vulnerabilities in GitHub Actions workflow files themselves. Use **Zizmor** as defence-in-depth for Actions-specific patterns (impostor commit detection, PPE patterns). ([OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/GitHub_Actions_Security_Cheat_Sheet.html))

### 3.8 `actions/checkout` — Disable Persistent Credentials

```yaml
- uses: actions/checkout@<SHA>
  with:
    persist-credentials: false  # Prevents Git credentials persisting in the runner environment
```

### 3.9 StepSecurity Harden-Runner: Network Egress Control

Harden-Runner is a CI/CD security agent that monitors network egress, file integrity, and process activity at the runner level. It is the primary technical control against secret exfiltration via outbound network calls. ([StepSecurity Harden-Runner](https://github.com/step-security/harden-runner))

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      # First step in EVERY job
      - name: Harden Runner
        uses: step-security/harden-runner@c6295a65d1254861815972266d5933fd6e532bdf  # v2.11.1
        with:
          egress-policy: audit      # Phase 1: audit mode, observe baseline
          # egress-policy: block    # Phase 2: block + allowed-endpoints allowlist
          # allowed-endpoints: >    # Phase 2: add after observing audit results
          #   github.com:443
          #   api.github.com:443
          #   objects.githubusercontent.com:443
```

Run in `audit` mode first for one release cycle to build a baseline of legitimate egress, then switch to `block` mode with an allowlist. Any future outbound call not in the baseline triggers an alert — including a compromised action attempting to exfiltrate secrets to attacker infrastructure (the reviewdog/action-setup attack pattern). ([CSA, May 2026](https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/05/CSA_research_note_ai_github_actions_security_20260503-csa-styled.pdf))

---

## 4. Agent-Specific Threat Mitigations

### 4.1 Stop Agents from Self-Approving PRs

**GitHub native controls (use all three in combination):**

1. **Org setting:** Disable "Allow GitHub Actions to create and approve pull requests" — this is the hard stop.
2. **Ruleset:** Require 2 human reviewers, with "Dismiss stale reviews on new push" — any new commit from the agent invalidates prior approvals, including its own.
3. **Ruleset:** Enable "Last push approval required" — the reviewer must approve the final state of the code, not an earlier version the agent quietly amended.
4. **CODEOWNERS:** Assign human-owned teams (never agent GitHub Apps) to `.github/`, `CODEOWNERS`, and critical infra directories.

**Supplementary check (defence-in-depth):**

```yaml
# .github/workflows/anti-self-approval.yml
name: Block Self-Approval
on:
  pull_request_review:
    types: [submitted]
permissions:
  pull-requests: read
  contents: read
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - name: Verify reviewer is not a committer
        uses: suzuki-shunsuke/deny-self-approve@<SHA>
        # Fails if any approver is also a committer on this PR
        # See: https://github.com/suzuki-shunsuke/deny-self-approve
```

### 4.2 Stop Agents from Editing `.github/`

**Push ruleset (§2) blocks it at the Git protocol level.** Additionally:

- **CODEOWNERS:** `.github/ @amplified-partners/security-team` (human team only)
- **Branch protection:** CODEOWNERS review required, so even if somehow pushed, merging requires the security team
- **Required workflow:** A workflow in the `shared-security` repo (where agents have no write access) validates that no `.github/` files were modified in agent-created PRs without security team sign-off

```yaml
# In the org-level required workflow:
- name: Detect .github/ changes in agent PRs
  run: |
    AGENT_LOGINS="claude-code[bot] cursor[bot] devin[bot] antigravity[bot]"
    PR_AUTHOR="${{ github.event.pull_request.user.login }}"
    if echo "$AGENT_LOGINS" | grep -q "$PR_AUTHOR"; then
      CHANGED=$(git diff --name-only origin/${{ github.base_ref }}...HEAD | grep '^\.github/')
      if [ -n "$CHANGED" ]; then
        echo "ERROR: Agent PR modifies .github/ — requires security team review"
        echo "$CHANGED"
        exit 1
      fi
    fi
```

### 4.3 GitHub Apps vs PATs for Agent Identity

| Property | PAT (Classic) | Fine-Grained PAT | GitHub App |
|----------|---------------|------------------|------------|
| Scope | All repos the user can access | Specific repos, specific permissions | Specific repos, specific permissions |
| Identity | Human user account | Human user account | Distinct app identity (auditable) |
| Expiry | Optional (often never) | Required max 1 year | Installation token: 1 hour |
| Org approval | No | **Required** (GA March 2025) | **Required** per installation |
| Revocation | Manual | Manual | Per installation, instant |
| Audit trail | User's actions | User's actions | **App's distinct actor — trackable in audit log** |
| Bypass prevention | Hard — tied to user | Easier to restrict | **Best — fine-grained, installation-scoped** |

**Recommendation:** Every AI agent (Claude Code, Cursor, Devin, Antigravity) must authenticate as a **GitHub App**, not a PAT. GitHub Apps:

- Can be restricted to specific repositories at installation time
- Issue installation access tokens that expire after 1 hour
- Show up as a distinct actor in the audit log (not masquerading as a human)
- Can be granted **subset permissions** at token-generation time even below the app's registered permissions ([GitHub Docs — GitHub App Best Practices](https://docs.github.com/en/apps/creating-github-apps/about-creating-github-apps/best-practices-for-creating-a-github-app))

**Minimum permissions for an agent GitHub App (PR-opening only):**

```
Repository permissions:
  Contents:       Read  (to read code and push branches)
  Pull requests:  Write (to open PRs)
  Checks:         Read  (to read CI status)
  Metadata:       Read  (required)

NOT granted:
  Administration: None
  Environments:   None
  Secrets:        None
  Workflows:      None  ← prevents self-modifying workflow files
  Members:        None
```

**Fine-grained PAT org policy (GA March 2025):** Set org to "Require administrator approval" for all fine-grained PATs. This means no agent can create an unreviewed PAT with org access. ([GitHub Changelog — Fine-grained PATs GA, March 2025](https://github.blog/changelog/2025-03-18-fine-grained-pats-are-now-generally-available/))

### 4.4 Environment Protection Rules: Deploy Gates Agents Cannot Bypass

```yaml
# production environment configuration (via GitHub UI or API):
#   Required reviewers: [security-team, lead-engineers]  (human teams)
#   Prevent self-reviews: ENABLED  ← key for agents
#   Disallow administrators bypass: ENABLED
#   Deployment branches: Selected — only releases/* and main

jobs:
  deploy-production:
    environment: production     # This job is gated
    permissions:
      id-token: write
      contents: read
    steps:
      - name: Deploy
        # This step only runs after a human from security-team or lead-engineers approves
```

The "Prevent self-reviews" setting explicitly blocks a user who initiated the deployment from also approving it. ([GitHub Docs — Managing Environments](https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-deployments/managing-environments-for-deployment))

**"Disallow administrators bypass"** must be explicitly enabled — by default, admins can force deployments around protection rules.

### 4.5 Prevent Agents from Reading Secrets in Action Logs

1. **Least-privilege secrets scoping:** Use environment secrets, not repo or org secrets, for production credentials. Agents whose workflows don't reference the `production` environment never receive those secrets.
2. **Structured data prohibition:** Never store structured data (JSON, YAML, base64-encoded bundles) as a single secret value — GitHub's log redaction cannot reliably catch transformed representations. Use individual key-value secrets.
3. **Register transformed values:** If a secret is base64-encoded in a step, also register the base64 value as a separate secret so it gets masked. ([GitHub Docs — Security Hardening for GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions))
4. **Network egress block:** With Harden-Runner in block mode, even if an agent is tricked into attempting exfiltration, the outbound call to non-allowlisted endpoints fails.
5. **Copilot Coding Agent workflow approval:** By default, when any GitHub App or bot opens a PR, Actions workflows do not run until a human clicks "Approve and run workflows". Keep this default — do not use the March 2026 "skip approval" setting for agents in production repos. ([GitHub Changelog, March 2026](https://github.blog/changelog/2026-03-13-optionally-skip-approval-for-copilot-coding-agent-actions-workflows/))

### 4.6 Constrain Agent Tool Set (Architectural Principle)

> "GitHub's published security architecture for Agentic Workflows — in which the agent process never holds write tokens or API keys, with secrets confined to isolated downstream jobs that run only after agent output has been reviewed — offers a structural model that reduces the blast radius of successful prompt injection." — [CSA, May 2026](https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/05/CSA_research_note_ai_github_actions_security_20260503-csa-styled.pdf)

**Pattern for Amplified-Partners:**

```
Agent (Claude Code, Cursor, Devin)
  ↓ opens PR (PAT/App: contents:write, pull-requests:write only)
  ↓ no secrets, no deployment access, no .github/ write
PR reviewed by human
  ↓ human approves
  ↓ human triggers merge
Merge triggers deploy workflow (separate job)
  ↓ uses OIDC tokens (no static secrets)
  ↓ gated by `production` environment (human approval required)
  ↓ agent has NO write access to this workflow's execution context
```

### 4.7 Prompt Injection: Treat Repository Content as Untrusted Input

Every source of repository content reachable by an AI agent must be treated as untrusted input ([CSA, May 2026](https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/05/CSA_research_note_ai_github_actions_security_20260503-csa-styled.pdf)):

- PR titles and body text
- Issue titles and body text
- Code comments in PR diff
- Commit messages
- Branch names
- GitHub Discussions content

**Structural mitigations:**

1. Delimit untrusted content from system instructions using explicit prompt boundaries — never interpolate raw issue/PR text directly into the agent's system prompt.
2. Where agents use GitHub context variables, route through an intermediate environment variable (prevents shell injection as well as prompt injection):

```yaml
# BAD — direct interpolation into run commands
- run: echo "Processing PR: ${{ github.event.pull_request.title }}"

# GOOD — intermediate environment variable
- env:
    PR_TITLE: ${{ github.event.pull_request.title }}
  run: echo "Processing PR: $PR_TITLE"
```

---

## 5. Commit Integrity

### 5.1 Required Signed Commits via Rulesets

Enable in the org-level ruleset:

```
Rule: Require signed commits
Enforcement: Active
Target branches: main, releases/**, develop
```

> "With rulesets, GitHub checks only the commits that aren't accessible from other branches." — [GitHub Docs — Available Rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)

This is more precise than branch protection rules, which don't verify signed commits on branch creation.

### 5.2 Gitsign/Sigstore: Keyless Agent Commit Signing

Traditional GPG requires key management. **Gitsign** uses Sigstore OIDC to sign commits keylessly — the signing identity is the OIDC claim from the Actions runner, binding the commit cryptographically to the specific workflow that made it. ([Gitsign — Sigstore Docs](https://docs.sigstore.dev/cosign/signing/gitsign/); [Ken Muse — Keyless Git Commit Signing, April 2025](https://www.kenmuse.com/blog/using-gitsign-for-keyless-git-commit-signing/))

```yaml
# Gitsign signing in a GitHub Actions job (agent or automated workflow)
jobs:
  commit-signed:
    permissions:
      contents: write
      id-token: write    # Required: OIDC token for Sigstore
    steps:
      - uses: actions/checkout@<SHA>
        with:
          persist-credentials: false

      - name: Install Gitsign
        run: |
          wget -q https://github.com/sigstore/gitsign/releases/download/v0.13.0/gitsign_0.13.0_linux_amd64.deb
          sudo dpkg -i gitsign_0.13.0_linux_amd64.deb

      - name: Configure Gitsign
        run: |
          git config --local commit.gpgsign true
          git config --local tag.gpgsign true
          git config --local gpg.format x509
          git config --local gpg.x509.program gitsign
          git config --local gitsign.matchCommitter true
          # Identity tied to workflow path — auditable, unforgeable
          git config --local user.name "https://github.com/${{ github.workflow_ref }}"
          git config --local user.email "41898282+github-actions[bot]@users.noreply.github.com"

      - name: Make changes and commit
        run: |
          # ... agent work here ...
          git add .
          git commit -m "feat: agent automated change [skip ci]"
          git push
```

**Verifying agent commit identity in a required workflow:**

```bash
gitsign verify \
  --certificate-identity="https://github.com/amplified-partners/shared-security/.github/workflows/agent-commit.yml@refs/heads/main" \
  --certificate-oidc-issuer=https://token.actions.githubusercontent.com \
  HEAD
```

This verification proves the commit was made by a specific named workflow, not an arbitrary PAT or rogue process.

### 5.3 Immutable Tags (GA October 2025)

Enable immutable releases at the org level: Settings → Releases → **Enable immutable releases**.

Once enabled:
- All new release assets are locked (cannot be added, modified, or deleted after publication)
- Tags for immutable releases are protected (cannot be deleted or moved)
- Each release receives a **signed attestation** in Sigstore bundle format
- If immutability is later disabled, previously immutable releases **remain immutable**

([GitHub Changelog — Immutable Releases GA, October 2025](https://github.blog/changelog/2025-10-28-immutable-releases-are-now-generally-available/))

```bash
# Verify release asset authenticity with GitHub CLI
gh attestation verify dist/fleet-api-v1.2.3.tar.gz \
  -R amplified-partners/fleet-api
```

### 5.4 Blocking Force Pushes

Enabled by default in rulesets. Ensure it is not disabled. Force pushes allow rewriting signed commit history — an agent with a compromised token could rewrite its own commits to remove evidence of malicious activity.

### 5.5 Tag Ruleset: Protect Version Tags

```json
{
  "name": "AP-Protect-Release-Tags",
  "target": "tag",
  "enforcement": "active",
  "conditions": {
    "ref_name": {
      "include": ["refs/tags/v*"]
    }
  },
  "rules": [
    { "type": "deletion" },
    { "type": "non_fast_forward" },
    { "type": "require_signed_commits" }
  ]
}
```

---

## 6. Secrets Architecture

### 6.1 Eliminate Static Secrets — OIDC First

> "If deploying to a cloud provider or using HashiCorp Vault for secret management, use OpenID Connect to create short-lived, well-scoped access tokens for workflow runs." — [GitHub Docs — Security Hardening for GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)

Goal: **zero long-lived cloud credentials in GitHub Secrets**.

```yaml
# AWS OIDC example — no AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY stored anywhere
jobs:
  deploy:
    environment: production
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: aws-actions/configure-aws-credentials@<SHA>
        with:
          role-to-assume: arn:aws:iam::123456789:role/amplified-deploy-production
          aws-region: eu-west-1
          # Role assumed via OIDC — no static credentials
```

**Critically tighten the OIDC trust policy.** Without `sub` constraints, *any* GitHub repo can assume the role. ([GitHub Docs — OIDC Security Hardening](https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect); [CSA, May 2026](https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/05/CSA_research_note_ai_github_actions_security_20260503-csa-styled.pdf))

```json
// AWS IAM trust policy — lock to specific repo AND environment
{
  "StringEquals": {
    "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
    "token.actions.githubusercontent.com:sub": "repo:amplified-partners/fleet-api:environment:production"
  }
}

// NOT this (too broad — any repo on GitHub can assume the role):
{
  "StringLike": {
    "token.actions.githubusercontent.com:sub": "repo:amplified-partners/*"
  }
}
```

For Azure and GCP, equivalent constraints apply to the federated identity credential `subject` field.

### 6.2 Infisical (or HashiCorp Vault) as External Secret Store

For secrets that cannot be OIDC-federated (third-party API keys, database passwords), inject at runtime from an external secret manager using OIDC authentication. No static credentials ever stored in GitHub Secrets.

```yaml
# Infisical OIDC pattern — no Infisical token stored in GitHub
jobs:
  build:
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@<SHA>

      - name: Fetch secrets from Infisical
        uses: Infisical/secrets-action@v1.0.9
        with:
          method: "oidc"
          identity-id: "your-infisical-machine-identity-id"  # safe to commit — not a secret
          project-slug: "amplified-partners"
          env-slug: "production"
        # Result: secrets injected as environment variables for this job only
```

Configure the Infisical machine identity trust with `repo:amplified-partners/<repo>:environment:production` subject constraints, matching the specific repo and environment. ([Infisical Docs — GitHub Actions OIDC](https://infisical.com/docs/integrations/cicd/githubactions))

### 6.3 Secret Scanning + Push Protection

**Enable at org level:**

1. Settings → Code Security → Secret scanning: **Enabled for all repos**
2. Push protection: **Enabled** — blocks commits containing secrets before they reach the repo
3. **Delegated bypass controls** (GA at enterprise level, September 2025): Designate a security team as the only reviewers who can approve bypass requests — agents cannot self-approve a push-protection bypass. ([GitHub Changelog — Delegated Bypass Controls, September 2025](https://github.blog/changelog/2025-09-16-delegated-bypass-controls-for-push-protection-now-available-at-the-enterprise-level/))

Push protection now blocks secrets in:
- Command-line pushes
- GitHub UI commits
- File uploads
- REST API requests
- GitHub MCP Server interactions (public repos) ([GitHub Docs — Push Protection](https://docs.github.com/en/code-security/secret-scanning/protecting-pushes-with-secret-scanning))

**Custom patterns for Amplified-Partners:**  
Define patterns for internal tokens (e.g., `AP_[A-Z]{6}_[0-9a-f]{32}`). These ensure proprietary secrets specific to your stack are also detected.

**Non-provider patterns:** Enabled by default in the GitHub-recommended security configuration (as of August 2024) — detects private keys, generic API keys, and other non-provider-specific secrets.

### 6.4 Leaked-Secret Rotation Protocol

When a secret is detected (by scanning, audit, or incident):

1. **Immediately revoke** the exposed credential at the provider — do not wait.
2. **Rotate** the credential (generate new value).
3. Dismiss the secret scanning alert as "revoked" (keeps audit trail).
4. Run `git-filter-repo` to remove from history **only if** the credential cannot be fully revoked — history rewriting carries high operational cost and is usually unnecessary after revocation.
5. **Audit scope:** Check the audit log for any API calls made with the compromised credential in the window between exposure and revocation.
6. If the secret was a GitHub App private key: generate new key, update all services using it, revoke old key immediately.

### 6.5 Per-Job Secrets: Never Inherit Wholesale

```yaml
# BAD — all calling workflow's secrets passed to reusable workflow
jobs:
  call-reusable:
    uses: ./.github/workflows/deploy.yml
    secrets: inherit  # ← passes ALL secrets including ones the workflow doesn't need

# GOOD — pass only what's needed
jobs:
  call-reusable:
    uses: ./.github/workflows/deploy.yml
    secrets:
      deploy-key: ${{ secrets.DEPLOY_KEY }}
      # Nothing else
```

([OWASP GitHub Actions Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/GitHub_Actions_Security_Cheat_Sheet.html))

---

## 7. What's New 2025–2026

| Feature | Date | Significance for Amplified-Partners |
|---------|------|-------------------------------------|
| **Org rulesets for GitHub Team plans** | June 2025 | Org-wide enforcement now available without Enterprise plan — enables all §2 controls |
| **Fine-grained PATs GA** | March 2025 | PAT approval required by org admins by default — close the PAT self-service gap |
| **Fine-grained PAT org approval default-on** | March 2025 | All org PAT requests now require admin approval unless explicitly disabled |
| **Immutable releases GA** | October 2025 | Tags and release assets tamper-proof with Sigstore attestations — use for all production releases |
| **Delegated bypass for push protection (enterprise)** | September 2025 | Human-only reviewers for push-protection bypass — agents cannot self-bypass |
| **OIDC expanded to Dependabot and code scanning** | May 2026 | Dependabot can use OIDC for private registries — remove static registry credentials |
| **Copilot Coding Agent GA** | September 2025 | Now widely available; treat same as Cursor/Devin — apply all agent controls |
| **GitHub Agentic Workflows technical preview** | February 2026 | Agents can write `.github/workflows/` via natural language Markdown — push ruleset blocking `.github/` is now even more critical |
| **Comment-and-Control attack class documented** | April 2026 | All AI agents running in Actions workflows must be treated as injection targets |
| **OWASP Top 10 for Agentic Applications** | December 2025 | Prompt injection is the #1 risk — formalises the threat model |
| **Push protection for GitHub MCP Server** | 2025–2026 | Secrets blocked even when pushed via MCP server interactions |

---

## 8. Prioritised Hardening Checklist

### Priority 0 — Do This Today (Prevent Catastrophic Agent Abuse)

- [ ] **Org-level:** Disable "Allow GitHub Actions to create and approve pull requests" (Settings → Actions → General)
- [ ] **Org-level:** Set default workflow permissions to "Read repository contents and packages" (read-only)
- [ ] **Org ruleset:** Enable "Require last-push approval" and "Dismiss stale reviews on new push" on all default branches
- [ ] **Org ruleset / push:** Block pushes to `.github/**` and `CODEOWNERS` — no bypass for agent apps, break-glass only via PR
- [ ] **CODEOWNERS:** `.github/ @amplified-partners/security-team` (human team, never an agent app)
- [ ] **Agent GitHub Apps:** Audit all agent apps; revoke `workflows:write` permission immediately; revoke any `Administration:write`
- [ ] **Actions:** Disable `pull_request_target` triggers in any workflow that also checks out PR code OR that has access to secrets

### Priority 1 — This Week (Close Privilege Escalation Paths)

- [ ] **Every workflow file:** Add `permissions: {}` at workflow level; grant only needed permissions at job level
- [ ] **Every action reference:** Pin all `uses:` to full commit SHA; run StepSecurity or Scorecard to find unpinned refs
- [ ] **Org-level:** Require admin approval for all fine-grained PAT requests (Settings → Personal access tokens)
- [ ] **Org-level:** Block classic PATs from accessing the org if all agents and automation have been migrated to GitHub Apps
- [ ] **Secret scanning:** Enable at org level with push protection enabled
- [ ] **Push protection bypass:** Set delegated bypass reviewers to security team only; agents cannot approve their own bypass
- [ ] **Every `actions/checkout`:** Add `persist-credentials: false`
- [ ] **Production environment:** Enable "Prevent self-reviews" and "Disallow administrators bypass"; restrict to `releases/**` and `main` branches
- [ ] **Org ruleset:** Enable "Require signed commits" on all default and release branches

### Priority 2 — This Sprint (Harden the Supply Chain)

- [ ] **All workflows:** Add Harden-Runner as first step in every job (start in `audit` mode)
- [ ] **Shared security repo:** Create org-wide required workflow that checks for `.github/` changes in agent PRs
- [ ] **Org-level:** Enable CodeQL for all repos with `language: actions` to scan workflow files
- [ ] **Dependency review:** Add as required workflow via org ruleset; fail on `high` severity
- [ ] **Release workflows:** Add `actions/attest-build-provenance` to generate SLSA attestations
- [ ] **Org-level:** Enable immutable releases
- [ ] **Reusable build workflow:** Move all release builds to a central reusable workflow in `shared-security` repo for SLSA Level 3
- [ ] **Zizmor:** Add to PR checks for Actions-specific vulnerability scanning (impostor commit, PPE patterns)
- [ ] **Dependabot:** Configure with `cooldown` delay (e.g., 7 days) for action version updates

### Priority 3 — This Quarter (Eliminate Static Credentials)

- [ ] **Cloud credentials:** Migrate all AWS/Azure/GCP credentials to OIDC federation; remove static keys from GitHub Secrets
- [ ] **OIDC trust policies:** Audit all existing trust policies for missing `sub` constraints; lock each to specific repo + environment
- [ ] **External secret store:** Deploy Infisical or HashiCorp Vault; migrate non-OIDC-federatable secrets to OIDC-authenticated runtime injection
- [ ] **Gitsign rollout:** Enable Gitsign keyless signing for all automated commits in agent workflows; verify with `gitsign.matchCommitter true`
- [ ] **Tag rulesets:** Apply tag rulesets to `v*` tags blocking deletion and unsigned tags
- [ ] **Harden-Runner:** Transition from `audit` to `block` mode with per-workflow egress allowlists
- [ ] **Custom secret patterns:** Define and enable secret scanning custom patterns for internal AP tokens
- [ ] **Reusable workflows:** Audit all `secrets: inherit` usage; replace with explicit per-secret passing

### Priority 4 — Ongoing (Continuous Assurance)

- [ ] **Audit log streaming:** Stream org audit log to SIEM; alert on `ruleset_bypass`, `workflow.secret_action`, `org.update_actions_secret`
- [ ] **OpenSSF Scorecard:** Enable via GitHub Actions on a schedule; track score over time
- [ ] **Agent red-teaming:** Quarterly prompt injection tests against all agent workflows — test all untrusted input channels (PR title, issue body, commit message, code comments)
- [ ] **Secret rotation:** Rotate all remaining GitHub Secrets on a schedule (max 90-day TTL)
- [ ] **Dependabot updates:** Keep action and dependency references current
- [ ] **Ruleset reviews:** Quarterly review of bypass list membership; remove stale actors
- [ ] **Break-glass audit:** Review every break-glass bypass event; investigate any unexplained use

---

## 9. Copy-Ready YAML Patterns

### 9.1 Secure Workflow Template (applies to all agent-triggered jobs)

```yaml
# Template: .github/workflows/_secure-base.yml
# Use as a reusable workflow or copy the structure into agent-facing workflows

name: Secure Agent Workflow Template

on:
  pull_request:
    branches: [main, 'releases/**']
  # NEVER use pull_request_target for agent workflows

# DENY ALL at workflow level
permissions: {}

jobs:
  # ─── Security gate (runs first, no secrets) ────────────────────────────
  security-gate:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      security-events: write
    steps:
      - name: Harden Runner
        uses: step-security/harden-runner@c6295a65d1254861815972266d5933fd6e532bdf  # v2.11.1
        with:
          egress-policy: audit  # Switch to block after baseline established

      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
        with:
          persist-credentials: false

      - name: Detect .github/ changes from agent PRs
        env:
          PR_AUTHOR: ${{ github.event.pull_request.user.login }}
        run: |
          AGENT_PATTERN="(claude|cursor|devin|antigravity)\[bot\]"
          if echo "$PR_AUTHOR" | grep -qE "$AGENT_PATTERN"; then
            CHANGED=$(git diff --name-only origin/${{ github.base_ref }}...HEAD | grep '^\.github/' || true)
            if [ -n "$CHANGED" ]; then
              echo "::error::Agent PR modifies .github/ without security team review"
              echo "$CHANGED"
              exit 1
            fi
          fi

      - name: Run Zizmor (Actions vulnerability scan)
        uses: woodruffw/zizmor-action@<SHA>
        with:
          minimum-severity: medium

  # ─── Build (uses only read permissions) ────────────────────────────────
  build:
    needs: security-gate
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - name: Harden Runner
        uses: step-security/harden-runner@c6295a65d1254861815972266d5933fd6e532bdf  # v2.11.1
        with:
          egress-policy: audit

      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
        with:
          persist-credentials: false

      - name: Build
        run: make build

  # ─── Deploy (gated by environment, uses OIDC) ──────────────────────────
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: production          # Human approval required before this job runs
    permissions:
      contents: read
      id-token: write                # OIDC only — no static secrets
    steps:
      - name: Harden Runner
        uses: step-security/harden-runner@c6295a65d1254861815972266d5933fd6e532bdf  # v2.11.1
        with:
          egress-policy: block
          allowed-endpoints: >
            sts.amazonaws.com:443
            s3.amazonaws.com:443

      - uses: aws-actions/configure-aws-credentials@<SHA>
        with:
          role-to-assume: arn:aws:iam::123456789:role/amplified-deploy-prod
          aws-region: eu-west-1

      - name: Deploy
        run: make deploy
```

### 9.2 Agent-Signed Commit Workflow

```yaml
# .github/workflows/agent-commit.yml
# Used when an agent (Claude Code, etc.) needs to push signed commits

name: Agent Signed Commit
on: workflow_dispatch
  inputs:
    branch:
      description: Target branch
      required: true

permissions: {}

jobs:
  commit:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      id-token: write  # For Gitsign OIDC certificate

    steps:
      - name: Harden Runner
        uses: step-security/harden-runner@c6295a65d1254861815972266d5933fd6e532bdf  # v2.11.1
        with:
          egress-policy: audit

      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
        with:
          persist-credentials: false
          ref: ${{ inputs.branch }}

      - name: Install and configure Gitsign
        run: |
          wget -q https://github.com/sigstore/gitsign/releases/download/v0.13.0/gitsign_0.13.0_linux_amd64.deb
          sudo dpkg -i gitsign_0.13.0_linux_amd64.deb
          git config --local commit.gpgsign true
          git config --local tag.gpgsign true
          git config --local gpg.format x509
          git config --local gpg.x509.program gitsign
          git config --local gitsign.matchCommitter true
          git config --local gitsign.timestampServerURL "http://timestamp.digicert.com"
          # Identity is the workflow path — auditable, verifiable
          git config --local user.name "https://github.com/${{ github.workflow_ref }}"
          git config --local user.email "41898282+github-actions[bot]@users.noreply.github.com"

      - name: Agent makes changes (read output from agent step above)
        run: |
          # Agent changes applied here
          git add .
          git commit -m "chore: agent automated update

          Workflow: ${{ github.workflow_ref }}
          Run: ${{ github.run_id }}
          SHA: ${{ github.sha }}"
          git push origin ${{ inputs.branch }}
```

### 9.3 Org Ruleset JSON (importable via `github/ruleset-recipes`)

```json
{
  "name": "AP-Default-Branch-Protection",
  "target": "branch",
  "enforcement": "active",
  "conditions": {
    "ref_name": {
      "include": ["~DEFAULT_BRANCH", "refs/heads/releases/**"],
      "exclude": []
    }
  },
  "rules": [
    { "type": "deletion" },
    { "type": "non_fast_forward" },
    { "type": "required_signatures" },
    {
      "type": "pull_request",
      "parameters": {
        "required_approving_review_count": 2,
        "require_last_push_approval": true,
        "dismiss_stale_reviews_on_push": true,
        "require_code_owner_review": true,
        "allowed_merge_methods": ["squash", "rebase"]
      }
    },
    {
      "type": "required_status_checks",
      "parameters": {
        "required_status_checks": [
          {
            "context": "security-gate",
            "integration_id": 12345
          },
          {
            "context": "dependency-review",
            "integration_id": 12345
          }
        ],
        "strict_required_status_checks_policy": true
      }
    },
    { "type": "required_linear_history" }
  ],
  "bypass_actors": [
    {
      "actor_type": "App",
      "actor_id": 99999,
      "bypass_mode": "pull_request"
    }
  ]
}
```

### 9.4 OIDC AWS Trust Policy (Locked Pattern)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::123456789:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
          "token.actions.githubusercontent.com:sub": "repo:amplified-partners/fleet-api:environment:production"
        }
      }
    }
  ]
}
```

---

## Sources

| Source | URL | Date |
|--------|-----|------|
| GitHub Docs — About Rulesets | https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets | Accessed June 2026 |
| GitHub Docs — Available Rules for Rulesets | https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets | Accessed June 2026 |
| GitHub Docs — Security Hardening for GitHub Actions | https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions | Accessed June 2026 |
| GitHub Docs — Artifact Attestations | https://docs.github.com/en/actions/security-for-github-actions/using-artifact-attestations/using-artifact-attestations-to-establish-provenance-for-builds | Accessed June 2026 |
| GitHub Docs — Managing Environments | https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-deployments/managing-environments-for-deployment | Accessed June 2026 |
| GitHub Docs — About Secret Scanning | https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning | Accessed June 2026 |
| GitHub Docs — Push Protection | https://docs.github.com/en/code-security/secret-scanning/protecting-pushes-with-secret-scanning | Accessed June 2026 |
| GitHub Docs — Dependency Review | https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/about-dependency-review | Accessed June 2026 |
| GitHub Docs — OIDC Security Hardening | https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect | Accessed June 2026 |
| GitHub Docs — GitHub App Best Practices | https://docs.github.com/en/apps/creating-github-apps/about-creating-github-apps/best-practices-for-creating-a-github-app | Accessed June 2026 |
| CSA — Prompt Injection in AI-Powered GitHub Actions | https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/05/CSA_research_note_ai_github_actions_security_20260503-csa-styled.pdf | May 2026 |
| GitHub Changelog — Org Rulesets for Team Plans | https://github.blog/changelog/2025-06-16-organization-rulesets-now-available-for-github-team-plans/ | June 2025 |
| GitHub Changelog — Immutable Releases GA | https://github.blog/changelog/2025-10-28-immutable-releases-are-now-generally-available/ | October 2025 |
| GitHub Changelog — Delegated Bypass Controls | https://github.blog/changelog/2025-09-16-delegated-bypass-controls-for-push-protection-now-available-at-the-enterprise-level/ | September 2025 |
| GitHub Changelog — Fine-Grained PATs GA | https://github.blog/changelog/2025-03-18-fine-grained-pats-are-now-generally-available/ | March 2025 |
| GitHub Changelog — Copilot Coding Agent Workflow Approval | https://github.blog/changelog/2026-03-13-optionally-skip-approval-for-copilot-coding-agent-actions-workflows/ | March 2026 |
| GitHub Changelog — OIDC Expanded to Dependabot | https://github.blog/changelog/2026-05-19-expanded-oidc-support-for-dependabot-and-code-scanning/ | May 2026 |
| OWASP — GitHub Actions Security Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/GitHub_Actions_Security_Cheat_Sheet.html | Accessed June 2026 |
| StepSecurity — Harden-Runner | https://github.com/step-security/harden-runner | Accessed June 2026 |
| Sigstore — Gitsign Configuration | https://docs.sigstore.dev/cosign/signing/gitsign/ | Accessed June 2026 |
| Ken Muse — Keyless Git Commit Signing | https://www.kenmuse.com/blog/using-gitsign-for-keyless-git-commit-signing/ | April 2025 |
| Infisical — GitHub Actions OIDC | https://infisical.com/docs/integrations/cicd/githubactions | Accessed June 2026 |
| Debugg.AI — Keyless OIDC Sigstore Workload Identity | https://debugg.ai/resources/goodbye-ssh-keys-keyless-git-oidc-sigstore-workload-identity-2025 | August 2025 |
