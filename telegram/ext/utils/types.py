#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2021
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
"""This module contains custom typing aliases."""
from typing import TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from telegram.ext import CallbackContext  # noqa: F401

CCT = TypeVar('CCT', bound='CallbackContext')
"""An instance of :class:`telegram.ext.CallbackContext` or a custom subclass."""
UD = TypeVar('UD')
"""Type of the user data for a single user."""
CD = TypeVar('CD')
"""Type of the chat data for a single user."""
BD = TypeVar('BD')
"""Type of the bot data."""