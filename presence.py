import time
import json
import ssl
import urllib.request
import psutil
from pypresence import Presence

ct = ssl.create_default_context()
ct.check_hostname = False
ct.verify_mode = ssl.CERT_NONE

CLIENT_ID = '699358451494682714'
AOS_RPC = Presence(CLIENT_ID)
AOS_RPC.connect()
try:
    def fetch_server(cmdline_again, key):
        # Request json serverlist that buildandshoot hosts.
        serverlist_url = "https://services.buildandshoot.com/serverlist.json"
        req = urllib.request.urlopen(serverlist_url, context=ct)
        data = req.read()
        enc = req.info().get_content_charset('utf-8')
        json_obj = json.loads(data.decode(enc))

        # Add localhost identifier to serverlist:
        with open("localhost.json") as f:
            data = json.load(f)
        json_obj.append(data)

        count = 0

        # Removing "/" at the end of the server identifier to avoid an index out of range error
        # that is being thrown for some reason idk
        server_identifier = cmdline_again.strip("/")

        while True:
            # If the identifier from the serverlist is valid with the current server player plays,
            # get the requested key in function "fetch_server", compare it with key
            # from serverlist and return it.
            # For example key is the 'name' or 'game_mode'.
            if json_obj[count]['identifier'] == server_identifier:
                variable = json_obj[count][key]
                return variable
            else:
                count += 1

    def keep_alive(pid, cmdline):
        print('Process found. Starting presence.')
        start_time = time.time()
        while pid is not None:
            # Check if the process still exists. If not, then go back to process searching.
            if psutil.pid_exists(pid) is False:
                print('Process was closed. Clearing presence.')
                AOS_RPC.clear(pid=pid)
                scan_for_process()
            print('Updating presence.')

            server_name = fetch_server(cmdline, 'name') # request server name from serverlist
            server_map = fetch_server(cmdline, 'map') # same for here but for map etc.
            server_game_mode = fetch_server(cmdline, 'game_mode')
            server_players_current = fetch_server(cmdline, 'players_current')
            server_players_max = fetch_server(cmdline, 'players_max')

            print(AOS_RPC.update(pid=pid,
                                 details=server_name,
                                 state='Map: {} ({})\nPlayers: {}/{}'.format(server_map,
                                                                             server_game_mode,
                                                                             server_players_current,
                                                                             server_players_max),
                                 start=start_time,
                                 large_image='ace_of_spades1',
                                 large_text='Ace of Spades v0.75'))
            time.sleep(15)

    print('Waiting for a process...')
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
except KeyboardInterrupt:
    print('Interrupt caught. Closing connection.')
    AOS_RPC.close()
