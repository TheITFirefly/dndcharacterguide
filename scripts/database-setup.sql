CREATE TABLE Party
(
  ID SERIAL,
  Name VARCHAR(50) NOT NULL,
  PRIMARY KEY (ID)
);
CREATE TABLE Race
(
  RaceName VARCHAR(50) NOT NULL,
  Page_Number INT NOT NULL,
  RaceID SERIAL,
  PRIMARY KEY (RaceID),
  UNIQUE (RaceName)
);
CREATE TABLE Class
(
  ClassName VARCHAR(50) NOT NULL,
  Page_Number INT NOT NULL,
  ClassID SERIAL,
  PRIMARY KEY (ClassID),
  UNIQUE (ClassName)
);
CREATE TABLE Background
(
  BackgroundName VARCHAR(50) NOT NULL,
  Page_Number INT NOT NULL,
  BackgroundID SERIAL,
  PRIMARY KEY (BackgroundID),
  UNIQUE (BackgroundName)
);
CREATE TABLE Users
(
  username VARCHAR(25) NOT NULL,
  password VARCHAR(32) NOT NULL,
  ID BIGINT UNSIGNED,
  PRIMARY KEY (username),
  FOREIGN KEY (ID) REFERENCES Party(ID)
);
CREATE TABLE Characters
(
  ID SERIAL,
  CharacterName VARCHAR(50) NOT NULL,
  Strength_Ability_Score INT NOT NULL,
  Dexterity_Ability_Score INT NOT NULL,
  Constitution_Ability_Score INT NOT NULL,
  Intelligence_Ability_Score INT NOT NULL,
  Wisdom_Ability_Score INT NOT NULL,
  Charisma_Ability_Score INT NOT NULL,
  Proficiency_bonus INT NOT NULL,
  username VARCHAR(25) NOT NULL,
  BackgroundID BIGINT UNSIGNED NULL,
  RaceID BIGINT UNSIGNED NOT NULL,
  ClassID BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (ID),
  FOREIGN KEY (username) REFERENCES Users(username),
  FOREIGN KEY (BackgroundID) REFERENCES Background(BackgroundID),
  FOREIGN KEY (RaceID) REFERENCES Race(RaceID),
  FOREIGN KEY (ClassID) REFERENCES Class(ClassID)
);
CREATE TABLE Skills
(
  SkillName VARCHAR(50) NOT NULL,
  Modifier INT NOT NULL,
  Proficiency BOOL NOT NULL,
  ID BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (SkillName, ID),
  FOREIGN KEY (ID) REFERENCES Characters(ID) ON DELETE CASCADE
);
CREATE TABLE Saving_Throws
(
  Saving_ThrowName VARCHAR(50) NOT NULL,
  Modifier INT NOT NULL,
  Proficiency BOOL NOT NULL,
  ID BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (Saving_ThrowName, ID),
  FOREIGN KEY (ID) REFERENCES Characters(ID) ON DELETE CASCADE
);
CREATE VIEW CharacterDetails AS
SELECT * FROM Characters c
JOIN Race r ON c.RaceID = r.RaceID
JOIN Background b ON c.BackgroundID = b.BackgroundID
JOIN Class cl ON c.ClassID = cl.ClassID
JOIN Skills s ON c.ID = s.ID
JOIN Saving_Throws st ON c.ID = st.ID
GROUP BY c.username;