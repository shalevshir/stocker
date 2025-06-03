# AI-Powered Stock-Market Assistant

## Project Overview
An AI assistant that delivers actionable daily stock market insights and trade recommendations using data-driven analysis and machine learning.

## Key Features
- Automated data ingestion (prices, fundamentals, news sentiment)
- Feature engineering (technical indicators, fundamental ratios)
- Predictive modeling (LightGBM)
- Daily signal generation and ranking
- Telegram bot integration for notifications and feedback

## Technology Stack
- Python, PostgreSQL, LightGBM
- Docker, AWS EC2
- GitHub Actions for CI/CD

## Getting Started
1. Clone the repository
2. Set up a Python virtual environment
3. Install dependencies (requirements.txt to be added)
4. Prepare a `.env` file with your API keys and tokens (see below)

### Example `.env` file
```
EOD_API_KEY=your_eodhistoricaldata_key
NEWS_API_KEY=your_newsapi_key
TELEGRAM_TOKEN=your_telegram_bot_token
```

## Phase 0: Project Kick-off & Environment
- Initialize Git repository
- Set up AWS EC2 instance (t3.small, 50 GB gp3)
- Install Docker, git, Python
- Prepare `.env` file

---

For more details, see the project plan and documentation as the project evolves. 