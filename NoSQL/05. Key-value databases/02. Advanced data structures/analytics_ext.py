from db import init
r = init()

r.delete('page:home', 'page:catalog', 'page:about', 'site:total')

r.pfadd('page:home',    *[f'user:{i}' for i in range(1, 5001)])
r.pfadd('page:catalog', *[f'user:{i}' for i in range(3001, 8001)])
r.pfadd('page:about',   *[f'user:{i}' for i in range(7001, 9001)])

r.pfmerge('site:total', 'page:home', 'page:catalog', 'page:about')

print(f"Головна: {r.pfcount('page:home'):,} (реально: 5 000)")
print(f"Каталог: {r.pfcount('page:catalog'):,} (реально: 5 000)")
print(f"Про нас: {r.pfcount('page:about'):,} (реально: 2 000)")
print(f"Всього: {r.pfcount('site:total'):,}  (реально: 9 000)")