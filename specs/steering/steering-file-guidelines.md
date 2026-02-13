# Steering File Guidelines

This file explains the two-file pattern used for steering files and how AI assistants should create or update them to maintain consistency across different AI systems.

## Core Architecture

Steering files follow a **two-file pattern**:

1. **Source of truth** in `specs/steering/` - Detailed, self-contained guidance documents that work with any AI tool
2. **Pointer files** in tool-specific directories - Lightweight files that reference the source of truth

| Directory | Target Tool | Content |
|-----------|-------------|---------|
| `specs/steering/` | Any AI assistant | Full detailed guidance |
| `.kiro/steering/` | Kiro | Pointer with optional frontmatter |
| `CLAUDE.md` (root) | Claude Code | Top-level entry point with quick reference |

## Key Principles

### AI-Agnostic Content
Write `specs/steering/` files so they are useful to any AI coding assistant, not just one specific tool. Avoid tool-specific syntax or directives in the source-of-truth files.

### Token Efficiency
Keep steering files focused and scannable. Use tables for structured data. Avoid verbose prose when a list or table communicates the same information. AI assistants load these files into context, so every token matters.

### Easy Maintenance
Each steering file covers a single topic. When information changes, there is exactly one place to update (the `specs/steering/` file). Pointer files only need updating if the file is renamed or the scope changes.

### Portability
If a new AI tool is adopted, only new pointer files need to be created. The source-of-truth content in `specs/steering/` remains unchanged.

## Creating a New Steering File

### 1. Create the Source File

Add a new Markdown file to `specs/steering/`:

```markdown
# Topic Name

Brief description of what this file covers and when it applies.

## Section 1
...

## Section 2
...
```

**Content guidelines:**
- Start with an H1 heading matching the topic
- Include a brief description of scope
- Use H2 for major sections
- Prefer tables and lists over paragraphs
- Include concrete examples where helpful
- Reference related steering files with relative links

### 2. Create Pointer Files

**Kiro pointer** (`.kiro/steering/<name>.md`):

```markdown
# Topic Name

See [specs/steering/<name>.md](../../specs/steering/<name>.md) for the full guidance.

Brief one-line summary of when this applies.
```

For files that should only load when editing certain paths, add frontmatter:

```markdown
---
inclusion: fileMatch
fileMatchPattern: "infra/terraform/**"
---

# Topic Name

See [specs/steering/<name>.md](../../specs/steering/<name>.md) for the full guidance.
```

### 3. Update CLAUDE.md

Add a link to the new steering file in the "Steering Files" section of `CLAUDE.md`.

## Content Scope

### Include
- Architectural patterns and project structure
- Conventions and standards (naming, formatting, file organization)
- Build and test workflows
- Common development tasks
- Error handling and troubleshooting guidance

### Exclude
- Complete API documentation (link to external docs instead)
- Full configuration file contents (reference the file path)
- Step-by-step tutorials (link to external resources)
- Information that changes frequently (use file references)

## Maintenance

When modifying the project in ways that affect steering files:

1. Update the relevant `specs/steering/` file
2. Verify pointer files still reference the correct path
3. Check that `CLAUDE.md` quick reference is still accurate
4. If adding a new subsystem, consider whether it needs its own steering file
