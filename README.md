### How to use

* open chrome, goto http://gsxt.saic.gov.cn/, choose a region ( e.g. fujian, jiangxi )
* open '抽查检查公示', use the chrome dev tool to copy data request as cUrl format
* open single company page, use the chrome dev tool to copy data request as cUrl format
* edit taskFile, add region configuration
* run: scrapy crawl list -a region

### How it works

gsxtCrawl adapt the cUrl request format, to scrapy Request object

lanc@fxiaoke.com