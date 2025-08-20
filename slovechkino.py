import pandas as pd
import tkinter as tk
from tkinter import messagebox, scrolledtext
from collections import Counter


# Загружаем словарь существительных
try:
    df_dict = pd.read_csv('data/nouns.csv', sep='\t')
    word_set = set(df_dict['bare'].str.lower().dropna())
except Exception as e:
    messagebox.showerror("Ошибка", f"Не удалось загрузить словарь:\n{e}")
    exit()

def find_words_from_set(letters: str, word_set: set) -> dict:
    """
    Находит все слова из word_set, которые можно составить из введённых букв.
    Результаты группируются по длине слова.
    """
    letters = letters.lower()
    letters_counter = Counter(letters)
    results_by_length = {}

    for word in word_set:
        word_lower = word.lower()
        if not word_lower.isalpha():
            continue  # пропускаем "слова" с цифрами или спецсимволами

        word_counter = Counter(word_lower)
        # проверяем, можно ли составить слово из букв
        if not (word_counter - letters_counter):
            results_by_length.setdefault(len(word_lower), []).append(word_lower)

    # сортируем слова в каждой группе
    for length in results_by_length:
        results_by_length[length] = sorted(results_by_length[length])

    return results_by_length

def on_find_words():
    input_letters = entry.get().strip()
    if not input_letters.isalpha():
        messagebox.showwarning("Некорректный ввод", "Введите только буквы, без пробелов и цифр.")
        return

    results = find_words_from_set(input_letters, word_set)
    output.delete(1.0, tk.END)

    if not results:
        output.insert(tk.END, "Ничего не найдено.")
        return

    for length in sorted(results.keys()):
        output.insert(tk.END, f"\n--- Слова из {length} букв ---\n")
        for word in results[length]:
            output.insert(tk.END, f"{word}\n")

# Интерфейс приложения
root = tk.Tk()
root.title("Поиск слов из букв")
root.geometry("500x500")
root.resizable(False, False)

label = tk.Label(root, text="Введите буквы:")
label.pack(pady=5)

entry = tk.Entry(root, font=("Arial", 14), justify="center")
entry.pack(pady=5)

button = tk.Button(root, text="Найти слова", command=on_find_words)
button.pack(pady=5)

output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, font=("Courier", 10))
output.pack(pady=5)

root.mainloop()
