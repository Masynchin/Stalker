# Stalker

Работа для курса "Базы Данных и Сетевые Технологии" СПбГУ 2023/24.

## ТЗ

- [ ] Интеграция с API
  - [ ] Используя YouTube API собрать информацию из 1000 видео и сохранить в БД.
- [ ] База данных
  - [ ] Предусмотреть возможность сохранения файлов/картинок и тд.
  - [x] Каждое сообщение собирать с метаданными - от кого (id, username, firstname, lastname), дата.
  - [x] Данные сохранять в sqlite3. Разработать архитектуру БД (ER-модель).
  - [x] Необходимо иметь список каналов, с которых собирали комментарии, информацию о пользователях.
- [ ] GUI
  - [ ] Реализовать GUI для просмотра БД.
  - [x] Реализовать форму для поиска по пользователю,по временному интервалу, по видео, по слову/части слова.
  - [ ] Иметь возможность сортировки в форме, иметь возможность вывода только тех пользователей, которые имеют более заданного количества комментариев. 
  - [x] Реализовать форму для проброса в БД прямого запроса для получения результата.
