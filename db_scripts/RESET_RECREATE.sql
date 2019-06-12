
--  DELETE ALL TABLES
DROP TABLE testrun_product;
DROP TABLE testrun_metric;
DROP TABLE metric_dimension;
DROP TABLE product;
DROP TABLE metric;
DROP TABLE dimension;
DROP TABLE testrun;


create table metric
(
    id_metric     serial                 not null
        constraint metric_pk
            primary key,
    name          varchar(50)            not null,
    target        varchar(50),
    value         real                   not null,
    scalar_index  integer      default 0 not null,
    description   varchar(100) default ''::character varying,
    qualifier     varchar(15)  default ''::character varying,
    acquired_time timestamp
);

alter table metric
    owner to robotiq;

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
    owner to robotiq;

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
    owner to robotiq;

create unique index "PK_product"
    on product (id_product);

create table metric_dimension
(
    id_metric    integer not null
        constraint "FK_62"
            references metric,
    id_dimension integer not null
        constraint "FK_65"
            references dimension
);

alter table metric_dimension
    owner to robotiq;

create index "fkIdx_62"
    on metric_dimension (id_metric);

create index "fkIdx_65"
    on metric_dimension (id_dimension);

create table testrun
(
    id_test      serial      not null
        constraint testrun_pk
            primary key,
    build_number varchar(20) not null,
    status       integer     not null,
    run_time     timestamp   not null,
    run_type     varchar(25) default 'dev'::character varying,
    scenario     varchar(50) not null
);

alter table testrun
    owner to robotiq;

create unique index "PK_testrun"
    on testrun (id_test);

create table testrun_product
(
    id_test    integer not null
        constraint "FK_33"
            references testrun,
    id_product integer not null
        constraint "FK_38"
            references product
);

alter table testrun_product
    owner to robotiq;

create index "fkIdx_33"
    on testrun_product (id_test);

create index "fkIdx_38"
    on testrun_product (id_product);

create table testrun_metric
(
    id_metric integer not null
        constraint "FK_56"
            references metric,
    id_test   integer not null
        constraint "FK_59"
            references testrun
);

alter table testrun_metric
    owner to robotiq;

create index "fkIdx_56"
    on testrun_metric (id_metric);

create index "fkIdx_59"
    on testrun_metric (id_test);




