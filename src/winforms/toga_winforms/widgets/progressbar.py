
from travertino.size import at_least

from toga_winforms.libs import WinForms

from .base import Widget

from datetime import datetime, timedelta


PROGRESSBAR_MINIMUM_INTERNAL = 0
PROGRESSBAR_MAXIMUM_INTERNAL = 100
PROGRESSBAR_STEP_INTERNAL = -1
PROGRESSBAR_TICK_INTERNAL = 100  # milliseconds


class ProgressBar(Widget):
    def create(self):
        self.native = WinForms.ProgressBar()
        self.native.interface = self.interface
        self.native.Minimum = PROGRESSBAR_MINIMUM_INTERNAL
        self.native.Step = PROGRESSBAR_STEP_INTERNAL

    def _normalize_value(self, value):
        return ((value - PROGRESSBAR_MINIMUM_INTERNAL) / (self.interface.max - PROGRESSBAR_MINIMUM_INTERNAL)) * (PROGRESSBAR_MAXIMUM_INTERNAL - PROGRESSBAR_MINIMUM_INTERNAL) + PROGRESSBAR_MINIMUM_INTERNAL # noqa E501

    def _wait_to_update(self, callback):
        while self.interface.is_running:
            desired = datetime.now() + timedelta(PROGRESSBAR_TICK_INTERNAL)
            while desired < datetime.now():
                # continute running event loop
                # until ready to update bar
                WinForms.Application.DoEvents()
            callback()

    def _pulse(self):
        if self.native.Value == self._normalize_value(self.interface.value) or self.native.Value == PROGRESSBAR_MINIMUM_INTERNAL: #noqa E501
            # the pulse has reached the current or minimum value
            # invert the step direction
            self.native.Step *= -1
        self.native.PerformStep()

    def start(self):
        #self.native.Value = PROGRESSBAR_MINIMUM_INTERNAL
        self.native.Style = WinForms.ProgressBarStyle.Continuous
        self.interface._is_running = True
        self._wait_to_update(self._pulse)


        # self.native.MarqueeAnimationSpeed = PROGRESSBAR_TICK_INTERNAL
        # self.native.Style = WinForms.ProgressBarStyle.Marquee

        # if self.interface.is_determinate:
        #     self.native.Style = WinForms.ProgressBarStyle.Continuous
        #     self._wait_to_update(PROGRESSBAR_TICK_INTERNAL, self._pulse)
        # else:
        #     # place the progress bar in Marquee mode
        #     self.native.MarqueeAnimationSpeed = PROGRESSBAR_TICK_INTERNAL
        #     self.native.Style = WinForms.ProgressBarStyle.Marquee

    def stop(self):
        self.native.Style = WinForms.ProgressBarStyle.Continuous
        self.native.Value = PROGRESSBAR_MINIMUM_INTERNAL

    def set_max(self, value):
        if value is None:
            self.set_enabled = True if self.is_running else False
        else:
            self.native.Maximum = self._normalize_value(value)

    def set_value(self, value):
        self.native.Value = self._normalize_value(value)

    def rehint(self):
        # Height must be non-zero
        # Set a sensible min-width
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = self.native.PreferredSize.Height
