-- Test 1: a camp must have a join code
-- Expected: ERROR ... null value in column "join_code" ... violates not-null constraint
INSERT INTO camp (name) VALUES ('no code');

-- Test 2: join_code differs between camps 
-- Expected : ERROR ... duplicate key value violates unique constraint "camp_join_code_key"
INSERT INTO camp (name, join_code, start_date, end_date) VALUES ('camp1', 'code1', '2027-07-01', '2027-07-07'); -- succeed
INSERT INTO camp (name, join_code, start_date, end_date) VALUES ('camp2', 'code1', '2027-07-01', '2027-07-07'); -- fail 