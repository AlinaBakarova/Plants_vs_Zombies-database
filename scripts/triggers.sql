-- 1) триггер для проверки стоимости растения перед добавлением (не может быть отрицательной)
CREATE OR REPLACE FUNCTION check_plant_cost()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.plant_cost < 0 THEN
        RAISE EXCEPTION 'Стоимость растения не может быть отрицательной!';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_plant_cost_validation
BEFORE INSERT OR UPDATE ON Plants
FOR EACH ROW EXECUTE FUNCTION check_plant_cost();

-- 2) триггер для автоматического обновления сложности локации при добавлении сложных уровней
CREATE OR REPLACE FUNCTION update_location_complexity()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT COUNT(*) FROM Levels WHERE location_id = NEW.location_id) > 10 THEN
        UPDATE Location 
        SET complexity = 'Difficult' 
        WHERE location_id = NEW.location_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_location_complexity_update
AFTER INSERT ON Levels
FOR EACH ROW EXECUTE FUNCTION update_location_complexity();



-- 3) Триггер для проверки сложности уровня при добавлении колоссального зомби. 
-- На лёгких локациях не может быть колоссальных зомби
-- На нормальных - не больше 1
-- На сложных - не больше 3
CREATE OR REPLACE FUNCTION check_level_difficulty()
RETURNS TRIGGER AS $$
DECLARE
    location_complexity complexity_type2;
    colossal_zombies_count INT;
BEGIN

    SELECT complexity INTO location_complexity
    FROM Location
    WHERE location_id = (SELECT location_id FROM Levels WHERE level_id = NEW.level_id);
    

    SELECT COUNT(*) INTO colossal_zombies_count
    FROM Wave_Zombies wz
    JOIN Zombies z ON wz.zombie_id = z.zombie_id
    WHERE wz.wave_id = NEW.wave_id AND z.toughness = 'Colossal';
    
    IF (location_complexity = 'Easy' AND colossal_zombies_count > 0) OR
       (location_complexity = 'Normal' AND colossal_zombies_count > 1) OR
       (location_complexity = 'Difficult' AND colossal_zombies_count > 3) THEN
        RAISE EXCEPTION 'Нарушен баланс сложности! Локация: %, колоссальных зомби: %', 
                        location_complexity, colossal_zombies_count;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_level_difficulty_check
BEFORE INSERT OR UPDATE ON Levels
FOR EACH ROW EXECUTE FUNCTION check_level_difficulty();
