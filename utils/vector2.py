class Vector2:
    '''
    https://realpython.com/operator-function-overloading/#overloading-built-in-operators
    '''
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __abs__(self) -> "Vector2":
        return Vector2(abs(self.x), abs(self.y))
    
    def __add__(self, v: "Vector2") -> "Vector2":
        return Vector2(self.x + v.x, self.y + v.y)

    def __sub__(self, v: "Vector2") -> "Vector2":
        return Vector2(self.x - v.x, self.y - v.y)

    def __mul__(self, v: "Vector2") -> "Vector2":
        return Vector2(self.x * v.x, self.y * v.y)

    def __iadd__(self, v: "Vector2") -> "Vector2":
        self.x += v.x
        self.y += v.y
        return self

    def __isub__(self, v: "Vector2") -> "Vector2":
        self.x -= v.x
        self.y -= v.y
        return self

    def __imul__(self, v: "Vector2") -> "Vector2":
        self.x *= v.x
        self.y *= v.y
        return self

    def __rmul__(self, f: float) -> "Vector2":
        return Vector2(self.x*f, self.y*f)

    def __rdiv__(self, f: float) -> "Vector2":
        return Vector2(self.x/f, self.y/f)

    def get(self) -> tuple[float, float]:
        return (self.x, self.y)
