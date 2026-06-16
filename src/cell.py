class Cell:
    def __init__(self) -> None:
        self.can_be: set[str] = set(["1", "2", "3", "4", "5", "6", "7", "8", "9"])

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        tmp = list(self.can_be)
        return tmp[0] if len(tmp) == 1 else "A"
