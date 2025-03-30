
--1. Найти все растения, которые можно открыть до 3 уровня
SELECT plant_id, plant_name, plant_type, unlock_level
FROM Plants
WHERE unlock_level <= 3
ORDER BY unlock_level, plant_name;

--2. Топ-5 самых долгих уровней

SELECT l.level_id, l.level_number, loc.location_name, l.time_limit
FROM Level l
JOIN Location loc ON l.location_id = loc.location_id
ORDER BY l.time_limit DESC
LIMIT 5;

--3. Вывести растения, которые разблокируются после прохожения уровней с зомби, прочности Colossal

SELECT p.plant_id, p.plant_name, p.plant_type
FROM Plants p
WHERE p.plant_id IN (
    SELECT l.plant_id
    FROM Level l
    JOIN Wave_Zombies wz ON l.wave_id = wz.wave_id
    JOIN Zombies z ON wz.zombie_id = z.zombie_id
    WHERE z.toughness = 'Colossal'
)
ORDER BY p.plant_name;

--4. Вывести достижения с наградой 500 монет или 5 алмазов

SELECT a.achievement_name,
       loc.location_name,
       a.reward_coins,
       a.reward_gems,
       CASE 
           WHEN a.reward_coins > 500 AND a.reward_gems > 5 THEN 'High'
           WHEN a.reward_coins > 300 OR a.reward_gems > 3 THEN 'Medium'
           ELSE 'Low'
       END as reward_level
FROM Achievements a
LEFT JOIN Location loc ON a.location_id = loc.location_id
WHERE a.reward_coins > 500 OR a.reward_gems > 5
ORDER BY a.reward_coins DESC, a.reward_gems DESC;

--5. Полная информация об уровнях с перечислением зомби в волнах и растений для разблокировки

SELECT l.level_id, l.level_number, loc.location_name,
       p.plant_name as unlock_plant,
       STRING_AGG(DISTINCT z.zombie_name, ', ' ORDER BY z.zombie_name) as zombies_in_wave,
       COUNT(DISTINCT wz.zombie_id) as unique_zombie_types,
       SUM(wz.group_size) as total_zombies
FROM Level l
JOIN Location loc ON l.location_id = loc.location_id
JOIN Plants p ON l.plant_id = p.plant_id
JOIN Wave_Zombies wz ON l.wave_id = wz.wave_id
JOIN Zombies z ON wz.zombie_id = z.zombie_id
GROUP BY l.level_id, l.level_number, loc.location_name, p.plant_name
ORDER BY l.level_id;

--6. Списко зомби, отсортированный по прочности (живучести)

SELECT zombie_name, toughness 
FROM Zombies 
ORDER BY toughness DESC, zombie_name;

--7. Количество уровней каждой сложности

SELECT location_name, COUNT(*) as level_count 
FROM Location 
JOIN Level ON Location.location_id = Level.location_id 
GROUP BY location_name;

--8. Средняя стоимость растений по типам, где средняя стоимость превышает 150
SELECT plant_type, AVG(plant_cost) as avg_cost 
FROM Plants 
GROUP BY plant_type 
HAVING AVG(plant_cost) > 150;

--9. Номер уровня и название растения, которое открывается на этом уровне 
SELECT l.level_number, p.plant_name 
FROM Level l 
JOIN Plants p ON l.plant_id = p.plant_id;

--10. Растения, которые разблокируются на ночных уровнях

SELECT plant_name 
FROM Plants 
WHERE plant_id IN (
    SELECT plant_id 
    FROM Level 
    WHERE location_id = 2
);