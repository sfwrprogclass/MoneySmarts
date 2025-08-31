from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, List, Optional, Dict, Any

@dataclass
class Quest:
    id: str
    title: str
    description: str
    condition: Callable[["Game"], bool]
    reward_cash: int = 0
    completed: bool = False
    hidden_until_complete: bool = False

    def check(self, game: "Game") -> bool:
        if not self.completed and self.condition(game):
            self.completed = True
            if self.reward_cash > 0 and game.player:
                game.player.cash += self.reward_cash
            return True
        return False

class QuestManager:
    def __init__(self, game: "Game"):
        self.game = game
        self.quests: List[Quest] = []
        self._init_default_quests()

    def _init_default_quests(self):
        gcond = lambda attr: (lambda game: bool(getattr(game.player, attr, None)))
        self.quests = [
            Quest("open_bank", "Bank Beginnings", "Open your first bank account.", lambda game: bool(game.player and game.player.bank_account), reward_cash=25),
            Quest("get_job", "First Paycheck", "Obtain your first job.", lambda game: bool(game.player and game.player.job), reward_cash=50),
            Quest("buy_vehicle", "Wheels", "Acquire a vehicle asset.", lambda game: any(a.asset_type == "Car" for a in getattr(game.player, 'assets', [])), reward_cash=75),
            Quest("buy_home", "Home Owner", "Purchase a home asset.", lambda game: any(a.asset_type == "House" for a in getattr(game.player, 'assets', [])), reward_cash=100),
            Quest("networth_100k", "Six Figures", "Reach $100,000 net worth.", lambda game: game.player and game.compute_net_worth() >= 100000, reward_cash=500),
            Quest("meet_mentor", "Meet a Mentor", "Talk to an in‑world NPC mentor.", lambda game: getattr(game,'met_mentor', False), reward_cash=40)
        ]

    def active_quests(self) -> List[Quest]:
        return [q for q in self.quests if not q.completed and not q.hidden_until_complete]

    def completed_quests(self) -> List[Quest]:
        return [q for q in self.quests if q.completed]

    def check_all(self) -> List[Quest]:
        completed_now = []
        for q in self.quests:
            if q.check(self.game):
                completed_now.append(q)
        return completed_now

    def complete_by_id(self, qid: str):
        for q in self.quests:
            if q.id == qid and not q.completed:
                q.completed = True
                if q.reward_cash and self.game.player:
                    self.game.player.cash += q.reward_cash
                return q
        return None

    def serialize(self) -> List[Dict[str, Any]]:
        return [{
            'id': q.id,
            'completed': q.completed
        } for q in self.quests]

    def restore(self, data: List[Dict[str, Any]]):
        status = {d['id']: d.get('completed', False) for d in data}
        for q in self.quests:
            if q.id in status:
                q.completed = status[q.id]

    def as_summary(self) -> Dict[str, Any]:
        return {
            'active': [(q.id, q.title) for q in self.active_quests()],
            'completed': [q.id for q in self.completed_quests()]
        }

__all__ = ["Quest", "QuestManager"]
