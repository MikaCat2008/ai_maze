class Vector2:
    x: float
    y: float

    def __init__(self, x = 0.0, y = 0.0) -> None:
        self.x = x
        self.y = y

    @property
    def t(self) -> tuple[float, float]:
        return self.x, self.y

    def copy(self) -> "Vector2":
        return Vector2(self.x, self.y)


class Vector3(Vector2):
    z: float

    def __init__(self, x = 0.0, y = 0.0, z = 0.0) -> None:
        super().__init__(x, y)
        
        self.z = z

    @property
    def t(self) -> tuple[float, float, float]:
        return self.x, self.y, self.z

    def copy(self) -> "Vector3":
        return Vector3(self.x, self.y, self.z)


class Vector4(Vector3):
    a: float

    def __init__(self, x = 0.0, y = 0.0, z = 0.0, a = 255) -> None:
        super().__init__(x, y, z)
        
        self.a = a

    @property
    def t(self) -> tuple[float, float, float, float]:
        return self.x, self.y, self.z, self.a

    def copy(self) -> "Vector3":
        return Vector4(self.x, self.y, self.z, self.a)
