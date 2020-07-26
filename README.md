# Reverso-API

### What's this?
*This is a wrapper around Reverso's ([reverso.net](https://reverso.net)) API for Python.*

## What is Reverso?
[Reverso](https://reverso.net) is a pretty powerful and useful tool for those who learn foreign languages.
It consists of such sub-apps:
+ [Context](https://context.reverso.net) -- translation of words and complex phrases with usage examples provided.
+ [Conjugator](https://conjugator.reverso.net) -- a verb conjugator.
+ [Dictionary](https://dictionary.reverso.net) -- a dictionary (both definitions and translations to other languages).
+ [Spell Checker](https://reverso.net/spell-checker) -- a spell checker.
+ [Translation](https://www.reverso.net/text_translation.aspx) -- a translator which supports sentences, apart from words and phrases.
+ and others

It also has a pretty good "Say" feature for various languages ([Reverso Voice](https://voice.reverso.net/RestPronunciation.svc/help);
[here](https://voice.reverso.net/RestPronunciation.svc/v1/output=json/GetVoiceStream/voiceName=Heather22k?inputText=VGhpcyBpcyBhbiBleGFtcGxlIG9mIGEgdGV4dCwgc3Bva2VuIGJ5IFJldmVyc28gVm9pY2U=) is an example of text, spoken by it).

### Features
Currently, the wrapper provides Reverso Context API and Reverso Voice API.

### Getting started

#### Installation
First, install the package with pip. Just type this in the terminal/command-line:
```
pip install reverso-api
```

#### Docs
Docs are not ready yet. However, there is a draft in the [docs](https://github.com/demian-wolf/Reverso-API/tree/master/docs) project directory.

#### Examples
In addition there are several examples that can help you to figure out how to use this library.
You can find them in the [examples](https://github.com/demian-wolf/ReversoAPI/tree/master/examples)
project directory.

Note that examples that have speaking feature require pygame to work.