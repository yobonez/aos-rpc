import sys
import pymem
from logs import logger
from rpc import scan_for_process, RPC

tools = {
    0: ["largeimagekey_spade", "Digging blocks with a spade"],
    1: ["largeimagekey_block", "Building stuff with blocks"],
    2: ["largeimagekey_weapon", "Killing enemies with a weapon"],
    3: ["largeimagekey_grenade", "Destroying enemy forces with grenades"]
}

def update(pid, version):
    def game_version(tool_value):
        if tool_value == 0:
            current_tool = tools[tool_value]
        elif tool_value == 1:
            current_tool = tools[tool_value]
        elif tool_value == 2:
            current_tool = tools[tool_value]
        elif tool_value == 3:
            current_tool = tools[tool_value]
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

        tool_value_75 = handle.read_int(base_addr+0x13CF808)
        tool_value_76 = handle.read_int(base_addr+0x13CF488)

        if version == '0.75':
            curr_tool = game_version(tool_value_75)
        else:
            curr_tool = game_version(tool_value_76)
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
