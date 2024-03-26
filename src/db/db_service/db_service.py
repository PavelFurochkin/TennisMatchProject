from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.db_model.main_model import Base, Player, Match
from sqlalchemy import select, and_
from src.uuid_generator import UUIDGenerator


class TennisDBService:
    def __init__(self):
        self._ENGINE = create_engine('sqlite+pysqlite:///src/db/tennis_db.db')
        Base.metadata.create_all(self._ENGINE)
        self.Session = sessionmaker(bind=self._ENGINE)

    def get_player_id_by_name(self, name: str) -> int:
        with self.Session() as session:
            player = select(Player.id).where(Player.name == name)
            result = session.scalars(player).first()
            return result

    def add_player(self, name):
        new_player = self.get_player_id_by_name(name)
        if new_player is None:
            try:
                with self.Session() as session:
                    session.merge(Player(name=name))
                    session.commit()
                    print(f"Игрок {name} успешно добавлен")
            except Exception as e:
                print(f"Произошла ошибка при добавлении игрока {name}: {str(e)}")
        else:
            print(f"Игрок уже есть в базе")

    def checking_available_players(self, player1, player2):
        with self.Session() as session:
            self.add_player(player1)
            self.add_player(player2)
            player1_in_game = select(Match.winner).filter(
                and_(
                    Match.player1 == player1 or Match.player2 == player1,
                    Match.winner is None
                )
            )
            player1_available = session.scalars(player1_in_game).first
            player2_in_game = select(Match.winner).filter(
                and_(
                    Match.player1 == player2 or Match.player2 == player2,
                    Match.winner is None
                )
            )
            player2_available = session.scalars(player2_in_game).first
            if player1_available and player2_available is None:
                return True
            elif player1_available is not None:
                print(f'Игрок {player1} занят в матче')
                return False
            elif player2_available is not None:
                print(f'Игрок {player2} занят в матче')
                return False

    def add_match(self, player1, player2):
        __new_uuid = UUIDGenerator.get_uuid()
        with self.Session() as session:
            match = Match(uuid=__new_uuid, player1=player1, player2=player2)
            session.add(match)
            session.commit()
