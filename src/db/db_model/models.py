from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, event

from exceptions import OtherError


class Base(DeclarativeBase):
    pass


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), index=True, unique=True)

    @staticmethod
    def validate_and_clean(mapper, connection, target):
        # Удаляем пробелы по краям и проверяем, пустая ли строка
        if target.name:
            target.name = target.name.strip()
            if target.name == "":
                raise OtherError("Имя не может состоять только из пробелов.")


# Привязываем обработчик к событию "before_insert" и "before_update"
event.listen(Player, 'before_insert', Player.validate_and_clean)
event.listen(Player, 'before_update', Player.validate_and_clean)



class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(unique=True)
    player1: Mapped[int] = mapped_column(ForeignKey("players.id", ondelete="CASCADE"))
    player2: Mapped[int] = mapped_column(ForeignKey("players.id", ondelete="CASCADE"))
    winner: Mapped[int] = mapped_column(ForeignKey("players.id", ondelete="CASCADE"), nullable=True)
    score: Mapped[str] = mapped_column(String(500), nullable=True)


 