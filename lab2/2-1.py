# 1 import statements
from utime import ticks_ms
from microbit import *
import music

ON = Image.SQUARE
OFF = Image.SQUARE_SMALL

# 2 base state machine
class StateMachine:
    """
    The following code segment defines a basis state machine.
    Leave this code as it is. (Or be careful what you do.)"""

    def __init__(self, timer_names=["t1", "t2", "t3"]):
        self.active = False
        self.state = "initial"
        self.timer_names = timer_names
        self.timers = {}

    def _ticks_ms(self):
        # return int(round(time() * 1000))
        return ticks_ms()

    def initial_transition(self, timers):
        """Overwrite this method to define the initial transition.
        Must return the name of the first state."""
        return None

    def transition(self, state, event, timers):
        """Overwrite this method to define the transitions.

        `state` - the current state
        `event` - the triggering event
        `timers` - to start and stop timers

        Return the name of the next state,
        or None to stay in current state."""
        return None

    def start(self, name, timeout):
        """Start a timer.
        The name must be t1, t2 or t2.
        The timeout is given in milliseconds.
        """
        self.timers[name] = self._ticks_ms() + timeout

    def stop(self, name):
        """Stop a timer."""
        self.timers[name] = None

    def _detect_event(self):
        now = self._ticks_ms()
        for timer in self.timer_names:
            if (timer in self.timers) and (self.timers[timer] is not None):
                if self.timers[timer] < now:
                    self.timers[timer] = None
                    return timer
        if button_a.was_pressed():
            return "button_a"
        if button_b.was_pressed():
            return "button_b"
        if accelerometer.was_gesture("shake"):
            return "shake"
        if pin_logo.is_touched():
            return "touch"
        return None

    def run(self):
        """Run the state machine."""
        self.active = True
        while self.active:
            if self.state == "initial":
                next_state = self.initial_transition(self)
                if next_state:
                    if next_state == "final":
                        self.active = False
                    self.state = next_state
            event = self._detect_event()
            if event is not None:
                next_state = self.transition(self.state, event, self)
                if next_state:
                    self.state = next_state
            sleep(100)
            
class Dispenser(StateMachine):
    
    def initial_transition(self, timers):
        display.show("R")
        return "ready"

    def transition(self, state, event, timers):
        if state == "ready":
            if event == "touch":
                display.show(Image.ARROW_S)
                music.play("C2:8")
                timers.start("t1",800)
                return "dispensing"
        if state == "dispensing":
            if event == "t1":
                display.clear()
                timers.start("t2",2000)
                music.play(["C4:4","C4:4"])
                return "timelock"
        if state == "timelock":
            if event == "t2":
                display.show("R")
                return "ready"
                
stm = Dispenser()
stm.run()