# Camply: design decisions

A running log of design decisions. Each entry has a status:

- **Decided**: stated as a requirement by the project owner
- **Provisional**: a working assumption; revisit before it is baked into the schema
- **Open**: unresolved; needs an answer before the affected table is written

Format per entry: decision, why, alternatives considered, when to revisit.

### 2026-11-02: 
### camp start and end can be same day 
- **Decision**: End camp date and start camp date can be the same, so use >= when comparing
- **Why**: To accomodate one-day activities

### camp deletion 
- **Decision**: Deleting the camp uses ON DELETE CASCADE on calendar
- **Why**: When camps are deleted, the calendars should go with, since theres no need for it anymore 
- **Alternatives**: Considered using RESTRICT, which means that all the calendars must be deleted before deleting camp, which is tedious 
- **Revisit if**: Only when calendars themselves are deemed more important than the camp 

### 2026-11-03: 
### trash bin design 
- **Decision**: Choosing to delete a camp first assigns it a deleted_at label which will track when it was deleted
- **Why**: Since camps contain lots of info, they can be viewed in the recently deleted bin in case user wants to retrieve it again

### active camp
- **Decision**: created a new filter for camps that are not in the recently deleted bin
- **Why**: This is to avoid recently deleted bins from showing up in queries

### 2026-11-04: 
### finished rest of ER diagram

### 2026-11-05:
### models.py
- **Decision**: using SQLAlchemy, wrote the database in python so that it translates later commands into sql to search the database

### interesting thing
- Discovered that I didn't need to write any constraint checks nor on delete scenarios because Postgres already handles that for me and is already defined in schema.sql!

### 2026-11-09:
### Finished creating a scalable structure for the backend
- The base of the backend is done! Before moving on and adding all the different endpoints, right now i only have camp, I will explain in my own words how the structure connects altogether 

### 2026-11-14:
### Explaining the structure
- Speaking from a very broad lens, the backend uses SQLAlchemy as an ORM (Object-Relational Mapper) to interact with and store data inside PostgreSQL 
- The main connector is through database.py, which holds the engine, sessionlocal and base 
    - Engine: this is the part that actually connects the Postgre database 
    - SessionLocal: this piece creates a new environment(?) which is used to make changes without changing the database directly and can be safely used and reverted 
    - Base: this tracks which python classes map to which tables so Alembic can compare them against the real database 
- models.py imports Base from database.py and uses it to create the SQL tables in python
- schemas.py defines the shape of JSON for both input schemas and output schemas and Pydantic validates both the structure and the value
- dependencies.py imports SessionLocal from database.py and opens a new session for each action that the application performs and then closes it once its done
- routers/camps.py contains the actual logic for each action that is performed on camp in the database
    - importing models to query the database
    - using router, .get, .post, etc. to select the action to be performed
    - importing schemas to validate the action
    - importing depencencies to open a database session
    - importing APIRouter to select the route of the query  
    - raising HTTPExceptions corresponding to invalid checks
- main.py is the first entrypoint, creating the fastapi app and registers the routers, which bring their own routes

- In use
    1. an HTTP request will flow through main.py to find the right router
    2. then selects the right .py file in the routers folder which will run an endpoint function 
    3. then dependencies is called to open a new get_db session 
    4. then models uses SQLAlchemy to query PostgreSQL
    5. then schemas uses pydantic to shape the response 
    6. finally a HTTP response is outputted


---

## 1. Principles

| ID | Decision | Status |
|---|---|---|
| P1 | Learn by building: write the code, use AI for explanation and review, not generation. Explain every merged chunk in your own words. | Decided |
| P2 | Build in vertical slices. Deploy a walking skeleton to Fly.io before building features. | Decided |
| P3 | Write the schema as plain SQL first, then reproduce it as SQLAlchemy models and Alembic migrations. | Decided |
| P4 | Every constraint gets a "should fail" test proving it rejects bad data for the right reason. | Provisional |

---

## 2. People, roles, and identity

### D1. Leader is a global entity; role and team live on the per-camp membership
- **Status:** Decided
- **Why:** A person recurs across years, but their role and team change per camp. Role and team are attributes of the *relationship* between a leader and a camp.
- **Alternatives:** Per-camp leader rows (forces re-entering names yearly); role stored on the leader (can't differ across camps).
- **Revisit if:** Cross-year reporting on a person turns out not to matter.

### D2. Three roles: `leader` < `csj` < `coord`
- **Status:** Decided
- **Why:** Higher tiers can do everything lower tiers can. Only `coord` changes roles, class membership, and block structure.
- **Note:** For content editing, `leader` and `csj` are now identical. The only difference between them is that a `csj` can self-assign as planner of a block. Decide whether an ordered integer hierarchy is still worth it, or whether an explicit per-action rule table is clearer.

### D3. Role and team are independent axes
- **Status:** Decided
- **Why:** Role answers "what may you do"; team answers "where are you". Coords may or may not be on a team, so `team_id` on the membership is nullable.
- **Consequence:** The join-lookup uniqueness constraint must handle `NULL` team correctly (see D9).

### D4. Regular leaders have no account; coords and csjs authenticate
- **Status:** Provisional (the no-account rule is Decided; the auth mechanism is proposed)
- **Why:** Name-only entry is identification, not authentication. It is acceptable only because a leader's powers are low. Elevated roles require a real identity, and Google OAuth is needed for Drive anyway.
- **Threat model:** Impersonating a leader is tolerated (they can only edit content on blocks assigned to them). Impersonating a csj or coord is not.
- **Alternatives:** Per-leader PINs; magic links by email.
- **Revisit if:** Leaders gain any ability that is costly to abuse.

### D5. Joining a camp = camp code + full name + team, matched against a coord-populated roster
- **Status:** Decided (code + name + team); Provisional (match-only, no self-registration)
- **Why:** Matching against a pre-built roster prevents junk entries and duplicates. First-time leaders are added to the roster by a coord before the camp.
- **Hardening to do:** normalize input (case, whitespace, accents); rate-limit attempts; unguessable, rotatable codes.

---

## 3. Camp structure

### D6. Classes, stations, and calendars are camp-scoped and created by coords during camp creation
- **Status:** Decided
- **Why:** They are created per camp, so each carries `camp_id`.
- **Hardening (later):** composite foreign keys `(camp_id, id)` so a row cannot reference a class from one camp and a station from another.
- **v2 idea:** copy structure from a previous camp.

### D7. A team belongs to exactly one of: a class, or a station
- **Status:** Decided
- **Why:** Teams stay together all day. A team staffs either a class or a station.
- **Implementation options to compare:** (a) two nullable FKs + `CHECK (num_nonnulls(class_id, station_id) = 1)`; (b) discriminator column + FKs; (c) separate link tables. Reference design uses (a).
- **Open:** can a class or station have more than one team? Reference design assumes yes.

### D8. Class-to-leader membership is derived via team, never stored directly
- **Status:** Decided
- **Why:** Storing it in both places duplicates a fact and invites update anomalies.

### D9. Join key uniqueness: unique `(camp, full name, team)`, with NULL handled explicitly
- **Status:** Provisional
- **Why:** In PostgreSQL a standard `UNIQUE` treats NULLs as distinct, so two team-less coords with the same name would both be allowed.
- **Options:** `UNIQUE NULLS NOT DISTINCT` (Postgres 15+), or two partial unique indexes.
- **Open:** where does the constraint live, given `full_name` sits on `leader` and `team_id` on `camp_membership`? Either denormalize or enforce in a transaction in application code.

### D10. One team per leader per camp
- **Status:** Provisional
- **Why:** Simplest model that matches "teams stay together all day". Single `team_id` on the membership.
- **Revisit if:** A leader needs to belong to two teams at once. Use `leader_override` (D13) for one-off moves first.

---

## 4. Scheduling model

### D11. Block structure is fixed up front; only coords edit it, and only in edit mode
- **Status:** Decided
- **Why:** Time, title, and calendar of a block change rarely. The camp has a state (for example `planning`, `live`, `locked`) and a coord-only edit mode.
- **Policy:** `can_edit_structure(actor, camp) = actor.role == coord AND camp allows structure edits`.
- **Consequence:** Authorization takes the camp's state as an input, not just the actor's role.

### D12. Class-to-station placement is a ternary assignment per block
- **Status:** Decided
- **Why:** The fact is `(time_block, class) -> station`.
- **Constraints:** `UNIQUE (time_block_id, class_id)` (a class is in one place per block). `UNIQUE (time_block_id, station_id)` (a station hosts one class per block) only if that is actually true: verify.
- **Note:** No row is required for blocks without stations (meals, worship).

### D13. Defaults plus exceptions for location
- **Status:** Decided (the principle); Provisional (the shape)
- **Why:** A leader's location is derived: team -> class -> station for that block, or team -> fixed station. Only deviations are stored in `leader_override`. Effective location = override if present, else derived default.
- **Why not materialize:** Storing a row per leader per block creates a cascade of edits whenever a class moves.

### D14. Content edit rule
- **Status:** Decided
- **Rule:** `can_edit_content(actor, block) = actor.role == coord OR actor is responsible for block`.
- **Content fields:** description, resources (slides, materials). **Structural fields:** times, title, calendar (see D11).

### D15. One responsible leader per block at a time
- **Status:** Provisional
- **Why:** Matches "csj plans, later transfers to a leader". Modeled as a nullable `responsible_leader_id` on the block.
- **Related provisional rule:** transfer is performed by the current responsible csj or by a coord.
- **Revisit if:** Several people share a block. Then use a join table.

### D16. Time storage
- **Status:** Provisional
- **Why:** Store instants as `timestamptz`. Store the camp's IANA timezone on the camp and convert for display, since schedules are read as wall-clock time.
- **Constraint:** `CHECK (ends_at > starts_at)`.
- **Open:** may blocks in the same calendar overlap? If not, add an exclusion constraint on `tstzrange`. 

---

## 5. Points

### D17. Points are an append-only ledger, not a counter
- **Status:** Provisional
- **Why:** Gives an audit trail (who, when, why), makes corrections a negative entry, avoids lost-update races, and a live leaderboard is just `SUM`.
- **Alternative:** `points` column on class, updated atomically (`SET points = points + :n`). Simpler, but no history.
- **Open:** who may award points. Working assumption: any leader on the team of the station where the class currently is.

---

## 6. Permission matrix (reference)

| Action | Leader | CSJ | Coord |
|---|---|---|---|
| View schedule | yes | yes | yes |
| Edit content of a block they are responsible for | yes | yes | yes |
| Edit content of any other block | no | no | yes |
| Self-assign as planner of a block | no | yes | yes |
| Edit block structure (in edit mode only) | no | no | yes |
| Change roles, class membership, teams | no | no | yes |

Enforce on the server for every endpoint; the UI hiding a button is not authorization.

---

## 7. Deferred (not yet modeled)

- Task page for privileged users (entity, assignment, link to blocks)
- Audit log of structural and role changes
- Google Drive: decide link-only vs export vs two-way sync before modeling
- Live updates (polling first; SSE or WebSockets later); conflict handling (last-write-wins vs optimistic locking with a version column)
- Soft deletes vs hard deletes
- Description format (plain text, markdown, or rich text)

## 8. Open questions

1. Can more than one team staff a class or station? (D7)
2. Can blocks in one calendar overlap? (D16)
3. Who may award points? (D17)
4. Do you need leaders in multiple teams at once? (D10)