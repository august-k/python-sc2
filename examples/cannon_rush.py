import random

import sc2
from sc2 import Race, Difficulty
from sc2.constants import *
from sc2.player import Bot, Computer

class CannonRushBot(sc2.BotAI):
    async def on_step(self, state, iteration):
        if not self.units(NEXUS).exists:
            for worker in self.workers:
                worker.attack(self.enemy_start_locations[0])
            return
        else:
            nexus = self.units(NEXUS).first

        if self.workers.amount + len(nexus.orders) < 14:
            if self.can_afford(PROBE):
                await self.do(nexus.train(PROBE))

        elif not self.units(PYLON).exists and not self.already_pending(PYLON):
            if self.can_afford(PYLON):
                await self.build(PYLON, near=nexus)

        elif not self.units(FORGE).exists:
            pylon = self.units(PYLON).ready
            if pylon.exists:
                if self.can_afford(FORGE):
                    await self.build(FORGE, near=pylon.closest_to(nexus))

        elif self.units(PYLON).amount < 2:
            if self.can_afford(PYLON):
                pos = self.enemy_start_locations[0].towards(self.game_info.map_center, random.randrange(8, 15))
                await self.build(PYLON, near=pos)

        elif not self.units(PHOTONCANNON).exists:
            if self.units(PYLON).ready.amount >= 2 and self.can_afford(PHOTONCANNON):
                pylon = self.units(PYLON).closer_than(20, self.enemy_start_locations[0]).random
                await self.build(PHOTONCANNON, near=pylon)

        else:
            if self.can_afford(PYLON) and self.can_afford(PHOTONCANNON): # ensure "fair" decision
                for _ in range(20):
                    pos = self.enemy_start_locations[0].random_on_distance(random.randrange(5, 12))
                    building = PHOTONCANNON if state.psionic_matrix.covers(pos) else PYLON
                    await self.build(building, near=pos)

def main():
    sc2.run_game(sc2.maps.get("Abyssal Reef LE"), [
        Bot(Race.Protoss, CannonRushBot()),
        Computer(Race.Protoss, Difficulty.Medium)
    ], realtime=True)

if __name__ == '__main__':
    main()
