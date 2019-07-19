import requests
from bs4 import BeautifulSoup
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')


headers = { 'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7,ja;q=0.6',
'Connection': 'keep-alive',
'Cookie': 'UM_distinctid=16b42c587c93a4-0fbe59f9c42c1e-e353165-1fa400-16b42c587ca906; Search=1; CNZZDATA1256195895=1142608531-1562507310-%7C1562814353; Hm_lvt_dcb5060fba0123ff56d253331f28db6a=1563343159,1563343182,1563343193,1563343203; Hm_lpvt_dcb5060fba0123ff56d253331f28db6a=1563343247',
'Host': 'ku.gamersky.com',
'Referer': 'http://ku.gamersky.com/sp/',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
'X-Requested-With': 'XMLHttpRequest'
}

r = requests.get("http://ku.gamersky.com/SearchGameLibAjax.aspx?jsondata=%7BrootNodeId%3A20039%2CpageIndex%3A2%2CpageSize%3A36%2Csort%3A%2700%27%7D&_=1563330124891", headers=headers)
r.encoding = "utf8"
ti = BeautifulSoup(r.text)
print(ti.prettify())