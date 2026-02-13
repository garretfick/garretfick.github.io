# Claude Code Instructions

This file provides entry points for Claude Code when working on garretfick.github.io.

## Steering Files

Before making changes, read the relevant steering files in `specs/steering/`:

- **[Common Tasks](specs/steering/common-tasks.md)** - Build commands, testing workflows, and justfile-based development tasks
- **[Development Standards](specs/steering/development-standards.md)** - Content conventions, code quality, spell checking, and blog post standards
- **[Project Architecture](specs/steering/project-architecture.md)** - Monorepo structure, Jekyll site, Cloudflare infrastructure, and RAG pipeline
- **[Steering File Guidelines](specs/steering/steering-file-guidelines.md)** - How to create and maintain steering files (for AI assistants updating documentation)

## MANDATORY: Before Creating a PR

**You MUST run the full test suite and verify it passes before creating any PR:**

```bash
just build && just test
```

This builds the Jekyll site (including embedding generation) and runs HTML validation, spell checking, and retrieval quality evaluation. **All checks must pass.**

If any check fails:
1. Fix the issues
2. Re-run `just build && just test`
3. Only create the PR after all checks pass

**Common failures:**
- **Spell check errors** - Add legitimate words to `site/aspell-dict.txt`, or fix the misspelling
- **HTML validation errors** - Fix invalid HTML in layouts, includes, or post content
- **Missing embeddings** - Ensure `generate_embeddings.py` dependencies are installed (`pip install sentence-transformers numpy`)
- **Retrieval quality below threshold** - Review chunking or embedding changes that may have degraded quality

## Quick Reference

### Key Commands
- `just build` - **Build the Jekyll site** (includes embedding generation)
- `just test` - **Run all tests** (HTML validation, spell check, retrieval evaluation)
- `just build && just test` - **Full CI pipeline (REQUIRED before PR)**
- `cd site && just run` - Start local development server at http://localhost:4000
- `just infra/test` - Validate Terraform configuration
- `just deploy` - Deploy infrastructure (requires credentials)

See [specs/steering/common-tasks.md](specs/steering/common-tasks.md) for the complete command reference.

### Project Structure
- `site/` - Jekyll website (GitHub Pages)
- `infra/` - Cloudflare Worker and Terraform infrastructure
- `specs/` - Design specifications and steering files
- `.github/workflows/` - CI/CD pipeline

### Critical Rules
1. **Run `just build && just test` before creating any PR**
2. **Spell check all content** - Add false positives to `site/aspell-dict.txt`
3. **Blog post filenames** follow Jekyll convention: `YYYY-MM-DD-title-slug.md`
4. **Blog posts use kramdown** Markdown with YAML front matter
5. **Infrastructure changes** require Terraform validation (`just infra/test`)
6. **Secrets** are never committed - use environment variables and GitHub secrets
