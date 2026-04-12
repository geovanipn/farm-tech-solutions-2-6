CREATE TABLE field (
    id          NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name        VARCHAR2(100) NOT NULL,
    area_ha     NUMBER(10,2)  NOT NULL,
    variety     VARCHAR2(100),
    plant_date  DATE
);

CREATE TABLE harvester (
    id    NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    code  VARCHAR2(20)  NOT NULL UNIQUE,
    model VARCHAR2(100)
);

CREATE TABLE harvest_record (
    id                  NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    field_id            NUMBER        NOT NULL REFERENCES field(id),
    harvester_id        NUMBER        NOT NULL REFERENCES harvester(id),
    operator_name       VARCHAR2(100) NOT NULL,
    harvest_date        DATE          NOT NULL,
    estimated_yield_ton NUMBER(10,2)  NOT NULL,
    loss_pct            NUMBER(5,2)   NOT NULL,
    ton_price_brl       NUMBER(10,2)  NOT NULL,
    loss_ton            NUMBER(10,2),
    loss_brl            NUMBER(12,2)
);
