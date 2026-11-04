\set VERBOSITY terse


\warn '-- Test 1: a camp must have a join code'
-- Expected: ERROR ... null value in column "join_code" ... violates not-null constraint
INSERT INTO camp (name) 
    VALUES ('no code'); 


\warn '-- Test 2: join_code differs between camps'
-- Expected: ERROR ... duplicate key value violates unique constraint "camp_join_code_key"
INSERT INTO camp (name, join_code, start_date, end_date) 
    VALUES ('fail_camp2', 'code1', '2027-07-01', '2027-07-07'); -- succeed
INSERT INTO camp (name, join_code, start_date, end_date) 
    VALUES ('fail_camp3', 'code1', '2027-07-01', '2027-07-07'); -- fail 


\warn '-- Test 3: camp cannot end before it has started'
-- Expected: ERROR ... new row ... violates check constraint "camp_date_ok"
INSERT INTO camp (name, join_code, start_date, end_date) 
    VALUES ('fail_camp3', 'fail_code3', '2027-07-07', '2027-07-01'); 


\warn '-- Test 4: calendar must refer to a camp'
-- Expected: ERROR ... insert or update on table "calendar" violates foreign key constraint "calendar_camp_id_fkey"
INSERT INTO calendar (camp_id, name) 
    VALUES (0, 'dne_camp_calendar');


\warn '-- Test 5: time block cannot end before it has started'
-- Expected: ERROR ... new row ... violates check constraint "time_block_ok"
INSERT INTO camp (name, join_code, start_date, end_date) 
    VALUES ('T5_camp', 'T5', '2027-07-01', '2027-07-07');
INSERT INTO calendar (camp_id, name) 
    SELECT id, 'T5_calendar' FROM camp WHERE join_code = 'T5';
INSERT INTO time_block (calendar_id, title, starts_at, ends_at) 
    SELECT id, 'fail_block1', '2027-07-01 09:00-04', '2027-07-01 09:00-00' FROM calendar WHERE name = 'T5_calendar'; -- fail


\warn '-- Test 6: same leader joining same camp twice'
-- Expected: ERROR ... duplicate key value violates unique constraint "camp_membership_pkey"
INSERT INTO camp (name, join_code, start_date, end_date)
    VALUES ('T6_camp', 'T6', '2027-07-01', '2027-07-07');
INSERT INTO leader (full_name)
    VALUES ('T6_leader');
INSERT INTO camp_membership (camp_id, leader_id, role)
    SELECT camp.id, leader.id, 'leader' 
    FROM camp, leader 
    WHERE join_code = 'T6' AND full_name = 'T6_leader';
INSERT INTO camp_membership (camp_id, leader_id, role)
    SELECT camp.id, leader.id, 'leader' 
    FROM camp, leader 
    WHERE join_code = 'T6' AND full_name = 'T6_leader';


\warn '-- Test 7: camp membership with invalid role'
-- Expected: ERROR ... new row ... violates check constraint "camp_role_ok"
INSERT INTO camp (name, join_code, start_date, end_date)
    VALUES ('T7_camp', 'T7', '2027-07-01', '2027-07-07');
INSERT INTO leader (full_name)
    VALUES ('T7_leader');
INSERT INTO camp_membership (camp_id, leader_id, role)
    SELECT camp.id, leader.id, 'invalid_role' 
    FROM camp, leader 
    WHERE join_code = 'T7' AND full_name = 'T7_leader';


\warn '-- Test 8: team assigned to both station and class'
-- Expected ERROR ... new row ... violates check constraint "team_assignment_ok"
INSERT INTO camp (name, join_code, start_date, end_date)
    VALUES ('T8_camp', 'T8', '2027-07-01', '2027-07-07');
INSERT INTO team (camp_id, name, class_id, station_id)
    SELECT camp.id, 'Team8', 0, 0
    FROM camp WHERE join_code = 'T8';


\warn '-- Test 9: team assigned to neither station and class'
-- Expected ERROR ... new row ... violates check constraint "team_assignment_ok"
INSERT INTO camp (name, join_code, start_date, end_date)
    VALUES ('T9_camp', 'T9', '2027-07-01', '2027-07-07');
INSERT INTO team (camp_id, name)
    SELECT camp.id, 'Team9'
    FROM camp WHERE join_code = 'T9';