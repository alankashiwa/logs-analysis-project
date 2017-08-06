# 1. What are the most popular three articles of all time ?
#
# Which articles have been accessed the most?
# Present this information as a sorted list with the most popular
# article at the top.
#
# (ex)
# "Princess Shellfish Marries Prince Handsome" — 1201 views
# "Baltimore Ravens Defeat Rhode Island Shoggoths" — 915 views
# "Political Scandal Ends In Political Scandal" — 553 views

# 2. Who are the most popular article authors of all time?
#
# When you sum up all of the articles each author has written,
# which authors get the most page views?
# Present this as as sorted list with the most popular author at the top.
#
# (ex)
# Ursula La Multa — 2304 views
# Rudolf von Treppenwitz — 1985 views
# Markoff Chaney — 1723 views
# Anonymous Contributor — 1023 views

# 3. On which days did more than 1% of requests lead to errors?
#
# The log table includes a column status that indicates the HTTP status
# code that the news site sent to the user's browser.
#
# (ex)
# July 29, 2016 — 2.5% errors

import psycopg2, bleach

DBNAME = "news"

def get_data(query):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query)
    data = c.fetchall()
    db.close()
    return data

def list_popular_articles():
    query = """
    select title, count(*) as num
    from articles, log
    where log.path like '%' || articles.slug
    group by title
    order by num desc
    """
    result = get_data(query)[:3]
    print('⋅The most popular three articles of all time:')
    for record in result:
        print('"{}" - {} views'.format(record[0], record[1]))

def list_popular_authors():
    query = """
    select name, count(*) as num
    from authors, articles, log
    where authors.id = articles.author and log.path like '%' || articles.slug
    group by name
    order by num desc
    """
    result = get_data(query)
    print('⋅The most popular article authors of all time:')
    for record in result:
        print('{} - {} views'.format(record[0], record[1]))

def list_days_with_error(per):
    view1 = """
    create view daily_access as
    select to_char(time, 'Month, DD, YYYY') as date, count(status) as access
    from log
    group by date
    order by date
    """
    view2 = """
    create view daily_error as
    select to_char(time, 'Month, DD, YYYY') as date, count(status) as error
    from log
    where status like '4%'
    group by date
    order by date
    """
    view3 = """
    create view error_rate as
    select daily_access.date, round(100.00 * error / access, 2) as rate
    from daily_access, daily_error
    where daily_access.date = daily_error.date
    """
    query = 'select * from error_rate where rate >' + str(per);

    result = get_data(query)
    print('⋅Days with error rate above ' + str(per) + '%:')
    for record in result:
        print('{} - {}% errors'.format(record[0], record[1]))

if __name__ == '__main__':
    print('[Analysis Report]')
    print('')
    list_popular_articles()
    print('')
    list_popular_authors()
    print('')
    list_days_with_error(per=1)
    print('')
