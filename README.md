# Reverso-API
##### A Pythonic wrapper around Reverso's ([reverso.net](https://reverso.net)) API.

### About Reverso services
[Reverso](https://reverso.net) is a really powerful tool for foreign languages learners.
It provides many different services, including but not limited to these:
+ [Context](https://context.reverso.net) — translates words and complex phrases with usage examples
+ [Conjugator](https://conjugator.reverso.net) — verb conjugator
+ [Dictionary](https://dictionary.reverso.net) — a dictionary (both definitions and translations to other languages)
+ [Spell Checker](https://reverso.net/spell-checker) — a spell checker
+ [Translation](https://www.reverso.net/text_translation.aspx) — a translator that supports sentences, words and phrases

Another great feature of this website is its own text-to-speech engine for plenty of languages. ([Reverso Voice](https://voice.reverso.net/RestPronunciation.svc/help);
[here](https://voice.reverso.net/RestPronunciation.svc/v1/output=json/GetVoiceStream/voiceName=Heather22k?inputText=VGhpcyBpcyBhbiBleGFtcGxlIG9mIGEgdGV4dCwgc3Bva2VuIGJ5IFJldmVyc28gVm9pY2U=) is an example of text, spoken by it).

### About this wrapper
Currently, Context and Voice services are supported.

#### Contributing
I keep working on this project, adding new features and fixing bugs every couple of weeks.
If you want to help me, file/respond to an issue or create a PR request! Any contributions would be greatly appreciated!

### Getting started

#### Installation
You have to install the package via pip. Just type this in the terminal/command line:
```
pip install reverso-api
```

#### Docs
Docs are not ready yet.

#### Examples
There are some usage examples to help you figure out how to use this library.
You can find them in the [examples](https://github.com/demian-wolf/ReversoAPI/tree/master/examples)
project directory.

**Keep in mind** that examples with text-to-speech require pygame to work!
