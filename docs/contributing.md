# Contributing to EchoSphere Docs

We welcome improvements to the documentation. This guide explains how to contribute and how docs are maintained.

## How to Contribute
1. Fork the repository and create a feature branch.
2. Edit Markdown files under `docs/`.
3. Preview locally with MkDocs Material:
   ```sh
   pip install mkdocs mkdocs-material
   mkdocs serve
   ```
4. Submit a pull request with a clear description and screenshots if visual changes are significant.

## Style Guide
- Be concise and task‑oriented; prefer examples over theory.
- Use sentence case for headings.
- Use admonitions for notes, tips, and warnings.
- Keep code blocks copy‑paste ready.

## Structure
- Getting Started → quick paths for new users
- User Guide → workflows and how‑tos
- Command Reference → precise CLI options
- Reference → configuration and environment variables
- Advanced → CI/CD, performance, scale
- Examples/Tutorials → cookbook and end‑to‑end guides
- Troubleshooting → common issues and resolutions

## Maintenance Plan
- Review high‑traffic pages monthly; full sweep quarterly.
- Keep docs in sync with releases; update command and option references.
- CI should build docs and check links (planned).

## Code of Conduct
Please be respectful and constructive. See the repository’s main guidelines for behavior and reporting.
