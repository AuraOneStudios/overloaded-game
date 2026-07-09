# Qodo Code Review and PR Merge Rules
- NEVER merge a PR before Qodo (PR-Agent) finishes its review.
- ALWAYS write a professional and detailed code review in English before approving a PR.
- NEVER use short or generic messages like "LGTM" for approval.

# GitFlow Rules
- ALWAYS use "Create a merge commit" (`--no-ff`) when merging `develop` into `main` to preserve synchronized histories. NEVER use "Squash and merge" for main syncs.
- "Squash and merge" should only be used when merging `feature/`, `chore/`, or `bugfix/` branches into `develop`.

# GitHub Actions Security Rules
- ALWAYS pin GitHub Actions to full 40-character commit SHAs instead of mutable version tags (e.g. `uses: actions/checkout@<sha>`) to enforce supply-chain hardening and build reproducibility.
- ALWAYS include a descriptive comment indicating the release tag version next to the SHA (e.g., `# v7.0.0`) to ensure readability and maintainability.
