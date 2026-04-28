# Children Stagnation Detector — AI-детектор застоя прогресса

Автоматическое выявление детей с отсутствием прогресса по доменам развития.

**Репозиторий:** https://github.com/SKZHPRVT/children_stagnation

---

## 🚀 Быстрый старт

```bash
git clone https://github.com/SKZHPRVT/children_stagnation.git
cd children_stagnation
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
pytest tests/ -v
```

### Docker
```bash
docker build -t children-stagnation .
docker run -v $(pwd)/data:/app/data -v $(pwd)/outputs:/app/outputs children-stagnation
```

---

## 🛠️ Технологии и обоснование

| Технология | Почему выбрана |
|------------|----------------|
| Python 3.12 | Стабильный язык с богатой DS-экосистемой |
| pandas | Группировка сессий, расчёт дельт, фильтрация |
| numpy | Числовые операции |
| matplotlib/seaborn | Графики динамики баллов |
| pytest | 4 unit-теста бизнес-логики |
| Docker | Контейнеризация |

---

## 📁 Архитектура решения

```
children_stagnation/
├── data/children_sessions.xlsx
├── src/
│   ├── parser.py          # load_sessions(), автозаполнение флагов
│   ├── analysis.py        # detect_stagnation(df, min_days=28)
│   └── reporting.py       # CSV, summary.md, графики
├── tests/
│   ├── test_parser.py     # Тест автозаполнения progress_flag
│   └── test_analysis.py   # Тесты detect_stagnation
├── outputs/
│   ├── stagnation_report.csv
│   ├── summary.md
│   └── plots/             # 5 графиков
├── main.py                # CLI — запуск одной командой
├── Dockerfile
└── README.md
```

### Пайплайн обработки
```
Excel → load_sessions() → _fill_progress_flags() → detect_stagnation(min_days=28)
                                                          ↓
                                          CSV + summary.md + графики
```

### Логика detect_stagnation
1. Группировка по child_id + domain
2. Поиск последовательностей с одинаковым assessment_score
3. Расчёт длительности застоя в днях
4. Уровень риска: 28-30=low, 30-60=medium, 60-90=high, 90+=critical
5. Сбор контекста: даты, баллы, количество сессий

---

## ⚠️ Компромиссы

| Решение | Почему |
|---------|--------|
| Автозаполнение progress_flag | Если флаг пуст — определяем по дельтам баллов |
| min_sessions=2 | Минимум 2 сессии для признания застоя |
| Только числовые баллы | Качественные оценки не влияют на расчёт |
| Риск только по длительности | Без учёта веса домена или возраста |

---

## ✅ Проверка работы

### Тесты
```bash
pytest tests/ -v
```
Результат: **4 passed**

### Валидация отчёта
- stagnation_report.csv — 10 случаев, корректные даты/баллы
- summary.md — текст для супервизора
- plots/ — 5 графиков PNG

### Пример вызова
```python
from src.parser import load_sessions
from src.analysis import detect_stagnation
df = load_sessions("data/children_sessions.xlsx")
result = detect_stagnation(df, min_days=28)
print(result[["child_id","domain","days_stagnant","risk_level"]])
```

---

## 📊 Скриншоты графиков

### Распределение уровня риска
![Риски](outputs/plots/risk_distribution.png)

### Застой по доменам
![Домены](outputs/plots/stagnation_by_domain.png)

### Средний балл по детям
![Баллы](outputs/plots/avg_score_by_child.png)

### Динамика СП10 (71 день, высокий риск)
![СП10](outputs/plots/SP10_Listening.png)

### Динамика СП21 (69 дней, высокий риск)
![СП21](outputs/plots/SP21_Verbal_Request.png)

---

## 📊 Результаты

Обнаружено **10 случаев застоя** среди 20 детей:

| Риск | Количество |
|------|------------|
| high | 2 (СП10, СП21) |
| medium | 7 |
| low | 1 |

---

## 💼 Мотивация

### 1. Почему мне интересен этот проект?
Проект помогает детям с ОВЗ — автоматизация экономит время педагогов.

### 2. Моя роль в команде
Data Science: анализ паттернов, модели риска, визуализация, метрики.

### 3. Время
15-20 ч/неделю, 3-6 месяцев.

---

## 📬 Контакты
- GitHub: [SKZHPRVT](https://github.com/SKZHPRVT)
- Telegram: @twentyseventwentysix
