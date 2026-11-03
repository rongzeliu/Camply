\set VERBOSITY terse


\warn '-- Test 1: a camp that begins and ends on the same day' 
-- Expected: INSERT 0 1 
INSERT INTO camp (name, join_code, start_date, end_date) VALUES ('pass_camp1', 'pass_code1', '2027-07-07', '2027-07-07');

\warn '-- Test 2: a timeblock that starts and ends at the same time'
-- Expected: INSERT 0 1 
INSERT INTO camp (name, join_code, start_date, end_date) 
    VALUES ('T2_camp', 'T2', '2027-07-01', '2027-07-07');
INSERT INTO calendar (camp_id, name) 
    SELECT id, 'T2_calendar' FROM camp WHERE join_code = 'T2'; 
INSERT INTO time_block (calendar_id, title, starts_at, ends_at) 
    SELECT id, 'pass_block1', '2027-07-01 09:00-04', '2027-07-01 09:00-04' FROM calendar WHERE name = 'T2_calendar'; 