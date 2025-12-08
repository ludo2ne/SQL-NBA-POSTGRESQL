-- Connect to the database

CREATE TABLE nba.team (
	full_name text NULL,
	abbreviation text NULL,
	nickname text NULL,
	city text NULL,
	state text NULL,
	year_founded float4 NULL,
	id int4 NULL,
	conference varchar(10) NULL
);

INSERT INTO nba.team (full_name,abbreviation,nickname,city,state,year_founded,id,conference) VALUES
	 ('Atlanta Hawks','ATL','Hawks','Atlanta','Georgia',1949.0,1610612737,'East'),
	 ('Boston Celtics','BOS','Celtics','Boston','Massachusetts',1946.0,1610612738,'East'),
	 ('Cleveland Cavaliers','CLE','Cavaliers','Cleveland','Ohio',1970.0,1610612739,'East'),
	 ('New Orleans Pelicans','NOP','Pelicans','New Orleans','Louisiana',2002.0,1610612740,'West'),
	 ('Chicago Bulls','CHI','Bulls','Chicago','Illinois',1966.0,1610612741,'East'),
	 ('Dallas Mavericks','DAL','Mavericks','Dallas','Texas',1980.0,1610612742,'West'),
	 ('Denver Nuggets','DEN','Nuggets','Denver','Colorado',1976.0,1610612743,'West'),
	 ('Golden State Warriors','GSW','Warriors','Golden State','California',1946.0,1610612744,'West'),
	 ('Houston Rockets','HOU','Rockets','Houston','Texas',1967.0,1610612745,'West'),
	 ('Los Angeles Clippers','LAC','Clippers','Los Angeles','California',1970.0,1610612746,'West'),
	 ('Los Angeles Lakers','LAL','Lakers','Los Angeles','California',1948.0,1610612747,'West'),
	 ('Miami Heat','MIA','Heat','Miami','Florida',1988.0,1610612748,'East'),
	 ('Milwaukee Bucks','MIL','Bucks','Milwaukee','Wisconsin',1968.0,1610612749,'East'),
	 ('Minnesota Timberwolves','MIN','Timberwolves','Minnesota','Minnesota',1989.0,1610612750,'West'),
	 ('Brooklyn Nets','BKN','Nets','Brooklyn','New York',1976.0,1610612751,'East'),
	 ('New York Knicks','NYK','Knicks','New York','New York',1946.0,1610612752,'East'),
	 ('Orlando Magic','ORL','Magic','Orlando','Florida',1989.0,1610612753,'East'),
	 ('Indiana Pacers','IND','Pacers','Indiana','Indiana',1976.0,1610612754,'East'),
	 ('Philadelphia 76ers','PHI','76ers','Philadelphia','Pennsylvania',1949.0,1610612755,'East'),
	 ('Phoenix Suns','PHX','Suns','Phoenix','Arizona',1968.0,1610612756,'West'),
	 ('Portland Trail Blazers','POR','Trail Blazers','Portland','Oregon',1970.0,1610612757,'West'),
	 ('Sacramento Kings','SAC','Kings','Sacramento','California',1948.0,1610612758,'West'),
	 ('San Antonio Spurs','SAS','Spurs','San Antonio','Texas',1976.0,1610612759,'West'),
	 ('Oklahoma City Thunder','OKC','Thunder','Oklahoma City','Oklahoma',1967.0,1610612760,'West'),
	 ('Toronto Raptors','TOR','Raptors','Toronto','Ontario',1995.0,1610612761,'East'),
	 ('Utah Jazz','UTA','Jazz','Utah','Utah',1974.0,1610612762,'West'),
	 ('Memphis Grizzlies','MEM','Grizzlies','Memphis','Tennessee',1995.0,1610612763,'West'),
	 ('Washington Wizards','WAS','Wizards','Washington','District of Columbia',1961.0,1610612764,'East'),
	 ('Detroit Pistons','DET','Pistons','Detroit','Michigan',1948.0,1610612765,'East'),
	 ('Charlotte Hornets','CHA','Hornets','Charlotte','North Carolina',1988.0,1610612766,'East');

ALTER TABLE nba.player_stat_match
DROP COLUMN IF EXISTS teamcity,
DROP COLUMN IF EXISTS teamname,
DROP COLUMN IF EXISTS teamtricode,
DROP COLUMN IF EXISTS teamslug,
DROP COLUMN IF EXISTS firstname,
DROP COLUMN IF EXISTS familyname,
DROP COLUMN IF EXISTS namei,
DROP COLUMN IF EXISTS playerslug;

ALTER TABLE nba.regular_season_stat
DROP COLUMN IF EXISTS player_name,
DROP COLUMN IF EXISTS nickname,
DROP COLUMN IF EXISTS team_abbreviation,
DROP COLUMN IF EXISTS age;

ALTER TABLE nba.game
DROP COLUMN IF EXISTS team_abbreviation,
DROP COLUMN IF EXISTS team_name;

ALTER TABLE nba.team
DROP COLUMN IF EXISTS team_city,
DROP COLUMN IF EXISTS team_name,
DROP COLUMN IF EXISTS team_abbreviation,
DROP COLUMN IF EXISTS team_code,
DROP COLUMN IF EXISTS team_slug;
