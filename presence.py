import time
import json
import ssl
import urllib.request
import psutil
from pypresence import Presence

SSLCONTEXT = ssl.create_default_context()
SSLCONTEXT.check_hostname = False
SSLCONTEXT.verify_mode = ssl.CERT_NONE

CLIENT_ID = '699358451494682714'
AOS_RPC = Presence(CLIENT_ID)
AOS_RPC.connect()

def fetch_data(cmdline_again, key):
    # Request json serverlist that buildandshoot hosts.
    serverlist_url = "https://services.buildandshoot.com/serverlist.json"
    req = urllib.request.urlopen(serverlist_url, context=SSLCONTEXT)
    data = req.read()
    enc = req.info().get_content_charset('utf-8')
    json_obj = json.loads(data.decode(enc))

    # Add localhost identifier to serverlist:
    with open("localhost.json") as file:
        data = json.load(file)
    json_obj.append(data)
    file.close()
    count = 0

    # Removing "/" at the end of the server identifier to avoid an index out of range error
    # that is being thrown for some reason idk
    server_identifier = cmdline_again.strip("/")

    while True:
        # If the identifier from the serverlist matches with the current server player is on,
        # get the requested by function "keep_alive" 'key' in function "fetch_data", compare it with key
        # from serverlist and return it.
        # For example key is the 'name' or 'game_mode'.
        try:
            if json_obj[count]['identifier'] == server_identifier:
                variable = json_obj[count][key]
                return variable
            else:
                count += 1
        # Handle an error when the server is not published to the master server
        except IndexError:
            if key == 'name':
                return '(Server isn\'t published to the master server)'
            else:
                return '-'

def keep_alive(pid, cmdline):
    try:
        print('Process found. Starting presence.')
        start_time = time.time()
        while pid is not None:
            # Check if the process still exists. If not, then go back to process searching.
            if psutil.pid_exists(pid) is False:
                print('Process was closed. Clearing presence.')
                AOS_RPC.clear(pid=pid)
                print('Waiting for process.')
                scan_for_process()
            
            print('Updating presence.')
            server_name = fetch_data(cmdline, 'name') # request server name key from serverlist
            server_map = fetch_data(cmdline, 'map') # same for here but for map etc.
            server_game_mode = fetch_data(cmdline, 'game_mode')
            server_players_current = fetch_data(cmdline, 'players_current')
            server_players_max = fetch_data(cmdline, 'players_max')

            print(AOS_RPC.update(pid=pid,
                                 details=server_name,
                                 state='Map: {} ({})\nPlayers: {}/{}'.format(server_map,
                                                                             server_game_mode,
                                                                             server_players_current,
                                                                             server_players_max),
                                 start=start_time,
                                 large_image='ace_of_spades1',
                                 large_text='Ace of Spades v0.75'))
            time.sleep(7.5)
    except KeyboardInterrupt:
        print('Interrupt caught. Closing.')
        AOS_RPC.clear(pid=pid)
        AOS_RPC.close()
        exit(0)

print('Waiting for process.')
def scan_for_process():
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
                    scan_for_process()
                keep_alive(ps_pid, ps_cmdline)
            else:
                time.sleep(0.05)

if __name__ == "__main__":
    # Start script
    scan_for_process()
