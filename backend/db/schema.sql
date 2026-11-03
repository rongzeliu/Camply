CREATE TABLE camp(
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    join_code TEXT UNIQUE NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    CONSTRAINT camp_date_ok CHECK (end_date >= start_date)
);

CREATE TABLE calendar(
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    camp_id bigint NOT NULL REFERENCES camp(id) ON DELETE CASCADE,
    name TEXT NOT NULL
);