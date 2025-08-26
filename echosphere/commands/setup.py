# import typer
#
# from echosphere.core.suite_display import display_test_names_table, display_test_sql_code
#
# app = typer.Typer()
#
#
# @app.command(name="suite", help="List current test suite.")
# def list_test_suite():
#     """
#     List current test suite.
#
#     This command retrieves a list of SQL test files and presents them in a
#     structured table format. It uses the `Table` utility for formatting the
#     output and prints it to the console.
#
#     :raises RuntimeError: If there are issues in retrieving test files or
#         displaying the table on the console.
#     :return: None
#     """
#     display_test_names_table()
#
#
# @app.command(name="test", help="View the SQL code for a given test file.")
# def view_test_sql(name: str):
#     display_test_sql_code(name)
