-- Test 1: a camp must have a join code
-- Expected: ERROR ... null value in column "join_code" ... violates not-null constraint
INSERT INTO camp (name) VALUES ('no code'); 

-- Test 2: join_code differs between camps 
-- Expected: ERROR ... duplicate key value violates unique constraint "camp_join_code_key"
INSERT INTO camp (name, join_code, start_date, end_date) VALUES ('fail_camp2', 'code1', '2027-07-01', '2027-07-07'); -- succeed
INSERT INTO camp (name, join_code, start_date, end_date) VALUES ('fail_camp3', 'code1', '2027-07-01', '2027-07-07'); -- fail 

-- Test 3: camp cannot end before it has started 
-- Expected: ERROR ... new row ... violates check constraint "camp_date_ok"
INSERT INTO camp (name, join_code, start_date, end_date) VALUES ('fail_camp3', 'fail_code3', '2027-07-07', '2027-07-01'); 

-- Test 4: calendar must refer to a camp
-- Expected: ERROR ... insert or update on table "calendar" violates foreign key constraint "calendar_camp_id_fkey"
INSERT INTO calendar (camp_id, name) VALUES (0, 'dne_camp_calendar');