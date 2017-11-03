#Udacity Logs Analysis Project - Views Added

##view to get top three articles:

```
 create view top_three as  select "right"(log.path, '-9') as "right", count(*) as num from log where length(log.path) > 1 group by log.path order by count(*) desc limit 3;
```

##views to get top authors:

``` 
create view usable_log as select "right"(log.path, '-9') as "right", status, time from log where length(log.path) > 1;
```
###sample data from usable_log

		right         | status |          time
----------------------+--------+------------------------
 candidate-is-jerk    | 200 OK | 2016-07-01 07:00:47+00
 goats-eat-googles    | 200 OK | 2016-07-01 07:00:34+00
 goats-eat-googles    | 200 OK | 2016-07-01 07:00:52+00
 balloon-goons-doomed | 200 OK | 2016-07-01 07:00:23+00
 candidate-is-jerk    | 200 OK | 2016-07-01 07:00:54+00
 bears-love-berries   | 200 OK | 2016-07-01 07:01:13+00
 trouble-for-troubled | 200 OK | 2016-07-01 07:00:56+00
 candidate-is-jerk    | 200 OK | 2016-07-01 07:01:14+00
 bad-things-gone      | 200 OK | 2016-07-01 07:01:02+00
 bears-love-berries   | 200 OK | 2016-07-01 07:01:12+00
 
```
create view match_authors as select usable_log.right, articles.id from usable_log join ar
ticles on usable_log.right = articles.slug;
```
###sample data from match_authors

           right           | author |          name
---------------------------+--------+------------------------
 candidate-is-jerk         |      2 | Rudolf von Treppenwitz
 goats-eat-googles         |      1 | Ursula La Multa
 goats-eat-googles         |      1 | Ursula La Multa
 balloon-goons-doomed      |      4 | Markoff Chaney
 candidate-is-jerk         |      2 | Rudolf von Treppenwitz
 bears-love-berries        |      1 | Ursula La Multa
 trouble-for-troubled      |      2 | Rudolf von Treppenwitz
 candidate-is-jerk         |      2 | Rudolf von Treppenwitz
 bad-things-gone           |      3 | Anonymous Contributor
 bears-love-berries        |      1 | Ursula La Multa
 balloon-goons-doomed      |      4 | Markoff Chaney


##for percent of errors over 1%

```
create view total_status as select date_trunc('day', time) as days, count(*) from log gro
up by days order by days;
```

```
create view total_status as select date_trunc('day', time) as days, count(*) from log gro
up by days where status = '404 NOT FOUND' order by days;
```

```
create view total_and_error as select total_status.count, total_status.days, error_status
.count as error_count from total_status join error_status on total_status.days = error_status.da
ys;
```

```
create view mathed_up select days, error_count, count, round(error_count * 100 / count, 1
) as percent from total_and_error;
```
