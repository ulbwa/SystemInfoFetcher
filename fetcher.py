import os
import platform
import socket
import subprocess
import time
import colorama
import psutil
import getpass
import speedtest as speed

from threading import Thread
from requests import get
from os import path, environ
from json import loads

DEFAULT_TEMPLATE = """{user}@{hostname}
 -
{key}: {value}"""

CONSOLE_TEMPLATE = colorama.Fore.GREEN + '{user}' + \
                   '@' + colorama.Fore.RESET + \
                   colorama.Fore.CYAN + '{hostname}' + colorama.Fore.RESET
CONSOLE_TEMPLATE += '\n' + colorama.Fore.CYAN + ' -' + colorama.Fore.RESET
CONSOLE_TEMPLATE += '\n' + colorama.Fore.GREEN + '{key}' \
                    + ': ' + colorama.Fore.RESET \
                    + colorama.Fore.CYAN + '{value}' \
                    + colorama.Fore.RESET
CONSOLE_ART = """                       .,,uod8B8bou,,.                             
              ..,uod8BBBBBBBBBBBBBBBBRPFT?l!i:.                    
         ,=m8BBBBBBBBBBBBBBBRPFT?!||||||||||||||                   
         !...:!TVBBBRPFT||||||||||!!^^""'   ||||                   
         !.......:!?|||||!!^^""'            ||||                   
         !.........||||                     ||||                   
         !.........||||                     ||||                   
         !.........||||                     ||||                   
         !.........||||                     ||||                   
         !.........||||                     ||||                   
         `.........||||                    ,||||                   
          .;.......||||               _.-!!|||||                   
   .,uodWBBBBb.....||||       _.-!!|||||||||!:'                    
!YBBBBBBBBBBBBBBb..!|||:..-!!|||||||!iof68BBBBBb....               
!..YBBBBBBBBBBBBBBb!!||||||||!iof68BBBBBBRPFT?!::   `.             
!....YBBBBBBBBBBBBBBbaaitf68BBBBBBRPFT?!:::::::::     `.           
!........YBBBBBBBBBBRPFT?!::::::::::^''...::::::;         iBBbo.   
`..........YBRPFT?!::::::::::::::::::::::::;iof68bo.      WBBBBbo. 
  `..........:::::::::::::::::::::::;iof688888888888b.     `YBBBP^'
    `........::::::::::::::::;iof688888888888888888888b.     `     
      `......:::::::::;iof688888888888888888888888888888b.         
        `....:::;iof688888888888888888888888888888888899fT!        
          `..::!8888888888888888888888888888888899fT|!^"'          
            `' !!988888888888888888888888899fT|!^"'                
                `!!8888888888888888899fT|!^"'                      
                  `!988888888899fT|!^"'                            
                    `!9899fT|!^"'                                  
                      `!^"'                                        """


def clear_console():
    return os.system('cls') if psutil.WINDOWS else os.system('clear')


def check_output(command: str):
    try:
        return subprocess.check_output(command, shell=True,
                                       universal_newlines=True,
                                       stderr=subprocess.DEVNULL)

    except subprocess.CalledProcessError:
        return False


def put_to_dict(dictionary: dict, key: str, value: any):
    dictionary[key] = value


class Fetcher:
    def __init__(self):
        command = (
            'powershell neofetch --stdout --config none'
        ) if psutil.WINDOWS else (
            (
                'curl -Ls https://github.com/dylanaraps/neofetch/raw/master/neofetch | '
                'bash -s -- --stdout --config none'
            ) if 'aws' in platform.platform() else (
                'neofetch --stdout --config none'
            )
        )

        output = check_output(command)
        self.header = {"user": getpass.getuser(), "hostname": socket.gethostname()}
        self.info = dict()

        if output:
            output = output.encode('utf8')
            output = output.decode('cp866') if psutil.WINDOWS else output.decode('utf8')
            for a in output.split('- \n')[1].split('\n'):
                if not a or a == ' ':
                    continue

                i, j = a.split(': ', maxsplit=1)
                self.info[i] = j[:-1]

                try:
                    put_to_dict(self.info, 'IP', get('https://ifconfig.me/ip').text) if i == 'Kernel' else str()
                except Exception:
                    pass
                put_to_dict(self.info, 'Boot', time.ctime(psutil.boot_time())
                            ) if i == 'Uptime' and 'ANDROID_DATA' not in environ else str()
                put_to_dict(self.info, 'CPU Architecture', platform.uname().machine.replace(
                    '_', '-')) if i == 'CPU' else str()
                put_to_dict(self.info, 'SWAP', '{}MiB / {}MiB'.format(
                    round(psutil.swap_memory().used / 1e+6),
                    round(psutil.swap_memory().total / 1e+6)
                )) if i == 'Memory' else str()
                put_to_dict(self.info, 'Storage', '{}GiB / {}GiB'.format(
                    round(psutil.disk_usage('/.').used / 1e+9),
                    round(psutil.disk_usage('/.').total / 1e+9)
                )) if i == 'Memory' else str()

        self.run_bench(__name__ == '__main__')
        self.run_speedtest(__name__ == '__main__')

    def run_bench(self, wait: bool = True):
        if 'ANDROID_DATA' in environ:
            return

        def run():
            data = loads(check_output(
                'python ' + path.join(path.dirname(path.abspath(__file__)), 'bench.py')))
            self.info['Bench/Single'] = '{}s.'.format(data['single_th'])
            self.info['Bench/Multi'] = '{}s.'.format(data['multi_th'])

        thread = Thread(target=run)
        thread.start()
        thread.join() if wait else str()

    def run_speedtest(self, wait: bool = True):
        def run():
            tester = speed.Speedtest()
            tester.get_best_server()
            tester.download(threads=None)
            tester.upload(threads=None)

            download = round(tester.results.dict()["download"] / 2 ** 20)
            upload = round(tester.results.dict()["upload"] / 2 ** 20)
            ping = round(tester.results.dict()["ping"])
            server = tester.results.dict()["server"]["country"] + ', ' + tester.results.dict()["server"]["name"]  # noqa

            self.info['ST/Download'] = '{} MiB/s'.format(download)
            self.info['ST/Upload'] = '{} MiB/s'.format(upload)
            self.info['ST/Ping'] = '{} ms.'.format(ping)
            self.info['ST/Server'] = '{} MiB/s'.format(server)

        thread = Thread(target=run)
        thread.start()
        thread.join() if wait else str()

    def get_formatted(self, template: str = DEFAULT_TEMPLATE, art: str = str()):
        header_template, separator_template, body_template = template.splitlines()[:3]

        header = header_template.format(user=self.header['user'], hostname=self.header['hostname'])
        separator = int(len(header) / len(separator_template)) * separator_template
        body = "\n".join(
            [(body_template.format(
                key=a, value=self.info[a]
            ) + '\n' + body_template.format(
                key='CPU Load', value='{}%'.format(
                    round(psutil.cpu_percent(0.5))))
              ) if a == 'CPU' and 'ANDROID_DATA' not in environ else (body_template.format(
                key=a, value=self.info[a])) for a in self.info])

        content = '{}\n{}\n{}'.format(header, separator, body)
        output = list()

        art_lines = art.splitlines()
        content_lines = content.splitlines()

        for a in range(max([len(art_lines), len(content_lines)])):
            line = str()

            try:
                line += art_lines[a]
            except IndexError:
                try:
                    line += len(art_lines[-1]) * ' '
                except IndexError:
                    pass

            try:
                line += (content_lines[a] if not line else ' ' + content_lines[a])
            except IndexError:
                pass

            output.append(line)

        return "\n".join(output)


if __name__ == '__main__':
    clear_console()
    print(colorama.Fore.CYAN, 'Loading...', colorama.Fore.RESET, sep='')
    information = Fetcher().get_formatted(template=CONSOLE_TEMPLATE,
                                          art=CONSOLE_ART if 'ANDROID_DATA' not in environ else '')
    clear_console()
    print('\n', information, sep='')
