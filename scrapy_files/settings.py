# ------------
# custom settings for healthgrades_spider
# refer to readme.txt for usage
# ------------

# Scrapy settings for healthgrades project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "healthgrades"

SPIDER_MODULES = ["healthgrades.spiders"]
NEWSPIDER_MODULE = "healthgrades.spiders"

FEEDS = {
    'doctors.csv': {'format': 'csv'}
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Authority": "www.healthgrades.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Cookie": "_hg-872c8312de8a4e5a92ec3eef6acc7f1d=75d3515c4e6e4a65ba00d953dcf5ca03; s_ecid=MCMID^%^7C29747080901590158292022131081540648461; chsn_cnsnt=www.healthgrades.com^%^3AC0001^%^2CC0002^%^2CC0003^%^2CC0004^%^2CC0005; tglr_anon_id=e980db5c-ac34-431e-b760-121cf8efc1bd; tglr_tenant_id=src_1zgskhQsph3kTH2xWewpaVom3Sc; slireg=https://scout.us1.salesloft.com; _fbp=fb.1.1686058206593.1243626996; sliguid=069ebe7e-fc34-4482-aa16-1850afa442ab; slirequested=true; cohsn_xs_id=99482df4-0bf8-4a0a-afa4-5d04b04c3525; btIdentify=fc590ad0-3417-4fa7-fd0d-b5452f74fa80; ORA_FPC=id=5554273d-8e47-4b85-9769-906d5b9402f0; dmd-tag=3f4a9470-046e-11ee-b43d-23a6006c7458; OptanonAlertBoxClosed=2023-06-06T13:30:24.163Z; drift_aid=4d28627b-fdc3-4351-a7a0-ff76fb895ba7; driftt_aid=4d28627b-fdc3-4351-a7a0-ff76fb895ba7; _hjSessionUser_713690=eyJpZCI6ImY0MjRhYzRkLTBiNjktNTgwMi05ZjY0LTVmNjE2ZGU5MGY3YSIsImNyZWF0ZWQiOjE2ODYwNTgyMDY1NzUsImV4aXN0aW5nIjp0cnVlfQ==; _cb=9amHeDXO8oWDM6ezo; _ga=GA1.2.1265312975.1686058206; AMCVS_905F67C25245B4660A490D4C^%^40AdobeOrg=1; s_cc=true; .AspNetCore.Session=CfDJ8JYSXri4EpNOqVNozSawW62^%^2Fa3qKxCmnlkqLbdLp4nxWXqxElmXGZfG3mT^%^2B^%^2FYq5b8S^%^2BUUrMxAXeohUwbHhCSfI72cz8NT1EWvbrkZG^%^2BDbIj^%^2F0R1XC79qELX7JQA^%^2FmL0MNyf3bAetvEEw8W4fHhDAUGw8C2sfpeBdE^%^2F^%^2FKmNko0ACo; __utmc=236544792; __utmz=236544792.1686337992.18.3.utmcsr=google^|utmccn=(organic)^|utmcmd=organic^|utmctr=(not^%^20provided); _gid=GA1.2.1196915527.1686505078; mmapi.P04^%^20Womens^%^20Health^%^20Intercept.P04campaignConditionTerm=^%^22Activated^%^20from^%^20Article^%^20Page^%^22; hg3.currentLoc=lat^%^3D40.73^%^26lon^%^3D-73.99^%^26isStateOnly^%^3DFalse^%^26city^%^3DNew^%^2BYork^%^26state^%^3DNY^%^26zip^%^3D10003; hg3.slocsticky=lat=40.73&lon=-73.99&isStateOnly=False&city=New+York&state=NY&zip=10003; _chartbeat2=.1686059255639.1686585686325.1110011.CAEBX1DsdyziBgBJBfDgIyQ-D_UAuH.2; __utma=236544792.1265312975.1686058206.1686591696.1686611294.25; __utmt=1; __utmt_b=1; tglr_sess_id=504acb14-de46-46bc-8aab-6490e08658b4; tglr_req=https://www.healthgrades.com/; tglr_sess_count=34; AMCV_905F67C25245B4660A490D4C^%^40AdobeOrg=359503849^%^7CMCIDTS^%^7C19520^%^7CMCMID^%^7C29747080901590158292022131081540648461^%^7CMCAAMLH-1687216094^%^7C7^%^7CMCAAMB-1687216094^%^7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y^%^7CMCOPTOUT-1686618494s^%^7CNONE^%^7CMCAID^%^7CNONE^%^7CvVersion^%^7C5.0.1; lux_uid=168661129402489832; _sess=1533331e-18e8-49a9-830c-1820b724da59.79d692da-97e8-4317-a831-96c4370223dc.1686611294.1; dmd-vid=79d692da-97e8-4317-a831-96c4370223dc; dmd-sid=1533331e-18e8-49a9-830c-1820b724da59; _hjIncludedInSessionSample_713690=0; _hjSession_713690=eyJpZCI6ImQ1OTEzNTMzLTdjNmItNDFlOC05NzA5LTllY2ZhYzhkMzgzZSIsImNyZWF0ZWQiOjE2ODY2MTEyOTQxMDgsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _bts=8fe17b83-bab2-4398-82fc-a3a925c7101d; mmapi.p.bid=^%^22prodiadcgus05^%^22; mmapi.p.srv=^%^22prodiadcgus05^%^22; mmapi.p.uat=^%^7B^%^22RCC^%^20Non-Spnsr^%^22^%^3A^%^22No^%^22^%^2C^%^22CRM^%^20Users^%^22^%^3A^%^22No^%^22^%^2C^%^22Provdr^%^20Non-Spns^%^22^%^3A^%^22No^%^22^%^2C^%^22Non-Sponsor^%^22^%^3A^%^22No^%^22^%^7D; _bti=^%^7B^%^22app_id^%^22^%^3A^%^22healthgrades^%^22^%^2C^%^22bsin^%^22^%^3A^%^22dDhYmem8jobpBLivDBTpV9Gp055Oa^%^2FzMIsHhL2DccfSyvgWxOLPZyv5Q6h2g5ybtmSIaCQ^%^2B^%^2FeGOmVxd2R3E9zg^%^3D^%^3D^%^22^%^2C^%^22is_identified^%^22^%^3Afalse^%^7D; dmd-sid4=^{^%^22id^%^22:^%^2202552730-0976-11ee-926e-5bdcec98dbc8^%^22^%^2C^%^22timestamp^%^22:1686611295000^}; dmd-ahk=5e8e01d4a4; dmd-signal-102-456-06EED9C9-1533331e-18e8-49a9-830c-1820b724da59=e30=; hg3.search=What=Family^%^20Medicine&Where=New^%^20York^%^2C^%^20NY^%^2010003&Pt=40.73^%^2C-73.99&PageNumber=1&Distance=1&SearchType=PracticingSpecialty&EntityCode=PS305&IsStateOnly=false&PracticingSpecialtyCode=PS305&SpecialtyIds=20&Category=Provider; hg3.searchlocation=lat=40.73&lon=-73.99&isStateOnly=False&city=New+York&state=NY&zip=10003; tglr_ref=https://www.healthgrades.com/; drift_campaign_refresh=5398a9c2-19b5-4e6c-9820-c466a753254d; hg3.sponsor=sponsor^%^3DNWHLTH^%^26facility^%^3DAC671F^%^26sponsorFound^%^3Dtrue^%^26h^%^3D2139062143; s_sq=^%^5B^%^5BB^%^5D^%^5D; utag_main=v_id:018890e6831e005c603b80982c8c0506f001d067009d8^$_sn:24^$_ss:0^$_st:1686613140850^$vapi_domain:healthgrades.com^$ses_id:1686611293587^%^3Bexp-session^$_pn:5^%^3Bexp-session; mmapi.e.P04LastURL=^%^22^%^2Fphysician^%^2Fdr-eric-ascher-xylj6x6^%^22; mmapi.e.P04sawXUniqueURLs=78; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Jun+12+2023+19^%^3A09^%^3A02+GMT-0400+(Eastern+Daylight+Time)&version=202302.1.0&isIABGlobal=false&hosts=&consentId=e33535f8-79d0-43dc-8728-8e321b9c6fa9&interactionCount=1&landingPath=NotLandingPage&groups=C0001^%^3A1^%^2CC0003^%^3A1^%^2CC0002^%^3A1^%^2CC0004^%^3A1^%^2CC0005^%^3A1&geolocation=US^%^3BNY&AwaitingReconsent=false; __utmb=236544792.6.10.1686611294; mmapi.p.pd=^%^22ONkXYZWsk9p961cupMllPLvN-yEs3jjMpbFuYupRNB4^%^3D^%^7CnQAAAApDH4sIAAAAAAAEAGNh8BW-pVcgHnqAgTkzMYVRiIHRieH47QQraYbnAVwss7Jve_jFmSpPSrvtwQAE_6GAgc0lsyg1uYSxQFwaJA4Gi_mYGeYDMYhmZJD1ZWQwET1h1FQoDtbGWCheKP7_PyMDUA4IGIVUmRl4JrMwMIGUiwBFQFq5wAaBpF0BH1BhGZoAAAA^%^3D^%^22; hg.sessionInfo=c2Vzc2lvbklkPVMzNzNhJnJlcXVlc3RJZD1SYzg3MDg5NTFmOTNiNDZmZiZleHBpcmVzPTA2JTJGMTIlMkYyMDIzKzIzJTNBMzklM0EyMQ--",
    "Pragma": "no-cache",
    "Referer": "https://www.healthgrades.com/usearch?what=Family^%^20Medicine&pageNum=1&sort.provider=bestmatch",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "healthgrades.middlewares.HealthgradesSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "healthgrades.middlewares.HealthgradesDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "healthgrades.pipelines.HealthgradesPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 16
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
