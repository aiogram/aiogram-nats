from typing import Any, Dict, Optional

import ormsgpack
from aiogram import Bot
from aiogram.fsm.state import State
from aiogram.fsm.storage.base import BaseStorage, StorageKey, StateType
from nats.aio.client import Client
from nats.js.errors import NotFoundError
from nats.js.kv import KeyValue


# Source:
# https://github.com/Vermilonik/NatsWithFsmAiogram/blob/c8447a171c3e8ca2be8bb4aefd71a2d841962800/Entry.py
class NATSFSMStorage(BaseStorage):
    def __init__(self, nc: Client, kv_states: KeyValue, kv_data: KeyValue):
        super().__init__()
        self.nc = nc
        self.kv_states = kv_states
        self.kv_data = kv_data

    @staticmethod
    def _key_formatter(key: StorageKey) -> str:
        return f"{key.bot_id}:{key.user_id}:{key.chat_id}:{key.destiny}"

    async def set_state(
        self, bot: Bot, key: StorageKey, state: Optional[StateType] = None
    ) -> None:
        state = state.state if isinstance(state, State) else state
        await self.kv_states.put(
            self._key_formatter(key), ormsgpack.packb(state or None)
        )

    async def get_state(self, bot: Bot, key: StorageKey) -> Optional[str]:
        try:
            entry = await self.kv_states.get(self._key_formatter(key))
            state = ormsgpack.unpackb(entry.value) if entry.value else None
            return state if isinstance(state, str) else None
        except NotFoundError:
            return None

    async def set_data(self, bot: Bot, key: StorageKey, data: Dict[str, Any]) -> None:
        await self.kv_data.put(self._key_formatter(key), ormsgpack.packb(data))

    async def get_data(self, bot: Bot, key: StorageKey) -> Dict[str, Any]:
        try:
            entry = await self.kv_data.get(self._key_formatter(key))
            data = ormsgpack.unpackb(entry.value) if entry.value else {}
            return data if isinstance(data, dict) else {}
        except NotFoundError:
            return {}

    async def close(self) -> None:
        await self.nc.close()
