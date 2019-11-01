from collections import OrderedDict
from random import shuffle
import codecs

from constants import *
from util import get_similarity_score

class Processor():
    def __init__(self):
        self.keywords = []
        self.examples = OrderedDict()
        self.picked_quizlet_pairs = None

    def generate_new_quizlet(self):
        self.extract_dictionary_from_file()
        self.pick_quizlet_set()
        self.write_quizlet_set()

    def extract_dictionary_from_file(self):
        dictionary_file = codecs.open(VOCABULARY_PATH, 'r', 'utf8')
        word_batch = []
        for line in dictionary_file:
            line = line.strip()
            if len(line) == 0:
                self.push_batch_to_dictionary(word_batch)
                word_batch = []
                continue
            word_batch.append(line)
        self.push_batch_to_dictionary(word_batch)

    def push_batch_to_dictionary(self, word_batch):
        if len(word_batch) < 2: return
        keyword = word_batch[0]
        self.keywords.append(keyword)
        self.examples[keyword] = word_batch[1:]

    def pick_quizlet_set(self):
        self.picked_quizlet_pairs = []
        self.shuffle_dictionary()
        for keyword in self.keywords[:NUM_QUIZLET_KEYWORDS]:
            self.picked_quizlet_pairs.append((keyword, self.examples[keyword][:NUM_EXAMPLES_PER_WORD]))

    def write_quizlet_set(self):
        quizlet_file = open(QUIZLET_PATH, 'w')
        for (keyword, full_sentences) in self.picked_quizlet_pairs:
            for full_sentence in full_sentences:
                answer, blank_sentence = self.get_answer_blank_sentence_pair(keyword, full_sentence)
                quizlet_content = "{}|{}\n".format(answer, blank_sentence)
                quizlet_file.write(quizlet_content)
                print (quizlet_content, end='')


    def shuffle_dictionary(self):
        for keyword in self.keywords:
            shuffle(self.examples[keyword])
        shuffle(self.keywords)

    def get_answer_blank_sentence_pair(self, keyword, full_sentence):
        word_list = self.get_word_list(full_sentence)
        similar_word, index = self.get_similar_word_and_index(keyword, word_list)
        word_list[index] = '_____________'
        return similar_word, ' '.join(word_list)

    def get_word_list(self, full_sentence):
        word_list = full_sentence.split(' ')
        word_list = [self.remove_redundant_chars(word) for word in word_list]
        return word_list

    def remove_redundant_chars(self, text):
        redudant_chars = ".,:;!?"
        return ''.join(c for c in text if c not in redudant_chars)

    def get_similar_word_and_index(self, keyword, word_list):
        max_similarity_score, max_index = -1, 0
        for index, word in enumerate(word_list):
            similarity_score = get_similarity_score(keyword.lower(), word.lower())
            if max_similarity_score < similarity_score:
                max_similarity_score = similarity_score
                max_index = index
        return word_list[max_index], max_index


