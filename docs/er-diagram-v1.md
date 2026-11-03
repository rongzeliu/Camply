# Camply: reference ER diagram

Renders on GitHub automatically. In VS Code, install the "Markdown Preview Mermaid Support" extension, or paste the block into https://mermaid.live to zoom and pan.

```mermaid
erDiagram
  LEADER ||--o| ACCOUNT : "may have"
  LEADER ||--o{ CAMP_MEMBERSHIP : joins
  CAMP ||--o{ CAMP_MEMBERSHIP : has
  CAMP ||--o{ CALENDAR : has
  CAMP ||--o{ CAMP_CLASS : has
  CAMP ||--o{ STATION : has
  CAMP ||--o{ TEAM : has
  TEAM |o--o{ CAMP_MEMBERSHIP : "staffed by"
  CAMP_CLASS |o--o{ TEAM : "served by"
  STATION |o--o{ TEAM : "staffed by"
  CALENDAR ||--o{ TIME_BLOCK : contains
  LEADER |o--o{ TIME_BLOCK : "responsible for"
  TIME_BLOCK ||--o{ RESOURCE : links
  TIME_BLOCK ||--o{ BLOCK_ASSIGNMENT : schedules
  CAMP_CLASS ||--o{ BLOCK_ASSIGNMENT : placed
  STATION ||--o{ BLOCK_ASSIGNMENT : hosts
  TIME_BLOCK ||--o{ LEADER_OVERRIDE : exceptions
  LEADER ||--o{ LEADER_OVERRIDE : moved
  STATION ||--o{ LEADER_OVERRIDE : destination
  CAMP_CLASS ||--o{ POINT_EVENT : earns
  LEADER ||--o{ POINT_EVENT : awards

  LEADER {
    bigint id PK
    text full_name
  }
  ACCOUNT {
    bigint id PK
    bigint leader_id FK
    text google_sub UK
  }
  CAMP {
    bigint id PK
    text name
    text join_code UK
    date start_date
    date end_date
    text timezone
    text status
  }
  CAMP_MEMBERSHIP {
    bigint camp_id PK
    bigint leader_id PK
    text role
    bigint team_id FK
  }
  TEAM {
    bigint id PK
    bigint camp_id FK
    text name
    bigint class_id FK
    bigint station_id FK
  }
  CAMP_CLASS {
    bigint id PK
    bigint camp_id FK
    text name
  }
  STATION {
    bigint id PK
    bigint camp_id FK
    text name
  }
  CALENDAR {
    bigint id PK
    bigint camp_id FK
    text name
  }
  TIME_BLOCK {
    bigint id PK
    bigint calendar_id FK
    text title
    timestamptz starts_at
    timestamptz ends_at
    text description
    bigint responsible_leader_id FK
  }
  RESOURCE {
    bigint id PK
    bigint time_block_id FK
    text kind
    text label
    text url
  }
  BLOCK_ASSIGNMENT {
    bigint time_block_id PK
    bigint class_id PK
    bigint station_id FK
  }
  LEADER_OVERRIDE {
    bigint time_block_id PK
    bigint leader_id PK
    bigint station_id FK
    text note
  }
  POINT_EVENT {
    bigint id PK
    bigint class_id FK
    bigint awarded_by FK
    bigint time_block_id FK
    int amount
    text reason
    timestamptz created_at
  }
```