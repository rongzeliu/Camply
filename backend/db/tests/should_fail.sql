-- Test 1: a camp must have a join code
-- Expected: ERROR ... null value in column "join_code" ... violates not-null constraint
INSERT INTO camp (name) VALUES ('no code');

-- Test 2: join_code differs between camps 
-- Expected : ERROR ... duplicate key value violates unique constraint "camp_join_code_key"
INSERT INTO camp (name, join_code) VALUES ('camp1', 'code1'); -- succeed
INSERT INTO camp (name, join_code) VALUES ('camp2', 'code1'); -- fail 