# API Usage (Programmatic)

EchoSphere is primarily a CLI tool. While internal modules exist, the public, supported interface is the `es` command. Programmatic use is not considered stable and may change without notice.

That said, advanced users can embed the CLI using Typer’s application object.

## Invoke the CLI from Python
```python
from echosphere.main import app

# This will run the Typer application, similar to invoking `es` on the command line
# Be cautious: this will call sys.exit() on failures just like the CLI does.
if __name__ == "__main__":
    app()
```

## Recommended Approach
- Prefer invoking `es` via subprocess in automation scripts.
- Use `--junitxml` to generate machine-readable results for CI systems.
- Use `--export-failures` to capture failing rows for post-processing (captures up to 1000 rows per failed test, including column headers).

Example (Python):
```python
import subprocess

result = subprocess.run([
    "es", "run", "-e", "dev",
    "--junitxml", "reports/junit.xml",
], capture_output=True, text=True)

print(result.stdout)
print(result.stderr)
print(result.returncode)  # 0 = success
```

If you need a stabilized programmatic API in the future, please open a feature request describing your use case.
