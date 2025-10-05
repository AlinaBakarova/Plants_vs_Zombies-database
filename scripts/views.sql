-- Представление для растений, доступных на первых уровнях (unlock_level <= 3)
CREATE VIEW early_unlock_plants AS
SELECT plant_id, plant_name, plant_type, unlock_level
FROM Plants
WHERE unlock_level <= 3
ORDER BY unlock_level;

-- Представление для волн с зомби типа Colossal (Gargantuar, Zomboss и тд)
CREATE VIEW colossal_zombie_waves AS
SELECT wz.wave_id, z.zombie_name, wz.group_size, wz.start_time
FROM Wave_Zombies wz
JOIN Zombies z ON wz.zombie_id = z.zombie_id
WHERE z.toughness = 'Colossal';
