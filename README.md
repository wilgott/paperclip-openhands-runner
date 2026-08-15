# paperclip-openhands-runner

Public GitHub Actions runner for [Paperclip](http://mini.tail018d12.ts.net:3100) → OpenHands.

- **This repo is public** (free Actions minutes for the workflow YAML).
- **Secrets stay private** in Actions settings (not in git).
- Jobs clone **private** [`wilgott/klinky.io`](https://github.com/wilgott/klinky.io), run OpenHands, and open a PR when files change.

## Secrets (Settings → Secrets and variables → Actions)

| Secret | Purpose |
|---|---|
| `TAILSCALE_AUTHKEY` | Pre-approved (+ preferably ephemeral) Tailscale auth key |
| `OMNIROUTE_API_KEY` | LLM via OmniRoute over Tailscale |
| `KLINKY_REPO_TOKEN` | PAT/Fine-grained token with `contents:write` + `pull-requests:write` on `wilgott/klinky.io` |

Optional variable: `PAPERCLIP_OH_LLM_MODEL` (default `openai/my-combo`).

## Trigger

Paperclip Dev agent dispatches `paperclip-openhands.yml` on this repo (`executionMode=github_actions`).

Manual:

```bash
gh workflow run paperclip-openhands.yml -R wilgott/paperclip-openhands-runner \
  -f prompt='…' \
  -f run_marker="paperclip-run-manual-1" \
  -f target_repo=wilgott/klinky.io
```
