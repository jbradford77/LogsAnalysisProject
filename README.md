# Udacity Logs Analysis Project

* This uses Vagrant, VirtualBox, Python3, and PostgreSQL
* Uses psycopg2 to query a mock news database
1. VirtualBox can be found here https://www.virtualbox.org/ get 5.1 or earlier
2. Vagrant is here https://www.vagrantup.com/
3. Download the database here https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
* The included Vagrantfile will set up the database when you use vagrant up to start your virtual machine
* Database has 3 tables: articles, authors, and log (log is a server log)
4. Import views listed below
```
psql -d news -f create_views.sql
```
5. Run the program 
```
./newsdb.py
```


### Three questions are answered by this script
1. What are the three top articles of all time?
2. Who were the top authors?
3. Which days were the number of failure statuses higher than 2%?


## view to get top three articles:

```sql
CREATE VIEW top_three AS  
	SELECT path, count(*) AS num
	FROM log
	GROUP BY log.path;
```

## view to get top authors:

```sql
CREATE VIEW count_authors as
	SELECT authors.name, sum(num) as views
	FROM top_three
	JOIN articles on '/article/' || articles.slug = top_three.path
	INNER JOIN authors on articles.author = authors.id
	GROUP BY authors.id
	ORDER BY views desc;
```

## for percent of errors over 1%

```sql
CREATE VIEW error_status AS 
	SELECT date_trunc('day', time) AS days, 
		count(*) 
	FROM log 
	WHERE status = '404 NOT FOUND' 
	GROUP BY days 
	ORDER BY days;
```

```sql
CREATE VIEW total_status AS 
	SELECT date_trunc('day', time) AS days, 
		count(*) 
	FROM log 
	GROUP BY days 
	ORDER BY days;
```

```sql
CREATE VIEW total_and_error AS 
	SELECT total_status.count, total_status.days, error_status.count AS error_count 
	FROM total_status 
	JOIN error_status ON total_status.days = error_status.days;
```

```sql
CREATE VIEW mathed_up AS 
	SELECT days, error_count, count, 
	round(error_count * 100.0 / count, 1) AS percent 
	FROM total_and_error;
```

```sql
SELECT to_char(date, 'FMMonth DD, YYYY') AS date, 
		ROUND(error_percent, 1) AS error_percent
	FROM (
		SELECT time::date AS date, 
			100 * (COUNT(*) FILTER (WHERE status = '404 NOT FOUND') / 
				COUNT(*)::numeric) AS error_percent
		FROM log
		GROUP BY time::date
) a
WHERE error_percent > 1;
```
