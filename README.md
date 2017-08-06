# Project: Logs Analysis
This is the third project of [Udacity](https://www.udacity.com): [Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004)

**by Alan Po-Ching**

# About the project
Analyze the logs and generate a report for a newspaper site powered by [PostgreSQL datebase](https://www.postgresql.org).

The report should answer the following questions:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

# Requirements
* The code should generate correct answers to the questions
* The code should generate output in clearly formatted plain text.
* The answer should be derived mainly by SQL queries but not by python code.

# Set up the environment
1. Install [Python3](https://www.python.org/downloads/)
2. Download and install [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
3. Download and install [Vagrant](https://www.vagrantup.com/downloads.html)
4. Fort or clone this [repository](https://github.com/udacity/fullstack-nanodegree-vm)
5. Place the _report.py_ of this repo under the /vagrant directory
6. Download the [database script](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip), unzip and place it under the /vagrant directory
7. Navigate to the /vagrant directory and run `vagrant up` to start the virtual machine
8. Run `vagrant ssh` to log in the virtual machine


# Create the database and views
1. Run `psql -d news -f newsdata.sql` on the virtual machine /vagrant folder to create the database
2. Run the following code to create the necessary views:
```sql
create view daily_access as
select to_char(time, 'Month, DD, YYYY') as date, count(status) as access
from log
group by date
order by date
```
```sql
create view daily_error as
select to_char(time, 'Month, DD, YYYY') as date, count(status) as error
from log
where status like '4%'
group by date
order by date
```
```sql
create view error_rate as
select daily_access.date, round(100.00 * error / access, 2) as rate
from daily_access, daily_error
where daily_access.date = daily_error.date
```
3. Run `python3 report.py` to generate the analysis report
