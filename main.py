
---

### 9. Password Manager (Parol Saqlovchi)

**main.py**

```python
import sqlite3
import time
from functools import wraps
import datetime
import random
import string

def timer_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[DECORATOR] {func.__name__} — {end - start:.4f} soniya")
        return result
    return wrapper

class PasswordManager:
    def __init__(self, master_user="Admin"):
        self._master_user = master_user
        self._create_db()

    @property
    def master_user(self):
        return self._master_user

    @master_user.setter
    def master_user(self, value):
        if len(value.strip()) < 3:
            raise ValueError("Foydalanuvchi nomi kamida 3 harfdan iborat bo'lishi kerak!")
        self._master_user = value
        print(f"Master foydalanuvchi yangilandi: {value}")

    def _create_db(self):
        conn = sqlite3.connect("passwords.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY,
            site TEXT NOT NULL,
            username TEXT,
            password TEXT,
            created_at TEXT
        )''')
        conn.commit()
        conn.close()

    def _generate_password(self, length=12):
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choice(chars) for _ in range(length))

    @timer_decorator
    def add_password(self, site, username):
        password = self._generate_password()
        conn = sqlite3.connect("passwords.db")
        cursor = conn.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        cursor.execute("INSERT INTO passwords (site, username, password, created_at) VALUES (?, ?, ?, ?)",
                       (site, username, password, now))
        conn.commit()
        conn.close()
        print(f"✅ {site} uchun parol yaratildi va saqlandi!")
        print(f"Parol: {password}  (nusxa oling)")

    @timer_decorator
    def show_passwords(self):
        conn = sqlite3.connect("passwords.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM passwords ORDER BY site")
        rows = cursor.fetchall()
        conn.close()
        print(f"\n=== {self.master_user} ning Parollar Ombori ===")
        if not rows:
            print("Hozircha parollar yo'q.")
            return
        for r in rows:
            print(f"ID:{r[0]:<3} | Sayt: {r[1]:<20} | Username: {r[2]:<15} | Parol: {r[3]}")

    @timer_decorator
    def delete_password(self, site):
        conn = sqlite3.connect("passwords.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM passwords WHERE site=?", (site,))
        conn.commit()
        conn.close()
        print(f"✅ {site} paroli o'chirildi.")

    def info(self):
        print(f"\n🔐 Password Manager — {self.master_user}")

if __name__ == "__main__":
    pm = PasswordManager()
    print("=== Password Manager ===")
    while True:
        print("\n1. Yangi parol qo'shish\n2. Barcha parollarni ko'rish\n3. Sayt bo'yicha o'chirish\n4. Master ismni o'zgartirish\n5. Chiqish")
        choice = input("Tanlang (1-5): ").strip()
        if choice == "1":
            site = input("Sayt nomi (masalan: gmail.com): ").strip()
            username = input("Username: ").strip()
            pm.add_password(site, username)
        elif choice == "2":
            pm.show_passwords()
        elif choice == "3":
            site = input("Qaysi saytni o'chiramiz: ").strip()
            pm.delete_password(site)
        elif choice == "4":
            new_name = input("Yangi master ism: ").strip()
            try:
                pm.master_user = new_name
            except ValueError as e:
                print(e)
        elif choice == "5":
            print("Dastur tugadi!")
            break
        else:
            print("Noto'g'ri tanlov!")
          
