/**
 * CS482 Team Project Phase 1
 *
 * Create tables in database
 */

CREATE TABLE players (
    name        VARCHAR(64)             NOT NULL,
    playerID    INTEGER                 NOT NULL,
    teamName    VARCHAR(64),
        -- teamName could be null if player is between teams or a free agent
    position    ENUM('QB','RB','WR')    NOT NULL,
    touchdowns  INTEGER UNSIGNED        NOT NULL,
        -- UNSIGNED ensures no negative touchdowns
        -- NOT NULL because if player has no touchdowns it will just be '0'
    totalYards  INTEGER                 NOT NULL,
        -- apparently it is possible for a player to have negative yards in
        -- football, so this column is still signed
    salary      INTEGER UNSIGNED        NOT NULL,
        -- UNSIGNED ensures no negative salary

    PRIMARY KEY (playerID)
);

CREATE TABLE games (
    gameID          INTEGER             NOT NULL,
    date            DATE                NOT NULL,
    stadium         VARCHAR(64)         NOT NULL,
    result          ENUM('W','L','T'),
    attendance      INTEGER UNSIGNED,
    ticketRevenue   INTEGER UNSIGNED,
        -- result, attendance and ticketRevenue are all nullable because
        -- a game for a future date may be stored before it has been played
        -- attendance and ticketRevenue are UNSIGNED so that they cannot
        -- be negative

    PRIMARY KEY (gameID)
);

CREATE TABLE play (
    playerID    INTEGER NOT NULL,
    gameID      INTEGER NOT NULL,

    PRIMARY KEY (playerID, gameID),
    FOREIGN KEY (playerID)  REFERENCES players(playerID)
        ON DELETE CASCADE,
    FOREIGN KEY (gameID)    REFERENCES games(gameID)
        ON DELETE CASCADE

    -- We cascade as opposed to setting null because we do not want to have
    -- play entries with null values (because they would be useless at that
    -- point). Setting cascade means that deleting a player or game from
    -- their table will delete any corresponding entries in the play table.
);