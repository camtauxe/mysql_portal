/**
 * CS482 Team Project Phase 1
 *
 * Insert entries into database
 */

SET SQL_SAFE_UPDATES = 0;

-- Clear database at the start
DELETE FROM players;
DELETE FROM games;
DELETE FROM play;

-- Insert players
--                          name       ID  teamName    postion     touchdowns  totalYards  salary
INSERT INTO players values  ('Cameron', 0,  'Team 9',   'QB',       0,          -100,       2500000);
INSERT INTO players values  ('Jared',   1,  'Team 9',   'RB',       150,        1430,       4534000);
INSERT INTO players values  ('Kathleen',2,  'Team 9',   'WR',       72,         843,        40000);
INSERT INTO players values  ('Todd',    3,  'Slugs',    'QB',       85,         920,        730000);
INSERT INTO players values  ('Jackie',  4,  'Platypi',  'RB',       124,        356,        12000000);

-- Insert games
--                         ID  Date            Stadium Name            Result  Attendance  TicketRevenue
INSERT INTO games values   (0, '1996-12-01',   'Slushie Czar Center',  'W',    743,        53020);
INSERT INTO games values   (1, '2018-10-31',   'Tony Pepperoni Arena', NULL,   NULL,       NULL);
    -- this game hasn't happened yet
INSERT INTO games values   (2, '2005-04-14',   'Todd''s Backyard',      'L',    6,          70);
INSERT INTO games values   (3, '2013-02-11',   'Tony Pepperoni Arena',  'T',    7500,       420600);
INSERT INTO games values   (5, '1874-11-20',   'Her Majesty''s Court',  'W',    540,        20);

-- Insert plays
--                        playerID    gameID
INSERT INTO play values   (0,         0);
INSERT INTO play values   (1,         0);
INSERT INTO play values   (2,         0);
INSERT INTO play values   (3,         0);
INSERT INTO play values   (0,         2);
INSERT INTO play values   (1,         2);
INSERT INTO play values   (2,         2);
INSERT INTO play values   (3,         2);
INSERT INTO play values   (0,         5);
INSERT INTO play values   (1,         5);
INSERT INTO play values   (2,         5);
INSERT INTO play values   (4,         5);
INSERT INTO play values   (0,         3);
INSERT INTO play values   (1,         3);
INSERT INTO play values   (2,         3);
INSERT INTO play values   (4,         3);