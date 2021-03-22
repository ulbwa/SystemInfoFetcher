<div align="center">
  <h1>SystemInfoFetcher</h1>
  <p>A simple Python script to fetch system information.</p>

  <img align="center" src="https://img.shields.io/github/repo-size/ulbwa/SystemInfoFetcher" alt="GitHub repo size">
  <img align="center" src="https://img.shields.io/github/stars/ulbwa/SystemInfoFetcher" alt="GitHub Repo stars">
  <img align="center" src="https://img.shields.io/github/watchers/ulbwa/SystemInfoFetcher" alt="GitHub watchers">
  <img align="center" src="https://img.shields.io/github/last-commit/ulbwa/SystemInfoFetcher" alt="GitHub last commit">
  <img align="center" src="https://img.shields.io/github/languages/top/ulbwa/SystemInfoFetcher" alt="GitHub top language">
</div>

## Navigation

* [Quick start](#Quick-start)
  * [Installing dependencies](#Installing-dependencies)
  * [Examples](#Examples)
* [Screenshots](#Screenshots)

## Quick start
SystemInfoFetcher is based on Neofetch, so you need to install it.

### Installing dependencies
* Install SystemInfoFetcher as a submodule of your project:

```
$ git submodule add https://github.com/ulbwa/SystemInfoFetcher && sudo apt-get install neofetch && python3 -m pip install -r requirements.txt
```

* Or you can clone SystemInfoFetcher:

```
$ git clone https://github.com/ulbwa/SystemInfoFetcher && sudo apt-get install neofetch && python3 -m pip install -r requirements.txt
```

> For convenient work, it is recommended to use the first method.

### Examples
Show information in dictionary format:
```python
from SystemInfoFetcher.fetcher import Fetcher

hw = Fetcher()
print(hw.info)
```

```
>>> {'OS': 'Ubuntu 20.04 LTS x86_64', 'Host': '1.0', 'Kernel': '5.4.0-31-generic', 'IP': '*', 'Uptime': '23 hours, 26 mins', 'Boot': 'Sun Mar 21 11:38:15 2021', 'Packages': '1383 (dpkg)', 'Shell': 'zsh 5.8', 'Terminal': '/dev/pts/0', 'CPU': 'AMD Ryzen 5 3600 (12) @ 3.600GHz', 'CPU Architecture': 'x86-64', 'Memory': '12612MiB / 64314MiB', 'SWAP': '0MiB / 34325MiB', 'Storage': '299GiB / 469GiB'}
```

Using different templates:
```python
from SystemInfoFetcher.fetcher import Fetcher

hw = Fetcher()
template = """<b>{user}</b>@<i>{hostname}</i>
 -
<b>{key}</b>: <mono>{value}</mono>"""
print(hw.get_formatted(template=template, art=''))
```

```
>>> <b>ulba</b>@<i>Ubuntu-2004-focal-64-minimal</i>
>>>  - - - - - - - - - - - - - - - - - - - - - - -
>>> <b>OS</b>: <mono>Ubuntu 20.04 LTS x86_64</mono>
>>> <b>Host</b>: <mono>1.0</mono>
>>> <b>Kernel</b>: <mono>5.4.0-31-generic</mono>
>>> <b>IP</b>: <mono>*</mono>
>>> <b>Uptime</b>: <mono>23 hours, 31 mins</mono>
>>> <b>Boot</b>: <mono>Sun Mar 21 11:38:15 2021</mono>
>>> <b>Packages</b>: <mono>1383 (dpkg)</mono>
>>> <b>Shell</b>: <mono>zsh 5.8</mono>
>>> <b>Terminal</b>: <mono>/dev/pts/0</mono>
>>> <b>CPU</b>: <mono>AMD Ryzen 5 3600 (12) @ 3.600GHz</mono>
>>> <b>CPU Load</b>: <mono>45%</mono>
>>> <b>CPU Architecture</b>: <mono>x86-64</mono>
>>> <b>Memory</b>: <mono>12847MiB / 64314MiB</mono>
>>> <b>SWAP</b>: <mono>0MiB / 34325MiB</mono>
>>> <b>Storage</b>: <mono>299GiB / 469GiB</mono>
```

## Screenshots
<p align="center">
    <img src="https://i.imgur.com/aceyvin.jpeg" alt="screenshot">
</p>