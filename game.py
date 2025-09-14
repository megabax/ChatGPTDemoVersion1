import random
import json

def generate_secret_number(min_range, max_range):
    """Генерирует случайное целое число в заданном диапазоне."""
    return random.randint(min_range, max_range)

def get_user_guess():
    """Получает число от пользователя и обрабатывает ошибки ввода."""
    while True:
        try:
            guess = int(input("Ваше предположение: "))
            return guess
        except ValueError:
            print("Пожалуйста, введите целое число.")

def play_game(min_range, max_range, max_attempts):
    """Запускает игру "Угадай число"."""

    secret_number = generate_secret_number(min_range, max_range)
    attempts = 0

    print(f"Я загадал число от {min_range} до {max_range}. Попробуйте угадать!")

    while True:
        attempts += 1
        guess = get_user_guess()

        if guess == secret_number:
            print(f"Поздравляю! Вы угадали число {secret_number} за {attempts} попыток.")
            return attempts
        elif guess < secret_number:
            print("Загаданное число больше.")
        else:
            print("Загаданное число меньше.")

        if max_attempts and attempts >= max_attempts:
            print(f"К сожалению, вы исчерпали все попытки. Загаданное число было {secret_number}.")
            return None  #  None indicates a loss

def choose_difficulty():
    """Предлагает пользователю выбрать уровень сложности."""
    print("nВыберите уровень сложности:")
    print("1. Легкий (1-100, неограниченное количество попыток)")
    print("2. Средний (1-50, 7 попыток)")
    print("3. Сложный (1-20, 5 попыток)")

    while True:
        choice = input("Введите номер уровня сложности (1-3): ")
        if choice == '1':
            return 1, 100, None  # Легкий
        elif choice == '2':
            return 1, 50, 7    # Средний
        elif choice == '3':
            return 1, 20, 5    # Сложный
        else:
            print("Некорректный ввод. Пожалуйста, выберите 1, 2 или 3.")

def get_player_name():
    """Получает имя игрока."""
    return input("Введите ваше имя: ")

def save_score(name, difficulty, attempts, filename="scores.json"):
    """Сохраняет результат игры в файл."""
    try:
        with open(filename, 'r') as f:
            scores = json.load(f)
    except FileNotFoundError:
        scores = []

    scores.append({"name": name, "difficulty": difficulty, "attempts": attempts})

    with open(filename, 'w') as f:
        json.dump(scores, f, indent=4)  # Используем indent для читаемости

def load_scores(filename="scores.json"):
    """Загружает результаты игр из файла."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def display_leaderboard(filename="scores.json"):
    """Отображает таблицу рекордов."""
    scores = load_scores(filename)
    if not scores:
        print("Таблица рекордов пока пуста.")
        return

    # Сортируем результаты по количеству попыток (чем меньше, тем лучше)
    sorted_scores = sorted(scores, key=lambda x: x['attempts'])

    print("nТаблица рекордов:")
    print("------------------------------------")
    print("| Имя       | Уровень  | Попытки |")
    print("------------------------------------")
    for score in sorted_scores:
        print(f"| {score['name']:9} | {score['difficulty']:8} | {score['attempts']:7} |")
    print("------------------------------------")


def main():
    """Основная функция, запускающая игру."""
    print("Добро пожаловать в игру 'Угадай число'!")

    name = get_player_name()
    min_range, max_range, max_attempts = choose_difficulty()

    difficulty_names = {
        (1, 100, None): "Легкий",
        (1, 50, 7): "Средний",
        (1, 20, 5): "Сложный"
    }

    difficulty = difficulty_names.get((min_range, max_range, max_attempts), "Неизвестный")

    attempts = play_game(min_range, max_range, max_attempts)

    if attempts is not None:
        save_score(name, difficulty, attempts)

    display_leaderboard()

if __name__ == "__main__":
    main()
