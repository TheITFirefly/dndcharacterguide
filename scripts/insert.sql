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

INSERT INTO Characters (Name, Strength_Ability_Score, Dexterity_Ability_Score, Constitution_Ability_Score, Intelligence_Ability_Score, Wisdom_Ability_Score, Charisma_Ability_Score, Proficiency_bonus, username, BackgroundID, RaceID, ClassID)
VALUES ('Larry', 14, 15, 17, 55, 67, 1, 5, 'larry_bird', 1, 1, 1);

INSERT INTO Skills (Name, Modifier, Proficiency, ID)
VALUES ('Acrobatics', 8, True, 2);

INSERT INTO Saving_Throws (Name, Modifier, Proficiency, ID)
VALUES ('My Saving Throw', 6, False, 14);
