CREATE TABLE Party
(
  ID SERIAL,
  Name VARCHAR(50) NOT NULL,
  PRIMARY KEY (ID)
);

CREATE TABLE Race
(
  Name VARCHAR(50) NOT NULL,
  Page_Number INT NOT NULL,
  RaceID SERIAL,
  PRIMARY KEY (RaceID),
  UNIQUE (Name)
);

CREATE TABLE Class
(
  Name VARCHAR(50) NOT NULL,
  Page_Number INT NOT NULL,
  ClassID SERIAL,
  PRIMARY KEY (ClassID),
  UNIQUE (Name)
);

CREATE TABLE Background
(
  Name VARCHAR(50) NOT NULL,
  Page_Number INT NOT NULL,
  BackgroundID SERIAL,
  PRIMARY KEY (BackgroundID),
  UNIQUE (Name)
);

CREATE TABLE User
(
  username VARCHAR(25) NOT NULL,
  password VARCHAR(32) NOT NULL,
  ID BIGINT,
  PRIMARY KEY (username),
  FOREIGN KEY (ID) REFERENCES Party(ID)
);

CREATE TABLE Character
(
  ID SERIAL,
  Name VARCHAR(50) NOT NULL,
  Strength_Ability_Score INT NOT NULL,
  Dexterity_Ability_Score INT NOT NULL,
  Constitution_Ability_Score INT NOT NULL,
  Intelligence_Ability_Score INT NOT NULL,
  Wisdom_Ability_Score INT NOT NULL,
  Charisma_Ability_Score INT NOT NULL,
  Proficiency_bonus INT NOT NULL,
  username VARCHAR(25) NOT NULL,
  BackgroundID BIGINT NOT NULL,
  RaceID BIGINT NOT NULL,
  ClassID BIGINT NOT NULL,
  PRIMARY KEY (ID),
  FOREIGN KEY (username) REFERENCES User(username),
  FOREIGN KEY (BackgroundID) REFERENCES Background(BackgroundID),
  FOREIGN KEY (RaceID) REFERENCES Race(RaceID),
  FOREIGN KEY (ClassID) REFERENCES Class(ClassID)
);

CREATE TABLE Skills
(
  Name VARCHAR(50) NOT NULL,
  Modifier INT NOT NULL,
  Proficiency BOOL NOT NULL,
  ID BIGINT NOT NULL,
  PRIMARY KEY (Name, ID),
  FOREIGN KEY (ID) REFERENCES Character(ID)
);

CREATE TABLE Saving_Throws
(
  Name VARCHAR(50) NOT NULL,
  Modifier INT NOT NULL,
  Proficiency BOOL NOT NULL,
  ID BIGINT NOT NULL,
  PRIMARY KEY (Name, ID),
  FOREIGN KEY (ID) REFERENCES Character(ID)
);
