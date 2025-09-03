# Environment Variables

You can control EchoSphere behavior via environment variables.

- ES_ENV_NAME
  - Selects the target environment when running tests.
  - Equivalent to passing `--environment` on the CLI.
  - Example:
    ```sh
    ES_ENV_NAME=dev es run
    ```

Additional environment variables may be introduced in future releases as features evolve. Prefer the CLI options when available for clarity in scripts.
