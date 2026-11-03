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