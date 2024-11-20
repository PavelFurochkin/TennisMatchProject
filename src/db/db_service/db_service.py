from src.db.db_model.models import Base, Player, Match
from sqlalchemy import select, or_
from src.uuid_generator import UUIDGenerator
from src.score import score, ScoreUpdateService
from src.db.DAO.DAO import session_factory
from src.db.DAO.DAO import TennisDAO


class TennisDBService:

    @staticmethod
    def update_match(match, point_winner):
        with session_factory() as session:
            stm = select(Match).where(Match.uuid == match.uuid)
            upd_match = session.execute(stm).fetchone()[0]
            result = ScoreUpdateService.ScoreUpdateService.update(upd_match, point_winner)
            session.merge(Match(id=result.id))
            session.commit()
            stm_final = select(Match).where(Match.uuid == result.uuid)
            upd_match_final = session.execute(stm_final).fetchone()[0]
            return upd_match_final

    @staticmethod
    def add_match(player1, player2):
        __new_uuid = UUIDGenerator.get_uuid()
        _first_player = TennisDAO.get_player_id_by_name(player1)
        _second_player = TennisDAO.get_player_id_by_name(player2)
        _score = score.Score().serialize()
        with session_factory() as session:
            match = Match(uuid=__new_uuid, player1=_first_player, player2=_second_player, score=_score)
            session.add(match)
            session.commit()
            match1 = select(Match).where(Match.uuid == __new_uuid)
            result = session.execute(match1).fetchone()[0]
        return result

    @classmethod
    def paginate(cls, **kwargs):
        with session_factory() as session:
            # Основной запрос с JOIN и фильтром по имени игрока, если он передан
            stmt = select(Match).distinct().join(Player, or_(Player.id == Match.player1, Player.id == Match.player2))

            filter_by_player_name = kwargs.get('filter_by_player_name')
            if filter_by_player_name:
                stmt = stmt.where(Player.name == filter_by_player_name)

            # Получаем page и page_size с значениями по умолчанию, если они отсутствуют
            page = kwargs.get('page', 1)
            page_size = kwargs.get('page_size', 10)

            # Вычисляем offset
            offset = (page - 1) * page_size
            stmt = stmt.limit(page_size).offset(offset)

            # Выполняем запрос и получаем результат в виде списка объектов Match
            result = session.execute(stmt).fetchall()

            return result
        