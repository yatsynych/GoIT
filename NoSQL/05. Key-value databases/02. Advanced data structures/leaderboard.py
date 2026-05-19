from db import init
r = init()

LEADERBOARD = 'game:leaderboard'

# Очищаємо старі дані якщо є
r.delete(LEADERBOARD)

# Додаємо гравців з їхніми очками
r.zadd(LEADERBOARD, {
    'alice':   4850,
    'bob':     3210,
    'charlie': 5500,
    'diana':   4850,
    'eve':     6100,
})

print("=== Топ-3 гравця ===")
top3 = r.zrevrange(LEADERBOARD, 0, 2, withscores=True)
for rank, (player, score) in enumerate(top3, start=1):
    print(f"{rank}. {player}: {int(score)} очок")

print()
print("=== Позиція кожного гравця ===")
for player in ['alice', 'bob', 'charlie', 'diana', 'eve']:
    rank = r.zrevrank(LEADERBOARD, player)
    score = r.zscore(LEADERBOARD, player)
    print(f"{player}: місце: {rank + 1}, очок: {int(score)}")

print()
print("=== bob зіграв і набрав 5900 очок ===")
r.zadd(LEADERBOARD, {'bob': 5900}, xx=True)  # xx=True -- тільки оновити, не додавати

print("Новий топ-5:")
all_players = r.zrevrange(LEADERBOARD, 0, -1, withscores=True)
for rank, (player, score) in enumerate(all_players, start=1):
    print(f"{rank}. {player}: {int(score)}")

print()
print("=== Гравці з очками від 4000 до 5500 ===")
mid_range = r.zrangebyscore(LEADERBOARD, 4000, 5500, withscores=True)
for player, score in mid_range:
    print(f"{player}: {int(score)}")