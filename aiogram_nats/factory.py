from nats.aio.client import Client

from aiogram_nats import NATSFSMStorage


async def create_nats_fsm_storage(
        nc: Client,
        states_kv_name: str = "fsm_states_aiogram",
        data_kv_name: str = "fsm_data_aiogram",
) -> NATSFSMStorage:
    """
    Create NATSFSMStorage instance
    You have to manually create key-value stores for aiogram states and data
    :param nc: NATS client instance
    :param states_kv_name: name of the key-value store for aiogram states
    :param data_kv_name: name of the key-value store for aiogram data
    :return: NATSFSMStorage instance
    """
    js = nc.jetstream()
    kv_states = await js.key_value(states_kv_name)
    kv_data = await js.key_value(data_kv_name)
    return NATSFSMStorage(nc, kv_states, kv_data)
