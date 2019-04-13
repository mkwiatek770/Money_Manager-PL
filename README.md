# expenses-manager

App to manage your money in easy way. 

## Technology Stack:
* Python
* Flask
* PostgreSQL

## What you can do ?
* Put credit on your account
* Add expense (Ammount of money, description, category)
* Remove expense
* Display list of expenses
* Generate XLX report of all expenses `xlsxwriter` library
* Generate PDF report of all expenses using `reportlab` library
* Search for specific expense
* Check our balance

## Installation
1. Clone repository
2. Restore database (psql needed) `psql -U postgres -f database/sync_dump.sql -h localhost active_db`
3. Create virtual environment `virtualenv -p python3 venv`
4. Activate virtualenv `source venv/bin/activate`
5. `python3 manage.py run.py`

Done :)

