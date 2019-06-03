create database rqta_db
    with owner mpr;

create table metric
(
    id_metric   serial      not null,
    name        varchar(50) not null,
    description varchar(100) default ''::character varying,
    value       real        not null,
    qualifier   varchar(15)  default ''::character varying
);

alter table metric
    owner to mpr;

create unique index "PK_metric"
    on metric (id_metric);

create table dimension
(
    id_dimension serial                                    not null
        constraint dimension_pk
            primary key,
    name         varchar(50) default ''::character varying not null,
    value        varchar(50)                               not null
);

alter table dimension
    owner to mpr;

create unique index "PK_dimension"
    on dimension (id_dimension);

create table product
(
    id_product  serial      not null
        constraint product_pk
            primary key,
    name        varchar(50) not null,
    version     varchar(50) not null,
    description varchar(100) default ''::character varying
);

alter table product
    owner to mpr;

create unique index "PK_product"
    on product (id_product);

create table metric_dimension
(
    id_metric    integer not null
        constraint "FK_62"
            references metric (id_metric),
    id_dimension integer not null
        constraint "FK_65"
            references dimension
);

alter table metric_dimension
    owner to mpr;

create index "fkIdx_62"
    on metric_dimension (id_metric);

create index "fkIdx_65"
    on metric_dimension (id_dimension);

create table test_run
(
    id_test      serial      not null
        constraint test_run_pk
            primary key,
    scenario     varchar(50) not null,
    build_number varchar(20) not null,
    status       integer     not null,
    ts_run       timestamp   not null,
    test_group   varchar(25) default 'dev'::character varying
);

alter table test_run
    owner to mpr;

create unique index "PK_test_run"
    on test_run (id_test);

create table test_product
(
    id_test    integer not null
        constraint "FK_33"
            references test_run,
    id_product integer not null
        constraint "FK_38"
            references product
);

alter table test_product
    owner to mpr;

create index "fkIdx_33"
    on test_product (id_test);

create index "fkIdx_38"
    on test_product (id_product);

create table test_metric
(
    id_metric integer not null
        constraint "FK_56"
            references metric (id_metric),
    id_test   integer not null
        constraint "FK_59"
            references test_run
);

alter table test_metric
    owner to mpr;

create index "fkIdx_56"
    on test_metric (id_metric);

create index "fkIdx_59"
    on test_metric (id_test);

