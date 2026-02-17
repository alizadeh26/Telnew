name: Update VPN Subscription

# ←←← این خطوط جدید اضافه شد
permissions:
  contents: write

on:
  schedule:
    - cron: '*/5 * * * *'
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: pip install requests beautifulsoup4

      - name: Run scraper
        run: python update.py

      - name: Commit & Push
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          
          git add subscription.txt subscription_base64.txt last_update.txt
          
          if git diff --staged --quiet; then
            echo "No changes."
          else
            git commit -m "Update subscription $(date -u +'%Y-%m-%d %H:%M:%S UTC')"
            git push
          fi
