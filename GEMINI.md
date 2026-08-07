# GEMINI.md

This file serves as instructional context and a reference for developers and AI agents working on **pdf-hunter**.

---

## 1. Project Overview

**pdf-hunter** is a Python CLI/library designed to discover, validate, and download PDF file links directly from webpages. It is built with high code quality and simplicity in mind, using standard parsing libraries and modern Python packaging tooling.

### Key Technologies
- **Python**: `>=3.12` (tested and verified against Python 3.12, 3.13, and 3.14)
- **Dependency & Build Management**: managed via [Astral `uv`](https://github.com/astral-sh/uv) (uses `uv.lock` and `pyproject.toml` with `uv_build` backend)
- **Parsing**: `beautifulsoup4` for HTML scraping and link extraction
- **HTTP client**: `requests` for page fetching, standard `urllib.request` for PDF downloading
- **CLI Framework**: `click` for command-line parsing and output styling
- **Task Runner**: `poethepoet` (configured in `pyproject.toml`)
- **Code Quality**: `ruff` for linting and auto-formatting
- **Testing**: `pytest` and `pytest-cov` for testing with coverage tracking

---

## 2. Directory & Architectural Layout

```text
/workspaces/pdf_hunter/
├── pyproject.toml              # Project dependencies, build-system, tool configs, CLI script, and poe tasks
├── uv.lock                     # Lock file managed by uv
├── src/
│   └── pdf_hunter/
│       ├── __init__.py         # Package entry point exposing core functions, main, & UrlTransforms
│       ├── cli.py              # CLI entry point using Click
│       ├── search.py           # Scraping, validation, and file-download implementation
│       └── url_transforms.py   # Registry of URL transformers for preprocessing URLs before download
└── tests/
    ├── test_cli.py             # CLI-specific unit tests utilizing Click CliRunner
    └── test_search.py          # Pytest unit tests verifying scraping, parsing, and warning/errors
```

### Core Architecture & Modules

#### `src/pdf_hunter/__init__.py`
Exports the public API:
- `main(url, download, output_dir)` (CLI entrypoint)
- `get_pdf_urls(url: str) -> list[str]`
- `validate_pdf_url(pdf_url: str) -> None`
- `get_pdf_name(pdf_url: str) -> str`
- `download_file(pdf_url: str, folder_path: str | None = None) -> None`
- `download_pdf_files(url: str, folder_path: str | None = None) -> None`
- `UrlTransforms` (registry class for modifying download links)

#### `src/pdf_hunter/cli.py`
Exposes the `click` command-line interface:
- **Default usage**: `pdf-hunter <URL>` prints all discovered absolute PDF URLs to stdout (one per line).
- **Download option (`-d` / `--download`)**: fetches and downloads each found PDF to the output directory.
- **Output directory option (`-o` / `--output-dir`)**: specifies where to save the files (defaults to `.` if not specified).

#### `src/pdf_hunter/search.py`
Contains the core business logic:
- `get_pdf_urls`: fetches HTML with `requests.get`, parses `a` tags via `BeautifulSoup`, filters for `.pdf` suffixes, and resolves relative URLs using `urllib.parse.urljoin`.
- `validate_pdf_url`: raises `TypeError` if not a string, or `ValueError` if the link doesn't end with `.pdf`.
- `get_pdf_name`: extracts the file name from the path.
- `download_file`: checks if a file exists, resolves the target URL via `UrlTransforms.apply(url)`, and downloads it using `urllib.request.urlopen`. Safely catches standard HTTP/connection exceptions and emits a warning using `warnings.warn`.
- `download_pdf_files`: high-level wrapper to scrape and download all found PDFs from a source page URL sequentially.

#### `src/pdf_hunter/url_transforms.py`
Implements an extensible preprocessing pipeline for download links:
- `UrlTransforms` keeps an internal `_registry: list[Callable]` of transformation functions.
- Decorating a function with `@UrlTransforms.register` adds it to the pipeline.
- `UrlTransforms.apply(url: str) -> str` passes the input URL sequentially through all registered functions.
- *Default transform*: `modify_github_url` which automatically transforms GitHub URLs containing `/blob/` to use raw URL path `/raw/` instead.

---

## 3. Environment & Task Execution

This project strictly utilizes `uv` for all environment management and script executions.

### Initial Setup
To set up the workspace, sync all dependencies, and configure the local environment:
```bash
# Sync dependencies (including development groups)
uv sync --all-groups
```

### Running the CLI
The package installs a `pdf-hunter` executable target. You can run it locally with:
```bash
# List all PDF links found on a webpage
uv run pdf-hunter "https://example.com"

# Download all PDF links to the current directory
uv run pdf-hunter "https://example.com" -d

# Download all PDF links to a custom directory
uv run pdf-hunter "https://example.com" -d -o ./downloads
```

### Running Tasks
A task runner `poethepoet` is configured within `pyproject.toml`. All standard development tasks should be executed through `uv run poe <task_name>`:

| Task Name | Command | Description |
|---|---|---|
| **`format`** | `uv run poe format` | Formats all files in the project using `ruff format`. |
| **`lint`** | `uv run poe lint` | Lints the code and auto-fixes issues using `ruff check --fix`. |
| **`test`** | `uv run poe test` | Runs the test suite via `pytest` with coverage tracking. |
| **`check`** | `uv run poe check` | Sequence task that runs `format`, `lint`, and `test` in order. |

---

## 4. Development & Testing Conventions

When making changes to this codebase, adhere strictly to the following standards and patterns:

### Coding Standards
- **Imports order**: Python standard libraries first, third-party libraries second, and local package imports last. (Enforced by `ruff`).
- **No hacks or suppressions**: Avoid using `# type: ignore` or suppressing linter rules unless specifically required.
- **Minimal Commenting**: Focus comments on *why* something is done, especially for custom handling (e.g. why we transform GitHub URLs, why certain exceptions are caught), rather than describing *what* is done.

### Extensibility Pattern (URL Transformations)
If you need to add specialized handling for other web hosting platforms (e.g., GitLab, Bitbucket) that require URL modification before downloading:
1. Define a processing function in `src/pdf_hunter/url_transforms.py`.
2. Decorate it with `@UrlTransforms.register`.
3. Add a corresponding test case in `tests/test_search.py` under `test_url_transforms()`.

### Testing Strategy
- Tests reside in `tests/` and are named `test_*.py`.
- Ensure new features have 100% (or near-100%) test coverage. Use `uv run poe test` to review coverage in the terminal or open `htmlcov/index.html` to inspect.
- Use `unittest.mock` for mocking external network calls or operations when writing fast/offline unit tests (e.g., `mock.patch` for `get_pdf_urls`).
- Use `pytest.warns` to verify that invalid URLs or download issues raise correct user warnings (without failing the entire run).
- For CLI tests, use `click.testing.CliRunner` to execute and verify exit codes and output streams.
