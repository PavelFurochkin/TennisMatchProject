from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey


class Base(DeclarativeBase):
    pass


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), index=True, unique=True)

    # matches = relationship(
    #     "Match",
    #
    # )


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(unique=True)
    player1: Mapped[int] = mapped_column(ForeignKey("players.id", ondelete="CASCADE"))
    player2: Mapped[int] = mapped_column(ForeignKey("players.id", ondelete="CASCADE"))
    winner: Mapped[int] = mapped_column(ForeignKey("players.id", ondelete="CASCADE"), nullable=True)
    score: Mapped[str] = mapped_column(String(500), nullable=True)


 