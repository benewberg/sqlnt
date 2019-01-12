# sqlnt
Perform SQL on namedtuple objects.

# Examples
```
from sqlnt import SqlNt
from collections import namedtuple

nt = namedtuple('nt', 'external_id added_dt last_rating_dt note score abv style_id brewer_id beer id')

beer = [
    nt(23289,'2015-03-10','2018-08-12','',3.47,5.72,14,2,'75th Street Fountain City Irish Red',1),
    nt(39391,'2012-10-21','2017-10-02','Retired',3.29,None,14,3,'Abita Christmas Ale',2),
    nt(24012,'2012-10-26','2018-09-01','Retired',3.18,5.8,14,9,'Arcadia Amber Ale',3),
    nt(794,'2012-10-21','2017-10-02','',3.84,5.8,14,17,"Bell's Amber Ale",4),
    nt(1337,'2012-10-21','2018-09-01','Retired',3.08,5.6,14,81,'Berghoff Famous Red Ale',5)
]
```
Initialize the instance, giving it the namedtuple object and the name of the namedtuple you would reference in your query:

`ntq = SqlNt(beer, 'beer')`

Using the sqlnt() method, pass the sql to get the results of the query:

`ntq.sqlnt("select beer, score, abv from beer where score > 3.2 order by score desc;")`

...returns:

```
[nt(beer="Bell's Amber Ale", score=3.84, abv=5.8), nt(beer='75th Street Fountain City Irish Red', score=3.47, abv=5.72), nt(beer='Abita Christmas Ale', score=3.29, abv=None)]
```
By default, the results will be returned as a list of namedtuples.
To return the results as a list of tuples, change the option thusly:

`ntq.return_as_nt = False`

Re-running the same query will give the following results:
```
[("Bell's Amber Ale", 3.84, 5.8), ('75th Street Fountain City Irish Red', 3.47, 5.72), ('Abita Christmas Ale', 3.29, None)]
```

The SqlNt object has a few accessible properties:

`ntq.table`
...returns:

`'beer'`

`ntq.fields`
...returns:

`['external_id', 'added_dt', 'last_rating_dt', 'note', 'score', 'abv', 'style_id', 'brewer_id', 'beer', 'id']`

`ntq.nt`
...returns the original object:

```[nt(external_id=23289, added_dt='2015-03-10', last_rating_dt='2018-08-12', note='', score=3.47, abv=5.72, style_id=14, brewer_id=2, beer='75th Street Fountain City Irish Red', id=1), nt(external_id=39391, added_dt='2012-10-21', last_rating_dt='2017-10-02', note='Retired', score=3.29, abv=None, style_id=14, brewer_id=3, beer='Abita Christmas Ale', id=2), nt(external_id=24012, added_dt='2012-10-26', last_rating_dt='2018-09-01', note='Retired', score=3.18, abv=5.8, style_id=14, brewer_id=9, beer='Arcadia Amber Ale', id=3), nt(external_id=794, added_dt='2012-10-21', last_rating_dt='2017-10-02', note='', score=3.84, abv=5.8, style_id=14, brewer_id=17, beer="Bell's Amber Ale", id=4), nt(external_id=1337, added_dt='2012-10-21', last_rating_dt='2018-09-01', note='Retired', score=3.08, abv=5.6, style_id=14, brewer_id=81, beer='Berghoff Famous Red Ale', id=5)]```

