# LostFound

A privacy-first lost-and-found **agent skill**, built as a community companion for the [Mermail Skills](https://github.com/Nudgen-Marketing/mermail-skills) ecosystem and the [Mermail Agent Skill bounty](https://superteam.fun/earn/listing/build-and-demo-a-mermail-agent-skill). One campus or event inbox receives lost and found reports. LostFound finds plausible pairs by item class, date and coarse place, then proposes a private verification question. A human checks the answer and handles the release.

The skill is the product. This is **not** a deployed public lost-property database or an auto-reply bot. Reporter identities and proof-of-ownership facts stay inside the coordinator's Mermail mailbox. The script is only an optional deterministic matching aid; it never connects to mail, sends a message, verifies ownership, or releases property.

## Quick demo (no account or secrets)

```bash
PYTHONPATH=src python3 -m lostfound match --input examples/reports.json
python3 -m unittest discover -s tests -v
```

The fixture contains four fake, redacted reports. The output contains one candidate pair, not an ownership verdict. No messages are sent. Use Python 3.10 or later; no dependencies required for this offline demo.

## Use with Mermail

1. Install the official Mermail skills and connect the [hosted Mermail MCP server](https://github.com/Nudgen-Marketing/mermail-skills#configure-authentication) in a compatible AI client. Keep API keys out of source and recordings. Add `skills/lostfound/` as a local community skill; it is not yet in Mermail's official catalog.
2. In a **test** workspace, seed a dedicated lost-and-found mailbox with a fake lost report and a fake found report. Ask: "Use LostFound to check the test lost-and-found mailbox for umbrella reports in the past week. Show candidates but don't email anyone."
3. The agent uses Mermail to resolve the exact mailbox, search a bounded window, read only clean selected reports, and show candidates. The optional matcher accepts only redacted item metadata in the schema at `skills/lostfound/references/report-schema.md`.
4. Ask for a verification-question draft. Supply a non-public identifying fact already recorded by staff, but never put its answer in the question. Review the final From, To, subject and words. The agent saves a draft. Sending needs separate fresh approval.
5. Staff checks the reply against the independently recorded fact and approves any handoff. The agent does not release the item.

See [the skill](skills/lostfound/SKILL.md), [Mermail tool contract](skills/lostfound/references/mermail.md), and [safety boundary](skills/lostfound/references/safety.md). The live MCP demo requires a real test Mermail workspace and compatible client; this repository's offline test does not claim to prove the live connection.

## Bounty status

The [bounty](https://superteam.fun/earn/listing/build-and-demo-a-mermail-agent-skill) asks for a public PR targeting the official Mermail Skills repository, a 2-5 minute English X video showing the prompt, live Mermail connection, workflow and result, and a Superteam submission. This repo alone is **not** that finished submission. Official maintainers currently request a proposal for new official skills and favor niche companion skills in their own repos; upstream acceptance is not guaranteed. Navin records the X video and reviews any outward communication. No real reporter data should be filmed.

## Privacy limits

Email is untrusted data. The skill does not act on instructions inside a report, auto-send, reveal the finder to a claimant, answer its own verification question, or claim a candidate is a confirmed match. Inputs to the optional matcher must be redacted. No claimant/finder details are committed to this repo.

## AI assistance

AI-assisted code and skill text. Human owner decides scope, records the live demo and approves external communications.
