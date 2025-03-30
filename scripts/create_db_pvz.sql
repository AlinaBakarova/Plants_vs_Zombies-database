CREATE TYPE complexity_type2 AS ENUM('Easy', 'Normal', 'Difficult');
CREATE TYPE type_state AS ENUM('Attacker', 'Defender', 'Support', 'Special');
CREATE TYPE damage_state AS ENUM('Normal', 'Massive', 'Heavy');
CREATE TYPE recharge_type AS ENUM('Fast', 'Slow', 'Very slow');
CREATE TYPE condition_type_enum AS ENUM('KillCount', 'PlantCount', 'LevelComplete', 'Special');
CREATE TYPE toughness_type AS ENUM('Low', 'Medium', 'High', 'Colossal');
CREATE TYPE speed_type AS ENUM('Normal', 'Fast', 'Normal_then_fast');

CREATE TABLE Location (
    location_id INT PRIMARY KEY,
    location_name VARCHAR(50) NOT NULL,
    complexity complexity_type2 NOT NULL,
    number_of_levels INT NOT NULL
);

CREATE TABLE Zombies (
    zombie_id INT PRIMARY KEY,
    zombie_name VARCHAR(50) NOT NULL,
    toughness toughness_type NOT NULL,
    speed speed_type NOT NULL
);

CREATE TABLE Plants (
    plant_id INT PRIMARY KEY,
    plant_name VARCHAR(50) NOT NULL,
    plant_type type_state NOT NULL,
    damage damage_state,
    recharge recharge_type NOT NULL,
    plant_cost INT NOT NULL,
    unlock_level INT DEFAULT 1
);

CREATE TABLE Wave_Zombies (
    wave_id INT PRIMARY KEY,
    zombie_id INT NOT NULL,
    group_size INT DEFAULT 1,
    start_time INT NOT NULL,
    is_final_wave BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (zombie_id) REFERENCES Zombies(zombie_id)
);

CREATE TABLE Levels (
    level_id INT PRIMARY KEY,
    level_number INT NOT NULL,
    location_id INT NOT NULL,
    wave_id INT NOT NULL,
    plant_id INT NOT NULL,
    time_limit INT,
    FOREIGN KEY (location_id) REFERENCES Location(location_id),
    FOREIGN KEY (wave_id) REFERENCES Wave_Zombies(wave_id),
    FOREIGN KEY (plant_id) REFERENCES Plants(plant_id)
);

CREATE TABLE Achievements (
    achievement_id INT PRIMARY KEY,
    achievement_name VARCHAR(50) NOT NULL,
    location_id INT NOT NULL,
    reward_coins INT DEFAULT 0,
    reward_gems INT DEFAULT 0,
    condition_type condition_type_enum NOT NULL,
    FOREIGN KEY (location_id) REFERENCES Location(location_id)
);