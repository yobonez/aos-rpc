import time
import json
import ssl
import urllib.request
import sys
import psutil
from pypresence import exceptions as pypresenceException
from pypresence import Presence
import pymem
import gameinfo
from logs import logger

SSLCONTEXT = ssl.create_default_context()
SSLCONTEXT.check_hostname = False
SSLCONTEXT.verify_mode = ssl.CERT_NONE

CLIENT_ID = '699358451494682714'
RPC = Presence(CLIENT_ID)

join_button = True

def clear_rpc(rpc_pid):
    '''for two exceptions in update_presence() to keep code a bit cleaner'''

    logger.info("Process was closed. Clearing presence.")
    try:
        RPC.clear(pid=rpc_pid)
    except AttributeError:
        pass
    return


def fetch_data(cmdline_again, keys):
    global join_button
    join_button = True
    identifier = cmdline_again.strip('/')

    lhostmatch = identifier.find("aos://16777343")

    if lhostmatch != -1 and keys[0] == 'name':
        # If player plays on localhost then just pass this info and done
        join_button = False
        return ['(Playing on localhost)', '-', '-', '-', '-', '-']
    else:
        try:
            # Request json serverlist that buildandshoot hosts.
            request = urllib.request.urlopen("https://services.buildandshoot.com/serverlist.json", context=SSLCONTEXT)
        except urllib.error.URLError:
            logger.warning('No internet connection.')
            time.sleep(5)
            return

        data = request.read()
        encoding = request.info().get_content_charset('utf-8')
        serverlist = json.loads(data.decode(encoding))

        try:
            for server_num in range(0, len(serverlist)+1):
                presence_info = []

                if serverlist[server_num]['identifier'] == identifier:
                    current_server = serverlist[server_num]
                    for variable in keys:
                        presence_info.append(current_server[variable])

                if len(presence_info) == 6:
                    return presence_info
        except IndexError:
            join_button = False
            return ['(Server is not broadcasting to master server)', '-', '-', '-', '-', '-']

def update_presence(pid, cmdline, p_handle):
    playtime_start = time.time()
    current_map = None

    logger.info('Process found. Starting presence.')

    while pid is not None:
        # Check if the process still exists. If not, then go back to process searching.
        if psutil.pid_exists(pid) is False:
            logger.info('Process was closed. Clearing presence.')
            RPC.clear(pid=pid)
            return

        try:
            logger.debug('Getting base address.')
            base_addr = p_handle.process_base.lpBaseOfDll
        except pymem.exception.ProcessNotFound:
            clear_rpc(pid)
        except pymem.exception.ProcessError:
            clear_rpc(pid)

        logger.debug('Fetching server data')
        server_info = fetch_data(cmdline, ['name', 'map', 'game_mode', 'players_current', 'players_max', 'game_version'])

        server_name = server_info[0]
        server_map = server_info[1]
        server_game_mode = server_info[2]
        server_players_current = server_info[3]
        server_players_max = server_info[4]
        server_game_version = server_info[5]

        if server_map != current_map:
            # reset the "time elapsed" when map changes
            playtime_start = time.time()
            logger.debug("Map changed. Resetting \"time elapsed\".")
        current_map = server_map

        logger.info('Updating presence.')

        try:
            player_status = gameinfo.update(pid=pid, version=server_game_version, proc_handle=p_handle, base_address=base_addr)

            if player_status[0][0] != 'ace_of_spades':
                s_image = 'ace_of_spades'
                s_additional_text = ''

                if server_game_mode in ('tow', 'tc'):
                    pass
                elif player_status[1]: # if holds_intel from gameinfo.update() is true
                    s_image = 'smallimagekey_intel'
                    s_additional_text = 'Holds enemy intel!'

                s_text = '{} Players: {}/{}, Version: {}'.format(s_additional_text,
                                                                 server_players_current,
                                                                 server_players_max,
                                                                 server_game_version)
            else:
                s_image = None
                s_text = None

            logger.debug(RPC.update(pid=pid,
                                    details=server_name,
                                    state='Map: {} ({})'.format(server_map, server_game_mode),
                                    start=playtime_start,
                                    large_image=player_status[0][0],
                                    large_text=player_status[0][1],
                                    small_image=s_image,
                                    small_text=s_text,
                                    buttons = [{"label": "Join", "url": cmdline}, {"label": "Server list", "url": "http://aos.acornserver.com"}] if join_button else None ))
        except pypresenceException.InvalidID:
            logger.warning('Discord is not running, or client ID isn\'t valid.')
            RPC.clear(pid=pid)
            RPC.close()
            connect_discord()
        except pymem.exception.CouldNotOpenProcess:
            logger.info('Could not open process.')
            RPC.clear(pid=pid)
            return
        except pypresenceException.ServerError:
            logger.warning('Button load fail')
            RPC.clear(pid=pid)
            return

        time.sleep(7.5)

def scan_for_process():
    logger.info('Waiting for aos client.')

    ps_pid = None
    ps_cmdline = None

    while True:
        # Iterate thru processes to find one that matches our wanted one
        # and assign important variables for further functions that will be executed
        for proc in psutil.process_iter(['name', 'pid', 'cmdline']):
            if proc.info['name'] == 'client.exe':
                ps_pid = proc.info['pid']

                try:
                    ps_cmdline = proc.info['cmdline'][1] # This is the server identifier "aos://XXXXXXXXXX:XXXXX"

                    handle = pymem.Pymem('client.exe')
                    if handle.process_id != ps_pid:
                        logger.info("Not a valid aos process.")
                        return
                        
                except IndexError:
                    break
                except pymem.exception.ProcessNotFound:
                    break
                except pymem.exception.CouldNotOpenProcess:
                    break

                update_presence(ps_pid, ps_cmdline, handle)
            else:
                time.sleep(0.05)

def connect_discord():
    logger.info('Waiting for discord')
    while True:
        try:
            RPC.connect()
            logger.info('Connected to Discord.')
            scan_for_process()
        except pypresenceException.InvalidID:
            logger.info('Discord is not running, or client ID isn\'t valid.')
            time.sleep(5)
        except pypresenceException.InvalidPipe:
            time.sleep(5)
        except pypresenceException.PipeClosed:
            time.sleep(5)

if __name__ == "__main__":
    try:
        connect_discord()
    except KeyboardInterrupt:
        logger.warning('KeyboardInterrupt caught. Closing.')
        sys.exit(0)
