-- Test: deleting a camp deletes its calendars
INSERT INTO camp (name, join_code, start_date, end_date)
  VALUES ('cascade1', 'CASCADE1', '2027-07-01', '2027-07-07');
INSERT INTO calendar (camp_id, name) VALUES (1, 'Main');

SELECT count(*) FROM calendar;   -- expect 1

DELETE FROM camp WHERE id = 1;

SELECT count(*) FROM calendar;   -- expect 0