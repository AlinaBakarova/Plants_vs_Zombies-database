import pytest
from analysis.analysis import execute_query  # Предполагаемый модуль для работы с БД

class TestDatabaseQueries:
    @pytest.fixture(autouse=True)
    def setup(self, db_connection):
        """Фикстура для инициализации тестов"""
        self.conn = db_connection

    def test_plants_unlocked_by_level_3(self):
        """
        Тест 1: Проверка запроса растений, доступных до 3 уровня
        Ожидаемый результат: возвращаются только растения с unlock_level <= 3
        """
        query = """
        SELECT plant_id, plant_name, plant_type, unlock_level
        FROM Plants
        WHERE unlock_level <= 3
        ORDER BY unlock_level, plant_name;
        """
        result = execute_query(self.conn, query)
        
        # Проверяем, что результат не пустой
        assert len(result) > 0
        
        # Проверяем, что все растения имеют unlock_level <= 3
        for plant in result:
            assert plant[3] <= 3
        
        # Проверяем сортировку (сначала по уровню, затем по имени)
        for i in range(len(result)-1):
            if result[i][3] == result[i+1][3]:
                assert result[i][1] <= result[i+1][1]

    def test_top5_longest_levels(self):
        """
        Тест 2: Проверка запроса топ-5 самых долгих уровней
        Ожидаемый результат: 5 уровней с наибольшим time_limit, отсортированные по убыванию
        """
        query = """
        SELECT l.level_id, l.level_number, loc.location_name, l.time_limit
        FROM Level l
        JOIN Location loc ON l.location_id = loc.location_id
        ORDER BY l.time_limit DESC
        LIMIT 5;
        """
        result = execute_query(self.conn, query)
        
        # Проверяем, что вернулось ровно 5 записей
        assert len(result) == 5
        
        # Проверяем сортировку по убыванию time_limit
        for i in range(len(result)-1):
            assert result[i][3] >= result[i+1][3]

    def test_plants_unlocked_with_colossal_zombies(self):
        """
        Тест 3: Проверка запроса растений, разблокируемых на уровнях с зомби прочности Colossal
        Ожидаемый результат: возвращаются только растения, связанные с уровнями, где есть Colossal зомби
        """
        query = """
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
        """
        result = execute_query(self.conn, query)
        
        # Проверяем, что результат не пустой
        assert len(result) > 0
        
        # Проверяем, что все возвращенные растения действительно связаны с Colossal зомби
        plant_ids = [plant[0] for plant in result]
        check_query = """
        SELECT COUNT(*) FROM Level l
        JOIN Wave_Zombies wz ON l.wave_id = wz.wave_id
        JOIN Zombies z ON wz.zombie_id = z.zombie_id
        WHERE z.toughness = 'Colossal' AND l.plant_id IN %s
        """
        count = execute_query(self.conn, check_query, (tuple(plant_ids),))[0][0]
        assert count == len(result)

    def test_high_reward_achievements(self):
        """
        Тест 4: Проверка запроса достижений с наградой >500 монет или >5 алмазов
        Ожидаемый результат: возвращаются только достижения с указанными наградами
        """
        query = """
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
        """
        result = execute_query(self.conn, query)
        
        # Проверяем, что результат не пустой
        assert len(result) > 0
        
        # Проверяем условия фильтрации
        for achievement in result:
            assert achievement[2] > 500 or achievement[3] > 5
        
        # Проверяем правильность расчета reward_level
        for achievement in result:
            coins, gems = achievement[2], achievement[3]
            if coins > 500 and gems > 5:
                assert achievement[4] == 'High'
            elif coins > 300 or gems > 3:
                assert achievement[4] == 'Medium'
            else:
                assert achievement[4] == 'Low'

    def test_levels_full_info(self):
        """
        Тест 5: Проверка запроса полной информации об уровнях
        Ожидаемый результат: корректная агрегация данных о зомби и растениях
        """
        query = """
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
        """
        result = execute_query(self.conn, query)
        
        # Проверяем, что результат не пустой
        assert len(result) > 0
        
        # Проверяем структуру данных
        for level in result:
            assert level[0] is not None  # level_id
            assert level[1] is not None  # level_number
            assert level[2] is not None  # location_name
            assert level[3] is not None  # unlock_plant
            assert level[4] is not None  # zombies_in_wave (может быть пустой строкой)
            assert level[5] >= 0         # unique_zombie_types
            assert level[6] >= 0         # total_zombies

    def test_zombies_sorted_by_toughness(self):
        """
        Тест 6: Проверка запроса зомби, отсортированных по прочности
        Ожидаемый результат: зомби отсортированы по убыванию прочности, затем по имени
        """
        query = """
        SELECT zombie_name, toughness 
        FROM Zombies 
        ORDER BY toughness DESC, zombie_name;
        """
        result = execute_query(self.conn, query)
        
        # Определяем правильный порядок сортировки toughness
        toughness_order = ['Colossal', 'High', 'Medium', 'Low']
        
        # Проверяем сортировку
        for i in range(len(result)-1):
            current_toughness = toughness_order.index(result[i][1])
            next_toughness = toughness_order.index(result[i+1][1])
            
            # Проверяем сортировку по toughness DESC
            assert current_toughness <= next_toughness
            
            # Если toughness одинаковый, проверяем сортировку по имени
            if current_toughness == next_toughness:
                assert result[i][0] <= result[i+1][0]

    def test_levels_count_by_complexity(self):
        """
        Тест 7: Проверка запроса количества уровней по сложности
        Ожидаемый результат: корректное количество уровней для каждой локации
        """
        query = """
        SELECT location_name, COUNT(*) as level_count 
        FROM Location 
        JOIN Level ON Location.location_id = Level.location_id 
        GROUP BY location_name;
        """
        result = execute_query(self.conn, query)
        
        # Проверяем, что результат не пустой
        assert len(result) > 0
        
        # Проверяем, что количество уровней соответствует ожидаемому
        expected_counts = {
            'Day': 10,
            'Night': 10,
            'Pool': 5,
            'Fog': 5,
            'Roof': 0  # В тестовых данных нет уровней для Roof
        }
        
        for location in result:
            if location[0] in expected_counts:
                assert location[1] == expected_counts[location[0]]

    def test_avg_plant_cost_by_type(self):
        """
        Тест 8: Проверка запроса средней стоимости растений по типам (где средняя > 150)
        Ожидаемый результат: только типы растений со средней стоимостью > 150
        """
        query = """
        SELECT plant_type, AVG(plant_cost) as avg_cost 
        FROM Plants 
        GROUP BY plant_type 
        HAVING AVG(plant_cost) > 150;
        """
        result = execute_query(self.conn, query)
        
        # Проверяем, что результат не пустой
        assert len(result) > 0
        
        # Проверяем условие HAVING
        for plant_type in result:
            assert plant_type[1] > 150

    def test_levels_with_unlock_plants(self):
        """
        Тест 9: Проверка запроса номеров уровней и названий растений, которые они открывают
        Ожидаемый результат: корректное соответствие уровней и растений
        """
        query = """
        SELECT l.level_number, p.plant_name 
        FROM Level l 
        JOIN Plants p ON l.plant_id = p.plant_id;
        """
        result = execute_query(self.conn, query)
        
        # Проверяем, что результат не пустой
        assert len(result) > 0
        
        # Проверяем, что все записи имеют и номер уровня, и название растения
        for level in result:
            assert level[0] is not None
            assert level[1] is not None

    def test_plants_unlocked_in_night_levels(self):
        """
        Тест 10: Проверка запроса растений, разблокируемых на ночных уровнях
        Ожидаемый результат: только растения, связанные с ночными уровнями (location_id = 2)
        """
        query = """
        SELECT plant_name 
        FROM Plants 
        WHERE plant_id IN (
            SELECT plant_id 
            FROM Level 
            WHERE location_id = 2
        );
        """
        result = execute_query(self.conn, query)
        
        # Проверяем, что результат не пустой
        assert len(result) > 0
        
        # Проверяем, что все растения действительно связаны с ночными уровнями
        plant_names = [plant[0] for plant in result]
        check_query = """
        SELECT COUNT(*) FROM Level l
        JOIN Plants p ON l.plant_id = p.plant_id
        WHERE l.location_id = 2 AND p.plant_name IN %s
        """
        count = execute_query(self.conn, check_query, (tuple(plant_names),))[0][0]
        assert count == len(result)
