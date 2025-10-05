-- Индекс для ускорения поиска растений по типу
CREATE INDEX idx_plants_type ON Plants(plant_type);

-- Индекс для ускорения фильтрации зомби по toughness
CREATE INDEX idx_zombies_toughness ON Zombies(toughness);
