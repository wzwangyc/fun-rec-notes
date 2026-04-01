# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- 

### Changed
- 

### Fixed
- 

### Security
- 

---

## [0.2.0] - 2026-04-01

### Added
- Financial domain types (`MoneyValue`, `PnL`, `Return`, `Currency`, `ReturnUnit`)
- Input validation for data loader (symbol, date range, source validation)
- Timezone-aware timestamps (UTC default)
- Fail-fast logic in all core functions
- 53 new tests (100% coverage for types and data loader modules)
- Security scanning workflow (GitHub Actions)
- CHANGELOG.md for change tracking

### Changed
- Rewrote `data/loader.py` with strict input validation
- Updated `requirements.txt` with locked versions for security
- Updated audit report with P1 fixes

### Fixed
- **P1-01**: No explicit domain types for financial values
- **P1-02**: No input validation at system boundaries
- **P1-03**: No timezone-aware timestamps
- **P1-04**: No explicit fail-fast logic in core functions
- **P1-05**: Backtest-live consistency (in progress, due 2026-04-14)

### Security
- Added automated security scanning with `safety` and `pip-audit`
- Locked all dependency versions to prevent supply chain attacks
- Weekly automated security scans scheduled

---

## [0.1.0] - 2026-04-01

### Added
- Initial release
- Baseline models (Random Walk, ARIMA, ETS, LightGBM, XGBoost, CatBoost)
- SOTA models (PatchTST, Autoformer, FEDformer, Informer)
- Data loader with akshare and yfinance support
- Evaluation metrics (Sharpe, MaxDD, Return, Volatility)
- Backtest framework
- Bilingual documentation (EN/CN)
- 53 passing tests

### Known Issues
- P2 issues pending (see P2_ISSUES_AND_FIXES.md)
- Test coverage incomplete for baseline and SOTA models
- No chaos testing implemented
- No observability framework

---

## Version History

| Version | Date | Status | Notes |
|---------|------|--------|-------|
| 0.1.0 | 2026-04-01 | Released | Initial release |
| 0.2.0 | 2026-04-01 | Released | P1 fixes, security improvements |
| 1.0.0 | 2026-05-01 | Planned | All P2 fixes, production ready |

---

## Upcoming Releases

### v0.3.0 (Planned: 2026-04-15)
- Determinism guarantee with seed management
- Core model test coverage (50%)

### v0.4.0 (Planned: 2026-04-25)
- Chaos testing suite
- Business comments for all core logic
- AI code audit trail

### v1.0.0 (Planned: 2026-05-01)
- All P2 issues resolved
- 100% test coverage for core logic
- Full observability framework
- Production ready

---

**Last Updated**: 2026-04-01 20:30 SGT  
**Maintainer**: Development Team
