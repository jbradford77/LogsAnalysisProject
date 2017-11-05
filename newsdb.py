#!/usr/bin/env python3

import psycopg2

try:
    db = psycopg2.connect(database="news")
except:
    print("Could not connect to database")

c = db.cursor()
c.execute("""SELECT title, num
			FROM articles, top_three
			WHERE '/article/' || articles.slug = top_three.path
			ORDER BY num DESC
			LIMIT 3;""")
top_articles = c.fetchall()

c.execute("""SELECT *
            FROM count_authors;""")
top_authors = c.fetchall()

c.execute("""SELECT to_char(days::date, 'FMMonth DD, YYYY'), percent
            FROM mathed_up
            WHERE percent > 1;""")
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
