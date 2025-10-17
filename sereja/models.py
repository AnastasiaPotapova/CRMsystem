from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Boolean, and_, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Настройка базы данных
engine = create_engine("sqlite:///users.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Excursion(Base):
    __tablename__ = "Excursions"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    n_visitors = Column(Integer)
    guide = Column(String,default="not defined", nullable=True)  #потом связь с юзером прикрутим
    phone = Column(String)

    poll = relationship("Poll", back_populates="excursions")
    poll_id = Column(Integer, ForeignKey("polls.id"))
    def __repr__(self):
        return f"Excursion(id={self.id}, date={self.date}, guide={self.guide}, n_visitors={self.n_visitors}, phone={self.phone})"

class ExcursionManager:
    def __init__(self):
        self.session = Session()

    def post(self, date, n_visitors, phone):
        """Добавить экскурсию"""
        excursion = Excursion(date=date, n_visitors=n_visitors,phone=phone)
        self.session.add(excursion)
        try:
            self.session.commit()
            print(f"[OK] Экскурсия {date} добавлена")
        except Exception as e:
            self.session.rollback()
            print("[ERR]", e)

    def get(self, excursion_id):
        """Получить экскурсию по id"""
        return self.session.query(Excursion).filter_by(id=excursion_id).first()

    def get_date(self, date):
        """Получить все экскурсии по дате"""
        return self.session.query(Excursion).filter_by(date=date).all()
    def get_guide(self, guide):
        """Получить все экскурсии гида"""
        return self.session.query(Excursion).filter_by(guide=guide).all()
    def get_all(self):
        """Получить все экускурсии"""
        return self.session.query(Excursion).all()

    def edit(self, excursion_id, date=None, n_visitors=None, guide=None, phone=None):
        """Редактировать экскурсию"""
        excursion = self.get(excursion_id)
        if not excursion:
            print("[ERR] Экскурсия не найдена")
            return
        if date:
            excursion.date = date
        if n_visitors:
            excursion.n_visitors = n_visitors
        if guide:
            excursion.guide = guide
        if phone:
            excursion.phone = phone
        try:
            self.session.commit()
            print(f"[OK] Экскурсия {excursion_id} обновлена")
        except Exception as e:
            self.session.rollback()
            print("[ERR]", e)

    def delete(self, excursion_id):
        """Удалить экскурсию"""
        excursion = self.get(excursion_id)
        if not excursion:
            print("[ERR] Экскурсия не найдена")
            return
        try:
            self.session.delete(excursion)
            self.session.commit()
            print(f"[OK] Экскурсия {excursion_id} удалена")
        except Exception as e:
            self.session.rollback()
            print("[ERR]", e)

class Poll(Base):
    __tablename__ = "polls"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    week_start = Column(Date)
    week_end = Column(Date)
    is_active = Column(Boolean, default=True)

    excursions = relationship("Excursion", back_populates="poll")

    def __repr__(self):
        return f"Опрос за {self.week_start}-{self.week_end} с {len(self.excursions)} экскурсиями"

class PollManager:
    def __init__(self):
        self.session = Session()

    def post(self, week_start, week_end):
        poll = Poll(week_start=week_start, week_end=week_end)
        self.session.add(poll)
        self.session.flush()

        excursions = self.session.query(Excursion).filter(
            and_(Excursion.date >= week_start, Excursion.date <= week_end)
        ).all()
        for ex in excursions:
            ex.poll = poll

        try:
            self.session.commit()
            print(f"[OK] Опрос создан для недели {week_start} - {week_end} с {len(excursions)} экскурсиями")
        except Exception as e:
            self.session.rollback()
            print("[ERR]", e)

    def get(self,poll_id):
        return self.session.query(Poll).filter_by(id=poll_id).first()

    def get_all(self):
        return self.session.query(Poll).all()

# Создаем таблицы
Base.metadata.create_all(engine)