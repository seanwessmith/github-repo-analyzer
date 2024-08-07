# GitHub Repo Analyzer

This tool analyzes GitHub repositories, focusing on issue statistics and trends. It fetches data from the GitHub API, stores it in a SQLite database, and provides various insights through SQL queries.

## Features

- Fetches issues from a specified GitHub repository
- Stores issue data in a SQLite database
- Provides various analytical queries, including:
  - Count of issues by state
  - Average time to close issues
  - Number of issues created per month
  - Top months with the most issues created
  - Percentage of closed issues
  - Long-standing issues (open for more than 30 days)
  - Monthly closure rates

## Requirements

- Python 3.7+
- Required Python packages:
  - requests
  - pandas
  - sqlite3

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/seanwessmith/github-repo-analyzer.git
   cd github-repo-analyzer
   ```

2. Install the required packages:
   ```
   pip install requests pandas
   ```

3. Update the `owner` and `repo` variables in the script to point to the GitHub repository you want to analyze.

## Usage

1. Run the main script to fetch and store the data:
   ```
   python main.py
   ```

2. Use the provided SQL queries to analyze the data. You can run these queries using the SQLite CLI, a SQLite GUI tool, or by integrating them into your Python script.

## Sample Queries

Here are some example queries you can run:

1. Count of issues by state:
   ```sql
   SELECT state, COUNT(*) as issue_count
   FROM issues
   GROUP BY state;
   ```

2. Average time to close issues (in days):
   ```sql
   SELECT AVG(JULIANDAY(closed_at) - JULIANDAY(created_at)) as avg_days_to_close
   FROM issues
   WHERE state = 'closed' AND closed_at IS NOT NULL;
   ```

3. Number of issues created per month:
   ```sql
   SELECT strftime('%Y-%m', created_at) as month, COUNT(*) as issue_count
   FROM issues
   GROUP BY month
   ORDER BY month;
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Contact

If you have any questions or feedback, please open an issue on the GitHub repository.
