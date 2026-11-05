CREATE TABLE camp(
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    join_code TEXT UNIQUE NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    deleted_at timestamptz,
    CONSTRAINT camp_date_ok CHECK (end_date >= start_date)
);

CREATE VIEW active_camp AS
    SELECT * FROM camp WHERE deleted_at IS NULL;

CREATE TABLE calendar(
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    camp_id bigint NOT NULL REFERENCES camp(id) ON DELETE CASCADE,
    name TEXT NOT NULL
);

CREATE TABLE time_block(
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    calendar_id bigint NOT NULL REFERENCES calendar(id) ON DELETE CASCADE,
    title text NOT NULL,
    starts_at timestamptz NOT NULL,
    ends_at timestamptz NOT NULL,
    CONSTRAINT time_block_ok CHECK (ends_at >= starts_at)
);

CREATE TABLE leader(
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    full_name text NOT NULL
);

CREATE TABLE camp_membership(
    camp_id bigint NOT NULL REFERENCES camp(id) ON DELETE CASCADE,
    leader_id bigint NOT NULL REFERENCES leader(id) ON DELETE CASCADE,
    PRIMARY KEY (camp_id, leader_id),
    role text NOT NULL,
    CONSTRAINT camp_role_ok CHECK (role IN ('csj', 'coord', 'leader')),
    team_id bigint 
);

CREATE TABLE team(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    camp_id bigint NOT NULL REFERENCES camp(id) ON DELETE CASCADE,
    name text NOT NULL,
    class_id bigint,
    station_id bigint,
    CONSTRAINT team_assignment_ok CHECK (num_nonnulls(class_id, station_id) = 1)
);

CREATE TABLE camp_class(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    camp_id bigint NOT NULL REFERENCES camp(id) ON DELETE CASCADE,
    name text NOT NULL
);

CREATE TABLE station(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    camp_id bigint NOT NULL REFERENCES camp(id) ON DELETE CASCADE,
    name text NOT NULL
);

CREATE TABLE block_assignment(
    time_block_id bigint REFERENCES time_block(id) ON DELETE CASCADE,
    class_id bigint REFERENCES camp_class(id) ON DELETE CASCADE,
    PRIMARY KEY (time_block_id, class_id),
    station_id bigint REFERENCES station(id) ON DELETE CASCADE NOT NULL
);

CREATE TABLE resource(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    time_block_id bigint NOT NULL REFERENCES time_block(id) ON DELETE CASCADE,
    kind text NOT NULL,
    CONSTRAINT resource_kind_ok CHECK (kind IN ('slides', 'materials')), 
    label text NOT NULL,
    url text NOT NULL
);


ALTER TABLE team
    ADD CONSTRAINT team_class_id_fkey
    FOREIGN KEY (class_id) REFERENCES camp_class(id) ON DELETE SET NULL;

ALTER TABLE team
    ADD CONSTRAINT station_camp_id_fkey
    FOREIGN KEY (station_id) REFERENCES station(id) ON DELETE SET NULL;

ALTER TABLE camp_membership
    ADD CONSTRAINT camp_membership_team_id_fkey
    FOREIGN KEY (team_id) REFERENCES team(id) ON DELETE SET NULL;