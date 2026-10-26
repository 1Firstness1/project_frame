-- ====================================================================
-- Сервис управления списком гостей: проверенные SQL-запросы (ПР7)
-- ====================================================================

-- 1. Выборка всех событий с сортировкой по названию
SELECT id, name, date, places
FROM events
ORDER BY name ASC;

-- 2. Выборка всех гостей с сортировкой по возрасту (от старших к младшим)
SELECT id, name, age
FROM guests
ORDER BY age DESC;

-- 3. Поиск событий с вместимостью не менее 20 мест (WHERE >=)
SELECT id, name, date, places
FROM events
WHERE places >= 20
ORDER BY places ASC;

-- 4. Выборка совершеннолетних гостей (WHERE)
SELECT id, name, age
FROM guests
WHERE age >= 18
ORDER BY name ASC;

-- 5. Поиск подтверждённых приглашений по status_id = 2 (WHERE)
SELECT id, event_id, guest_id
FROM invitations
WHERE status_id = 2;

-- 6. Полная информация о приглашениях (JOIN 4 таблиц)
SELECT invitations.id,
       events.name AS event_name,
       events.date AS event_date,
       guests.name AS guest_name,
       guests.age AS guest_age,
       statuses.title AS status_title
FROM invitations
JOIN events ON invitations.event_id = events.id
JOIN guests ON invitations.guest_id = guests.id
JOIN statuses ON invitations.status_id = statuses.id
ORDER BY events.date ASC;

-- 7. Список гостей с подтверждённым участием в событиях (JOIN + WHERE)
SELECT guests.name AS guest_name,
       events.name AS event_name,
       events.date AS event_date
FROM invitations
JOIN guests ON invitations.guest_id = guests.id
JOIN events ON invitations.event_id = events.id
JOIN statuses ON invitations.status_id = statuses.id
WHERE statuses.code = 'confirmed'
ORDER BY guests.name ASC;

-- 8. Поиск событий, на которые гость с ID = 1 ещё не был приглашён (NOT IN)
SELECT events.id, events.name, events.date, events.places
FROM events
WHERE events.id NOT IN (
    SELECT invitations.event_id
    FROM invitations
    WHERE invitations.guest_id = 1
)
ORDER BY events.name ASC;

-- 9. Общее количество подтверждённых приглашений (агрегатная функция COUNT)
SELECT COUNT(*) AS confirmed_invitations_count
FROM invitations
JOIN statuses ON invitations.status_id = statuses.id
WHERE statuses.code = 'confirmed';

-- 10. Агрегатные показатели возраста гостей (COUNT, MIN, MAX, AVG)
SELECT COUNT(*) AS total_guests,
       MIN(age) AS min_age,
       MAX(age) AS max_age,
       ROUND(AVG(age), 1) AS avg_age
FROM guests;

-- 11. Количество приглашений по событиям с LEFT JOIN и группировкой (GROUP BY)
SELECT events.id,
       events.name AS event_name,
       COUNT(invitations.id) AS invitations_count
FROM events
LEFT JOIN invitations ON events.id = invitations.event_id
GROUP BY events.id, events.name
ORDER BY invitations_count DESC;

-- 12. События с количеством приглашений больше одного (HAVING)
SELECT events.name AS event_name,
       COUNT(invitations.id) AS invitations_count
FROM events
JOIN invitations ON events.id = invitations.event_id
GROUP BY events.id, events.name
HAVING COUNT(invitations.id) > 1
ORDER BY invitations_count DESC;

-- 13. Группировка приглашений по категориям/статусам (GROUP BY)
SELECT statuses.title AS status_title,
       COUNT(invitations.id) AS invitations_count
FROM statuses
LEFT JOIN invitations ON statuses.id = invitations.status_id
GROUP BY statuses.id, statuses.title
ORDER BY invitations_count DESC;
