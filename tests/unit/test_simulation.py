from src.gameplay.simulation import SimulationState, Simulation
import mock


def test_simulation_play_method_pauses_while_running():
    simulation = Simulation(mock.Mock(), mock.Mock())
    simulation.state = SimulationState.RUNNING
    simulation.play()
    assert simulation.get_state() == SimulationState.PAUSED


def test_simulation_play_resumes_while_paused():
    simulation = Simulation(mock.Mock(), mock.Mock())
    simulation.state = SimulationState.PAUSED
    simulation.play()
    assert simulation.get_state() == SimulationState.RUNNING


def test_simulation_play_starts_running_when_first_method_called_on_object():
    simulation = Simulation(mock.Mock(), mock.Mock())
    simulation.play()
    assert simulation.get_state() == SimulationState.RUNNING


def test_simulation_play_starts_running_when_inactive():
    simulation = Simulation(mock.Mock(), mock.Mock())
    simulation.play()
    assert simulation.get_state() == SimulationState.RUNNING


def test_simulation_play_has_no_effect_ater_win():
    simulation = Simulation(mock.Mock(), mock.Mock())
    simulation.state = SimulationState.WIN
    simulation.play()
    assert simulation.get_state() == SimulationState.WIN


def test_simulation_play_has_no_effect_ater_loss():
    simulation = Simulation(mock.Mock(), mock.Mock())
    simulation.state = SimulationState.LOSS
    simulation.play()
    assert simulation.get_state() == SimulationState.LOSS


def test_simulation_restart_reloads_level_whe():
    level = mock.Mock()
    simulation = Simulation(level, mock.Mock())
    simulation.restart()
    level.reload_level.assert_called_once()


def test_simulation_restart_has_no_effect_when_inactive():
    simulation = Simulation(mock.Mock(), mock.Mock())
    simulation.state = SimulationState.INACTIVE
    simulation.restart()
    assert simulation.get_state() == SimulationState.INACTIVE


def test_simulation_tick_calls_level_tick_when_running():
    level = mock.Mock()
    simulation = Simulation(level, mock.Mock())
    simulation.state = SimulationState.RUNNING
    simulation.tick()
    level.tick.assert_called_once()


def test_simulation_tick_does_not_call_level_tick_when_not_running():
    for state in [SimulationState.LOSS, SimulationState.WIN, SimulationState.PAUSED, SimulationState.INACTIVE]:
        level = mock.Mock()
        simulation = Simulation(level, mock.Mock())
        simulation.state = state
        simulation.tick()
        level.tick.assert_not_called()


def test_simulation_cancel_reloads_simulation():
    level = mock.Mock()
    simulation = Simulation(level, mock.Mock())
    simulation.state = SimulationState.RUNNING
    simulation.cancel()
    level.reload_simulation.assert_called_once()


def test_simulation_cancel_sets_state_to_inactive():
    for state in [SimulationState.LOSS, SimulationState.WIN, SimulationState.PAUSED,
                  SimulationState.INACTIVE, SimulationState.RUNNING]:
        simulation = Simulation(mock.Mock(), mock.Mock())
        simulation.state = state
        simulation.cancel()
        assert simulation.get_state() == SimulationState.INACTIVE
