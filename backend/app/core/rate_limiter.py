from collections import defaultdict

class JobCircuit:
    def __init__(self):
        self.off = set()
        self.counts = defaultdict(int)

    def mark_off(self, source: str):
        self.off.add(source)

    def is_off(self, source: str) -> bool:
        return source in self.off

    def inc(self, source: str):
        self.counts[source] += 1

    def count(self, source: str) -> int:
        return self.counts[source]
