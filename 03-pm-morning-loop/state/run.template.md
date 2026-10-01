# Step file: state/<YYYY-MM-DD>/<n>-<name>.md

step: 2-align
status: pending | checking | failed | awaiting-approval | approved | done | skipped
retries: 0
gate_a: PASS | FAIL | OVERRIDDEN by user
gate_b: approved | edited | rejected | n/a
updated: YYYY-MM-DD HH:MM

## Output
<the maker's output block, as last produced; for edits, the version after the user's changes>

## Checker verdict
<the checker's last RULE RESULTS block>

## Human notes
<edits made at gate B, rejection reasons, override reasons>
