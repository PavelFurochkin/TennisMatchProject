from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from src.db.db_model.models import Base, Player, Match
from sqlalchemy import select, and_, or_
from src.uuid_generator import UUIDGenerator
from exceptions import MatchNotFoundByUUID, OtherError
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
        if 3 > len(name) or len(name) > 20:
            message = f"Имя должно быть от 3 до 20 символов."
            raise OtherError(message)
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
            raise OtherError('Игрок не может играть сам с собой.')
        with session_factory() as session:
            TennisDBService.add_player(player1)
            TennisDBService.add_player(player2)
            stmt = select(Match.uuid).where(
                and_(
                    Match.player1 == TennisDBService.get_player_id_by_name(player1) or
                    Match.player2 == TennisDBService.get_player_id_by_name(player2),
                    Match.winner == None
                ))
            player_available = session.execute(stmt).scalars().first()
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

    @classmethod
    def get_all_players(cls):
        with session_factory() as session:
            player_names_list = [row[0] for row in
                                 session.execute(select(Player.name).order_by(Player.name.asc())).fetchall()]
        return player_names_list

    @classmethod
    def get_matches_count(cls, **kwargs):
        with session_factory() as session:
            filter_by_player_name = kwargs.get("filter_by_player_name")
            query = select(func.count()).select_from(Match).distinct().join(
                Player, or_(Player.id == Match.player1, Player.id == Match.player2))
            if filter_by_player_name:
                query = query.where(Player.name == filter_by_player_name)

            result = session.execute(query).scalar()
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
        