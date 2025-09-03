# Performance Optimization

EchoSphere is designed to execute tests concurrently. Use the tips below to keep runs fast and stable.

## Parallel Execution
- EchoSphere runs tests in parallel to reduce total runtime.
- Keep individual tests lightweight; avoid full table scans when possible.
- Partition large validations by date or key ranges.

## Query Tuning
- Filter early and select only needed columns.
- Use appropriate clustering/partitioning in Snowflake to improve aggregation and filter performance.
- Consider pre-aggregations for expensive checks and validate the aggregates instead of raw detail.

## Managing Resources
- Choose a warehouse size appropriate for your workload.
- Run heavy suites during off-peak hours where possible.
- Use separate warehouses for CI to avoid contention with production workloads.

## Flaky Tests
- Avoid nondeterministic functions unless inputs are fixed.
- Control time-based logic by fixing a date window (e.g., yesterday) instead of `CURRENT_DATE` when appropriate.

## Measuring
- Track duration of suites across runs (your CI can record job duration).
- Export failing rows to analyze patterns of slowness in specific checks.
