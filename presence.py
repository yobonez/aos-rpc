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

def fetch_data(cmdline_again, key):
    # If player plays on localhost then just pass this info and done
    lhostmatch = cmdline_again.find("aos://16777343")
    if lhostmatch != -1:
        if key == 'name':
            return '(Playing on localhost)'
        else:
            return '-'
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

        # Removing "/" at the end of the server identifier to avoid an index out of range error
        # that is being thrown for some reason idk
        server_identifier = cmdline_again.strip("/")

        count = 0
        while True:
            # If the identifier from the serverlist matches with the current server player is on,
            # get the requested by function "keep_alive" 'key' in function "fetch_data", compare it with key
            # from serverlist and return it.
            # For example key is the 'name' or 'game_mode'.
            try:
                if serverlist[count]['identifier'] == server_identifier:
                    variable = serverlist[count][key]
                    return variable
                else:
                    count += 1
            # If the list is out of range and nothing found, that means the server is not broadcasting
            # itself to master so we need to handle that
            except IndexError:
                if key == 'name':
                    return '(Server isn\'t being broadcasted to master server)'
                else:
                    return '-'

def keep_alive(pid, cmdline):
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
        server_name = fetch_data(cmdline, 'name') # request server name key from serverlist
        server_map = fetch_data(cmdline, 'map') # same for here but for map etc.
        server_game_mode = fetch_data(cmdline, 'game_mode')
        server_players_current = fetch_data(cmdline, 'players_current')
        server_players_max = fetch_data(cmdline, 'players_max')
        server_protocol_version = fetch_data(cmdline, 'game_version')

        if server_map != current_map:
            # reset playtime if next map was changed
            playtime_start = time.time()
            logger.debug("Playtime was reset due to map change")
        current_map = server_map

        logger.info('Updating presence.')
        try:
            current_weapon = gameinfo.update(pid=pid, version=server_protocol_version)
            logger.debug(RPC.update(pid=pid,
                                    details=server_name,
                                    state='Map: {} ({})'.format(server_map, server_game_mode),
                                    start=playtime_start,
                                    large_image=current_weapon[0],
                                    large_text=current_weapon[1],
                                    small_image='ace_of_spades',
                                    small_text='Players: {}/{}, Version: {}'.format(server_players_current,
                                                                                    server_players_max,
                                                                                    server_protocol_version)))
        except pypresenceException.InvalidID:
            logger.warning('Discord is not running, or client ID isn\'t valid.')
            RPC.clear(pid=pid)
            RPC.close()
            connect_discord()
        except pymemException.CouldNotOpenProcess:
            logger.info('Could not open process.')
            RPC.clear(pid=pid)
            scan_for_process()
        time.sleep(10)

def scan_for_process():
    logger.info('Waiting for aos client.')
    ps_pid = None
    ps_cmdline = None
    while True:
        # Iterate thru processes to find one that matches our wanted one
        # and assign important variables for further functions that will be executed
        for p in psutil.process_iter(['name', 'pid', 'cmdline']):
            if p.info['name'] == 'client.exe':
                ps_pid = p.info['pid']
                try:
                    ps_cmdline = p.info['cmdline'][1] # This is the server identifier "aos://XXXXXXXXXX:XXXXX"
                except IndexError:
                    break
                keep_alive(ps_pid, ps_cmdline)
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
        except pypresenceException.InvalidPipe:
            time.sleep(5)

if __name__ == "__main__":
    try:
        connect_discord()
    except KeyboardInterrupt:
        logger.warning('Interrupt caught. Closing.')
        sys.exit(0)
