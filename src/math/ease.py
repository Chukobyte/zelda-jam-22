import math
from typing import Callable

from seika.math import Vector2, Math


def lerp(source, dest, amount):
    return source + (dest - source) * amount


class Ease:
    class Cubic:
        @staticmethod
        def ease_in(
            elapsed_time: float, from_pos: float, to_pos: float, duration: float
        ) -> float:
            change = to_pos - from_pos
            elapsed_time = elapsed_time / duration
            if elapsed_time > math.fabs(1.0):
                return to_pos
            return change * elapsed_time * elapsed_time * elapsed_time + from_pos

        @staticmethod
        def ease_out(
            elapsed_time: float, from_pos: float, to_pos: float, duration: float
        ) -> float:
            change = to_pos - from_pos
            elapsed_time = elapsed_time / duration - 1.0
            if elapsed_time > math.fabs(1.0):
                return to_pos
            return (
                change * (elapsed_time * elapsed_time * elapsed_time + 1.0) + from_pos
            )

        @staticmethod
        def ease_in_vec2(
            elapsed_time: float, from_pos: Vector2, to_pos: Vector2, duration: float
        ) -> Vector2:
            return Vector2(
                Ease.Cubic.ease_in(elapsed_time, from_pos.x, to_pos.x, duration),
                Ease.Cubic.ease_in(elapsed_time, from_pos.y, to_pos.y, duration),
            )

        @staticmethod
        def ease_out_vec2(
            elapsed_time: float, from_pos: Vector2, to_pos: Vector2, duration: float
        ) -> Vector2:
            return Vector2(
                Ease.Cubic.ease_out(elapsed_time, from_pos.x, to_pos.x, duration),
                Ease.Cubic.ease_out(elapsed_time, from_pos.y, to_pos.y, duration),
            )

    class Bounce:
        @staticmethod
        def ease_in(
            elapsed_time: float, from_pos: float, to_pos: float, duration: float
        ) -> float:
            change = to_pos - from_pos
            return (
                change
                - Ease.Bounce.ease_out(elapsed_time, from_pos, to_pos, duration)
                + from_pos
            )

        @staticmethod
        def ease_out(
            elapsed_time: float, from_pos: float, to_pos: float, duration: float
        ) -> float:
            change = to_pos - from_pos
            elapsed_time = elapsed_time / duration
            if elapsed_time < 1 / 2.75:
                return change * (7.5625 * elapsed_time * elapsed_time) + from_pos
            elif elapsed_time < 2 / 2.75:
                elapsed_time = elapsed_time - (1.5 / 2.75)
                return change * (7.5625 * elapsed_time * elapsed_time + 0.75) + from_pos
            elif elapsed_time < 2.5 / 2.75:
                elapsed_time = elapsed_time - (2.25 / 2.75)
                return (
                    change * (7.5625 * elapsed_time * elapsed_time + 0.9375) + from_pos
                )
            else:
                elapsed_time = elapsed_time - (2.626 / 2.75)
                return (
                    change * (7.5625 * elapsed_time * elapsed_time + 0.984375)
                    + from_pos
                )

        @staticmethod
        def ease_in_vec2(
            elapsed_time: float, from_pos: Vector2, to_pos: Vector2, duration: float
        ) -> Vector2:
            return Vector2(
                Ease.Bounce.ease_in(elapsed_time, from_pos.x, to_pos.x, duration),
                Ease.Bounce.ease_in(elapsed_time, from_pos.y, to_pos.y, duration),
            )

        @staticmethod
        def ease_out_vec2(
            elapsed_time: float, from_pos: Vector2, to_pos: Vector2, duration: float
        ) -> Vector2:
            return Vector2(
                Ease.Bounce.ease_out(elapsed_time, from_pos.x, to_pos.x, duration),
                Ease.Bounce.ease_out(elapsed_time, from_pos.y, to_pos.y, duration),
            )

    class Elastic:
        @staticmethod
        def ease_in(
            elapsed_time: float,
            from_pos: float,
            to_pos: float,
            duration: float,
            amplitude=0.0,
            period=0.0,
        ) -> float:
            change = to_pos - from_pos
            if elapsed_time == 0:
                return from_pos
            elapsed_time = elapsed_time / duration
            if elapsed_time == 1:
                return from_pos + change

            if period == 0:
                period = duration * 0.3

            if amplitude == 0 or amplitude < abs(change):
                amplitude = change
                s = period / 4
            else:
                s = period / (2 * Math.PI) * math.asin(change / amplitude)

            elapsed_time = elapsed_time - 1
            return (
                -(
                    amplitude
                    * math.pow(2, 10 * elapsed_time)
                    * math.sin((elapsed_time * duration - s) * (2 * Math.PI) / period)
                )
                + from_pos
            )

        @staticmethod
        def ease_out(
            elapsed_time: float,
            from_pos: float,
            to_pos: float,
            duration: float,
            amplitude=0.0,
            period=0.0,
        ) -> float:
            change = to_pos - from_pos
            if elapsed_time == 0:
                return from_pos
            elapsed_time = elapsed_time / duration
            if elapsed_time == 1:
                return from_pos + change

            if period == 0:
                period = duration * 0.3

            if amplitude == 0:
                amplitude = change
                s = period / 4
            else:
                s = period / (2 * Math.PI) * math.asin(change / amplitude)

            return (
                amplitude
                * math.pow(2, -10 * elapsed_time)
                * math.sin((elapsed_time * duration - s) * (2 * Math.PI) / period)
                + change
                + from_pos
            )

        @staticmethod
        def ease_in_vec2(
            elapsed_time: float,
            from_pos: Vector2,
            to_pos: Vector2,
            duration: float,
            amplitude=0.0,
            period=0.0,
        ) -> Vector2:
            return Vector2(
                Ease.Elastic.ease_in(
                    elapsed_time, from_pos.x, to_pos.x, duration, amplitude, period
                ),
                Ease.Elastic.ease_in(
                    elapsed_time, from_pos.y, to_pos.y, duration, amplitude, period
                ),
            )

        @staticmethod
        def ease_out_vec2(
            elapsed_time: float,
            from_pos: Vector2,
            to_pos: Vector2,
            duration: float,
            amplitude=0.0,
            period=0.0,
        ) -> Vector2:
            return Vector2(
                Ease.Elastic.ease_out(
                    elapsed_time, from_pos.x, to_pos.x, duration, amplitude, period
                ),
                Ease.Elastic.ease_out(
                    elapsed_time, from_pos.y, to_pos.y, duration, amplitude, period
                ),
            )


class Easer:
    def __init__(self, from_pos, to_pos, duration: float, func: Callable):
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.duration = duration
        self.func = func
        self.elapsed_time = 0.0

    def ease(self, delta: float):
        self.elapsed_time += delta
        return self.func(self.elapsed_time, self.from_pos, self.to_pos, self.duration)
