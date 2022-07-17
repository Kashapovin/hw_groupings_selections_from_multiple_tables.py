import psycopg2
import sqlalchemy
from pprint import pprint
engine = sqlalchemy.create_engine('postgresql://demo_netology:pass@localhost:5432/demo')
connection = engine.connect()


pprint(#количество исполнителей в каждом жанре
connection.execute(
"""
SELECT name, COUNT(artist_id) artist_q FROM jenres j
JOIN artistjenre a
ON j.id = a.id
GROUP BY j.name
ORDER BY artist_q DESC;
""").fetchall())

pprint(#количество треков, вошедших в альбомы 2019-2020 годов
connection.execute(
"""
SELECT a.year_of_release, COUNT(t.name) FROM albums a
JOIN tracks t
ON t.id = a.id
WHERE year_of_release BETWEEN 2000 AND 2020
GROUP BY a.year_of_release;
""").fetchall())


pprint(#средняя продолжительность треков по каждому альбому
connection.execute(
"""
SELECT a.name, ROUND(AVG(t.duration), 2) FROM albums a
JOIN tracks t
ON a.id = t.id
GROUP BY a.name;
  """).fetchall())


print(connection.execute(#все исполнители, которые не выпустили альбомы в 2020 году;
"""
SELECT albumartist.artist_id, albums.year_of_release FROM albumartist
JOIN albums
ON albumartist.id = albums.id
WHERE year_of_release = 2020;
  """).fetchall())


print(connection.execute(#названия сборников, в которых присутствует конкретный исполнитель
"""
SELECT collections.name, artists.name FROM collections
JOIN artists
ON collections.id = artists.id
WHERE artists.name = 'name_3';
  """).fetchall())


print(connection.execute(#название альбомов, в которых присутствуют исполнители более 1 жанра
"""
SELECT albums.name, COUNT(artist_id) count_a FROM albums
WHERE count_a > 1
GROUP BY albums.name;
  """).fetchall())

pprint(#наименование треков, которые не входят в сборники
connection.execute(
"""
SELECT tracks.name, trackcollection.track_id FROM tracks
JOIN trackcollection
ON tracks.id = trackcollection.id
WHERE tracks.name NOT IN trackcollection;
""").fetchall())

pprint(#исполнителя(-ей), написавшего самый короткий по продолжительности трек
connection.execute(
"""
SELECT artists.name, tracks.duration FROM artists
JOIN tracks
ON artists.id = tracks.id
ORDER BY tracks.duration;
""").fetchone())

pprint(#название альбомов, содержащих наименьшее количество треков
connection.execute(
"""
SELECT albums.name, COUNT(tracks.name) FROM albums
JOIN tracks
ON albums.id = tracks.id
GROUP BY albums.name;
""").fetchone())

