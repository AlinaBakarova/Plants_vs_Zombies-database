DELETE FROM Location;
DELETE FROM Plants;
DELETE FROM Zombies;


INSERT INTO Location (location_id, location_name, complexity, number_of_levels) VALUES
(1, 'Day', 'Easy', 10),
(2, 'Night', 'Normal', 10),
(3, 'Pool', 'Normal', 5),
(4, 'Fog', 'Difficult', 8),
(5, 'Roof', 'Difficult', 8);

INSERT INTO Plants (plant_id, plant_name, plant_type, damage, recharge, plant_cost, unlock_level) VALUES
(1, 'Peashooter', 'Attacker', 'Normal', 'Fast', 100, 1),
(2, 'Sunflower', 'Support', Null, 'Fast', 50, 1),
(3, 'Cherry Bomb', 'Special', 'Massive', 'Very slow', 150, 1),
(4, 'Wall-nut', 'Defender', Null, 'Slow', 50, 1),
(5, 'Potato Mine', 'Special', 'Massive', 'Slow', 25, 1),
(6, 'Snow pea', 'Attacker', 'Normal', 'Fast', 175, 1),
(7, 'Chomper', 'Special', 'Massive', 'Fast', 150, 1),
(8, 'Repeater', 'Attacker', 'Normal', 'Fast', 200, 1),
(9, 'Puff-shroom', 'Attacker', 'Normal', 'Fast', 0, 1),
(10, 'Sun-shroom', 'Defender', Null, 'Fast', 25, 1),
(11, 'Fume-shroom', 'Attacker', 'Normal', 'Fast', 75, 1),
(12, 'Grave Buster', 'Special', Null, 'Fast', 75, 1),
(13, 'Hypno-shroom', 'Special', Null, 'Slow', 75, 1),
(14, 'Lily pad', 'Support', Null, 'Fast', 25, 1),
(15, 'Plantern', 'Support', Null, 'Slow', 25, 1),
(16, 'Melon-pult', 'Attacker', 'Heavy', 'Fast', 300, 5),
(17, 'Spikerock', 'Defender', 'Massive', 'Very slow', 125, 5),
(18, 'Doom-shroom', 'Special', 'Massive', 'Very slow', 125, 5),
(19, 'Tall-nut', 'Defender', Null, 'Slow', 125, 5),
(20, 'Threepeater', 'Attacker', 'Normal', 'Fast', 325, 5),
(21, 'Flower-pot', 'Support', Null, 'Fast', 25, 5),
(22, 'Umbrella-leaf', 'Defender', Null, 'Fast', 100, 5),
(23, 'Cattail', 'Attacker', 'Normal', 'Fast', 225, 5),
(24, 'Kernel-pult', 'Attacker', 'Heavy', 'Fast', 100, 5),
(25, 'Winter Melon', 'Attacker', 'Massive', 'Slow', 500, 5),
(26, 'Cob Cannon', 'Attacker', 'Massive', 'Very slow', 700, 5),
(27, 'Imitater', 'Special', NULL, 'Very slow', 30, 5),
(28, 'Gatling Pea', 'Attacker', 'Heavy', 'Fast', 450, 5),
(29, 'Gloom-shroom', 'Attacker', 'Normal', 'Fast', 150, 5),
(30, 'Gold Magnet', 'Support', NULL, 'Fast', 50, 5);

INSERT INTO zombies (zombie_id, zombie_name, toughness, speed) VALUES
(1, 'Basic Zombie', 'Medium', 'Normal'),
(2, 'Conehead Zombie', 'High', 'Normal'),
(3, 'Buckethead Zombie', 'High', 'Normal'),
(4, 'Flag Zombie', 'Medium', 'Normal'),
(5, 'Newspaper Zombie', 'Medium', 'Normal_then_fast'),
(6, 'Screen Door Zombie', 'High', 'Normal'),
(7, 'Football Zombie', 'Colossal', 'Fast'),
(8, 'Dancing Zombie', 'Medium', 'Normal'),
(9, 'Backup Dancer', 'Low', 'Fast'),
(10, 'Snorkel Zombie', 'Medium', 'Normal'),
(11, 'Zomboni', 'Colossal', 'Normal'),
(12, 'Dolphin Rider Zombie', 'Medium', 'Fast'),
(13, 'Jack-in-the-Box Zombie', 'Low', 'Fast'),
(14, 'Balloon Zombie', 'Low', 'Fast'),
(15, 'Digger Zombie', 'Medium', 'Fast'),
(16, 'Pogo Zombie', 'Medium', 'Fast'),
(17, 'Zombie Yeti', 'Colossal', 'Normal'),
(18, 'Bungee Zombie', 'Low', 'Fast'),
(19, 'Ladder Zombie', 'High', 'Normal'),
(20, 'Catapult Zombie', 'High', 'Normal'),
(21, 'Gargantuar', 'Colossal', 'Normal'),
(22, 'Imp', 'Low', 'Fast'),
(23, 'Dr. Zomboss', 'Colossal', 'Normal'),
(24, 'Peasant Zombie', 'Medium', 'Normal'),
(25, 'Jester Zombie', 'Medium', 'Normal'),
(26, 'Wizard Zombie', 'Medium', 'Normal'),
(27, 'Ra Zombie', 'High', 'Normal'),
(28, 'Ankylosaurus Zombie', 'Colossal', 'Normal'),
(29, 'Camel Zombie', 'High', 'Normal'),
(30, 'Explorer Zombie', 'Medium', 'Normal');

INSERT INTO Wave_Zombies (wave_id, zombie_id, group_size, start_time, is_final_wave) VALUES
-- Первые 10 волн (ранние, простые)
(1, 1, 5, 30, FALSE),  -- Basic Zombie
(2, 4, 3, 60, FALSE),  -- Flag Zombie
(3, 2, 4, 90, FALSE),  -- Conehead Zombie
(4, 9, 6, 120, FALSE), -- Backup Dancer
(5, 5, 3, 150, FALSE), -- Newspaper Zombie
(6, 1, 8, 180, FALSE), -- Basic Zombie
(7, 3, 2, 210, FALSE), -- Buckethead Zombie
(8, 10, 4, 240, FALSE), -- Snorkel Zombie
(9, 6, 3, 270, FALSE), -- Screen Door Zombie
(10, 8, 5, 300, TRUE),  -- Dancing Zombie (первая финальная волна)

-- Средние волны (11-20)
(11, 15, 4, 45, FALSE), -- Digger Zombie
(12, 16, 3, 90, FALSE), -- Pogo Zombie
(13, 19, 2, 135, FALSE), -- Ladder Zombie
(14, 12, 3, 180, FALSE), -- Dolphin Rider Zombie
(15, 14, 5, 225, FALSE), -- Balloon Zombie
(16, 24, 4, 270, FALSE), -- Peasant Zombie
(17, 25, 3, 315, FALSE), -- Jester Zombie
(18, 26, 2, 360, FALSE), -- Wizard Zombie
(19, 27, 3, 405, FALSE), -- Ra Zombie
(20, 30, 5, 450, TRUE),  -- Explorer Zombie (финальная волна)

-- Сложные волны (21-30)
(21, 7, 1, 60, FALSE),  -- Football Zombie (колоссальный)
(22, 11, 1, 120, FALSE), -- Zomboni (колоссальный)
(23, 17, 1, 180, FALSE), -- Zombie Yeti (колоссальный)
(24, 21, 1, 240, FALSE), -- Gargantuar (колоссальный)
(25, 28, 1, 300, FALSE), -- Ankylosaurus Zombie (колоссальный)
(26, 20, 2, 360, FALSE), -- Catapult Zombie
(27, 22, 6, 420, FALSE), -- Imp
(28, 18, 4, 480, FALSE), -- Bungee Zombie
(29, 13, 5, 540, FALSE), -- Jack-in-the-Box Zombie
(30, 23, 1, 600, TRUE);  -- Dr. Zomboss (финальный босс)

INSERT INTO Level (level_id, level_number, location_id, wave_id, plant_id, time_limit) VALUES
-- Дневные уровни (1-10)
(1, 1, 1, 1, 1, 300),  -- Открывает Peashooter
(2, 2, 1, 2, 2, 300),  -- Открывает Sunflower
(3, 3, 1, 3, 4, 350),  -- Открывает Wall-nut
(4, 4, 1, 4, 5, 350),  -- Открывает Potato Mine
(5, 5, 1, 5, 6, 400),  -- Открывает Snow pea
(6, 6, 1, 6, 8, 400),  -- Открывает Repeater
(7, 7, 1, 7, 9, 450),  -- Открывает Puff-shroom
(8, 8, 1, 8, 11, 450), -- Открывает Fume-shroom
(9, 9, 1, 9, 14, 500), -- Открывает Lily pad
(10, 10, 1, 10, 16, 500), -- Открывает Melon-pult

-- Ночные уровни (11-20)
(11, 1, 2, 11, 10, 350), -- Открывает Sun-shroom
(12, 2, 2, 12, 12, 350), -- Открывает Grave Buster
(13, 3, 2, 13, 13, 400), -- Открывает Hypno-shroom
(14, 4, 2, 14, 15, 400), -- Открывает Plantern
(15, 5, 2, 15, 17, 450), -- Открывает Spikerock
(16, 6, 2, 16, 18, 450), -- Открывает Doom-shroom
(17, 7, 2, 17, 19, 500), -- Открывает Tall-nut
(18, 8, 2, 18, 21, 500), -- Открывает Flower-pot
(19, 9, 2, 19, 22, 550), -- Открывает Umbrella-leaf
(20, 10, 2, 20, 23, 550), -- Открывает Cattail

-- Уровни с бассейном (21-25)
(21, 1, 3, 21, 24, 400), -- Открывает Kernel-pult
(22, 2, 3, 22, 25, 400), -- Открывает Winter Melon
(23, 3, 3, 23, 26, 450), -- Открывает Cob Cannon
(24, 4, 3, 24, 28, 450), -- Открывает Gatling Pea
(25, 5, 3, 25, 29, 500), -- Открывает Gloom-shroom

-- Уровни с туманом (26-30)
(26, 1, 4, 26, 27, 450), -- Открывает Imitater
(27, 2, 4, 27, 3, 450),  -- Открывает Cherry Bomb
(28, 3, 4, 28, 7, 500),  -- Открывает Chomper
(29, 4, 4, 29, 20, 500), -- Открывает Threepeater
(30, 5, 4, 30, 30, 550); -- Открывает Gold Magnet

INSERT INTO Achievements (achievement_id, achievement_name, location_id, reward_coins, reward_gems, condition_type) VALUES
-- Достижения для дневных уровней (location_id = 1)
(1, 'Sunny Days', 1, 500, 5, 'LevelComplete'),
(2, 'Pea Shooter Pro', 1, 300, 3, 'KillCount'),
(3, 'Wall-nut Defender', 1, 400, 4, 'PlantCount'),
(4, 'Potato Mine Expert', 1, 350, 3, 'Special'),
(5, 'Snow Patrol', 1, 450, 5, 'KillCount'),

-- Достижения для ночных уровней (location_id = 2)
(6, 'Night Owl', 2, 600, 6, 'LevelComplete'),
(7, 'Fungal Power', 2, 400, 4, 'PlantCount'),
(8, 'Grave Danger', 2, 500, 5, 'Special'),
(9, 'Hypno Master', 2, 550, 5, 'KillCount'),
(10, 'Plantern Light', 2, 450, 4, 'Special'),

-- Достижения для бассейна (location_id = 3)
(11, 'Pool Party', 3, 700, 7, 'LevelComplete'),
(12, 'Lily Padder', 3, 500, 5, 'PlantCount'),
(13, 'Winter is Coming', 3, 800, 8, 'Special'),
(14, 'Kernel Collector', 3, 600, 6, 'KillCount'),
(15, 'Cob Commander', 3, 750, 7, 'Special'),

-- Достижения для туманных уровней (location_id = 4)
(16, 'Fog Buster', 4, 900, 9, 'LevelComplete'),
(17, 'Umbrella Protector', 4, 650, 6, 'PlantCount'),
(18, 'Imitater Pro', 4, 800, 8, 'Special'),
(19, 'Chomper Champ', 4, 700, 7, 'KillCount'),
(20, 'Threepeater Ace', 4, 850, 8, 'Special'),

-- Достижения для крыш (location_id = 5)
(21, 'Roof Raider', 5, 1000, 10, 'LevelComplete'),
(22, 'Flower Pot Pro', 5, 750, 7, 'PlantCount'),
(23, 'Gold Collector', 5, 900, 9, 'Special'),
(24, 'Gatling Guru', 5, 800, 8, 'KillCount'),
(25, 'Gloom Master', 5, 950, 9, 'Special'),

-- Общие достижения (location_id может быть NULL или 1-5)
(26, 'Zombie Slayer', NULL, 2000, 20, 'KillCount'),
(27, 'Plant Collector', NULL, 1500, 15, 'PlantCount'),
(28, 'Perfect Gardener', NULL, 2500, 25, 'Special'),
(29, 'Speed Runner', NULL, 1800, 18, 'LevelComplete'),
(30, 'Ultimate Defender', NULL, 3000, 30, 'Special');