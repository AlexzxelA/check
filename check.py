#coding=UTF-8

# See https://github.com/AnttiKurittu/check/ for details.

import datetime

startTime = datetime.datetime.now()

import os, sys, socket, json, argparse, webbrowser, subprocess, zipfile,\
    dns.resolver, requests, GeoIP, StringIO, operator, random, hashlib,\
    dateutil.parser, time, zlib, gzip
from passivetotal import PassiveTotal
from base64 import b64encode, b64decode
from IPy import IP

parser = argparse.ArgumentParser(description='Get actions')
parser.add_argument(
                    "-d",
                    "--domain",
                    metavar='domain name',
                    type=str,
                    help="Target domain name")
parser.add_argument("-i",
                    "--ip",
                    metavar='IP address',
                    type=str,
                    help="Target IP address")
parser.add_argument("-a",
                    "--all",
                    help="run all queries",
                    action="store_true")
parser.add_argument("-l",
                    "--lists",
                    help="run all third-party queries (blacklists, spamlists, \
virustotal, passivetotal, whois, geoip)",
                    action="store_true")
parser.add_argument("-p",
                    "--probes",
                    help="run all host-contacting probes (ping, scan ports, \
scan headers, certificate)",
                    action="store_true")
parser.add_argument("-pg",
                    "--ping",
                    help="Ping IP address",
                    action="store_true")
parser.add_argument("-ws",
                    "--whois",
                    help="Query WHOIS information",
                    action="store_true")
parser.add_argument("-cr",
                    "--cert",
                    help="Display certificate information via OpenSSL",
                    action="store_true")
parser.add_argument("-sp",
                    "--scanports",
                    help="Scan common ports",
                    action="store_true")
parser.add_argument("-gi",
                    "--geoip",
                    help="Query GeoIP database",
                    action="store_true")
parser.add_argument("-sh",
                    "--scanheaders",
                    help="Scan common ports and try to retrieve HTTP headers",
                    action="store_true")
parser.add_argument("-gs",
                    "--googlesafebrowsing",
                    help="Check Google Safe Browsing database",
                    action="store_true")
parser.add_argument("-wt",
                    "--weboftrust",
                    help="Query Web Of Trust database",
                    action="store_true")
parser.add_argument("-sl",
                    "--spamlists",
                    help="Check SURBL and SpamHaus blocklists for IP",
                    action="store_true")
parser.add_argument("-bl",
                    "--blacklists",
                    help="Check blacklists for target",
                    action="store_true")
parser.add_argument("-pt",
                    "--passivetotal",
                    help="Query passive DNS records from PassiveTotal",
                    action="store_true")
parser.add_argument("-vt",
                    "--virustotal",
                    help="Query passive DNS records from VirusTotal",
                    action="store_true")
parser.add_argument("-nt",
                    "--note",
                    metavar='Add a note',
                    type=str,
                    help="Add a note to the output, \
this could be a project name or description of address.")
parser.add_argument("-O",
                    "--openlink",
                    help="Open GeoIP location in Google Maps",
                    action="store_true")
parser.add_argument("-L",
                    "--logfile",
                    type=str,
                    help="Specify log file, default is log/check-[IP]-[DATETIME].log")
parser.add_argument("-NL",
                    "--nolog",
                    help="Do not write log",
                    action="store_true")
parser.add_argument("-M", "--monochrome",
                    help="Suppress colors",
                    action="store_true")
parser.add_argument("-NG", "--nogfx",
                    help="Suppress line graphics",
                    action="store_true")
parser.add_argument("-S", "--nosplash",
                    help="Suppress cool ASCII header graphic",
                    action="store_true")

arg = parser.parse_args()

splash = [
"eJyVUj2LwzAM3f0rdIJcoAV16aAL/cjSpYRQbutyBC7tUjp66dDfXn04rRO4wgkiy0/vSbaVAP81oj\
DaxtP5B/9kr4BuNWOXaaqeefe2xUctjKQg+TqeKChmsboyMWKQXP/N3MrGMLrxRRlRujKTiQeCM2LNb\
RNWEmuVi6P3rfgGqoSKMCMYo0PmGYYviaE84lDNfW8oc4GQEdKJ+pZc5pbJrNPcqBnBD6S5N7LG0anM\
XuYz6G04Ei1GOrvZLwHNISMkhlaSUaMmDiXAVdZ2rckNOMqFdnkSSo1mCEtZUKeHiur4htexHR4T/CJ\
IhO5Hv5baPtUaWV1MoArDAzKkfNg=",  "eJxtjcENwDAIA/9MwS+fSl6goyA5+09RDE3VVkEiFodjz\
KtI3xVppQiPzVrY5KL2wZXSujBGmjDu0ekzX82pDz78NFRG3eqPchNvHDOsLzGkqzvliy0TRCDF3Zr/\
2C5j6z7d",  "eJxtTcsVwCAIuzNFskAH4MT+U1VIkdpX4Gl+ogGhyrtIC/FjYbSOGigjFbZMKafF3v\
CKURuefFC9AOmsDWNFk8GVNjj7Q3oeFMg6rCbbLWgr5TXIgatz/GuJYT/H5XYDCyc3BA==",  "eJyN\
T7ENwzAM230FtyRAET+QUwzwER5fUVIytEMrDRQpkLYGqoiv4ihU9EeFFEuSnpheJrSE1gpZYTOYhI1\
YMAloSTMmp+ZO1UPYOy1azp63BFyO9eOHd2L+aNFxLJ7kkRbXzkM4IwVWX3nCr3put+0vA9UYjvEGA0\
BOyA==",  "eJxtTrENwDAI27nCF4QHovxRCYlHcnxtaNUMRSjBBowNT4xM/EWm6VF3M3uq8UHj41Xx\
od6wdJXRIwgURpy0w7UZtRgTrWfRlAAu1lGiftKYZbBcLaxoM9YDWLSa7PmLP3rzELzOU1QGdJybZcT\
x9x+QuUtayG5w3EwF"]

if not arg.nosplash:
    print zlib.decompress(b64decode(random.choice(splash)))
    print "Check.py - Extended lookup tool. See -h for command line options.\n"

## Specify resources and API keys
ownPath = os.path.dirname(sys.argv[0]) + "/"
if ownPath is "/" or ownPath is "":
    ownPath = "./"
curDate = str(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M"))
eNow = int(time.mktime(dateutil.parser.parse(curDate).timetuple()))
GeoIPDatabaseFile = "/usr/local/share/GeoIP/GeoLiteCity.dat" # Specify database file location
targetPortscan = [80, 443, 8000, 20, 21, 22, 23, 25, 53] # What ports to scan
blacklistSourceFile = ownPath + "blacklists.txt"
sourceListSpamDNS = [
        "zen.spamhaus.org", "spam.abuse.ch", "cbl.abuseat.org",
        "virbl.dnsbl.bit.nl", "dnsbl.inps.de", "ix.dnsbl.manitu.net",
        "dnsbl.sorbs.net", "bl.spamcannibal.org", "bl.spamcop.net",
        "xbl.spamhaus.org", "pbl.spamhaus.org","dnsbl-1.uceprotect.net",
        "dnsbl-2.uceprotect.net", "dnsbl-3.uceprotect.net", "db.wpbl.info"
        ]
uapool = [
         'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/41.0.2228.0 Safari/537.36',
         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
         'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, \
like Gecko) Chrome/41.0.2227.0 Safari/537.36',
         'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
         'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; \
rv:11.0) like Gecko',
         'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 7.0; InfoPath.3; .NET \
c 3.1.40767; Trident/6.0; en-IN)',
         'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
         'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
         'Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; \
Trident/6.0)',
         'Mozilla/4.0 (Compatible; MSIE 8.0; Windows NT 5.2; Trident/6.0)',
         'Mozilla/4.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)',
         'Mozilla/1.22 (compatible; MSIE 10.0; Windows 3.1)',
         'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
         'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 \
(KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'
         ]
headers = {'user-agent': 'Mozilla/5.0 (Check.py extended address information \
lookup tool)', 'referer': 'https://www.github.com/AnttiKurittu/check'}
hasError = [] # Gather erring modules
logfile = None # Set variable as blank to avoid errors further on.
notRun = [] # Gather skipped modules
run = [] # Gather executed modules

if arg.monochrome:
  class c:
      HDR = ''
      B = ''
      G = ''
      Y = ''
      R = ''
      END = ''
      BOLD = ''
      UL = ''
else:
  class c:
      HDR = '\033[95m'
      B = '\033[94m'
      G = '\033[92m'
      Y = '\033[93m'
      R = '\033[91m'
      END = '\033[0m'
      BOLD = '\033[1m'
      UL = '\033[4m'

if arg.nogfx:
  class g:
      STAR = ''
      PLUS = ''
      PIPE = ''
      FAIL = ''
      MINUS = ''
else:
  class g:
      STAR = "[*] "
      PLUS = "[+] "
      PIPE = " |  "
      FAIL = "[!] "
      MINUS = "[-] "

class Logger(object): # Log output to file, remove colors.
    def __init__(self, filename = logfile):
        self.terminal = sys.stdout
        self.log = open(filename, "w")
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message.replace("\033[95m", "")\
        .replace("\033[94m", "").replace("\033[93m", "")\
        .replace("\033[92m", "").replace("\033[91m", "")\
        .replace("\033[0m", "").replace("\033[1m", "")\
        .replace("\033[4m", ""))
    def flush(self):
        self.terminal.flush()

def terminate(): # Graceful exit.
    stopTime = datetime.datetime.now()
    totalTime = stopTime - startTime
    if len(hasError) > 0:
        printh("Executed %s modules with errors in %s, runtime %s seconds." % (len(run),\
            ", ".join(hasError), totalTime.seconds))
    else:
        printh("Executed %s modules in %s seconds." % (len(run), totalTime.seconds))
    printh("Skipped %s modules."  % len(notRun))
    exit()

def trimcache(h): # Removes cache files older than h, returns removed megabyte amount.
    filelist = [ f for f in os.listdir(ownPath + "cache") ]
    removedSize = 0
    cacheSize = 0
    for f in filelist:
        filesize = os.path.getsize(ownPath + "cache/" + f)
        cacheSize = cacheSize + filesize
        filedate = 0
        difference = 0
        if len(f) == 43:
            filedate = f.split("-")
            filedate = int(filedate[0])
            difference = (eNow - filedate) / 8600
            if difference >= h:
                removedSize = removedSize + filesize
                os.remove(ownPath + "cache/" + f)
    megabytesRemoved = removedSize / 1000000
    megabytesLeft = (cacheSize - removedSize) / 1000000
    return megabytesRemoved, megabytesLeft

def printe(message, module):
    if module != "":
        print g.FAIL + c.R + ("%s: %s" % (module, message)) + c.END
        hasError.append(module)
    else:
        print g.FAIL + c.R + ("%s" % message) + c.END
    return True

def printh(message):
    print g.STAR + c.HDR + message + c.END
    return True

def printp(message):
    print g.PLUS + c.END + message
    return True

def validate_ip(ip): # Validate IP address format
    try:
        socket.inet_aton(ip)
    except Exception:
        return False
    return True

### PROCESS CLI ARGUMENTS
if arg.ip and arg.domain:
    printe("Specify an IP address or domain, not both! Exiting...", "Dual target")
    terminate()

if arg.ip:
    if validate_ip(arg.ip) == False:
        printe("Invalid IP address, exiting...", "Validate IP")
        terminate()
    else:
        IPaddr = arg.ip
        Domain = "Not defined"
elif arg.domain:
    Domain = arg.domain.replace("https://", "").replace("http://", "").replace("/", "")
    try:
        my_resolver = dns.resolver.Resolver()
        my_resolver.nameservers = ['8.8.8.8']
        answers = my_resolver.query(Domain, 'A')
        printh("%s IP addresses returned, using first A record %s for %s." % (len(answers), answers[0], Domain))
        IPaddr = str(answers[0])
    except dns.resolver.NXDOMAIN:
        printe("No A records returned from public DNS %s." % my_resolver.nameservers, "Domain resolve / Public")
    try:
        IPaddrLocal = socket.gethostbyname(Domain)
        if IPaddrLocal != IPaddr:
            printh("Public DNS reports different results (%s) from host DNS results (%s)" % (IPaddr, IPaddrLocal))
    except socket.gaierror:
        printe("Resolving domain %s failed, assignign 127.0.0.1 as ip" % Domain,"Domain resolve / Local")
        IPaddr = "127.0.0.1"

else:
    printe("No target given, exiting...", "Target")
    terminate()
if not arg.nolog:
    if arg.logfile:
        logfile = arg.logfile
    else:
        if arg.domain:
            logfile = ownPath + "log/check-" + Domain + "-"+ curDate + ".log"
        else:
            logfile = ownPath + "log/check-" + IPaddr + "-"+ curDate + ".log"
        sys.stdout = Logger(logfile)

if arg.note:
    printp("Note: %s" % arg.note)
    print g.PIPE

iIPr = IPaddr.split(".")
iIPr = iIPr[0] + "." + iIPr[1] + "." + iIPr[2] + ".0"

if Domain == "Not defined":
    printh("Using IP address %s, no domain specified. Unable to run some modules." % IPaddr)
else:
    printh("Using IP address %s for domain %s" % (IPaddr, Domain))
if IPaddr != "127.0.0.1":
    iptype = IP(IPaddr).iptype()
else:
    iptype="PUBLIC"
if iptype == "PRIVATE" or iptype == "LOOPBACK":
    printh("IP address type is %s this may lead to errors." % iptype.lower())
else:
    "Fully Qualified Doman Name: " + socket.getfqdn(IPaddr) + c.END

### GOOGLE SAFE BROWSING API LOOKUP
if (arg.googlesafebrowsing or arg.lists or arg.all) and Domain != "Not defined":
    try:
        GoogleAPIKey = os.environ['GAPIKEY']
        run.append("Google Safe Browsing")
        printh("Querying Google Safe Browsing API with domain name")
        target = 'http://' + Domain + '/'
        parameters = {'client': 'check-lookup-tool', 'key': GoogleAPIKey, 'appver': '1.0', 'pver': '3.1', 'url': target}
        reply = requests.get("https://sb-ssl.google.com/safebrowsing/api/lookup", params=parameters, headers=headers)
        if reply.status_code == 200:
            print g.PIPE + c.Y + "Status %s: Address http://%s/ found:" % (reply.status_code, Domain), reply.text + c.END
        elif reply.status_code == 204:
            print g.PIPE + c.G + "Status %s: The requested URL is legitimate." % (reply.status_code) + c.END
        elif reply.status_code == 400:
            printe("Status %s: Bad Request." % reply.status_code, "Google Safe Browsing")
        elif reply.status_code == 401:
            printe("Status %s: Not Authorized" % (reply.status_code), "Google Safe Browsing")
        elif reply.status_code == 503:
            printe("Status %s: Service Unavailable" % (reply.status_code), "Google Safe Browsing")
        else:
            printe("Status %s: Unhandled reply: " % (reply.status_code), "Google Safe Browsing")
        print g.PIPE
    except KeyError:
        printe("Google API key not present.", "Google Safe Browsing")
else:
    notRun.append("Google Safe Browsing")

### WEB OF TRUST API LOOKUP
if (arg.weboftrust or arg.lists or arg.all) and Domain != "Not defined":
    try:
        WOTAPIKey = os.environ['WOTAPIKEY'] ### same here.
        run.append("Web Of Trust")
        printh("Querying Web Of Trust reputation API with domain name")
        target = 'http://' + Domain + '/'
        parameters = {'hosts': Domain + "/", 'key': WOTAPIKey}
        reply = requests.get("http://api.mywot.com/0.4/public_link_json2", params=parameters, headers=headers)
        reply_dict = json.loads(reply.text)
        categories = {
        '101': c.R + 'Negative: Malware or viruses' + c.END,
        '102': c.R + 'Negative: Poor customer experience' + c.END,
        '103': c.R + 'Negative: Phishing' + c.END,
        '104': c.R + 'Negative: Scam' + c.END,
        '105': c.R + 'Negative: Potentially illegal' + c.END,
        '201': c.Y + 'Questionable: Misleading claims or unethical' + c.END,
        '202': c.Y + 'Questionable: Privacy risks' + c.END,
        '203': c.Y + 'Questionable: Suspicious' + c.END,
        '204': c.Y + 'Questionable: Hate, discrimination' + c.END,
        '205': c.Y + 'Questionable: Spam' + c.END,
        '206': c.Y + 'Questionable: Potentially unwanted programs' + c.END,
        '207': c.Y + 'Questionable: Ads / pop-ups' + c.END,
        '301': c.G + 'Neutral: Online tracking' + c.END,
        '302': c.G + 'Neutral: Alternative or controversial medicine' + c.END,
        '303': c.G + 'Neutral: Opinions, religion, politics ' + c.END,
        '304': c.G + 'Neutral: Other ' + c.END,
        '401': c.Y + 'Child safety: Adult content' + c.END,
        '402': c.Y + 'Child safety: Incindental nudity' + c.END,
        '403': c.R + 'Child safety: Gruesome or shocking' + c.END,
        '404': c.G + 'Child safety: Site for kids' + c.END,
        '501': c.G + 'Positive: Good site' + c.END}
        if reply.status_code == 200:
            hasKeys = False
            for key, value in reply_dict[Domain].iteritems():
                if key == "target":
                    printp("Server response OK, Web Of Trust Reputation Score for %s%s:" % (c.BOLD, value))
                elif key == "1":
                    () # Deprecated
                elif key == "2":
                    () # Deprecated
                elif key == "0" or key == "4":
                    hasKeys = True
                    if int(value[0]) >= 0:
                        assessment = c.R + "Very poor" + c.END
                    if int(value[0]) >= 20:
                        assessment = c.R + "Poor" + c.END
                    if int(value[0]) >= 40:
                        assessment = c.Y + "Unsatisfactory" + c.END
                    if int(value[0]) >= 60:
                        assessment = c.G + "Good" + c.END
                    if int(value[0]) >= 80:
                        assessment = c.G + "Excellent" + c.END
                    if key == "0":
                        print g.PIPE
                        print g.PIPE + "Trustworthiness:\t %s (%s) \t[%s%% confidence]" % (value[0], assessment, value[1])
                    elif key == "4":
                        print g.PIPE + "Child safety:\t %s (%s) \t[%s%% confidence]" % (value[0], assessment, value[1])
                elif key == "categories":
                    print g.PIPE
                    hasKeys = True
                    for e,s in value.iteritems():
                        print g.PIPE + "Category:\t %s \t[%s%% confidence]" % (categories[e], s)
                    print g.PIPE
                elif key == "blacklists":
                    hasKeys = True
                    for e,s in value.iteritems():
                        print g.PIPE + "Blacklisted:\t %s \tID: %s" % (e, s)
                else:
                    print "Unknown key", key, " => ", value
        if hasKeys == False:
            print g.PIPE + c.G + "Web Of Trust has no records for", Domain + c.END
            print g.PIPE
        if reply.status_code != 200:
            printe("Server returned status code %s see https://www.mywot.com/wiki/API for details." % reply.status_code, "Web Of Trust")
    except KeyError:
        printe("Web Of Trust API key not present.", "Web Of Trust")
else:
    notRun.append("Web Of Trust")

### BLACKLISTS
if arg.blacklists or arg.lists or arg.all:
    run.append("Blacklists")
    removed = trimcache(72) # Delete entries older than 72h
    print g.STAR + c.B + "Cache trim: %s MB removed, current cache size %s MB." % removed + c.END
    totalLines = 0
    if os.path.isfile(blacklistSourceFile) == True:
        with open(blacklistSourceFile) as sourcefile:
            blacklists = sourcefile.readlines()
            sourceCount = 0
    else:
        printe("No blacklist file found at %s" % blacklistSourceFile, "blacklist")
        blacklists = ""
        cachefilew = open(os.devnull, "w+")
        cachefiler = open(os.devnull, "r+")
    for line in blacklists:
        if line[:1] == "#":
            continue
        else:
            sourceCount += 1
    printh("Downloading and searching blacklists for address.")
    i = 0
    cacherefreshcount = 0
    for sourceline in blacklists:
        sourceline = sourceline.split("|")
        sourceurl = sourceline[0].replace("\n", "").replace(" ", "")
        if sourceurl[:1] == "#":
            continue # Skip comment lines
        try:
            sourcename = sourceline[1].replace("\n", "")
        except IndexError:
            sourcename = sourceline[0].replace("\n", "") # If no name specified use URL.
        i += 1
        listfile = ""
        linecount = 0
        domainmatch = False
        ipmatch = False
        printp("Downloading from %s%s%s [%s of %s sources]:" % (c.BOLD, sourcename, c.END, i, sourceCount))
        try:
            data = ""
            head = requests.head(sourceurl, headers=headers)
        except Exception:
            print g.PIPE + "[" + c.R + "Fail!" + c.END + "] Unable to connect to %s" % (sourcename)
            continue
        try:
            timestamp = head.headers['Last-Modified']
        except KeyError:
            timestamp = "1970-01-02 00:00:00"
        eStamp = int(time.mktime(dateutil.parser.parse(timestamp).timetuple()))
        agediff = eNow - eStamp
        filehash = hashlib.md5(sourceurl.encode('utf-8')).hexdigest()
        cachepath = ownPath + "cache/" + str(eStamp) + "-" + filehash
        if eStamp == 79200:
            usecache = False
        else:
            usecache = os.path.isfile(cachepath)
        if usecache == True:
            if agediff >= 60:
                age = "%s%s%s minutes ago" % (c.G, (agediff / 60), c.END)
            if agediff >= 3600:
                age = "%s%s%s hours ago" % (c.G, (agediff / 3600), c.END)
            if agediff >= 86400:
                if (agediff / 86400) >= 14:
                    age = "%s%s%s days ago, %sstale source?%s" %(c.R, (agediff / 86400), c.END, c.R, c.END)
                else:
                    age = "%s%s%s days ago" % (c.Y, (agediff / 86400), c.END)
            print g.PIPE + "[" + c.B + "Cache" + c.END + "] Using a cached copy. Source updated %s." % age
            cachefiler = gzip.open(cachepath, "r+")
            cachefilew = open(os.devnull, "w+")
        else:
            #os.remove(cachefilew)
            cachefilew = gzip.open(cachepath, "w+")
            cachefiler = open(os.devnull, "r+")
        if usecache == True:
            lines = cachefiler.readlines()
            for line in lines:
                linecount += 1
            print  g.PIPE + "Searching from %s lines." % (linecount) + c.END
            totalLines = totalLines + (linecount - 1)
            req = None
            for line in lines:
                if Domain != "Not defined":
                    if Domain in line:
                        domainmatch = True
                        print g.PIPE + c.Y + "Domain match! " + c.END + line.replace(Domain, c.R + Domain + c.END).replace("\n", "")
                if IPaddr in line:
                    ipmatch = True
                    print g.PIPE + c.Y + "IP match! " + c.END + line.replace(IPaddr, c.R + IPaddr + c.END).replace("\n", "")
                if iIPr in line:
                    ipmatch = True
                    print g.PIPE + c.Y + "Range match! " + c.END + line.replace(iIPr, c.R + iIPr + c.END).replace("\n", "")
            if domainmatch == False and ipmatch == True and Domain != "Not defined":
                print g.PIPE + "Domain name not found." + c.END
            elif ipmatch == False and domainmatch == True:
                print g.PIPE + "IP address not found." + c.END
            else:
                print g.PIPE + "Address "+ c.G + "not found" + c.END + " in list." + c.END
        if usecache == False:
            cacherefreshcount += 1
            req = requests.get(sourceurl, stream=True, headers=headers)
            try:
                cd = req.headers['Content-Disposition']
            except Exception:
                cd = ""
            filesize = req.headers.get('content-length')
            if not filesize:
                # Assuming no content-length header or content-type
                sys.stdout.write(g.PIPE + "[" + c.G + "Done!" + c.END + "] Content-length not received. " + cd + c.END)
                data = req.content
                cType = "text/plain"
            else:
                cType = req.headers.get('content-type')
                if not cType:
                    cType = "text/plain"
                sys.stdout.write(g.PIPE + "[" + c.R + "     " + c.END + "] Filesize: " + str(int(filesize) / 1024) + " kb \tContent type: " + str(cType) + " \r" + g.PIPE + "[")
                part = int(filesize) / 5
                count = 0
                for chunk in req.iter_content(part):
                    count += 1
                    if count <= 5:
                        if count == 1:
                            sys.stdout.write(c.G + "D" + c.END)
                        if count == 2:
                            sys.stdout.write(c.G + "o" + c.END)
                        if count == 3:
                            sys.stdout.write(c.G + "n" + c.END)
                        if count == 4:
                            sys.stdout.write(c.G + "e" + c.END)
                        if count == 5:
                            sys.stdout.write(c.G + "!" + c.END)
                        sys.stdout.flush()
                    data = data + chunk
                while count < 5: # Fill the meter if the chunks round down.
                    count += 1
                    sys.stdout.write(c.G + "!" + c.END)
                    sys.stdout.flush()
            if "application/zip" in cType:
                filelist = {}
                zip_file_object = zipfile.ZipFile(StringIO.StringIO(data))
                for info in zip_file_object.infolist(): # Get zip contents and put to a list
                    filelist[info.filename] = info.file_size # Add files to a list
                sortedlist = sorted(filelist.items(), key=operator.itemgetter(1)) # Sort list by value; largest file is last
                for key, value in sortedlist: # Iterate over list - last assigned value is the largest file
                    largestfile = key
                    largestsize = value
                sys.stdout.write("\r\n" + g.PIPE + "Decompressing and using largest file in archive: %s (%s bytes)." % (largestfile, largestsize))
                file = zip_file_object.open(largestfile)
                listfile = file.read()
            else:
                listfile = data
            cachefilew.write("Cached copy for %s\n" % cachepath)
            for line in listfile.splitlines():
                cachefilew.write(line.replace("\n", ""))
                cachefilew.write("\r\n")
                linecount += 1
            print "\r\n" + g.PIPE + "Searching from %s lines." % (linecount) + c.END
            totalLines = totalLines + linecount
            for line in listfile.splitlines():
                if Domain != "Not defined":
                    if Domain in line:
                        domainmatch = True
                        print g.PIPE + c.Y + "Domain match! " + c.END + line.replace(Domain, c.R + Domain + c.END).replace("\n", "")
                if IPaddr in line:
                    ipmatch = True
                    print g.PIPE + c.Y + "IP match! " + c.END + line.replace(IPaddr, c.R + IPaddr + c.END).replace("\n", "")
                if iIPr in line:
                    ipmatch = True
                    print g.PIPE + c.Y + "Range match! " + c.END + line.replace(iIPr, c.R + iIPr + c.END).replace("\n", "")
            if domainmatch == False and ipmatch == True and Domain != "Not defined":
                print g.PIPE + "Domain name not found." + c.END
            elif ipmatch == False and domainmatch == True:
                print g.PIPE + "IP address not found." + c.END
            else:
                print g.PIPE + "Address "+ c.G + "not found" + c.END + " in list." + c.END
    cachefiler.close()
    cachefilew.close()
    print g.PLUS + "A total of %s lines searched, %s cached files updated." % (totalLines, cacherefreshcount) + c.END
    print g.PIPE
else:
    notRun.append("Blacklists")

### SPAMLISTS
if arg.spamlists or arg.lists or arg.all:
    run.append("Spamlists")
    printh("Querying spamlists for %s..." % IPaddr)
    for bl in sourceListSpamDNS:
        try:
            my_resolver = dns.resolver.Resolver()
            query = '.'.join(reversed(str(IPaddr).split("."))) + "." + bl
            answers = my_resolver.query(query, "A")
            answer_txt = my_resolver.query(query, "TXT")
            print g.PIPE + c.Y + 'IP: %s IS listed in %s (%s: %s)' %(IPaddr, bl, answers[0], answer_txt[0]) + c.END
        except dns.resolver.NXDOMAIN:
            print g.PIPE + 'IP: %s is NOT listed in %s' %(IPaddr, bl)
    print g.PIPE
else:
    notRun.append("Spamlists")

### VIRUSTOTAL
if arg.virustotal or arg.lists or arg.all:
    try:
        VirusTotalAPIKey = os.environ['VTAPIKEY'] ### Export your api keys to shell variables or put them here, add "Export VTAPIKEY=yourapikey to .bashrc or whatever your using."
        run.append("VirusTotal")
        printh("Querying VirusTotal for %s..." % IPaddr)
        parameters = {
            'ip': IPaddr,
            'apikey': VirusTotalAPIKey
                    }
        vtresponse = requests.get('https://www.virustotal.com/vtapi/v2/ip-address/report', params=parameters).content
        vtresponse_dict = json.loads(vtresponse)
        if vtresponse_dict['response_code'] == 0:
            print g.STAR + c.Y + "VirusTotal response: IP address not in dataset." + c.END
        else:
            print g.PLUS + c.G + "VirusTotal response code", vtresponse_dict['response_code'], vtresponse_dict['verbose_msg'] + c.END
            for entry in vtresponse_dict['resolutions']:
                print g.PIPE + " =>", entry['hostname'], "Last resolved:", entry['last_resolved']
            print g.PIPE
            if len(vtresponse_dict['detected_urls']) >= 1:
                print c.G + g.PLUS + "Detections in this address:" + c.END
                for entry in vtresponse_dict['detected_urls']:
                    print g.PIPE + entry['url'].replace("http", "hxxp") + c.END
                    if entry['positives'] >= 1:
                        print g.PIPE + "Positives: ", c.R + str(entry['positives']) + c.END, "\tTotal:", entry['total'], "\tScan date:", entry['scan_date']
                    else:
                        print g.PIPE + "Positives: ", entry['positives'], "\tTotal:", entry['total'], "\tScan date:", entry['scan_date']
                    print g.PIPE
    except KeyError:
        printe("VirusTotal API key not present.", "VirusTotal")
else:
    notRun.append("VirusTotal")

### PASSIVETOTAL
if arg.passivetotal or arg.lists or arg.all:
    try:
        PassiveTotalAPIKey = os.environ['PTAPIKEY'] ### same here.
        run.append("PassiveTotal")
        #disable passivetotal's InsecureRequestWarning error message
        requests.packages.urllib3.disable_warnings()
        #define API key
        pt = PassiveTotal(PassiveTotalAPIKey)
        printh("Querying PassiveTotal for %s..." % IPaddr)
        try:
            response = ""
            response = pt.get_passive(IPaddr)
        except ValueError:
            printe("Value error - no data received.", "PassiveTotal")
        if response == "":
            g.FAIL + c.R + "Empty response, maybe your over your quota?"
        elif response['success']:
            print g.PIPE + "Query:", response['raw_query']
            print g.PIPE + "First Seen:", response['results']['first_seen']
            print g.PIPE + "Last Seen:", response['results']['last_seen']
            print g.PIPE + "Resolve Count: ", response['result_count']
            print g.PIPE + "Resolutions"
            response = response['results']
            for resolve in response['records']:
                print g.PIPE + "==> ", resolve['resolve'], "\t", resolve['firstSeen'], "\t", resolve['lastSeen'], "\t", ', '.join([ str(x) for x in resolve['source'] ])
        else:
            printe("%s" % response['error'], "PassiveTotal")
        print g.PIPE

    except KeyError:
        printe("PassiveTotal API key not present.", "PassiveTotal")
else:
    notRun.append("PassiveTotal")

### GEOIP
if arg.geoip or arg.lists or arg.all:
    run.append("GeoIP")
    if os.path.isfile(GeoIPDatabaseFile) == True:
        latitude = ""
        longitude = latitude
        try:
            gi = GeoIP.open(GeoIPDatabaseFile, GeoIP.GEOIP_STANDARD)
            gir = gi.record_by_addr(IPaddr)
            printh("Querying GeoIP database for %s" % IPaddr)
            if gir is None:
                printe("No geodata found for IP address.", "GeoIP")
            else:
                for key, value in gir.iteritems():
                    if key == "latitude":
                        latitude = value
                    elif key == "longitude":
                        longitude = value
                    print g.PIPE + str(key) + ": " + str(value)
                if latitude != "" and longitude != "":
                    print g.PIPE + "Google maps link for location: " + c.UL + "https://maps.google.com/maps?q="+str(latitude)+","+str(longitude) + c.END
                if arg.openlink:
                    webbrowser.open('https://maps.google.com/maps?q='+str(latitude)+','+str(longitude))
        except Exception:
            printe("Failed: %s %s " % (str(sys.exc_info()[0]), str(sys.exc_info()[1])), "GeoIP")
    else:
        printe("Database not found at %s" % GeoIPDatabaseFile, "GeoIP")
        printe("Please install GeoIP database. http://dev.maxmind.com/geoip/legacy/install/city/", "")
    print g.PIPE
else:
    notRun.append("GeoIP")

### WHOIS
if arg.whois or arg.lists or arg.all:
    run.append("Whois")
    results = results2 = ""
    try:
        results = subprocess.check_output("whois "+IPaddr, shell=True)
    except subprocess.CalledProcessError:
        printe("Whois returned an error.", "Whois")
    if Domain != "Not defined":
        try:
            results2 = subprocess.check_output("whois "+Domain, shell=True)
        except subprocess.CalledProcessError:
            printe("Whois returned an error.", "Whois")
    if results:
        printh("Querying IP Address %s" % IPaddr)
        for line in results.splitlines():
            if ("abuse" in line and "@" in line) or "address" in line or "person" in line or "phone" in line:
                print g.PIPE + c.BOLD + c.B + line + c.END
            elif "descr" in line:
                print g.PIPE + c.BOLD + c.Y + line + c.END
            else:
                print g.PIPE + line  + c.END
    if results2:
        print c.HDR +  g.PLUS + "Resolved address " + IPaddr + " for domain " + Domain + c.END
        for line in results2.splitlines():
            if "#" in line:
                ()
            elif ("abuse" in line and "@" in line) or "address" in line or "person" in line or "phone" in line:
                print g.PIPE + c.BOLD + c.B + line + c.END
            elif "descr" in line:
                print g.PIPE + c.BOLD + c.Y + line + c.END
            else:
                print g.PIPE + line  + c.END
        print g.PIPE
else:
    notRun.append("Whois")

#### PING
if arg.ping or arg.probes or arg.all:
    run.append("Ping")
    printh("Pinging %s, skip with CTRL-C..." % IPaddr)
    try:
        response = os.system("ping -c 1 " + IPaddr + " > /dev/null 2>&1")
        if response == 0:
            print g.PIPE + c.G + IPaddr, 'is responding to ping.' + c.END
        else:
            print g.PIPE + c.R + IPaddr, 'is not responding to ping.' + c.END
            print g.PIPE + c.END
    except KeyboardInterrupt:
        print c.Y + g.MINUS + "Skipping ping." + c.END
        notRun.append("Ping")
    print g.PIPE
else:
    notRun.append("Ping")

### OPENSSL
if arg.cert or arg.probes or arg.all:
    run.append("OpenSSL")
    results = None
    try:
        results = subprocess.check_output("echo | openssl s_client -showcerts -servername %s -connect %s:443 2>/dev/null | openssl x509 -inform pem -noout -text" % (Domain, Domain), shell=True)
    except subprocess.CalledProcessError:
        printe("OpenSSL returned an error.", "OpenSSL")
    if results:
        printh("Certificate information for https://%s/" % Domain)
        for line in results.splitlines():
            if "Issuer" in line or "Subject:" in line or "DNS:" in line or "Not Before" in line or "Not After" in line:
                print g.PIPE + c.B + line.replace("  ", " ") + c.END
            else:
                print g.PIPE + line.replace("  ", " ") + c.END
else:
    notRun.append("OpenSSL")

### SCANPORTS & SCANHEADERS
if arg.scanports or arg.scanheaders or arg.probes or arg.all:
    run.append("Portscan")
    printh("Scanning common ports...")
    socket.setdefaulttimeout(1)
    openports = []
    try:
        for port in targetPortscan:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((IPaddr, port))
            if result == 0:
                print g.PIPE + c.G + "port " + str(port) + " is open." + c.END
                openports.append(port)
            else:
                print g.PIPE + "Port %s is closed." % port
            sock.close()
        if (arg.scanheaders or arg.probes or arg.all) and Domain != "Not defined":
            for port in openports:
                url = "http://" + Domain
                try:
                    if port == 443:
                        protocol = "https://"
                    else:
                        protocol = "http://"
                    print g.PIPE
                    print g.PLUS + "Getting headers for %s%s:%s" % (protocol, Domain, port) + c.END
                    page = requests.head('%s%s:%s' % (protocol, Domain, port), headers={'user-agent': random.choice(uapool), 'referer': 'https://www.google.com'})
                    print g.PIPE + c.BOLD + "Server response code: %s" % page.status_code + c.END
                    for key, value in page.headers.items():
                        print g.PIPE + c.BOLD + "%s: %s" % (key, value) + c.END
                except Exception,e:
                    printe(str(e), "Headerscan")
    except KeyboardInterrupt:
        print c.R + g.STAR + "Caught Ctrl+C, interrupting..."
        sys.terminate()
    except socket.gaierror:
        print c.R + g.STAR + "Hostname could not be resolved. Exiting..."
        sys.terminate()
    except socket.error:
        print c.R + g.STAR + "Couldn't connect to server."
        sys.terminate()
    print g.PIPE + c.END
else:
    notRun.append("Portscan")
if logfile != None:
    printh("Writing log file to %s" % logfile)
terminate()
