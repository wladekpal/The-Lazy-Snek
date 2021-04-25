import enum
from ..engine.level import LevelState


class SimulationState(enum.Enum):
    INACTIVE = 1
    RUNNING = 2
    PAUSED = 3
    WIN = 4
    LOSS = 5
    STEPBYSTEP = 6


class Simulation():
    def __init__(self, level, level_view):
        self.levelView = level_view
        self.state = SimulationState.INACTIVE
        self.level = level

    def play(self):
        if self.state == SimulationState.RUNNING:
            self.state = SimulationState.PAUSED
        elif self.state in [SimulationState.PAUSED, SimulationState.INACTIVE]:
            self.state = SimulationState.RUNNING

    def restart(self):
        self.level.reload_level()
        self.state = SimulationState.INACTIVE
        self.levelView.blocks_pane.set_available_blocks(self.level.available_blocks)
        self.levelView.reset_simulation_ticks()

    def cancel(self):
        self.state = SimulationState.INACTIVE
        self.level.reload_simulation()
        self.levelView.reset_simulation_ticks()

    def stepbystep(self):
        self.state = SimulationState.STEPBYSTEP

    def get_state(self):
        return self.state

    def tick(self):
        tick_result = 0
        if self.state == SimulationState.RUNNING:
            tick_result = self.level.tick()
        elif self.state == SimulationState.STEPBYSTEP:
            tick_result = self.level.tick()
            self.state = SimulationState.PAUSED

        if tick_result == LevelState.LOSS:
            self.state = SimulationState.LOSS
        elif tick_result == LevelState.WIN:
            self.state = SimulationState.WIN
