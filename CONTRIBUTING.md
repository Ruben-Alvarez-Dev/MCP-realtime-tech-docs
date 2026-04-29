# Contributing to MCP-realtime-tech-docs

Thanks for your interest in contributing! This project aims to be the definitive documentation hub for realtime voice & video technologies.

## How to Contribute

### Adding Documentation

1. Fork the repository
2. Create a branch: `git checkout -b docs/add-product-name`
3. Add markdown files in the appropriate `docs/` subdirectory
4. Follow the naming convention: `NN-DESCRIPTIVE-NAME.md` (e.g., `01-QUICKSTART.md`)
5. Include source URLs in the header: `> Source: https://...`
6. Submit a Pull Request

### Adding a New Product

1. Create a new directory under `docs/`: `docs/your-product/`
2. Start with `00-OVERVIEW.md` (required)
3. Add API reference, code examples, architecture docs
4. Update the `install.sh` script if the product has its own install step
5. Submit a Pull Request with a clear description

### Reporting Issues

- Use GitHub Issues
- Include the product name and file path
- Describe what's wrong or missing

### Code Contributions

1. Fork and clone
2. Create venv: `python3 -m venv .venv && .venv/bin/pip install fastmcp`
3. Make changes in `src/`
4. Run tests: `.venv/bin/python3 tests/test_server.py`
5. Submit a Pull Request

## Documentation Standards

- **Format:** Markdown (.md)
- **Language:** English
- **Headers:** Include source URL on line 2
- **Code blocks:** Use fenced code blocks with language tags
- **No secrets:** Never commit API keys, tokens, or passwords
- **No personal info:** No names, emails, or personal identifiers
- **Placeholders:** Use `sk-xxx`, `tp-xxx`, `YOUR_API_KEY` for examples

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
