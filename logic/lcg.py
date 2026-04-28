import math
import random

class LCGGenerator:
    def __init__(self):
        self.m = 2**19 - 1
        self.a = 216
        self.c = 55
        self.x0 = 1024

    def gcd(self, a, b):
        while b:
            a, b = b, a % b
        return a

    def generate_sequence(self, n):
        results = []
        x = self.x0
        for _ in range(n):
            x = (self.a * x + self.c) % self.m
            results.append(x)
        return results

    def get_period_fast(self):
        def f(val):
            return (self.a * val + self.c) % self.m
        tortoise = f(self.x0)
        hare = f(f(self.x0))
        while tortoise != hare:
            tortoise = f(tortoise)
            hare = f(f(hare))
        period = 0
        first_in_cycle = tortoise
        while True:
            tortoise = f(tortoise)
            period += 1
            if tortoise == first_in_cycle:
                break
        return period

    def estimate_pi(self, n, mode="lcg"):
        coprime_count = 0
        x = self.x0
        for _ in range(n):
            if mode == "lcg":
                x = (self.a * x + self.c) % self.m
                rx = x
                x = (self.a * x + self.c) % self.m
                ry = x
            else:
                rx = random.randint(1, self.m)
                ry = random.randint(1, self.m)
            if self.gcd(rx, ry) == 1:
                coprime_count += 1
        if coprime_count == 0: return 0
        return math.sqrt(6 / (coprime_count / n))