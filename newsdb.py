#!/usr/bin/env python3

import psycopg2

db = psycopg2.connect(database="news")
c = db.cursor()
c.execute("select title, num from articles, top_three where articles.s"
          "lug = top_three.right order by num desc;")
top_articles = c.fetchall()

c.execute("select name, count(name) as num from count_authors group by name"
          " order by count(name) desc limit 10;")
top_authors = c.fetchall()

c.execute("select days::date, percent from mathed_up where percent > 1;")
fail_day = c.fetchall()

db.close()

print top_articles
print top_authors
print fail_day
