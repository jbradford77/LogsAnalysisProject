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

print("\nWhat are the three top articles of all time?\n")
for title, views in top_articles:
    print("  {}  --  {} views".format(title, views))
print("\nWho were the top authors?\n")
for name, count in top_authors:
    print("  {}  --  {} views".format(name, count))
print("\nWhich days were the number of failure statuses higher than 2%?\n")
for days, percent in fail_day:
    print("  {}  --  {}%".format(days, percent))
