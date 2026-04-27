from database import SessionLocal
from Services.BitsoService import BitsoService
from Models import BookStatistics
import logging

with SessionLocal() as session:
    bitsoService = BitsoService(session)

    try:
        statistics = session.query(BookStatistics).order_by(BookStatistics.id.desc()).limit(4).all()

        for stats in statistics:
            print(stats.book.book)
            print(stats.change_value)
            print(stats.change_percentage)
        
    except Exception as e:
        print(e)
        session.rollback()

    finally:
        session.close()

