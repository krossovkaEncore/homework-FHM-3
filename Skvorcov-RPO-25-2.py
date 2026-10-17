WEIGHINGS = (
    ( 0,  0,  0,  0, -1, -1, -1,  1,  1,  1, -1,  1),
    ( 0, -1, -1, -1,  1,  1,  0,  0,  0,  1, -1,  1),
    (-1,  1,  0, -1,  0, -1,  1,  0,  1, -1,  0,  1)
)

RESULT_NAMES = {
    -1: "правая чаша тяжелее",
     0: "равновесие",
     1: "левая чаша тяжелее"
}

DEFECT_NAMES = {
    1: "тяжелее",
    -1: "легче"
}


def build_hypotheses():# таб. всех возможных случаев
    hypotheses = {}

    for coin in range(12):
        for defect in (-1, 1):
            signature = tuple(
                WEIGHINGS[step][coin] * defect
                for step in range(3)
            )

            hypotheses[signature] = (coin + 1, defect)

    return hypotheses


def weigh(left, right, fake_coin, fake_weight):# взвешивание
    left_weight = sum(
        fake_weight if coin == fake_coin else 10
        for coin in left
    )

    right_weight = sum(
        fake_weight if coin == fake_coin else 10
        for coin in right
    )

    return (left_weight > right_weight) - (
        left_weight < right_weight
    )


def get_groups(step):# возвращает монеты для л и п
    row = WEIGHINGS[step]

    left = [
        coin + 1
        for coin, position in enumerate(row)
        if position == 1
    ]

    right = [
        coin + 1
        for coin, position in enumerate(row)
        if position == -1
    ]

    return left, right


def solve(fake_coin, fake_weight, show_steps=True):# взвешивание и поиск фальш.
    hypotheses = build_hypotheses()
    results = []

    for step in range(3):
        left, right = get_groups(step)

        result = weigh(
            left, right, fake_coin, fake_weight
        )
        results.append(result)

        if show_steps:
            print(f"\nВзвешивание {step + 1}")
            print("Левая чаша:", left)
            print("Правая чаша:", right)
            print("Результат:", RESULT_NAMES[result])

    signature = tuple(results)
    coin, defect = hypotheses[signature]

    print("\n=== Результат ===")
    print(f"Фальшивая монета: № {coin}")
    print(f"Характер дефекта: {DEFECT_NAMES[defect]}")

    return coin, defect


def verify_algorithm():# проверка всех 24-ех вариантов
    for coin in range(1, 13):
        for defect, weight in ((-1, 9), (1, 11)):
            result = solve(coin, weight, show_steps=False)

            if result != (coin, defect):
                print("Ошибка проверки!")
                print("Монета:", coin)
                print("Вес:", weight)
                print("Получен результат:", result)
                return False

    print("Проверка пройдена: все 24 случая определены верно.")
    return True


if __name__ == "__main__":# точка входа
    print("Задача о 12 монетах")
    print("1 — запустить симуляцию")
    print("2 — проверить все 24 случая")

    choice = input("Выберите режим: ")

    if choice == "1":
        coin = int(input("Номер фальшивой монеты (1–12): "))
        defect = input("Монета легче или тяжелее? ").lower()# lower - делает все буквы маленькими 

        weights = {
            "легче": 9,
            "тяжелее": 11
        }

        if coin not in range(1, 13) or defect not in weights:
            print("Ошибка: проверьте номер монеты и её дефект.")
        else:
            solve(coin, weights[defect])

    elif choice == "2":
        verify_algorithm()

    else:
        print("Неизвестный режим.")
