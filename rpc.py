import time
import json
import ssl
import urllib.request
import sys
import psutil
from pypresence import exceptions as pypresenceException
from pypresence import Presence
from pymem import exception as pymemException
import gameinfo
from logs import logger

SSLCONTEXT = ssl.create_default_context()
SSLCONTEXT.check_hostname = False
SSLCONTEXT.verify_mode = ssl.CERT_NONE

CLIENT_ID = '699358451494682714'
RPC = Presence(CLIENT_ID)

def fetch_data(cmdline_again, keys):
    identifier = cmdline_again.strip('/')

    # Use find, cuz someone maybe will do a server on localhost with different port
    lhostmatch = identifier.find("aos://16777343")
    if lhostmatch != -1:
        # If player plays on localhost then just pass this info and done
        if keys[0] == 'name':
            return ['(Playing on localhost)', '-', '-', '-', '-', '-']
    else:
        # Request json serverlist that buildandshoot hosts.
        serverlist_url = "https://services.buildandshoot.com/serverlist.json"
        try:
            req = urllib.request.urlopen(serverlist_url, context=SSLCONTEXT)
        except urllib.error.URLError:
            logger.warning('No internet connection.')
            time.sleep(5)
            return
        data = req.read()
        enc = req.info().get_content_charset('utf-8')
        serverlist = json.loads(data.decode(enc))

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
            return ['(Server is not broadcasting to master)', '-', '-', '-', '-', '-']

def update_presence(pid, cmdline):
    playtime_start = time.time()
    current_map = None
    logger.info('Process found. Starting presence.')
    while pid is not None:
        # Check if the process still exists. If not, then go back to process searching.
        if psutil.pid_exists(pid) is False:
            logger.info('Process was closed. Clearing presence.')
            RPC.clear(pid=pid)
            scan_for_process()

        logger.debug('Fetching server data')
        server_info = fetch_data(cmdline, ['name', 'map', 'game_mode', 'players_current', 'players_max', 'game_version'])

        # Assign every element from returned table (just for readability)
        server_name = server_info[0]
        server_map = server_info[1]
        server_game_mode = server_info[2]
        server_players_current = server_info[3]
        server_players_max = server_info[4]
        server_game_version = server_info[5]

        if server_map != current_map:
            # reset playtime if map will change
            playtime_start = time.time()
            logger.debug("Playtime was reset due to map change")
        current_map = server_map

        logger.info('Updating presence.')
        try:
            current_weapon = gameinfo.update(pid=pid, version=server_game_version)
            if current_weapon[0] != 'ace_of_spades':
                s_image = 'ace_of_spades'
                s_text = 'Players: {}/{}, Version: {}'.format(server_players_current,
                                                              server_players_max,
                                                              server_game_version)
            else:
                s_image = None
                s_text = None

            logger.debug(RPC.update(pid=pid,
                                    details=server_name,
                                    state='Map: {} ({})'.format(server_map, server_game_mode),
                                    start=playtime_start,
                                    large_image=current_weapon[0],
                                    large_text=current_weapon[1],
                                    small_image=s_image,
                                    small_text=s_text))
        except pypresenceException.InvalidID:
            logger.warning('Discord is not running, or client ID isn\'t valid.')
            RPC.clear(pid=pid)
            RPC.close()
            connect_discord()
        except pymemException.CouldNotOpenProcess:
            logger.info('Could not open process.')
            RPC.clear(pid=pid)
            scan_for_process()
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
                except IndexError:
                    break
                update_presence(ps_pid, ps_cmdline)
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
            logger.info('Waiting for discord.')
            time.sleep(5)
        except pypresenceException.InvalidPipe:
            time.sleep(5)

if __name__ == "__main__":
    try:
        connect_discord()
    except KeyboardInterrupt:
        logger.warning('Interrupt caught. Closing.')
        sys.exit(0)
