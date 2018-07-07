"""
This module provides a few buttons for an easy pygame GUI.
"""

import pygame
from _thread import start_new_thread
from time import time, sleep

from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION

from GUI.base import BaseWidget
from GUI.colors import bw_contrasted, mix
from GUI.draw import circle, roundrect
from GUI.font import Font
from GUI.locals import CENTER, BLUE, LIGHT_GREY, BLACK, ORANGE, GREEN
from GUI.text import SimpleText
from GUI.vracabulous import Separator


class BaseButton(BaseWidget):
    """Abstract base class for any button"""

    CALL_ON_PRESS = 1
    THREADED_CALL = 2

    def __init__(self, func, pos, size, anchor, flags=0):
        """
        Creates a new BaseButton object.

        :param func: calback function that takes no argument
        :param pos: the widget pos. Can be a callable or a 2-tuple
        :param size: the width size. Can be a callable or a 2-tuple
        :param flags: Can be:
            - CALL_ON_PRESS if you want func to be call when the button is pressed instead of when it's released
            - THREADED_CALL if you want func to be called in a thread
            You can pass multiple flags with the pipe operator |
        """
        super().__init__(pos, size, anchor)
        self.func = func
        self.flags = flags

    def click(self, force_no_call=False, milis=None):
        """
        Call when the button is pressed. This start the callback function in a thread
        If :milis is given, will release the button after :milis miliseconds
        """

        if self.clicked:
            return False

        if not force_no_call and self.flags & self.CALL_ON_PRESS:
            if self.flags & self.THREADED_CALL:
                start_new_thread(self.func, ())
            else:
                self.func()

        super().click()

        if milis is not None:
            start_new_thread(self.release, (), {'milis': milis})

    def release(self, force_no_call=False, milis=0):
        """
        Call this when the button is released
        Blocks for :milis miliseconds (used by .press() for auto release)
        """
        if not self.clicked:
            return False

        if milis:
            sleep(milis/1000)

        super().release()

        if force_no_call:
            return

        if not self.flags & self.CALL_ON_PRESS:
            if self.flags & self.THREADED_CALL:
                start_new_thread(self.func, ())
            else:
                self.func()

    def render(self, surf):
        raise NotImplementedError


class Button(BaseButton):
    """A basic button."""

    NO_MOVE = 4
    NO_SHADOW = 8
    NO_ROUNDING = 16
    NO_HOVER = 32

    def __init__(self, func, pos, size, text='', color=GREEN, anchor=CENTER, takeArg = False, enable = True, flags=0):
        """
        Creates a clickable button.

        :param func: callback function with no arguments
        :param size: widget size. Can be a callable or a 2-tuple.
        :param pos: widget position. Can be a callable or a 2-tuple.
        :param anchor: widget anchor
        :param text: Text to be displayed on the button
        :param color: the natural color of the button
        :param flags: see BaseButton
        """

        super().__init__(func, pos, size, anchor, flags)

        self.color = color
        self.hovered = False
        self.hover_enabled = True
        self.pressed = False
        self.takesArg = takeArg
        self._arg = None
        self._isEnabled = enable
        self.text = SimpleText(text, lambda: self.center, bw_contrasted(self.color), self.color,
                               Font(self.height - 6, unit=Font.PIXEL))

    @property
    def isEnabled(self):
        return self._isEnabled

    @isEnabled.setter
    def isEnabled(self, value):
        if not isinstance(value, bool):
            raise TypeError("Value must be a boolean type. Got "+ str(type(value))+" instead.")

    @property
    def arg(self):
        return self._arg

    @arg.setter
    def arg(self, value):
        if self.takesArg == False:
            raise KeyError("This button does not take arguments")
        else:
            self._arg = value

    def click(self, force_no_call=False, milis=None):
        """
        Call when the button is pressed. This start the callback function in a thread
        If :milis is given, will release the button after :milis miliseconds
        Completely overridden because the super class's method did not take arguments
        """
        if not self.isEnabled:
            return False

        if self.clicked:
            return False

        if not force_no_call and self.flags & self.CALL_ON_PRESS:
            if self.flags & self.THREADED_CALL:
                if self.takesArg:
                    start_new_thread(self.func, self.arg)
                else:
                    start_new_thread(self.func, ())
            else:
                if(self.takesArg):
                    self.func(self.arg)
                else: self.func()

        BaseWidget.click()

        if milis is not None:
            start_new_thread(self.release, (), {'milis': milis})

    def _get_color(self):
        """Return the color of the button, depending on its state"""
        if self.clicked and self.hovered:  # the mouse is over the button
            color = mix(self.color, BLACK, 0.8)

        elif self.hovered and not self.flags & self.NO_HOVER:
            color = mix(self.color, BLACK, 0.93)

        else:
            color = self.color

        self.text.bg_color = color
        return color

    @property
    def _front_delta(self):
        """Return the offset of the colored part."""
        if self.flags & self.NO_MOVE:
            return Separator(0, 0)

        if self.clicked and self.hovered:  # the mouse is over the button
            delta = 2

        elif self.hovered and not self.flags & self.NO_HOVER:
            delta = 0

        else:
            delta = 0

        return Separator(delta, delta)

    @property
    def _bg_delta(self):
        """Return the offset of the shadow."""
        if self.flags and self.NO_MOVE:
            return Separator(2, 2)

        if self.clicked and self.hovered:  # the mouse is over the button
            delta = 2

        elif self.hovered and not self.flags & self.NO_HOVER:
            delta = 2

        else:
            delta = 2

        return Separator(delta, delta)

    def update(self, event_or_list):
        """Update the button with the events."""

        for e in super().update(event_or_list):
            if e.type == MOUSEBUTTONDOWN:
                if e.pos in self:
                    self.click()
                else:
                    self.release(force_no_call=True)

            elif e.type == MOUSEBUTTONUP:
                self.release(force_no_call=e.pos not in self)

            elif e.type == MOUSEMOTION:
                if e.pos in self:
                    self.hovered = True
                else:
                    self.hovered = False

    def render(self, surf):
        """Render the button on a surface."""
        pos, size = self.topleft, self.size

        if not self.flags & self.NO_SHADOW:
            if self.flags & self.NO_ROUNDING:
                pygame.draw.rect(surf, LIGHT_GREY, (pos + self._bg_delta, size))
            else:
                roundrect(surf, (pos + self._bg_delta, size), LIGHT_GREY + (100,), 5)

        if self.flags & self.NO_ROUNDING:
            pygame.draw.rect(surf, self._get_color(), (pos + self._front_delta, size))
        else:
            roundrect(surf, (pos + self._front_delta, size), self._get_color(), 5)

        self.text.center = self.center + self._front_delta
        self.text.render(surf)

