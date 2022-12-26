import reverso_api

def translate_sentence2arabic(text):
    try:
        api = reverso_api.context.ReversoContextAPI(text, "", "en", "ar")
        return api.translate_sentence()
    except Exception as e:
        print(f"translate_sentence2arabic -> {e}")
        
    
def main():
    word       = "Hello, World!"
    translated = translate_sentence2arabic(word)
    print(translated)


if __name__ == '__main__':
	main()