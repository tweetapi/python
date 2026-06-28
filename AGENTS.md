# TweetAPI Python SDK Agent Notes

## Repository Context

This repository is the official Python SDK for TweetAPI.

- GitHub: https://github.com/tweetapi/python
- PyPI package: https://pypi.org/project/tweetapi/
- Import package: `tweetapi`
- Distribution package: `tweetapi`

This repo is not a deployed web service. Customer impact happens when changes are
merged to the public GitHub repository and, separately, when a new package
version is built and uploaded to PyPI.

## Package And Release Model

Package metadata lives in `pyproject.toml`. The package uses Hatchling:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

When preparing a release:

1. Update the version in `pyproject.toml`.
2. Update `tweetapi/__init__.py` so `__version__` matches.
3. Run tests and compile checks.
4. Build distributions with `python -m build`.
5. Inspect the generated `dist/` contents.
6. Upload to PyPI only when explicitly requested by the maintainer.

Do not publish to PyPI from an agent run unless the user explicitly asks for it.
Do not reuse a version number that already exists on PyPI.

## API Surface Policy

Expose documented customer-facing routes only. The SDK should map Pythonic
snake_case method parameters to the backend's camelCase JSON body and query
parameters.

Do not expose hidden, internal, or undocumented routes, including:

- `/tw-v2/internal/*`
- `/tw-v2/interaction/home-timeline`
- `/tw-v2/interaction/following-timeline`
- `/tw-v2/interaction/search`
- `/tw-v2/interaction/tweet-details`
- device follow notification routes

Authenticated Twitter/X actions still require a customer-provided `auth_token`
and, when required by the endpoint, `proxy`. The TweetAPI API key is passed by
the client through the `X-API-Key` header.

## Code Patterns

- Resource classes live in `tweetapi/resources/`.
- `TweetAPI` registers resources in `tweetapi/client.py`.
- Lightweight JSON-compatible response and request shapes live in
  `tweetapi/types.py` as `TypedDict` definitions and aliases.
- Keep method names and arguments Pythonic (`snake_case`), but serialize request
  payload keys exactly as the backend expects (`camelCase`).
- `TweetAPI._get` and `TweetAPI._post` strip `None` values. Prefer passing
  optional fields through those helpers instead of hand-filtering in resources.
- Add tests with `responses` for new request paths and serialized bodies.

## Verification

Run these before considering changes ready:

```bash
pytest
python -m compileall tweetapi
```

For release candidates that add mutating authenticated endpoints, add mocked
request-body tests locally and consider a controlled live smoke test against a
test Twitter/X account before publishing to PyPI.

## Customer Safety

Merging code to GitHub does not automatically update installed customer
packages. Customers receive new SDK code only after a PyPI release and a local
upgrade such as:

```bash
python -m pip install --upgrade tweetapi
```

Treat PyPI publishing as the production release step for this SDK.
