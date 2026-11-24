import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Папки проекта
DATA = Path("data")
RESULTS = Path("analysis_results")
RESULTS.mkdir(exist_ok=True)

# Загрузка CSV-файлов
users = pd.read_csv(DATA / "users.csv")
tasks = pd.read_csv(DATA / "tasks.csv")
categories = pd.read_csv(DATA / "categories.csv")
schedule = pd.read_csv(DATA / "daily_schedule.csv")
stats = pd.read_csv(DATA / "time_statistics.csv")

# Настройка графиков
plt.rcParams["font.family"] = "DejaVu Sans"


def save_chart(name):
    plt.tight_layout()
    plt.savefig(RESULTS / name, dpi=150)
    plt.close()


# 1. Распределение времени по категориям
merged = schedule.merge(categories, on="category_id")
time_by_category = merged.groupby("name")["planned_minutes"].sum()

time_by_category.plot(kind="bar", figsize=(9, 5))
plt.title("Распределение времени по категориям")
plt.xlabel("Категории")
plt.ylabel("Время (минуты)")
plt.xticks(rotation=35, ha="right")
save_chart("01_categories.png")


# 2. Распределение задач по статусам
tasks["status"].value_counts().plot(
    kind="pie", autopct="%1.1f%%", figsize=(7, 7)
)
plt.title("Распределение задач по статусам")
plt.ylabel("")
save_chart("02_status.png")


# 3. Количество задач по приоритетам
tasks["priority"].value_counts().plot(
    kind="bar", figsize=(8, 5)
)
plt.title("Количество задач по приоритетам")
plt.xlabel("Приоритет")
plt.ylabel("Количество задач")
save_chart("03_priority.png")


# 4. Планируемое и фактическое время
tasks.groupby("status")[
    ["planned_minutes", "actual_minutes"]
].mean().plot(kind="bar", figsize=(8, 5))

plt.title("Планируемое и фактическое время")
plt.xlabel("Статус задачи")
plt.ylabel("Среднее время (минуты)")
plt.legend(["Запланировано", "Фактически"])
plt.xticks(rotation=0)
save_chart("04_planned_actual.png")


# 5. Изменение времени по дням
stats["stat_date"] = pd.to_datetime(stats["stat_date"])

daily = stats.groupby("stat_date")[
    ["planned_minutes", "actual_minutes"]
].mean()

daily.plot(figsize=(10, 5))
plt.title("Изменение затрат времени по дням")
plt.xlabel("Дата")
plt.ylabel("Среднее время (минуты)")
plt.legend(["Запланировано", "Фактически"])
save_chart("05_daily_time.png")


# 6. Распределение продуктивности
stats["productivity_percent"].plot(
    kind="hist", bins=15, figsize=(8, 5)
)
plt.title("Распределение показателей продуктивности")
plt.xlabel("Продуктивность (%)")
plt.ylabel("Количество записей")
save_chart("06_productivity.png")


# Основные показатели
summary = f"""
АНАЛИЗ ДАННЫХ ПРОЕКТА TIMEBUDGET

Количество пользователей: {len(users)}
Количество задач: {len(tasks)}
Количество категорий: {len(categories)}
Количество записей расписания: {len(schedule)}
Количество записей статистики: {len(stats)}

Выполнено задач: {(tasks['status'] == 'completed').sum()}
Доля выполненных задач: {
    (tasks['status'] == 'completed').mean() * 100:.1f
}%

Среднее планируемое время:
{tasks['planned_minutes'].mean():.1f} минут

Среднее фактическое время:
{tasks['actual_minutes'].mean():.1f} минут

Средняя продуктивность:
{stats['productivity_percent'].mean():.1f}%
"""

(RESULTS / "summary.txt").write_text(summary, encoding="utf-8")

print("Анализ завершён!")
print("Графики и статистика сохранены в папке analysis_results.")
print(summary)
