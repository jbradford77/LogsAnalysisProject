CREATE VIEW top_three AS  
	SELECT path, count(*) AS num
	FROM log
	GROUP BY log.path;

CREATE VIEW count_authors as
	SELECT authors.name, sum(num) as views
	FROM top_three
	JOIN articles on '/article/' || articles.slug = top_three.path
	INNER JOIN authors on articles.author = authors.id
	GROUP BY authors.id
	ORDER BY views desc;

CREATE VIEW error_status AS 
	SELECT date_trunc('day', time) AS days, 
		count(*) 
	FROM log 
	WHERE status = '404 NOT FOUND' 
	GROUP BY days 
	ORDER BY days;

CREATE VIEW total_status AS 
	SELECT date_trunc('day', time) AS days, 
		count(*) 
	FROM log 
	GROUP BY days 
	ORDER BY days;

CREATE VIEW total_and_error AS 
	SELECT total_status.count, total_status.days, error_status.count AS error_count 
	FROM total_status 
	JOIN error_status ON total_status.days = error_status.days;

CREATE VIEW mathed_up AS 
	SELECT days, error_count, count, 
	round(error_count * 100.0 / count, 1) AS percent 
	FROM total_and_error;
