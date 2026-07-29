# Security Policy

## Reporting

Use GitHub private vulnerability reporting if enabled on this repository, otherwise email
`admin@gexiro.com`.

The most useful report here is a case where the linter *misses* a secret-shaped string it should
catch, or where the contract's OPSEC guidance is wrong or incomplete. Never include a real secret in
a report — describe its shape.

## The OPSEC rule this repo exists to protect

A versioned, mirrored vault keeps every write forever. The contract (`AGENTS.md`, OPSEC section) is
blunt about it: secrets never go into a note, not even redacted, because redaction does not remove
them from git history or any mirror. If one lands there, the primary control is to rotate the secret
out-of-band immediately, then scrub history — in that order.

`tools/lint_vault.py` includes a coarse secret-shaped-string check as a backstop. It is a safety
net, not a guarantee: pair it with a real pre-commit secret scanner (gitleaks or trufflehog) as the
contract recommends.
