import enum


class SimulationState(enum.Enum):
    INACTIVE = 1
    RUNNING = 2
    PAUSED = 3
    WIN = 4
    LOSS = 5


class Simulation():
    def __init__(self, level, levelView):
        self.levelView = levelView
        self.state = SimulationState.INACTIVE
        self.level = level

    def play(self):
        if self.state == SimulationState.RUNNING:
            self.state = SimulationState.PAUSED
        elif self.state in [SimulationState.PAUSED, SimulationState.INACTIVE]:
            self.state = SimulationState.RUNNING

    def restart(self):
        self.level.reload_level()
        if self.state == SimulationState.INACTIVE:
            return
        self.levelView.reset_simulation_ticks()
        self.state = SimulationState.RUNNING

    def cancel(self):
        self.level.reload_level()
        self.state = SimulationState.INACTIVE

    def get_state(self):
        return self.state

    def tick(self):
        if self.state == SimulationState.RUNNING:
            tick_result = self.level.tick()
            if tick_result == -1:
                self.state = SimulationState.LOSS
            elif tick_result == 1:
                self.state = SimulationState.WIN
