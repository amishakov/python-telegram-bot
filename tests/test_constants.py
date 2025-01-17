#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2022
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
import json
from enum import IntEnum

import pytest
from flaky import flaky

from telegram import constants
from telegram._utils.enum import StringEnum
from telegram.error import BadRequest
from tests.conftest import data_file


class StrEnumTest(StringEnum):
    FOO = "foo"
    BAR = "bar"


class IntEnumTest(IntEnum):
    FOO = 1
    BAR = 2


class TestConstants:
    """Also test _utils.enum.StringEnum on the fly because tg.constants is currently the only
    place where that class is used."""

    def test__all__(self):
        expected = {
            key
            for key, member in constants.__dict__.items()
            if (
                not key.startswith("_")
                # exclude imported stuff
                and getattr(member, "__module__", "telegram.constants") == "telegram.constants"
            )
        }
        actual = set(constants.__all__)
        assert (
            actual == expected
        ), f"Members {expected - actual} were not listed in constants.__all__"

    def test_to_json(self):
        assert json.dumps(StrEnumTest.FOO) == json.dumps("foo")
        assert json.dumps(IntEnumTest.FOO) == json.dumps(1)

    def test_string_representation(self):
        assert repr(StrEnumTest.FOO) == "<StrEnumTest.FOO>"
        assert str(StrEnumTest.FOO) == "StrEnumTest.FOO"

    def test_string_inheritance(self):
        assert isinstance(StrEnumTest.FOO, str)
        assert StrEnumTest.FOO + StrEnumTest.BAR == "foobar"
        assert StrEnumTest.FOO.replace("o", "a") == "faa"

        assert StrEnumTest.FOO == StrEnumTest.FOO
        assert StrEnumTest.FOO == "foo"
        assert StrEnumTest.FOO != StrEnumTest.BAR
        assert StrEnumTest.FOO != "bar"
        assert StrEnumTest.FOO != object()

        assert hash(StrEnumTest.FOO) == hash("foo")

    def test_int_inheritance(self):
        assert isinstance(IntEnumTest.FOO, int)
        assert IntEnumTest.FOO + IntEnumTest.BAR == 3

        assert IntEnumTest.FOO == IntEnumTest.FOO
        assert IntEnumTest.FOO == 1
        assert IntEnumTest.FOO != IntEnumTest.BAR
        assert IntEnumTest.FOO != 2
        assert IntEnumTest.FOO != object()

        assert hash(IntEnumTest.FOO) == hash(1)

    @flaky(3, 1)
    async def test_max_message_length(self, bot, chat_id):
        await bot.send_message(chat_id=chat_id, text="a" * constants.MessageLimit.TEXT_LENGTH)

        with pytest.raises(
            BadRequest,
            match="Message is too long",
        ):
            await bot.send_message(
                chat_id=chat_id, text="a" * (constants.MessageLimit.TEXT_LENGTH + 1)
            )

    @flaky(3, 1)
    @pytest.mark.xfail(reason="Telegram apparently changed the limit without documenting it yet.")
    async def test_max_caption_length(self, bot, chat_id):
        good_caption = "a" * constants.MessageLimit.CAPTION_LENGTH
        with data_file("telegram.png").open("rb") as f:
            good_msg = await bot.send_photo(photo=f, caption=good_caption, chat_id=chat_id)
        assert good_msg.caption == good_caption

        bad_caption = good_caption + "Z"
        match = "Media_caption_too_long"
        with pytest.raises(BadRequest, match=match), data_file("telegram.png").open("rb") as f:
            await bot.send_photo(photo=f, caption=bad_caption, chat_id=chat_id)
