# intelx_parser
Export leaked credentials from intelx search results to excel file

```
usage: intelx_parser.py [-h] --domain example.com --apikey xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx [--extract EXTRACT]

Get leaked accounts from intelx

options:
  -h, --help            show this help message and exit
  --domain example.com, -d example.com
                        the domain to search for
  --apikey xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx, -k xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
                        intel.x API key value
  --extract EXTRACT, -e EXTRACT
                        extract only results containing this string
```

intelxapi.py is taken from https://github.com/IntelligenceX/SDK/blob/master/Python/intelxapi.py
