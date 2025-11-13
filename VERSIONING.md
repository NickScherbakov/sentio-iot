# Versioning and Release Process

Sentio IoT follows [Semantic Versioning 2.0.0](https://semver.org/).

## Version Format

```
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]

Example: 1.2.3-beta.1+20240115
```

### Version Components

- **MAJOR**: Incompatible API changes
- **MINOR**: New features (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)
- **PRERELEASE**: Optional pre-release identifier (alpha, beta, rc)
- **BUILD**: Optional build metadata

## Release Types

### Major Releases (x.0.0)

Breaking changes that require user action:

- API endpoint changes or removals
- Configuration format changes
- Database schema changes
- Protocol changes
- Dependency upgrades with breaking changes

**Example:** `1.0.0` → `2.0.0`

**Release Notes Must Include:**
- Migration guide
- Breaking changes list
- Deprecation warnings
- Upgrade instructions

### Minor Releases (0.x.0)

New features without breaking existing functionality:

- New API endpoints
- New protocol connectors
- New dashboard features
- Performance improvements
- New configuration options (with defaults)

**Example:** `1.1.0` → `1.2.0`

**Release Notes Must Include:**
- New features list
- Deprecation notices
- Upgrade instructions (if any)

### Patch Releases (0.0.x)

Bug fixes and minor improvements:

- Security patches
- Bug fixes
- Documentation updates
- Performance optimizations
- Dependency updates (no breaking changes)

**Example:** `1.2.3` → `1.2.4`

**Release Notes Must Include:**
- Fixed issues list
- Security advisories (if applicable)

## Pre-Release Versions

### Alpha (x.y.z-alpha.n)

Early development, unstable:

- New features in development
- Known bugs expected
- No backwards compatibility guarantee
- Not recommended for production

**Example:** `1.3.0-alpha.1`

### Beta (x.y.z-beta.n)

Feature complete, testing phase:

- All planned features implemented
- Testing in progress
- API likely stable
- Use in staging environments only

**Example:** `1.3.0-beta.2`

### Release Candidate (x.y.z-rc.n)

Near final release:

- All features complete and tested
- No known critical bugs
- Final testing before release
- Can be used in production with caution

**Example:** `1.3.0-rc.1`

## Release Process

### 1. Planning

- Define scope and features
- Create milestone in GitHub
- Update ROADMAP.md
- Assign issues to milestone

### 2. Development

- Create feature branches
- Write tests
- Update documentation
- Review and merge PRs

### 3. Pre-Release

```bash
# Create release branch
git checkout -b release/v1.2.0

# Update version in files
# - Update CHANGELOG.md
# - Update version numbers
# - Update documentation

# Commit changes
git commit -m "Prepare release v1.2.0"

# Create and push tag
git tag -a v1.2.0-rc.1 -m "Release candidate 1 for v1.2.0"
git push origin v1.2.0-rc.1
```

### 4. Testing

- Automated CI tests
- Manual testing
- Security scanning
- Performance testing
- Documentation review

### 5. Release

```bash
# Create final tag
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin v1.2.0

# Merge to main
git checkout main
git merge release/v1.2.0
git push origin main

# Delete release branch
git branch -d release/v1.2.0
git push origin --delete release/v1.2.0
```

### 6. Post-Release

- GitHub Release created automatically (via workflow)
- Docker images published automatically
- Announce on social media
- Update documentation site
- Close milestone

## Version File Locations

Update version numbers in these files:

- `api/main.py` - FastAPI app version
- `dashboard/package.json` - Dashboard version
- `CHANGELOG.md` - Release notes
- `docs/installation.md` - Installation instructions

## Changelog Format

Follow [Keep a Changelog](https://keepachangelog.com/):

```markdown
## [1.2.0] - 2024-01-15

### Added
- New Zigbee connector for MQTT devices
- Dashboard dark mode support
- API rate limiting

### Changed
- Improved query performance by 50%
- Updated dependencies

### Deprecated
- Old authentication method (will be removed in 2.0.0)

### Fixed
- Memory leak in collectors
- WebSocket disconnection issues
- Dashboard rendering bug

### Security
- Patched CVE-2024-XXXX in dependency
```

## Deprecation Policy

### Deprecation Notice

When deprecating features:

1. Add `[DEPRECATED]` to documentation
2. Log warnings when feature is used
3. Update CHANGELOG.md with deprecation notice
4. Announce in release notes
5. Keep feature for at least one major version

### Removal Process

Features can be removed:

- In next major version (after deprecation)
- At least 6 months after deprecation
- With migration guide provided

## Hotfix Process

For critical bugs in production:

```bash
# Create hotfix branch from tag
git checkout -b hotfix/v1.2.1 v1.2.0

# Fix the bug
git commit -m "Fix critical bug"

# Create and push tag
git tag -a v1.2.1 -m "Hotfix: Critical bug fix"
git push origin v1.2.1

# Merge to main
git checkout main
git merge hotfix/v1.2.1
git push origin main
```

## Version Support

| Version Type | Support Duration | Updates |
|--------------|-----------------|---------|
| Latest Major | Until next major | All updates |
| Previous Major | 12 months | Security only |
| Older Major | None | Upgrade recommended |
| Latest Minor | Until next minor | All updates |
| Previous Minor | 3 months | Security only |

## API Versioning

API versions are independent from release versions:

- Current: `/api/v1/`
- Future: `/api/v2/`

API versions are supported for:
- v1: At least 12 months after v2 release
- Deprecated endpoints: 6 months notice

## Compatibility

### Backwards Compatibility

We maintain backwards compatibility for:

- **API endpoints** - Within major version
- **Configuration files** - Within major version
- **Database schema** - Migration tools provided
- **Docker images** - Tags follow semver

### Breaking Changes

Breaking changes require:

1. Major version bump
2. Migration guide
3. Deprecation warnings (if possible)
4. 6-month notice (preferred)

## Questions?

- 📖 [Read the CHANGELOG](../CHANGELOG.md)
- 💬 [GitHub Discussions](https://github.com/NickScherbakov/sentio-iot/discussions)
- 🐛 [Report Issues](https://github.com/NickScherbakov/sentio-iot/issues)

---

Last updated: November 2024
