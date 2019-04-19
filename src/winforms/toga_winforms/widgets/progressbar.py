
from travertino.size import at_least

from toga_winforms.libs import WinForms

from .base import Widget

from datetime import datetime, timedelta


PROGRESSBAR_MINIMUM_INTERNAL = 0
PROGRESSBAR_MAXIMUM_INTERNAL = 100
PROGRESSBAR_STEP_INTERNAL = 1
PROGRESSBAR_TICK_INTERNAL = 50  # milliseconds


class ProgressBar(Widget):
    def create(self):
        self.native = WinForms.ProgressBar()
        self.native.interface = self.interface
        self.native.Minimum = PROGRESSBAR_MINIMUM_INTERNAL
        self.native.Maximum = PROGRESSBAR_MAXIMUM_INTERNAL
        self.native.Step = PROGRESSBAR_STEP_INTERNAL

    def _normalize_value(self):
        return ((self.interface.value - PROGRESSBAR_MINIMUM_INTERNAL) / (self.interface.max - PROGRESSBAR_MINIMUM_INTERNAL)) * (PROGRESSBAR_MAXIMUM_INTERNAL - PROGRESSBAR_MINIMUM_INTERNAL) + PROGRESSBAR_MINIMUM_INTERNAL # noqa E501

    def start(self):

        def wait_to_update(duration, callback, current_value):
            while datetime.now() + timedelta(duration) < datetime.now():
                WinForms.Application.DoEvents()
            callback(current_value)

        def pulse(current_value):
            if current_value == self.native.Value:
                self.native.Value = PROGRESSBAR_MINIMUM_INTERNAL
            self.native.Value += PROGRESSBAR_STEP_INTERNAL

        if self.interface.is_determinate:
            self.native.Style = WinForms.ProgressBarStyle.Continuous
            wait_to_update(PROGRESSBAR_TICK_INTERNAL, pulse, self.native.Value)
        else:
            # place the progress bar in Marquee style
            self.native.Style = WinForms.ProgressBarStyle.Marquee

    def stop(self):
        self.native.Style = WinForms.ProgressBarStyle.Continuous
        self.native.Value = PROGRESSBAR_MINIMUM_INTERNAL

    def set_max(self, value):
        if value is None:
            self.native.Value = PROGRESSBAR_MINIMUM_INTERNAL
            self.set_enabled = True if self.is_running else False
        else:
            self.native.Maximum = value

    def set_value(self, value):
        # difference = value - self.native.Value
        # step = 1 if difference >= 0 else -1
        # for tick in range(0, difference, step):
        #     self.native.PerformStep()
        #     time.sleep(PROGRESSBAR_TICK_INTERNAL)
        self.native.Value = self._normalize_value()

    def rehint(self):
        # Height must be non-zero
        # Set a sensible min-width
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = self.native.PreferredSize.Height
