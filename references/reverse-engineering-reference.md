# Authorized Reverse Engineering Reference

Use reverse engineering only for authorized game-development purposes.

## Default Route

Technical Director -> Lead Programmer -> Reverse Engineering Specialist -> QA Lead.

## Allowed Purposes

- owned or explicitly authorized game binaries
- legacy build analysis
- crash investigation
- save/resource/file-format understanding
- compatibility research
- migration support
- original tooling or documentation work

## Not Allowed

Do not help bypass:

- DRM
- anti-cheat
- account systems
- payment logic
- online protections

Do not extract proprietary commercial code, art, UI, names, economy, or assets for reuse.

## Preferred Workflow

1. Confirm authorization and target.
2. State the question being answered.
3. Explore read-only first: imports, exports, strings, functions, xrefs, decompile, disassemble.
4. Record evidence with addresses, function names, strings, xrefs, and confidence.
5. Convert findings into original development action.
6. Verify through a reproduction, test, or independent source where possible.

## Output Format

- Target and authorization basis.
- Question being answered.
- Evidence.
- Decompiled behavior summary.
- Confidence and uncertainty.
- Recommended original development action.
- Verification note.
