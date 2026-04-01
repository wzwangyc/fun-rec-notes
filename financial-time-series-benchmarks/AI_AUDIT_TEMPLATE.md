# AI Code Audit Template

**Version**: 1.0  
**Effective Date**: 2026-04-01  
**Owner**: Development Team

---

## Business Intent

Ensure all AI-generated code is fully audited, validated, and traceable.  
Prevent hallucinated logic, fake APIs, or non-existent dependencies.  
Maintain compliance with enterprise standards.

---

## Audit Checklist

### For Each AI-Generated File

**File Information**:
- [ ] File path: `path/to/file.py`
- [ ] AI Model: [e.g., GPT-4, Claude 3.5, etc.]
- [ ] Generation Date: YYYY-MM-DD
- [ ] Prompt Used: [Attach or summarize]

---

## 1. Business Logic Review

**Reviewer**: [Human name]  
**Review Date**: YYYY-MM-DD

### Review Items

- [ ] **All business logic is correct**
  - [ ] Financial formulas match industry standards
  - [ ] No logical errors in calculations
  - [ ] Edge cases handled correctly

- [ ] **All financial formulas are accurate**
  - [ ] Formula source documented
  - [ ] Units consistent
  - [ ] Boundary conditions validated

- [ ] **All edge cases are handled**
  - [ ] Empty inputs
  - [ ] Invalid inputs
  - [ ] Extreme values
  - [ ] NaN/Inf handling

- [ ] **All error messages are clear**
  - [ ] Error messages explain the issue
  - [ ] Error messages suggest fixes
  - [ ] No generic "something went wrong"

### Comments

[Add any comments or concerns here]

---

## 2. Security Review

**Reviewer**: [Security team member]  
**Review Date**: YYYY-MM-DD

### Review Items

- [ ] **No hardcoded secrets**
  - [ ] No API keys in code
  - [ ] No passwords in code
  - [ ] No credentials in code

- [ ] **No SQL injection vulnerabilities**
  - [ ] All queries parameterized
  - [ ] No string concatenation for SQL

- [ ] **No XSS vulnerabilities**
  - [ ] All outputs escaped
  - [ ] No user input in HTML without sanitization

- [ ] **All inputs validated**
  - [ ] Type validation
  - [ ] Range validation
  - [ ] Format validation
  - [ ] Fail-fast on invalid input

### Comments

[Add any security concerns here]

---

## 3. Testing Review

**Reviewer**: [Senior developer]  
**Review Date**: YYYY-MM-DD

### Review Items

- [ ] **Unit tests cover all paths**
  - [ ] Normal path tested
  - [ ] Error paths tested
  - [ ] Edge cases tested
  - [ ] Coverage ≥ 100% for core logic

- [ ] **Integration tests exist**
  - [ ] End-to-end workflow tested
  - [ ] Component interactions tested

- [ ] **Edge cases tested**
  - [ ] Empty inputs
  - [ ] Invalid inputs
  - [ ] Extreme values
  - [ ] Concurrent access (if applicable)

- [ ] **Failure scenarios tested**
  - [ ] API failures
  - [ ] Network timeouts
  - [ ] Data corruption
  - [ ] Resource exhaustion

### Test Coverage Report

| Module | Coverage | Target | Status |
|--------|----------|--------|--------|
| [Module] | XX% | 100% | ✅/❌ |

### Comments

[Add any testing concerns here]

---

## 4. Approval

### Final Decision

- [ ] **Code approved for production**
- [ ] **All comments reviewed and addressed**
- [ ] **All tests passing**
- [ ] **Security scan passed**
- [ ] **Performance benchmarks met**

### Signatures

**Lead Developer**: ________________  
**Date**: ________________

**Security Team**: ________________  
**Date**: ________________

**QA Team**: ________________  
**Date**: ________________

---

## Example: Completed Audit

### File Information

- **File path**: `src/evaluation/metrics.py`
- **AI Model**: Claude 3.5 Sonnet
- **Generation Date**: 2026-04-01
- **Prompt**: "Implement Sharpe ratio calculation with proper error handling and business comments"

### 1. Business Logic Review

**Reviewer**: John Doe  
**Review Date**: 2026-04-01

- [x] All business logic is correct
  - [x] Sharpe ratio formula verified against Sharpe (1966)
  - [x] Annualization correct (sqrt(252))
  - [x] Edge cases handled (zero volatility)

- [x] All financial formulas are accurate
  - [x] Formula: (mean_excess / std_excess) * sqrt(252)
  - [x] Source: Sharpe (1966)
  - [x] Units: dimensionless (ratio)

- [x] All edge cases are handled
  - [x] Empty array → ValueError
  - [x] NaN/Inf → ValueError
  - [x] Zero volatility → ZeroDivisionError

- [x] All error messages are clear
  - [x] Error messages specify the issue
  - [x] Error messages suggest fixes

**Comments**: All business logic verified. Formula matches academic standard.

### 2. Security Review

**Reviewer**: Jane Smith  
**Review Date**: 2026-04-01

- [x] No hardcoded secrets
- [x] No SQL injection vulnerabilities
- [x] No XSS vulnerabilities
- [x] All inputs validated

**Comments**: No security issues found.

### 3. Testing Review

**Reviewer**: Bob Johnson  
**Review Date**: 2026-04-01

- [x] Unit tests cover all paths
  - [x] Normal path tested
  - [x] Error paths tested
  - [x] Edge cases tested
  - [x] Coverage: 100%

- [x] Integration tests exist
- [x] Edge cases tested
- [x] Failure scenarios tested

**Test Coverage Report**:

| Module | Coverage | Target | Status |
|--------|----------|--------|--------|
| metrics.py | 100% | 100% | ✅ |

**Comments**: All tests passing. Coverage excellent.

### 4. Approval

**Final Decision**:

- [x] Code approved for production
- [x] All comments reviewed and addressed
- [x] All tests passing
- [x] Security scan passed
- [x] Performance benchmarks met

**Signatures**:

**Lead Developer**: John Doe  
**Date**: 2026-04-01

**Security Team**: Jane Smith  
**Date**: 2026-04-01

**QA Team**: Bob Johnson  
**Date**: 2026-04-01

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-04-01 | Development Team | Initial version |

---

**Effective Date**: 2026-04-01  
**Next Review**: 2026-07-01  
**Owner**: Development Team  
**Approved By**: Tech Lead
