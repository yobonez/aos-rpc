import sys
import pymem
from logs import logger
from rpc import RPC
import dicts

def update(pid, version, proc_handle, base_address):
    def return_weapon_or_tool(ply_id, ply_team, tool_id, ply_intel_status):
        holds_intel = False

        if ply_id == -1:
            current_tool = ["largeimagekey_loading", "Loading map..."]
            return [current_tool, holds_intel]

        if ply_team == -2:
            current_tool = ["largeimagekey_teamselection", "Choosing team"]
        elif ply_team == -1:
            current_tool = ["largeimagekey_spectating", "Spectating"]
        else:
            if tool_id == 2:
                current_tool = dicts.GUNS[proc_handle.read_int(base_address+dicts.WEAPON_ADDRS_PER_ID_75[ply_id])]
            else:
                current_tool = dicts.TOOLS[tool_id]

            if ply_intel_status[0] == ply_id or ply_intel_status[1] == ply_id: # if team1 id == playerId or team2 id == playerId
                holds_intel = True

            return [current_tool, holds_intel]
        return [current_tool, holds_intel]

    # inside update()
    try:
        if version == '0.75':
            ply_id_75 = proc_handle.read_int(base_address+0x13B1CF0)
            tool_id_75 = proc_handle.read_int(base_address+0x13CF808)
            ply_intel_status_team1_75 = proc_handle.read_int(base_address+0x13CF958) # it gives the ID of a player that holds an intel from team 1
            ply_intel_status_team2_75 = proc_handle.read_int(base_address+0x13CF924) # < - same here but team 2

            if ply_id_75 == -1:
                ply_team_75 = None
            else:
                ply_team_75 = proc_handle.read_int(base_address+dicts.TEAM_ADDRS_PER_ID_75[ply_id_75])

            ply_status = return_weapon_or_tool(ply_id_75, ply_team_75, tool_id_75, [ply_intel_status_team1_75, ply_intel_status_team2_75])

        elif version == '0.76':
            ply_id_76 = proc_handle.read_int(base_address+0x13B19B0)
            tool_id_76 = proc_handle.read_int(base_address+0x13CF488)
            ply_intel_status_team1_76 = proc_handle.read_int(base_address+0x13CF5D8) # here same thing but for another version
            ply_intel_status_team2_76 = proc_handle.read_int(base_address+0x13CF5A4)

            if ply_id_76 == -1:
                ply_team_76 = None
            else:
                ply_team_76 = proc_handle.read_int(base_address+dicts.TEAM_ADDRS_PER_ID_76[ply_id_76])

            ply_status = return_weapon_or_tool(ply_id_76, ply_team_76, tool_id_76, [ply_intel_status_team1_76, ply_intel_status_team2_76])

        else:
            ply_status = [["ace_of_spades", "(Server is not broadcasting to master server)"], None]

        return ply_status

    except KeyboardInterrupt:
        logger.warning('KeyboardInterrupt caught. Closing.')
        RPC.clear(pid=pid)
        RPC.close()
        try:
            proc_handle.close_process()
        except pymem.exception.ProcessError:
            sys.exit(0)
        sys.exit(0)
