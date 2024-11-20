from sqlalchemy import create_engine, select, and_
from sqlalchemy.orm import sessionmaker
from src.db.db_model.models import Base, Player, Match
from exceptions import MatchNotFoundByUUIDError, PlayerNameError, TooShortNameError
from settings import DB_URL


engine = create_engine(DB_URL)
session_factory: sessionmaker = sessionmaker(bind=engine)

class TennisDAO:
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
        if 3 > len(name) or len(name) > 20:
            raise TooShortNameError(name)
        with session_factory() as session:
            stmt = select(Player).where(Player.name == name)
            exiting_player = session.execute(stmt).scalar_one_or_none()

            if exiting_player:
                pass
            else:
                session.merge(Player(name=name))
                session.commit()
                print(f"Игрок {name} успешно добавлен")

    @staticmethod
    def checking_available_players(player1, player2):
        if player1 == player2:
            raise PlayerNameError(player1)
        with session_factory() as session:
            TennisDAO.add_player(player1)
            TennisDAO.add_player(player2)
            stmt = select(Match.uuid).where(
                and_(
                    Match.player1 == TennisDAO.get_player_id_by_name(player1) or
                    Match.player2 == TennisDAO.get_player_id_by_name(player2),
                    Match.winner == None
                ))
            player_available = session.execute(stmt).scalars().first()
            if player_available is None:
                return True
            else:
                print(f'Игрок занят в матче')
                return False

    @classmethod
    def get_all_players(cls):
        with session_factory() as session:
            player_names_list = [row[0] for row in
                                 session.execute(select(Player.name).order_by(Player.name.asc())).fetchall()]
        return player_names_list

    @classmethod
    def get_players_name(cls, player1_id, player2_id):
        with session_factory() as session:
            players_id = [player1_id, player2_id]
            stmt = select(Player.name).where(Player.id.in_(players_id))
            result = session.execute(stmt)
            name_list = result.fetchall()
            name_dict = {'player1_name': name_list[0][0], 'player2_name': name_list[1][0]}
            return name_dict

    @classmethod
    def get_match_by_uuid(cls, uuid):
        with session_factory() as session:
            try:
                match = select(Match).where(Match.uuid == uuid)
                result = session.execute(match).fetchone()[0]
                return result
            except TypeError:
                raise MatchNotFoundByUUIDError()
