# 1. What are the most popular three articles of all time ?
# 2. Who are the most popular article authors of all time?
# 3. On which days did more than 1% of requests lead to errors?

import psycopg2

DBNAME = "news"


def get_data(query):
    """ fetch data from news database """
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query)
    data = c.fetchall()
    db.close()
    return data


def list_popular_articles():
    """ display the popular articles """
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
    """ display the popular authors """
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
    """ display the days with error more than per% """
    query = 'select * from error_rate where rate >' + str(per)

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
