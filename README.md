# Udacity Logs Analysis Project

This uses Vagrant, VirtualBox, Python3, and PostgreSQL
VirtualBox can be found here https://www.virtualbox.org/ get 5.1 or earlier
Vagrant is here https://www.vagrantup.com/




## view to get top three articles:

```
 create view top_three as  
	select right(log.path, '-9') as right, 
		count(*) as num 
	from log 
	where length(log.path) > 1 
	group by log.path 
	order by count(*) desc 
	limit 3;
```

## views to get top authors:

``` 
create view usable_log as 
	select right(log.path, '-9') as right, status, time 
	from log 
	where length(log.path) > 1;
```

 
```
create view match_authors as
	select usable_log.right, articles.id
	from usable_log
	join articles on usable_log.right = articles.slug;
```
 
```
create view count_authors as 
	select usable_log.right, articles.author, authors.name 
	from usable_log 
	join articles on usable_log.right = articles.slug 
	inner join authors on articles.author = authors.id;
```

## for percent of errors over 1%

```
create view error_status as 
	select date_trunc('day', time) as days, 
		count(*) 
	from log 
	where status = '404 NOT FOUND' 
	group by days 
	order by days;
```

```
create view total_status as 
	select date_trunc('day', time) as days, 
		count(*) 
	from log 
	group by days 
	order by days;
```

```
create view total_and_error as 
	select total_status.count, total_status.days, error_status.count as error_count 
	from total_status 
	join error_status on total_status.days = error_status.days;

```

```
create view mathed_up as 
	select days, error_count, count, 
	round(error_count * 100.0 / count, 1) as percent 
	from total_and_error;
```
