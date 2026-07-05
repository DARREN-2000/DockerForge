# Examples

## Analyzing a Web API

Consider a simple FastAPI application (`src/main.py`).

```bash
dockerforge analyze src/main.py
```

**Output:**
```
INFO: dockerforge: file=src/main.py stdlib=[] third_party=['fastapi', 'uvicorn'] local=['routers']
```

## Remediating a Build

If a build fails because `psycopg2` requires `libpq-dev`, the initial build will fail. Running the remediate command:

```bash
dockerforge remediate Dockerfile build.log
```

DockerForge will parse `build.log`, match the apt failure or module failure against `PATTERNS` in `src/dockerforge/remediation/patterns.py`, and patch the `Dockerfile` to include the appropriate `apt-get` or `pip install` commands.
