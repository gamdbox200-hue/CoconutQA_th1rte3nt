import pytest
from datetime import datetime

from db_requester.db_client import get_db_session
from db_models.transaction import AccountTransactionTemplate
from db_models.movie import MovieDBModel
from utils.data_generator import DataGenerator

class TestTransaction:

    def test_insufficient_funds(self):
        db_session = get_db_session()

        stan = AccountTransactionTemplate(
            user=f"Stan_{DataGenerator.generate_random_int(10)}",
            balance=100
        )
        bob = AccountTransactionTemplate(
            user=f"Bob_{DataGenerator.generate_random_int(10)}",
            balance=500
        )
        db_session.add_all([stan,bob])
        db_session.commit()

        assert stan.balance == 100
        assert bob.balance == 500

        from_account = db_session.query(AccountTransactionTemplate)\
            .filter_by(user=stan.user).one()
        to_account = db_session.query(AccountTransactionTemplate)\
            .filter_by(user=bob.user).one()

        try:
            if from_account.balance < 200:
                raise ValueError("Недостаточно средств на счету")

            from_account.balance -= 200
            to_account.balance += 200
            db_session.commit()

        except ValueError:
            db_session.rollback()

        finally:
            stan_after = db_session.query(AccountTransactionTemplate)\
                .filter_by(user=stan.user).one()
            bob_after = db_session.query(AccountTransactionTemplate)\
                .filter_by(user=bob.user).one()

            assert stan_after.balance == 100,\
                f"Ожидалось 100, получено:{stan_after.balance}"
            assert bob_after.balance == 500,\
                f"Ожидалось 500, получено:{bob_after.balance}"

            db_session.delete(stan_after)
            db_session.delete(bob_after)
            db_session.commit()
            db_session.close()


class TestMoviesDB:

    def test_delete_movie_stable(self, api_manager, admin_session, db_session):
        movie_id = 99999

        movie = db_session.query(MovieDBModel)\
            .filter(MovieDBModel.id == movie_id).first()

        if not movie:
            movie = MovieDBModel(
                id=movie_id,
                name="Тестовый фильм для удаления",
                price=500,
                description="Создан через БД",
                location="MSK",
                published=True,
                genre_id=1,
                rating=0,
                created_at=datetime.now()
            )
            db_session.add(movie)
            db_session.commit()

        api_manager.movies_api.delete_movie(movie_id, expected_status=200)

        deleted = db_session.query(MovieDBModel)\
            .filter(MovieDBModel.id == movie_id).first()
        assert deleted is None, "Фильм должен быть удалён из БД"








