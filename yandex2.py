
days, die = [int(el) for el in input().split()]

all_days = [(int(el), i) for i, el in enumerate(input().split())]

global_set = {i for i in range(0, days)}
suma = 0
list_days = [0 for _ in range(0, days)]

if die == 1:
    print(sum(x[0] for x in all_days))
    print(*[1 for _ in range(0, days)])

else:
    sorted_tuples = sorted(all_days, key=lambda x: (x[0], x[1]))
    for el in sorted_tuples:
        date = el[1]
        price = el[0]
        for i in range(0, die):
            new_date = date + i
            if new_date in global_set:
                global_set.remove(new_date)
                list_days[date] += 1
                suma += price

        if len(global_set) == 0:
            break

    print(suma)
    print(*list_days)

