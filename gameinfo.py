import sys
import pymem
from logs import logger
from rpc import scan_for_process, RPC

WEAPON_ADDRS_PER_ID_75 = {
    0: 0x7ce5c,
    1: 0x7d204,
    2: 0x7d5ac,
    3: 0x7d954,
    4: 0x7dcfc,
    5: 0x7e0a4,
    6: 0x7e44c,
    7: 0x7e7f4,
    8: 0x7eb9c,
    9: 0x7ef44,
    10: 0x7f2ec,
    11: 0x7f694,
    12: 0x7fa3c,
    13: 0x7fde4,
    14: 0x8018c,
    15: 0x80534,
    16: 0x808dc,
    17: 0x80c84,
    18: 0x8102c,
    19: 0x813d4,
    20: 0x8177c,
    21: 0x81b24,
    22: 0x81ecc,
    23: 0x82274,
    24: 0x8261c,
    25: 0x829c4,
    26: 0x82d6c,
    27: 0x83114,
    28: 0x834bc,
    29: 0x83864,
    30: 0x83c0c,
    31: 0x83fb4,
    32: 0x8435c
}

WEAPON_ADDRS_PER_ID_76 = {
    0: 0x7bee8,
    1: 0x7c2f0,
    2: 0x7c6f8,
    3: 0x7cb00,
    4: 0x7cf08,
    5: 0x7d310,
    6: 0x7d718,
    7: 0x7db20,
    8: 0x7df28,
    9: 0x7e330,
    10: 0x7e738,
    11: 0x7eb40,
    12: 0x7ef48,
    13: 0x7f350,
    14: 0x7f758,
    15: 0x7fb60,
    16: 0x7ff68,
    17: 0x80370,
    18: 0x80778,
    19: 0x80b80,
    20: 0x80f88,
    21: 0x81390,
    22: 0x81798,
    23: 0x81ba0,
    24: 0x81fa8,
    25: 0x823b0,
    26: 0x827b8,
    27: 0x82bc0,
    28: 0x82fc8,
    29: 0x833d0,
    30: 0x837d8,
    31: 0x83be0,
    32: 0x83fe8
}

TOOLS = {
    0: ["largeimagekey_spade", "Digs blocks using spade"],
    1: ["largeimagekey_block", "Builds stuff with blocks"],
    3: ["largeimagekey_grenade", "Throws grenades"]
}

GUNS = {
    0: ["largeimagekey_rifle", "Shoots with Rifle"],
    1: ["largeimagekey_smg", "Shoots with SMG"],
    2: ["largeimagekey_shotgun", "Shoots with Shotgun"]
}

def update(pid, version):
    def return_weapon_or_tool(tool_value):
        if tool_value == 0:
            current_tool = TOOLS[tool_value]
        elif tool_value == 1:
            current_tool = TOOLS[tool_value]
        elif tool_value == 2:
            if version == '0.75':
                current_tool = GUNS[handle.read_int(base_addr+WEAPON_ADDRS_PER_ID_75[ply_id_75])]
            else:
                current_tool = GUNS[handle.read_int(base_addr+WEAPON_ADDRS_PER_ID_76[ply_id_76])]
        elif tool_value == 3:
            current_tool = TOOLS[tool_value]
        return current_tool
    try:
        try:
            handle = pymem.Pymem('client.exe')
            logger.debug('Getting base address.')
            base_addr = handle.process_base.lpBaseOfDll

            if handle.process_id != pid:
                logger.info("Not a valid aos process.")
                scan_for_process()

        except pymem.exception.ProcessNotFound:
            logger.info("Process was closed. Clearing presence.")
            try:
                RPC.clear(pid=pid)
            except AttributeError:
                pass
            scan_for_process()
        except pymem.exception.ProcessError:
            logger.debug('Process was closed. Clearing presence.')
            try:
                RPC.clear(pid=pid)
            except AttributeError:
                pass
            scan_for_process()

        ply_id_75 = handle.read_int(base_addr+0x13B1CF0)
        ply_id_76 = handle.read_int(base_addr+0x13B19B0)
        tool_value_75 = handle.read_int(base_addr+0x13CF808)
        tool_value_76 = handle.read_int(base_addr+0x13CF488)

        if version == '0.75':
            curr_tool = return_weapon_or_tool(tool_value_75)
        elif version == '0.76':
            curr_tool = return_weapon_or_tool(tool_value_76)
        else:
            curr_tool = ["ace_of_spades", "(Server is not broadcasting to master)"]
        handle.close_process()
        return curr_tool

    except KeyboardInterrupt:
        logger.warning('Interrupt caught. Closing.')
        RPC.clear(pid=pid)
        RPC.close()
        try:
            handle.close_process()
        except pymem.exception.ProcessError:
            sys.exit(0)
        sys.exit(0)
