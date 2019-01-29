## Introduction
It's a very simple command line script to translate use YouDao API developed by Python

YouDao:
http://fanyi.youdao.com/

**Big**: Now rigister you can get ￥100 for service.(*not AD*)
## Usage
```
git clone https://github.com/trisolaris233/trans
cd trans
./install.sh
```

then it will create a folder with some files where the configuration file and logs are stored
```
~/.trans/config.json
~/.trans/trans.log
```

in `config.json`, put your appkey and secret key into and save it.
Now everything is OK, you can use it.

---
### How to use
Here are the most simple examples for it.
```
trans hello
['你好']
```
```
trans "来呀快活呀"
['Come and have fun']
```

But for further using there're some options for you to use. You can type `trans -h` or `trans --help` for help. Now there I can show it for you.
```bash
trans -h

Welcome to trans.It is a very simple commandline-based translation software.
	-q(--query): show the query text
	-w(--web): show the web translation
	-l(--lan): show the language between source and target
	-f(--from) <language_type>: set the source language type into language_type
	-t(--to) <language_type>: set the target language type into langugae_type


Here're language types supported:
['zh', 'ja', 'en', 'ko', 'fr', 'ar', 'pl', 'da', 'de', 'ru', 'fi', 'nl', 'cs', 'ro', 'no', 'pt', 'sv', 'es', 'hi', 'id', 'it', 'th', 'tr', 'el', 'hu', 'auto']
```
