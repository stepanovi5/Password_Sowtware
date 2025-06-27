import random
import string
import os
from cryptography.fernet import Fernet

KEY_FILE = 'key.key'
ENC_FILE = 'accounts.encrypted'
DOMAINS = ['gmail.com', 'yandex.ru', 'mail.ru', 'outlook.com', 'icloud.com']

# --- Загрузка ключа ---
def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as f:
            f.write(key)
    else:
        with open(KEY_FILE, 'rb') as f:
            key = f.read()
    return key

# --- Генерация email и пароля ---
def generate_email():
    name = ''.join(random.choices(string.ascii_lowercase, k=6))
    num = ''.join(random.choices(string.digits, k=3))
    domain = random.choice(DOMAINS)
    return f"{name}{num}@{domain}"

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

# --- Работа с шифрованием ---
def decrypt_file(fernet):
    if not os.path.exists(ENC_FILE):
        return ""
    with open(ENC_FILE, 'rb') as f:
        return fernet.decrypt(f.read()).decode()

def encrypt_and_save(content, fernet):
    with open(ENC_FILE, 'wb') as f:
        f.write(fernet.encrypt(content.encode()))

# --- Разбор записей ---
def parse_entries(data):
    entries = data.strip().split('\n\n')
    return [e.strip() for e in entries if e.strip()]

# --- Формирование строки записи ---
def format_entry(comment, email, password):
    return f"{comment}:\n  Email: {email}\n  Pass:  {password}"

# --- Сохранение одной записи ---
def save_entry(comment, email, password, fernet):
    data = decrypt_file(fernet)
    entries = parse_entries(data)
    entries.append(format_entry(comment, email, password))
    encrypt_and_save('\n\n'.join(entries), fernet)
    print("✅ Запись сохранена.")

# --- Просмотр всех записей с номерами ---
def view_all(fernet):
    data = decrypt_file(fernet)
    entries = parse_entries(data)
    if not entries:
        print("Нет сохранённых записей.")
        return
    print("\n📂 Сохранённые записи:\n")
    for idx, entry in enumerate(entries, 1):
        print(f"[{idx}] {entry}\n")

# --- Удаление записи ---
def delete_entry(fernet):
    data = decrypt_file(fernet)
    entries = parse_entries(data)
    view_all(fernet)
    num = int(input("Введите номер записи для удаления: ")) - 1
    if 0 <= num < len(entries):
        removed = entries.pop(num)
        encrypt_and_save('\n\n'.join(entries), fernet)
        print("🗑️ Запись удалена:\n", removed)
    else:
        print("❌ Неверный номер.")

# --- Редактирование записи ---
def edit_entry(fernet):
    data = decrypt_file(fernet)
    entries = parse_entries(data)
    view_all(fernet)
    num = int(input("Введите номер записи для редактирования: ")) - 1
    if 0 <= num < len(entries):
        print("Оставьте поле пустым, чтобы не менять его.")
        lines = entries[num].splitlines()
        old_comment = lines[0].replace(":", "").strip()
        old_email = lines[1].replace("Email:", "").strip()
        old_pass = lines[2].replace("Pass:", "").strip()

        comment = input(f"Комментарий [{old_comment}]: ") or old_comment
        email = input(f"Email [{old_email}]: ") or old_email
        password = input(f"Пароль [{old_pass}]: ") or old_pass

        entries[num] = format_entry(comment, email, password)
        encrypt_and_save('\n\n'.join(entries), fernet)
        print("✏️ Запись обновлена.")
    else:
        print("❌ Неверный номер.")

# === 📤 Экспорт в текстовый файл ===
def export_to_txt(fernet, export_file='exported_accounts.txt'):
    data = decrypt_file(fernet)
    entries = parse_entries(data)
    if not entries:
        print("📭 Нет записей для экспорта.")
        return
    with open(export_file, 'w', encoding='utf-8') as f:
        for entry in entries:
            f.write(entry + "\n\n")
    print(f"📤 Экспорт завершён. Сохранено в файл: {export_file}")

# --- Основное меню ---
def main():
    key = load_key()
    fernet = Fernet(key)

    while True:
        print("\nВыберите действие:")
        print("1 — Сгенерировать email+пароль и сохранить")
        print("2 — Ввести вручную email+пароль и сохранить")
        print("3 — Просмотреть все записи")
        print("4 — Удалить запись")
        print("5 — Редактировать запись")
        print("6 — 📤 Экспортировать все записи в .txt файл")
        print("0 — Выход")

        choice = input("Ваш выбор: ")

        if choice == '1':
            email = generate_email()
            password = generate_password()
            print(f"📧 Email: {email}")
            print(f"🔐 Пароль: {password}")
            comment = input("Комментарий к записи: ")
            save_entry(comment, email, password, fernet)

        elif choice == '2':
            email = input("Введите email: ")
            password = input("Введите пароль: ")
            comment = input("Комментарий: ")
            save_entry(comment, email, password, fernet)

        elif choice == '3':
            view_all(fernet)

        elif choice == '4':
            delete_entry(fernet)

        elif choice == '5':
            edit_entry(fernet)

        elif choice == '6':
            export_to_txt(fernet)

        elif choice == '0':
            print("Выход.")
            break

        else:
            print("❌ Неверный выбор.")

if __name__ == "__main__":
    main()