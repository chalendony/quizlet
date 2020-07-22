from reverso_api.context import ReversoContextAPI


api = ReversoContextAPI(
                        "gelangen",
                        "",
                        "de",
                        "en "
                        )


for source_word, translation, frequency, part_of_speech, inflected_forms in api.get_translations():
    print(source_word, "==", translation)
    print("Frequency (how many word usage examples contain this word):", frequency)
    print("Part of speech:", part_of_speech if part_of_speech else "unknown")
    if inflected_forms:
        print("Inflected forms:", ", ".join(map(lambda form: str(form.translation), inflected_forms)))
    print()

examples = api.get_translation_examples_pair_by_pair()
for _ in range(10):
    source, target = next(examples)
    print(source.text, "==", target.text)