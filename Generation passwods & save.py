import random
import string


def generate_password(length=12, use_digits=True, use_upper=True, use_lower=True, use_special=True):
    characters = ''

    if use_digits:
        characters += string.digits
    if use_upper:
        characters += string.ascii_uppercase
    if use_lower:
        characters += string.ascii_lowercase
    if use_special:
        characters += string.punctuation

    if not characters:
        raise ValueError("Нужно выбрать хотя бы один тип символов!")

    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def save_password_with_comment(password, comment, filename='passwords.txt'):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(f"{comment}: {password}\n")
    print(f"✅ Пароль сохранён с комментарием в файл '{filename}'.")


def main():
    print("Выберите режим:")
    print("1 — Сгенерировать пароль")
    print("2 — Ввести пароль вручную")
    mode = input("Ваш выбор (1/2): ")

    if mode == '1':
        length = int(input("Введите длину пароля: "))
        password = generate_password(length)
        print("🔐 Сгенерированный пароль:", password)
    elif mode == '2':
        password = input("Введите ваш пароль: ")
        print("🔐 Введённый пароль принят.")
    else:
        print("❌ Неверный выбор.")
        return

    comment = input("Добавьте комментарий к паролю (например, 'Telegram', 'Личный Wi-Fi' и т.д.): ")
    save_password_with_comment(password, comment)


if __name__ == "__main__":
    main()
