# Using Fully-Qualified Table Names in SQL Test Files

When writing SQL test files, it is recommended to avoid using fully-qualified names (e.g., `database.schema.table`) for tables and other database objects. While it may seem convenient to explicitly define the full path to a database object, it significantly reduces the flexibility and reusability of the tests across different environments.

## Key Reasons to Avoid Fully-Qualified Names

1. **Environment Portability**  
   Fully-qualified names tie your test to a specific database and schema, making it difficult to execute the same test in different environments. For instance, database and schema names might vary between development, staging, and production (e.g., `dev_schema`, `staging_schema`, `prod_schema`). By relying on default schemas configured dynamically through the connection settings, you can write more portable tests that work seamlessly across environments without requiring changes to the test files.

2. **Test Maintenance**  
   Including fully-qualified names increases the effort needed to maintain your test suite. Any changes to database or schema names would require updating every test file where those are referenced, leading to potential errors and unnecessary overhead.

3. **Cleaner Test Files**  
   Omitting fully-qualified names makes tests easier to read and manage. Instead of focusing on environment-specific details, the test files can remain concise and focused on the SQL logic being tested, improving readability and reducing the cognitive load for developers.

## Best Practices

To achieve portability and maintainability:

- Configure the schema at the connection level (e.g., using your database configuration in the environment or connection string).
- Use `USE <schema>` or equivalent commands in a database setup script to set the schema context for the session before running tests.
- Avoid hardcoding database and schema names directly in the SQL queries inside test files.

By following these practices, your test files become portable, easy to maintain, and adaptable to any environment, ensuring a more effective testing process.