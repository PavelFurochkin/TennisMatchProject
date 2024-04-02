from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.db_model.models import Base, Player, Match
from sqlalchemy import select, and_
from src.uuid_generator import UUIDGenerator

engine = create_engine('sqlite+pysqlite:///src/db/tennis_db.db')
session_factory = sessionmaker(engine)


class TennisDBService:
    @staticmethod
    def create_tables():
        Base.metadata.create_all(engine)

    @staticmethod
    def get_player_id_by_name(name: str) -> int:
        with session_factory() as session:
            player = select(Player.id).where(Player.name == name)
            result = session.scalars(player).first()
            return result

    @staticmethod
    def add_player(name):
        new_player = TennisDBService.get_player_id_by_name(name)
        if new_player is None:
            try:
                with session_factory() as session:
                    session.merge(Player(name=name))
                    session.commit()
                    print(f"Игрок {name} успешно добавлен")
            except Exception as e:
                print(f"Произошла ошибка при добавлении игрока {name}: {str(e)}")
        else:
            print(f"Игрок уже есть в базе")

    @staticmethod
    def checking_available_players( player1, player2):
        with session_factory() as session:
            TennisDBService.add_player(player1)
            TennisDBService.add_player(player2)
            player1_in_game = session.query(Match).filter(
                and_(
                    Match.player1 == player1 or Match.player2 == player1,
                    Match.winner == None
                )
            )
            player1_available = session.scalars(player1_in_game).first()
            player2_in_game = session.query(Match).filter(
                and_(
                    Match.player1 == player2 or Match.player2 == player2,
                    Match.winner == None
                )
            )
            player2_available = session.scalars(player2_in_game).first()
            if (player1_available and player2_available) is None:
                return True
            elif player1_available is not None:
                print(f'Игрок {player1} занят в матче')
                return False
            elif player2_available is not None:
                print(f'Игрок {player2} занят в матче')
                return False
        return True

    @staticmethod
    def add_match(player1, player2):
        __new_uuid = UUIDGenerator.get_uuid()
        with session_factory() as session:
            match = Match(uuid=__new_uuid, player1=player1, player2=player2)
            session.add(match)
            session.commit()

#     @staticmethod
#     def test_request():
#         with session_factory() as session:
#             request = select(Player.id)
#             result = session.execute(request)
#             finaly = result.scalars().all()
#             return finaly
#
#             #     and_(
#             #         Match.player1 == player1 or Match.player2 == player1,
#             #         Match.winner is None
#             #     )
#             # )
#
#
# s = TennisDBService.test_request()
# print(s)