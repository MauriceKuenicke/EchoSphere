# CI/CD Integration

Integrate EchoSphere into your CI pipelines to continuously validate data quality.

## GitHub Actions
Example workflow that installs dependencies and runs tests on every push:

```yaml
name: echo-sphere-tests
on:
  push:
    branches: [ main ]
  pull_request:

jobs:
  tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install EchoSphere
        run: |
          pip install --upgrade pip
          pip install .
      - name: Configure environment
        env:
          ES_ENV_NAME: dev
          # Provide Snowflake secrets via GitHub Actions Secrets
          SNOWFLAKE_USER: ${{ secrets.SNOWFLAKE_USER }}
          SNOWFLAKE_PASSWORD: ${{ secrets.SNOWFLAKE_PASSWORD }}
        run: |
          # Template your es.ini from a secure location or use env variables
          echo "[default]" > es.ini
          echo "env = env.snowflake.dev" >> es.ini
          echo "[env.snowflake.dev]" >> es.ini
          echo "platform = snowflake" >> es.ini
          echo "user = ${SNOWFLAKE_USER}" >> es.ini
          echo "password = ${SNOWFLAKE_PASSWORD}" >> es.ini
          echo "account = ${{ secrets.SNOWFLAKE_ACCOUNT }}" >> es.ini
          echo "warehouse = ${{ secrets.SNOWFLAKE_WAREHOUSE }}" >> es.ini
          echo "role = ${{ secrets.SNOWFLAKE_ROLE }}" >> es.ini
          echo "database = ${{ secrets.SNOWFLAKE_DATABASE }}" >> es.ini
          echo "schema = ${{ secrets.SNOWFLAKE_SCHEMA }}" >> es.ini
      - name: Run EchoSphere
        run: |
          es run --junitxml reports/junit.xml || true
      - name: Publish Test Report
        if: always()
        uses: mikepenz/action-junit-report@v4
        with:
          report_paths: 'reports/junit.xml'
```

## Jenkins Pipeline
```groovy
pipeline {
  agent any
  stages {
    stage('Setup') {
      steps {
        sh 'pip install .'
      }
    }
    stage('Configure') {
      steps {
        sh '''
        cat > es.ini <<EOF
        [default]
        env = env.snowflake.dev
        [env.snowflake.dev]
        platform = snowflake
        user = $SNOWFLAKE_USER
        password = $SNOWFLAKE_PASSWORD
        account = $SNOWFLAKE_ACCOUNT
        warehouse = $SNOWFLAKE_WAREHOUSE
        role = $SNOWFLAKE_ROLE
        database = $SNOWFLAKE_DATABASE
        schema = $SNOWFLAKE_SCHEMA
        EOF
        '''
      }
    }
    stage('Test') {
      steps {
        sh 'es run --junitxml reports/junit.xml'
      }
      post {
        always {
          junit 'reports/junit.xml'
        }
      }
    }
  }
}
```

## Tips
- Examples above use Snowflake for brevity; Postgres is supported as well. Adapt `es.ini` stanzas accordingly and install the appropriate extra (`EchoSphere[postgres]`).
- Use `--export-failures` to attach detailed artifacts for debugging
- Fail the build when EchoSphere exits non‑zero, or allow failures but surface reports depending on your gate policy
- Keep secrets out of the repo; use CI secret stores
