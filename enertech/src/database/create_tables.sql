-- Create ADMIN table
CREATE TABLE admins
(
    id         SERIAL PRIMARY KEY,
    first_name VARCHAR(100)        NOT NULL,
    last_name  VARCHAR(100)        NOT NULL,
    email      VARCHAR(255) UNIQUE NOT NULL,
    password   VARCHAR(255)        NOT NULL,
    rol        VARCHAR(50)         NOT NULL,
    active     BOOLEAN             NOT NULL DEFAULT TRUE,
    department VARCHAR(100)        NOT NULL
);

-- Create TECHNICIAN table
CREATE TABLE technicians
(
    id                SERIAL PRIMARY KEY,
    first_name        VARCHAR(100)        NOT NULL,
    last_name         VARCHAR(100)        NOT NULL,
    email             VARCHAR(255) UNIQUE NOT NULL,
    password          VARCHAR(255)        NOT NULL,
    rol               VARCHAR(50)         NOT NULL,
    active            BOOLEAN             NOT NULL DEFAULT TRUE,
    max_active_orders INTEGER             NOT NULL
);

-- Create SUPERVISOR table
CREATE TABLE supervisors
(
    id            SERIAL PRIMARY KEY,
    first_name    VARCHAR(100)        NOT NULL,
    last_name     VARCHAR(100)        NOT NULL,
    email         VARCHAR(255) UNIQUE NOT NULL,
    password      VARCHAR(255)        NOT NULL,
    rol           VARCHAR(50)         NOT NULL,
    active        BOOLEAN             NOT NULL DEFAULT TRUE,
    assigned_area VARCHAR(100)        NOT NULL
);

-- Create INDUSTRIAL_ASSET table
CREATE TABLE industrial_assets
(
    id               SERIAL PRIMARY KEY,
    acquisition_date DATE         NOT NULL,
    location         VARCHAR(100) NOT NULL,
    model            VARCHAR(100) NOT NULL,
    asset_type       VARCHAR(100) NOT NULL
);

-- Create WORK_ORDER table
CREATE TABLE work_orders
(
    id                  SERIAL PRIMARY KEY,
    title               VARCHAR(255)             NOT NULL,
    assigned_to         INTEGER                  REFERENCES technicians (id) ON DELETE SET NULL,
    created_by          INTEGER                  NOT NULL REFERENCES supervisors (id) ON DELETE RESTRICT,
    asset_id            INTEGER                  NOT NULL REFERENCES industrial_assets (id) ON DELETE RESTRICT,
    maintenance_type    VARCHAR(100)             NOT NULL,
    priority            VARCHAR(50)              NOT NULL,
    status              VARCHAR(50)              NOT NULL,
    opened_at           TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at         TIMESTAMP WITH TIME ZONE,
    estimated_time      INTEGER                  NOT NULL,
    estimated_time_unit VARCHAR(20)              NOT NULL,
    resolved_on_time    BOOLEAN                  NOT NULL DEFAULT FALSE,
    description         TEXT                     NOT NULL,
    closure_comments    TEXT                     NOT NULL DEFAULT ''
    CHECK (resolved_at IS NULL OR resolved_at >= opened_at)
);