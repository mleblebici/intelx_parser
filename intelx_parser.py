from intelxapi import intelx
from os import listdir, mkdir, path, remove, rmdir, linesep
import xlsxwriter
import argparse

parser = argparse.ArgumentParser(description='Get leaked accounts from intelx')
parser.add_argument('--domain', '-d', metavar='example.com', type=str, help="the domain to search for", required=True)
parser.add_argument('--apikey', '-k', metavar='xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx', type=str, help="intel.x API key value", required=True)
parser.add_argument('--extract', '-e', type=str, help='extract only results containing this string', default='UNSPECIFIED', required=False)
args = parser.parse_args()

domain = args.domain
APIKEY = args.apikey
searchDomain = args.extract

print("[*] Searching intelx...")
intelx = intelx(APIKEY)
results = intelx.search(domain, media=24, maxresults=9000)

records = results['records']
print("\t[+] Got " + str(len(records)) + " records for " + domain)

if not path.exists(domain):
    mkdir(domain)
else:
    try:
        remove(domain + '/' + domain + '.xlsx')
    except:
        pass

    print("\n[*] Updating previous search results")

for record in records:
    if "password" in record['name'].lower():
        intelx.FILE_READ(record['systemid'], 0, record['bucket'], domain + '/' + record['name'].replace('/','')+'.txt')

if len(listdir(domain)) == 0:
    rmdir(domain)
    print("\n[-] No leaked account credentials found!")
    exit()
else:
    print("\n[*] Found " + str(len(listdir(domain))) + " leaked files.")
    
def getRecord(line, delimeter):
    result = line.replace(delimeter, '').strip()
    if result:
        return result
    else:
        return "EMPTY_RECORD"

filenames = listdir(domain)
    
urls = []
usernames = []
passwords = []

for filename in filenames:
    print("\t[+] Parsing [" + str(filenames.index(filename) + 1) + '/' + str(len(filenames)) + '] ' + filename + " ...")
    filename = domain + '/' + filename
    f = open(filename, encoding='unicode-escape')
    lines = f.readlines()
    f.close()

    for i in range(len(lines)):
        lines[i] = lines[i].replace('\n','')
        
    for line in lines:
        url = ''
        username = ''
        password = ''
        if "URL:" in line:
            url = getRecord(line, "URL:")
        elif "Url:" in line:
            url = getRecord(line, "Url:")
        elif "Host:" in line:
            url = getRecord(line, "Host:")
        elif "HOST:" in line:
            url = getRecord(line, "HOST:")
        
        if "Username:" in line:
            username = getRecord(line, "Username:")
        elif "Login:" in line:
            username = getRecord(line, "Login:")
        elif "USER:" in line:
            username = getRecord(line, "USER:")
            
        if "Password:" in line:
            password = getRecord(line, "Password:")
        elif "PASS:" in line:
            password = getRecord(line, "PASS:")
        
        if url:
            urls.append(url)
        if username:
            usernames.append(username)
        if password:
            passwords.append(password)
        
        

if ((len(urls) != len(usernames)) or (len(passwords) != len(urls)) or (len(usernames) != len(passwords))):
    print("Something went wrong during parsing, exiting...")
    exit()

print("\n[*] Writing results to " + domain + '.xlsx')

workbook = xlsxwriter.Workbook(domain + '/' + domain + '.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write(0, 0, "Domain")
worksheet.write(0, 1, "Username")
worksheet.write(0, 2, "Password")
row = 1
for i in range(len(urls)):
    if searchDomain != 'UNSPECIFIED':
        if searchDomain in urls[i]:
            worksheet.write(row, 0, urls[i])
            worksheet.write(row, 1, usernames[i])
            worksheet.write(row, 2, passwords[i])
            row = row + 1
    else:
        worksheet.write(row, 0, urls[i])
        worksheet.write(row, 1, usernames[i])
        worksheet.write(row, 2, passwords[i])
        row = row + 1

workbook.close()
