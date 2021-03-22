from SystemInfoFetcher.fetcher import Fetcher

hw = Fetcher()
template = """<b>{user}</b>@<i>{hostname}</i>
 -
<b>{key}</b>: <mono>{value}</mono>"""

print(hw.get_formatted(template=template, art=''))