from uuid import uuid4


class UUIDGenerator:
    @staticmethod
    def get_uuid() -> str:
        uuid = uuid4().hex
        return uuid
