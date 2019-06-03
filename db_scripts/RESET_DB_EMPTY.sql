

-- Empty all tables for testing purposes
DELETE from test_product where id_product is not null;
DELETE from test_metric where id_metric is not null;
DELETE from metric_dimension where id_metric is not null;
DELETE from product where id_product is not null;
DELETE from metric where id_metric is not null;
DELETE from dimension where id_dimension is not null;
DELETE from test_run where id_test is not null;

ALTER SEQUENCE product_id_product_seq RESTART WITH 1;
ALTER SEQUENCE metric_id_metric_seq RESTART WITH 1;
ALTER SEQUENCE dimension_id_dimension_seq RESTART WITH 1;
ALTER SEQUENCE test_run_id_test_seq RESTART WITH 1;



-- Test SQL
SELECT avg(m.value) from metric m
INNER JOIN metric_dimension md on m.id_metric = md.id_metric
INNER JOIN dimension d on md.id_dimension = d.id_dimension
WHERE m.name='Mem Usage' and (d.name='process' and d.value='java');
