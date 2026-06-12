# Sample Data

These files are intentionally tiny so teammates can inspect the full pipeline by eye.

## Files

| File | Purpose |
|---|---|
| `csv/orders.csv` | Baseline source for `spark/jobs/01_create_tables.py` |
| `json/orders.json` | Same sample records in newline-delimited JSON for ingestion experiments |

## Order fields

| Column | Type in pipeline | Notes |
|---|---|---|
| `order_id` | BIGINT | Business key for the sample order |
| `customer_id` | STRING | Sample customer identifier |
| `order_date` | DATE after silver casting | Source date string in CSV/JSON |
| `province` | STRING | Simple geographic dimension |
| `amount` | DECIMAL(12,2) | Positive source amount |
| `status` | STRING | Allowed values are `paid` and `refund` |

The baseline gold table treats `paid` as positive sales and `refund` as negative sales.

