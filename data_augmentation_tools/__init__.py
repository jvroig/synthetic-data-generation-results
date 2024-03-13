import random
import string
import contractions
from nltk.corpus import wordnet
from googletrans import Translator

global_default_rate=0.02

def random_char_insertion(input_string, insertion_rate=global_default_rate):
    num_chars_to_insert = int(len(input_string) * insertion_rate)
    chars_list = list(input_string)
    for _ in range(num_chars_to_insert):
        random_index = random.randint(0, len(chars_list))
        random_char = random.choice(string.ascii_letters + string.digits)
        chars_list.insert(random_index, random_char)
    return ''.join(chars_list)

def random_char_removal(input_string, removal_rate=global_default_rate):
    num_chars_to_remove = int(len(input_string) * removal_rate)
    chars_list = list(input_string)
    for _ in range(num_chars_to_remove):
        if chars_list:
            random_index = random.randint(0, len(chars_list) - 1)
            del chars_list[random_index]
    return ''.join(chars_list)

def random_char_replacement(input_string, replacement_rate=global_default_rate):
    num_chars_to_replace = int(len(input_string) * replacement_rate)
    chars_list = list(input_string)
    for _ in range(num_chars_to_replace):
        random_index = random.randint(0, len(chars_list) - 1)
        random_char = random.choice(string.ascii_letters + string.digits)
        chars_list[random_index] = random_char
    return ''.join(chars_list)
    
def random_adjacent_swap(input_string, swap_rate=global_default_rate):
    chars_list = list(input_string)
    for i in range(0, len(chars_list) - 1):
        if random.random() < swap_rate:
            chars_list[i], chars_list[i + 1] = chars_list[i + 1], chars_list[i]
    return ''.join(chars_list)
    
def random_word_deletion(input_string, deletion_rate=global_default_rate):
    words = input_string.split()
    num_words_to_delete = int(len(words) * deletion_rate)
    words_to_delete = random.sample(words, num_words_to_delete)
    output_words = [word for word in words if word not in words_to_delete]
    return ' '.join(output_words)

def random_word_insertion(input_string, insertion_rate=global_default_rate):
    words = input_string.split()
    num_words_to_insert = int(len(words) * insertion_rate)
    for _ in range(num_words_to_insert):
        random_index = random.randint(0, len(words))
        random_word = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, 10)))
        words.insert(random_index, random_word)
    return ' '.join(words)
    
def random_word_replacement(input_string, replacement_rate=global_default_rate):
    words = input_string.split()
    num_words_to_replace = int(len(words) * replacement_rate)
    replacement_words = ['apple', 'banana', 'orange', 'grape', 'peach']  # Example replacement words
    for _ in range(num_words_to_replace):
        random_index = random.randint(0, len(words) - 1)
        words[random_index] = random.choice(replacement_words)
    return ' '.join(words)
    
def random_sentence_deletion(input_string, deletion_rate=global_default_rate):
    sentences = input_string.split('.')
    num_sentences_to_delete = int(len(sentences) * deletion_rate)
    sentences_to_delete = random.sample(sentences, num_sentences_to_delete)
    output_sentences = [sentence for sentence in sentences if sentence not in sentences_to_delete]
    return '.'.join(output_sentences)

def random_word_shuffle(input_string, shuffle_rate=global_default_rate):
    words = input_string.split()
    shuffled_words = words.copy()
    for _ in range(len(words)):
        if random.random() < shuffle_rate:
            random.shuffle(shuffled_words)
            break  # Shuffle only once
    return ' '.join(shuffled_words)
    
    
def synonym_replacement(input_string, replacement_rate=global_default_rate):
    def get_synonyms(word):
        synonyms = set()
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name())
        return list(synonyms)

    words = input_string.split()
    num_words_to_replace = int(len(words) * replacement_rate)
    for _ in range(num_words_to_replace):
        random_index = random.randint(0, len(words) - 1)
        word = words[random_index]
        synonyms = get_synonyms(word)
        if synonyms:
            replacement = random.choice(synonyms)
            words[random_index] = replacement
    return ' '.join(words)

def expand_contractions(input_string):
    return contractions.fix(input_string)

def noise_injection(input_string, noise_rate=global_default_rate):
    num_noise_chars = int(len(input_string) * noise_rate)
    noise_chars = string.punctuation + string.digits  # Special characters and digits
    noisy_string = list(input_string)
    for _ in range(num_noise_chars):
        random_index = random.randint(0, len(noisy_string) - 1)
        noisy_string[random_index] = random.choice(noise_chars)
    return ''.join(noisy_string)
    
    
def back_translation_augmentation(input_string, target_lang='fr'):
    translator = Translator()
    translated = translator.translate(input_string, dest=target_lang).text
    back_translated = translator.translate(translated, dest='en').text
    return back_translated
    
def keyboard_typos_simulation(input_string, typo_rate=global_default_rate):
    adjacent_keys = {
        'a': 'qwsxz',
        'b': 'vghn',
        'c': 'xdfv',
        'd': 'serfcx',
        'e': 'wrsdf',
        'f': 'drtgvc',
        'g': 'ftyhbv',
        'h': 'gyujnb',
        'i': 'uojk',
        'j': 'huiknm',
        'k': 'jiolm',
        'l': 'kop',
        'm': 'njk',
        'n': 'bhjm',
        'o': 'iklp',
        'p': 'ol',
        'q': 'wa',
        'r': 'etfcd',
        's': 'awedxz',
        't': 'rygf',
        'u': 'yihj',
        'v': 'cfgb',
        'w': 'qase',
        'x': 'zsdc',
        'y': 'tugh',
        'z': 'asx',
    }
    typo_chars = string.ascii_lowercase + string.digits + ' '
    typo_string = list(input_string)
    for i in range(len(typo_string)):
        if random.random() < typo_rate:
            original_char = typo_string[i].lower()
            if original_char in adjacent_keys:
                replacement_char = random.choice(adjacent_keys[original_char])
                typo_string[i] = replacement_char if typo_string[i].islower() else replacement_char.upper()
            else:
                typo_string[i] = random.choice(typo_chars)
    return ''.join(typo_string)
    
def text_duplication(input_string, duplication_rate=0.1):
    start_pos = random.randint(0, len(input_string) - 1)
    end_pos = random.randint(start_pos + 1, len(input_string))
    duplicated_segment = input_string[start_pos:end_pos]
    return input_string[:end_pos] + duplicated_segment + input_string[end_pos:]




augmentation_functions = [
    random_char_insertion,
    random_char_removal,
    random_char_replacement,
    random_adjacent_swap,
    random_word_deletion,
    random_word_insertion,
    random_word_replacement,
    random_sentence_deletion,
    random_word_shuffle,
    # synonym_replacement,
    expand_contractions,
    noise_injection,
    # back_translation_augmentation,
    keyboard_typos_simulation,
    text_duplication,
]

def apply_augmentations(input_string, augmentation_functions=augmentation_functions):
    augmented_strings = []
    for func in augmentation_functions:
        augmented_strings.append(func(input_string))
    return augmented_strings