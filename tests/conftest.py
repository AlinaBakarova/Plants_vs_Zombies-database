import pytest
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Конфигурация тестовой БД
TEST_DB_NAME = "plants_vs_zombies_test"
DB_USER = "postgres"
DB_PASSWORD = "postgres"  # В реальном проекте используйте переменные окружения
DB_HOST = "localhost"
DB_PORT = "5432"

@pytest.fixture(scope="session")
def db_connection():
    """Фикстура для создания тестовой БД и подключения к ней"""
    
    # Подключаемся к серверу PostgreSQL без конкретной БД
    conn = psycopg2.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    # Пытаемся создать тестовую БД (игнорируем ошибку если она уже существует)
    try:
        cursor.execute(f"CREATE DATABASE {TEST_DB_NAME};")
    except psycopg2.errors.DuplicateDatabase:
        pass
    
    cursor.close()
    conn.close()
    
    # Подключаемся к тестовой БД
    test_conn = psycopg2.connect(
        dbname=TEST_DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    
    # Инициализируем тестовые данные
    _initialize_test_data(test_conn)
    
    yield test_conn
    
    # После завершения тестов закрываем соединение
    test_conn.close()
    
    # Удаляем тестовую БД (опционально, можно закомментировать для отладки)
    clean_conn = psycopg2.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    clean_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = clean_conn.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS {TEST_DB_NAME};")
    cursor.close()
    clean_conn.close()

def _initialize_test_data(conn):
    """Инициализация тестовых данных в БД"""
    cursor = conn.cursor()
    
    # Создаем типы
    cursor.execute("""
    DROP TYPE IF EXISTS complexity_type2 CASCADE;
    DROP TYPE IF EXISTS type_state CASCADE;
    DROP TYPE IF EXISTS damage_state CASCADE;
    DROP TYPE IF EXISTS recharge_type CASCADE;
    DROP TYPE IF EXISTS condition_type_enum CASCADE;
    DROP TYPE IF EXISTS toughness_type CASCADE;
    DROP TYPE IF EXISTS speed_type CASCADE;
    
    CREATE TYPE complexity_type2 AS ENUM('Easy', 'Normal', 'Difficult');
    CREATE TYPE type_state AS ENUM('Attacker', 'Defender', 'Support', 'Special');
    CREATE TYPE damage_state AS ENUM('Normal', 'Massive', 'Heavy');
    CREATE TYPE recharge_type AS ENUM('Fast', 'Slow', 'Very slow');
    CREATE TYPE condition_type_enum AS ENUM('KillCount', 'PlantCount', 'LevelComplete', 'Special');
    CREATE TYPE toughness_type AS ENUM('Low', 'Medium', 'High', 'Colossal');
    CREATE TYPE speed_type AS ENUM('Normal', 'Fast', 'Normal_then_fast');
    """)
    
    # Создаем таблицы
    cursor.execute("""
    DROP TABLE IF EXISTS Achievements CASCADE;
    DROP TABLE IF EXISTS Levels CASCADE;
    DROP TABLE IF EXISTS Wave_Zombies CASCADE;
    DROP TABLE IF EXISTS Plants CASCADE;
    DROP TABLE IF EXISTS Zombies CASCADE;
    DROP TABLE IF EXISTS Location CASCADE;
    
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
    """)
    
    # Вставляем тестовые данные
    cursor.execute("""
    INSERT INTO Location (location_id, location_name, complexity, number_of_levels) VALUES
    (1, 'Day', 'Easy', 10),
    (2, 'Night', 'Normal', 10),
    (3, 'Pool', 'Normal', 5),
    (4, 'Fog', 'Difficult', 8),
    (5, 'Roof', 'Difficult', 8);
    """)
    
    cursor.execute("""
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
    """)
    
    cursor.execute("""
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
    """)
    
    cursor.execute("""
    INSERT INTO Wave_Zombies (wave_id, zombie_id, group_size, start_time, is_final_wave) VALUES
    (1, 1, 5, 30, FALSE),
    (2, 4, 3, 60, FALSE),
    (3, 2, 4, 90, FALSE),
    (4, 9, 6, 120, FALSE),
    (5, 5, 3, 150, FALSE),
    (6, 1, 8, 180, FALSE),
    (7, 3, 2, 210, FALSE),
    (8, 10, 4, 240, FALSE),
    (9, 6, 3, 270, FALSE),
    (10, 8, 5, 300, TRUE),
    (11, 15, 4, 45, FALSE),
    (12, 16, 3, 90, FALSE),
    (13, 19, 2, 135, FALSE),
    (14, 12, 3, 180, FALSE),
    (15, 14, 5, 225, FALSE),
    (16, 24, 4, 270, FALSE),
    (17, 25, 3, 315, FALSE),
    (18, 26, 2, 360, FALSE),
    (19, 27, 3, 405, FALSE),
    (20, 30, 5, 450, TRUE),
    (21, 7, 1, 60, FALSE),
    (22, 11, 1, 120, FALSE),
    (23, 17, 1, 180, FALSE),
    (24, 21, 1, 240, FALSE),
    (25, 28, 1, 300, FALSE),
    (26, 20, 2, 360, FALSE),
    (27, 22, 6, 420, FALSE),
    (28, 18, 4, 480, FALSE),
    (29, 13, 5, 540, FALSE),
    (30, 23, 1, 600, TRUE);
    """)
    
    cursor.execute("""
    INSERT INTO Levels (level_id, level_number, location_id, wave_id, plant_id, time_limit) VALUES
    (1, 1, 1, 1, 1, 300),
    (2, 2, 1, 2, 2, 300),
    (3, 3, 1, 3, 4, 350),
    (4, 4, 1, 4, 5, 350),
    (5, 5, 1, 5, 6, 400),
    (6, 6, 1, 6, 8, 400),
    (7, 7, 1, 7, 9, 450),
    (8, 8, 1, 8, 11, 450),
    (9, 9, 1, 9, 14, 500),
    (10, 10, 1, 10, 16, 500),
    (11, 1, 2, 11, 10, 350),
    (12, 2, 2, 12, 12, 350),
    (13, 3, 2, 13, 13, 400),
    (14, 4, 2, 14, 15, 400),
    (15, 5, 2, 15, 17, 450),
    (16, 6, 2, 16, 18, 450),
    (17, 7, 2, 17, 19, 500),
    (18, 8, 2, 18, 21, 500),
    (19, 9, 2, 19, 22, 550),
    (20, 10, 2, 20, 23, 550),
    (21, 1, 3, 21, 24, 400),
    (22, 2, 3, 22, 25, 400),
    (23, 3, 3, 23, 26, 450),
    (24, 4, 3, 24, 28, 450),
    (25, 5, 3, 25, 29, 500),
    (26, 1, 4, 26, 27, 450),
    (27, 2, 4, 27, 3, 450),
    (28, 3, 4, 28, 7, 500),
    (29, 4, 4, 29, 20, 500),
    (30, 5, 4, 30, 30, 550);
    """)
    
    cursor.execute("""
    INSERT INTO Achievements (achievement_id, achievement_name, location_id, reward_coins, reward_gems, condition_type) VALUES
    (1, 'Sunny Days', 1, 500, 5, 'LevelComplete'),
    (2, 'Pea Shooter Pro', 1, 300, 3, 'KillCount'),
    (3, 'Wall-nut Defender', 1, 400, 4, 'PlantCount'),
    (4, 'Potato Mine Expert', 1, 350, 3, 'Special'),
    (5, 'Snow Patrol', 1, 450, 5, 'KillCount'),
    (6, 'Night Owl', 2, 600, 6, 'LevelComplete'),
    (7, 'Fungal Power', 2, 400, 4, 'PlantCount'),
    (8, 'Grave Danger', 2, 500, 5, 'Special'),
    (9, 'Hypno Master', 2, 550, 5, 'KillCount'),
    (10, 'Plantern Light', 2, 450, 4, 'Special'),
    (11, 'Pool Party', 3, 700, 7, 'LevelComplete'),
    (12, 'Lily Padder', 3, 500, 5, 'PlantCount'),
    (13, 'Winter is Coming', 3, 800, 8, 'Special'),
    (14, 'Kernel Collector', 3, 600, 6, 'KillCount'),
    (15, 'Cob Commander', 3, 750, 7, 'Special'),
    (16, 'Fog Buster', 4, 900, 9, 'LevelComplete'),
    (17, 'Umbrella Protector', 4, 650, 6, 'PlantCount'),
    (18, 'Imitater Pro', 4, 800, 8, 'Special'),
    (19, 'Chomper Champ', 4, 700, 7, 'KillCount'),
    (20, 'Threepeater Ace', 4, 850, 8, 'Special'),
    (21, 'Roof Raider', 5, 1000, 10, 'LevelComplete'),
    (22, 'Flower Pot Pro', 5, 750, 7, 'PlantCount'),
    (23, 'Gold Collector', 5, 900, 9, 'Special'),
    (24, 'Gatling Guru', 5, 800, 8, 'KillCount'),
    (25, 'Gloom Master', 5, 950, 9, 'Special'),
    (26, 'Zombie Slayer', NULL, 2000, 20, 'KillCount'),
    (27, 'Plant Collector', NULL, 1500, 15, 'PlantCount'),
    (28, 'Perfect Gardener', NULL, 2500, 25, 'Special'),
    (29, 'Speed Runner', NULL, 1800, 18, 'LevelComplete'),
    (30, 'Ultimate Defender', NULL, 3000, 30, 'Special');
    """)
    
    conn.commit()
    cursor.close()

@pytest.fixture
def db_cursor(db_connection):
    """Фикстура для создания курсора к тестовой БД"""
    cursor = db_connection.cursor()
    yield cursor
    cursor.close()
