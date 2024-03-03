INSERT INTO Party (Name)
VALUES ('thisismyparty');

INSERT INTO Race (Name, Page_Number)
VALUES ('Elf', 37);

INSERT INTO Class (Name, Page_Number)
VALUES ('Paladin', 38);

INSERT INTO Background (Name, Page_Number)
VALUES ('Gambler', 39);

INSERT INTO Users (username, password)
VALUES ('larry_bird', 'replace_this_with_hash');

SET @BackgroundID = (SELECT BackgroundID FROM Background WHERE Name = 'Gambler');
SET @RaceID = (SELECT RaceID FROM Race WHERE Name = 'Elf');
SET @ClassID = (SELECT ClassID FROM Class WHERE Name = 'Paladin');

INSERT INTO Characters (Name, Strength_Ability_Score, Dexterity_Ability_Score, Constitution_Ability_Score, Intelligence_Ability_Score, Wisdom_Ability_Score, Charisma_Ability_Score, Proficiency_bonus, username, BackgroundID, RaceID, ClassID)
VALUES ('Larry', 14, 15, 17, 55, 67, 1, 5, 'larry_bird', @BackgroundID, @RaceID, @ClassID);

SET @CharacterID = (SELECT ID FROM Characters WHERE Name = 'Larry');
INSERT INTO Skills (Name, Modifier, Proficiency, ID)
VALUES ('Acrobatics', 8, True, @CharacterID);

INSERT INTO Saving_Throws (Name, Modifier, Proficiency, ID)
VALUES ('My Saving Throw', 6, False, @CharacterID);
