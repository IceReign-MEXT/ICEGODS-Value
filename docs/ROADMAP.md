# MasterBot Roadmap

## Phase 1 — Core (Done in this reset)
- Clean skeleton, docs, and config template
- Telegram alert wiring via `config.env`

## Phase 2 — Monitors
- WalletMonitor: SOL + ETH balance & tx alerts (manual actions only)
- EmailMonitor: inbox watch + phishing heuristics
- SmartContractWatch: governance/staking/farm alerts, APR projections

## Phase 3 — Reliability
- Log rotation & error backoff
- Optional cloud dashboard (DO) for metrics

## Phase 4 — Safety & Scale
- Key isolation, `.env` only (no hardcoded secrets)
- Per-module rate limits, retries, circuit breakers

## Phase 5 — UX / Bot Commands
- Telegram commands: /status, /pause <module>, /resume <module>, /last
- Inline deep-links to explorers/tools
