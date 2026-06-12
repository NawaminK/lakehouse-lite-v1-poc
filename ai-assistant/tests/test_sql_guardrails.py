import unittest

from app.sql_guardrails import SqlValidationError, validate_sql


class SqlGuardrailTests(unittest.TestCase):
    def test_allows_select_and_normalizes_whitespace(self):
        self.assertEqual(
            validate_sql("  SELECT   province,   net_sales FROM daily_sales  "),
            "SELECT province, net_sales FROM daily_sales",
        )

    def test_allows_show(self):
        self.assertEqual(validate_sql("SHOW TABLES"), "SHOW TABLES")

    def test_allows_single_trailing_semicolon(self):
        self.assertEqual(validate_sql("SELECT * FROM daily_sales;"), "SELECT * FROM daily_sales")

    def test_blocks_non_read_only_statement(self):
        with self.assertRaisesRegex(SqlValidationError, "Only SELECT and SHOW"):
            validate_sql("DESCRIBE daily_sales")

    def test_blocks_destructive_keyword(self):
        with self.assertRaisesRegex(SqlValidationError, "Blocked SQL keyword: drop"):
            validate_sql("SELECT * FROM daily_sales DROP TABLE daily_sales")

    def test_blocks_multiple_statements(self):
        with self.assertRaisesRegex(SqlValidationError, "Multiple SQL statements"):
            validate_sql("SELECT * FROM daily_sales; SELECT * FROM other_table")

    def test_blocks_comments(self):
        with self.assertRaisesRegex(SqlValidationError, "comments"):
            validate_sql("SELECT * FROM daily_sales -- hide the rest")

    def test_blocks_empty_sql(self):
        with self.assertRaisesRegex(SqlValidationError, "required"):
            validate_sql("   ")


if __name__ == "__main__":
    unittest.main()

