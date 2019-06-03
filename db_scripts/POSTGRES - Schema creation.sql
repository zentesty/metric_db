
-- 
-- *************** SqlDBM: PostgreSQL ****************;
-- ***************************************************;


-- ************************************** "metric"

CREATE TABLE "metric"
(
 "id_metric"   int NOT NULL,
 "name"        varchar(50) NOT NULL,
 "description" varchar(100) NOT NULL,
 "index"       smallint NOT NULL,
 "value"       real NOT NULL,
 "qualifier"   varchar(15) NOT NULL

);

CREATE UNIQUE INDEX "PK_metric" ON "metric"
(
 "id_metric"
);



-- ************************************** "dimension"

CREATE TABLE "dimension"
(
 "id_dimension" int NOT NULL,
 "name"         varchar(50) NOT NULL,
 "value"        varchar(50) NOT NULL

);

CREATE UNIQUE INDEX "PK_dimension" ON "dimension"
(
 "id_dimension"
);




-- *************** SqlDBM: PostgreSQL ****************;
-- ***************************************************;


-- ************************************** "product"

CREATE TABLE "product"
(
 "id_product"  int NOT NULL,
 "name"        varchar(50) NOT NULL,
 "version"     varchar(50) NOT NULL,
 "description" varchar(100) NOT NULL

);

CREATE UNIQUE INDEX "PK_product" ON "product"
(
 "id_product"
);








-- ************************************** "metric_dimension"

CREATE TABLE "metric_dimension"
(
 "id_metric"     int NOT NULL,
 "id_dimension"  int NOT NULL,
 CONSTRAINT "FK_62" FOREIGN KEY ( "id_metric" ) REFERENCES "metric" ( "id_metric" ),
 CONSTRAINT "FK_65" FOREIGN KEY ( "id_dimension" ) REFERENCES "dimension" ( "id_dimension" )
);

CREATE INDEX "fkIdx_62" ON "metric_dimension"
(
 "id_metric"
);

CREATE INDEX "fkIdx_65" ON "metric_dimension"
(
 "id_dimension"
);



-- ************************************** "test_run"

CREATE TABLE "test_run"
(
 "id_test"      int NOT NULL,
 "scenario"     varchar(50) NOT NULL,
 "build_number" varchar(20) NOT NULL,
 "status"       int NOT NULL,
 "timestamp"    timestamp NOT NULL

);

CREATE UNIQUE INDEX "PK_test_run" ON "test_run"
(
 "id_test"
);




-- *************** SqlDBM: PostgreSQL ****************;
-- ***************************************************;


-- ************************************** "test_product"

CREATE TABLE "test_product"
(
 "id_test"    int NOT NULL,
 "id_product" int NOT NULL,
 CONSTRAINT "FK_33" FOREIGN KEY ( "id_test" ) REFERENCES "test_run" ( "id_test" ),
 CONSTRAINT "FK_38" FOREIGN KEY ( "id_product" ) REFERENCES "product" ( "id_product" )
);

CREATE INDEX "fkIdx_33" ON "test_product"
(
 "id_test"
);

CREATE INDEX "fkIdx_38" ON "test_product"
(
 "id_product"
);








-- ************************************** "test_metric"

CREATE TABLE "test_metric"
(
 "id_metric" int NOT NULL,
 "id_test"   int NOT NULL,
 CONSTRAINT "FK_56" FOREIGN KEY ( "id_metric" ) REFERENCES "metric" ( "id_metric" ),
 CONSTRAINT "FK_59" FOREIGN KEY ( "id_test" ) REFERENCES "test_run" ( "id_test" )
);

CREATE INDEX "fkIdx_56" ON "test_metric"
(
 "id_metric"
);

CREATE INDEX "fkIdx_59" ON "test_metric"
(
 "id_test"
);
