-- Test 1: a camp must have a join code
-- Expected: ERROR ... null value in column "join_code" ... violates not-null constraint
INSERT INTO camp (name) VALUES ('no code');