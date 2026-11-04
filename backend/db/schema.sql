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