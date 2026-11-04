from dataclasses import dataclass, field


@dataclass(order=True)
class Player:
    score: int
    name: str
    badges: list = field(default_factory=list)


def build_roster(pairs):
    players = []
    for name, score in pairs:
        p = Player(score, name)
        if score >= 90:
            p.badges.append("top")
        players.append(p)
    return [f"{p.name}:{len(p.badges)}" for p in sorted(players)]
