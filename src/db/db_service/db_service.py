from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.db_model.models import Base, Player, Match
from sqlalchemy import select, and_, or_
from src.uuid_generator import UUIDGenerator
from exceptions import MatchNotFoundByUUID
from src.score import score, ScoreUpdateService

engine = create_engine('sqlite+pysqlite:///src/db/tennis_db.db')
session_factory = sessionmaker(bind=engine)


class TennisDBService:
    @staticmethod
    def create_tables():
        Base.metadata.create_all(engine)

    @staticmethod
    def update_db(match, point_winner):
        with session_factory() as session:
            stm = select(Match).where(Match.uuid == match.uuid)
            upd_match = session.execute(stm).fetchone()[0]
            result = ScoreUpdateService.ScoreUpdateService.update(upd_match, point_winner)
            session.merge(Match(id=result.id))
            session.commit()
            stm1 = select(Match).where(Match.uuid == result.uuid)
            upd_match1 = session.execute(stm1).fetchone()[0]
            return upd_match1

    @staticmethod
    def get_player_id_by_name(name: str) -> int:
        with session_factory() as session:
            player = select(Player.id).where(Player.name == name)
            result = session.scalars(player).first()
            return result

    @staticmethod
    def add_player(name):
        try:
            with session_factory() as session:
                session.merge(Player(name=name))
                session.commit()
                print(f"Игрок {name} успешно добавлен")
        except Exception as e:
            print(f"Произошла ошибка при добавлении игрока {name}: {str(e)}")

    @staticmethod
    def checking_available_players(player1, player2):
        with session_factory() as session:
            TennisDBService.add_player(player1)
            TennisDBService.add_player(player2)
            player1_in_game = session.query(Match.uuid).filter(
                and_(
                    Match.player1 == TennisDBService.get_player_id_by_name(player1) or
                    Match.player2 == TennisDBService.get_player_id_by_name(player2),
                    Match.winner == None
            ))
            player_available = session.scalars(player1_in_game).first()
            if player_available is None:
                return True
            else:
                print(f'Игрок занят в матче')
                return False

    @staticmethod
    def add_match(player1, player2):
        __new_uuid = UUIDGenerator.get_uuid()
        _first_player = TennisDBService.get_player_id_by_name(player1)
        _second_player = TennisDBService.get_player_id_by_name(player2)
        _score = score.Score().serialize()
        with session_factory() as session:
            match = Match(uuid=__new_uuid, player1=_first_player, player2=_second_player, score=_score)
            session.add(match)
            session.commit()
            match1 = select(Match).where(Match.uuid == __new_uuid)
            result = session.execute(match1).fetchone()[0]
        return result

    @classmethod
    def get_match_by_uuid(cls, uuid):
        with session_factory() as session:
            try:
                match = select(Match).where(Match.uuid == uuid)
                result = session.execute(match).fetchone()[0]
                return result
            except TypeError:
                raise MatchNotFoundByUUID("Match not found")
                
    @classmethod
    def get_players_name(cls, player1_id, player2_id):
        with session_factory() as session:
            players_id = [player1_id, player2_id]
            stmt = select(Player.name).where(Player.id.in_(players_id))
            result = session.execute(stmt)
            name_list = result.fetchall()
            name_dict = {'player1_name': name_list[0][0], 'player2_name': name_list[1][0]}
            return name_dict
