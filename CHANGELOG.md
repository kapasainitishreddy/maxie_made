# Changelog

All notable changes to Maxie Made apps will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2026-06-07

### Security
- Added rate limiting middleware (100 req/min, 30 writes/min) to all 4 backends
- Added OWASP security headers (HSTS, CSP, X-Frame-Options, etc.) to all 4 backends
- Added request validation middleware (blocks SQL injection patterns, oversized payloads)
- Added dependency vulnerability scanning (pip-audit, pnpm audit) to CI
- Added weekly scheduled security scans via GitHub Actions
- Added secret scanning to CI (blocks commits with live API keys)
- Added bandit static analysis to CI

### Added
- Privacy policy pages for all 4 apps (/privacy)
- Terms of service pages for all 4 apps (/terms)
- Security disclosure pages for all 4 apps (/security)
- Plausible analytics integration (privacy-friendly, no cookies)
- Sentry error tracking integration (graceful no-op when DSN not set)

### Changed
- Replaced generic Lucide icons with custom SVG logos for all 4 apps
- Added "How it works" 4-step process diagrams to all 4 landing pages
- Added "Real case study" scenario sections with realistic company examples
- Added pricing pages for CloudFinOps, AutoHedge, and QuantaLab (PharmaIP had one)
- All 4 apps now have working dashboards with real data

## [0.4.0] - 2026-06-06

### Added
- Real working AutoHedge dashboard (backtest form, equity curve chart, positions table, 12 strategy cards)
- Real working CloudFinOps dashboard (3 stat cards, 2 accounts, 5 recommendations with terraform_hcl)
- Real working QuantaLab notebook + marketplace pages
- Input, Select, Badge, Skeleton UI components for all 4 apps
- DashboardLayout wrapper for non-PharmaIP apps

### Fixed
- CloudFinOps /recommendations endpoint: changed `created_at: str` to `created_at: datetime`
- All 4 apps: added "use client" directive to dashboard-layout.tsx
- PharmaIP sidebar: conditional UserButton (falls back to "Sign in" link when no Clerk key)
- CloudFinOps seeded 5 recommendations + 4 savings events with real cost data

## [0.3.0] - 2026-06-05

### Added
- 5 real pharma patent seeds (Keytruda, Humira, Skyrizi, Eliquis, Kymriah)
- 4 pricing tiers for PharmaIP Radar

## [0.2.0] - 2026-06-04

### Added
- 3D hero animations using react-three-fiber for all 4 apps
- 4 distinct color schemes (purple, teal, orange, violet)

## [0.1.0] - 2026-06-03

### Added
- Initial monorepo with 4 SaaS app scaffolds
- PharmaIP Radar: 60 backend tests passing
- CloudFinOps Co-Pilot: 30 backend tests passing
- AutoHedge Pro: 33 backend tests passing
- QuantaLab: 17 backend tests passing
- SQLite fallback for local development
- Dev auth bypass for testing without Clerk keys
