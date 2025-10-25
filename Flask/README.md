Тут микродокументация от нейронки
🧩 Структура БД

Excursion

Модель экскурсии.
Поля:
	•	id — первичный ключ
	•	date — дата экскурсии (Date)
	•	n_visitors — количество посетителей (Integer)
	•	guide — имя гида (String, может быть NULL)
	•	phone — контактный телефон (String)
	•	poll_id — внешний ключ на опрос (ForeignKey("polls.id"))

Связи:
	•	poll — связь многие-к-одному с моделью Poll (через back_populates="excursions")

⸻

Poll

Модель опроса (опрос за неделю).
Поля:
	•	id — первичный ключ
	•	created_at — дата создания (DateTime, по умолчанию datetime.now)
	•	week_start, week_end — начало и конец недели (Date)
	•	is_active — активен ли опрос (Boolean, по умолчанию True)

Связи:
	•	excursions — список экскурсий, относящихся к этому опросу

⸻

⚙️ Классы менеджеров

ExcursionManager

Работа с экскурсиями.

Методы:
	•	post(date, n_visitors, guide, phone) — создать экскурсию
	•	get(excursion_id) — получить экскурсию по ID
	•	get_date(date) — получить экскурсии по дате
	•	get_guide(guide) — получить экскурсии по гиду
	•	get_all() — получить все экскурсии
	•	edit(excursion_id, ...) — изменить данные экскурсии
	•	delete(excursion_id) — удалить экскурсию

⸻

PollManager

Работа с опросами.

Методы:
	•	post(week_start, week_end) — создать опрос за указанный период и автоматически привязать экскурсии, попадающие в диапазон дат

⸻

🗃️ Использование

manager = ExcursionManager()
manager.post(date=datetime(2025, 10, 10).date(), n_visitors=15, guide="Иван", phone="123-456")

poll_mgr = PollManager()
poll_mgr.post(week_start=datetime(2025, 10, 6).date(), week_end=datetime(2025, 10, 12).date())


⸻

	•	Отношение Poll ↔ Excursion — один-ко-многим.
	•	При создании опроса все экскурсии, попадающие в диапазон недель, автоматически связываются с ним.
(это было самое тяжелое)

poll.excursions# список объектов Excursion   