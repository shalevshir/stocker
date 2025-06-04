# MVP Database Schema — AI-Powered Stock Market Assistant

## Table: `prices`

| Column Name     | Data Type | Description                   |
|------------------|------------|-------------------------------|
| `ticker`         | TEXT       | Stock symbol (e.g., AAPL)     |
| `date`           | DATE       | Trading day                   |
| `open`           | NUMERIC    | Opening price                 |
| `high`           | NUMERIC    | Daily high                    |
| `low`            | NUMERIC    | Daily low                     |
| `close`          | NUMERIC    | Closing price                 |
| `volume`         | BIGINT     | Daily volume                  |
| `adjusted_close` | NUMERIC    | Adjusted close price          |

**Primary Key:** (`ticker`, `date`)

---

## Table: `fundamentals`

| Column Name     | Data Type | Description                      |
|------------------|------------|----------------------------------|
| `ticker`         | TEXT       | Stock symbol                     |
| `report_date`    | DATE       | Fiscal report date               |
| `pe_ratio`       | NUMERIC    | Price-to-Earnings ratio          |
| `eps_growth`     | NUMERIC    | EPS growth rate                  |
| `market_cap`     | NUMERIC    | Market capitalization            |
| `dividend_yield` | NUMERIC    | Dividend yield                   |

**Primary Key:** (`ticker`, `report_date`)

---

## Table: `news_sentiment`

| Column Name      | Data Type | Description                      |
|------------------|------------|----------------------------------|
| `id`             | UUID       | Unique ID                        |
| `ticker`         | TEXT       | Related stock symbol             |
| `headline`       | TEXT       | News headline                    |
| `source`         | TEXT       | News source                      |
| `published_at`   | TIMESTAMP  | Time of publication              |
| `sentiment_score`| NUMERIC    | Sentiment score (-1 to 1)        |

**Primary Key:** (`id`)

---

## Table: `signals`

| Column Name      | Data Type | Description                      |
|------------------|------------|----------------------------------|
| `ticker`         | TEXT       | Stock symbol                     |
| `date`           | DATE       | Signal generation date           |
| `signal_strength`| NUMERIC    | Normalized score (e.g., 0 to 1)  |
| `rank`           | INTEGER    | Daily rank among tickers         |

**Primary Key:** (`ticker`, `date`)

---

## Table: `feedback`

| Column Name      | Data Type | Description                      |
|------------------|------------|----------------------------------|
| `signal_id`      | UUID       | Foreign key to `signals`         |
| `user_id`        | TEXT       | Telegram or anonymized user ID   |
| `feedback_value` | INTEGER    | 1 (👍), -1 (👎), or 0 (neutral)   |
| `submitted_at`   | TIMESTAMP  | Time of feedback submission      |

**Primary Key:** (`signal_id`, `user_id`)