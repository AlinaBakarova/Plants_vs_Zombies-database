-- Процедура для добавления нового уровня
CREATE PROCEDURE add_level(
    IN p_level_number INT,
    IN p_location_id INT,
    IN p_wave_id INT,
    IN p_plant_id INT,
    IN p_time_limit INT
)
LANGUAGE SQL
AS $$
INSERT INTO Levels (level_number, location_id, wave_id, plant_id, time_limit)
VALUES (p_level_number, p_location_id, p_wave_id, p_plant_id, p_time_limit);
$$;

-- Функция для расчёта сложности уровня на основании зомби в волне
CREATE FUNCTION calculate_difficulty(wave_id INT) 
RETURNS VARCHAR(20)
LANGUAGE SQL
AS $$
DECLARE
    max_toughness VARCHAR(20);
BEGIN
    SELECT MAX(z.toughness) INTO max_toughness
    FROM Wave_Zombies wz
    JOIN Zombies z ON wz.zombie_id = z.zombie_id
    WHERE wz.wave_id = calculate_difficulty.wave_id;

    RETURN CASE
        WHEN max_toughness = 'Colossal' THEN 'Very Hard'
        WHEN max_toughness = 'High' THEN 'Hard'
        ELSE 'Normal'
    END;
END;
$$;

-- Процедура для обновления наград
CREATE PROCEDURE update_achievement_rewards(
    IN p_achievement_id INT,
    IN p_coins INT,
    IN p_gems INT
)
LANGUAGE SQL
AS $$
UPDATE Achievements
SET reward_coins = p_coins, reward_gems = p_gems
WHERE achievement_id = p_achievement_id;
$$;
