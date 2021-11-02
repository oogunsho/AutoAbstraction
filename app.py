# for the app as a whole
import nltk.data
import kivy
import re
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
import os
import platform

# for keyword extraction
from rake_nltk import Metric, Rake
from file_changer import FileChanger

# for abstract extraction
from collections import Counter

# from PyDictionary import PyDictionary
from nltk.stem import PorterStemmer
import nltk

nltk.download('punkt')
OUTPUT_FILE = "output.txt"


class AbstractFloat(FloatLayout):
    current_file = ""
    key_word_count = ObjectProperty(None)
    abstract_word_count = ObjectProperty(None)
    abstract_percent = ObjectProperty(None)
    error_label = None

    def _on_file_drop(self, window, file_path):
        self.current_file = str(file_path)[2:-1]
        return

    def on_touch_up(self, touch):
        if touch.is_double_tap:
            if self.error_label != None:
                self.remove_widget(self.error_label)
            self.error_label = None

    def set_key_words(self, x):
        self.key_word_count.text = x

    def set_abstract_words(self, x):
        self.abstract_word_count.text = x

    def set_abstract_percent(self, x):
        self.abstract_percent.text = x

    def create_error_label(self, x):
        if self.error_label:
            self.remove_widget(self.error_label)
        label = BackgroundLabel(
            text=x+"\nDouble Click to remove error message",
            font_size=20,
            size_hint=(.65, .2),
            halign='center',
            pos_hint={'x': .175, 'y': .4})
        label.set_bgcolor(1, 0, 0, 1)
        self.error_label = label
        self.add_widget(self.error_label)

    def extract_key_words(self, x):
        if not x:
            self.create_error_label(
                "No input detected for the number of key words")
            return
        if not self.current_file:
            self.create_error_label(
                "No file has been dropped into the app.\nPlease drop the file to be processed.")
            return
        try:
            f = open(self.current_file)
            f.close()
        except OSError:
            self.create_error_label(
                "File was not located in the path.\nPlease drop again the file to be processed.")
            return

        word_count = int(x)

        # string directly from file
        tf = FileChanger(self.current_file).text()
        with open(tf) as f:
            fs = f.read()
            # processed file string
            fs = " ".join(re.split('\W+', fs))
        

        # extracting key words
        extractor = Rake(ranking_metric=Metric.WORD_FREQUENCY, max_length=5)
        extractor.extract_keywords_from_text(fs)
        keywords = "\n".join(
            extractor.get_ranked_phrases()[:word_count])
        with open(OUTPUT_FILE, "w") as f:
            f.write(keywords)
        if platform.system() == "Windows":
            os.system("start " + OUTPUT_FILE)
        else:
            os.system("xdg-open " + OUTPUT_FILE)

    def extract_abstract(self, x):
        # errors
        if not x:
            self.create_error_label(
                "No input detected for the abstract word count")
            return
        if x == "%":
            self.create_error_label(
                "No input detected for the abstract word percentage")
            return
        if not self.current_file:
            self.create_error_label(
                "No file has been dropped into the app.\nPlease drop the file to be processed.")
            return
        try:
            f = open(self.current_file)
            f.close()
        except OSError:
            self.create_error_label(
                "File was not located in the path.\nPlease drop again the file to be processed.")
            return

        # code
        if x[-1] == "%":
            word_count = 0
        else:
            word_count = int(x)

        # change file to be preocessed to text/txt/plain file
        tf = FileChanger(self.current_file).text()

        # split the file into words
        with open(tf) as f:
            words = re.split('\W+', f.read())

        # create stop list from file
        sl = set()
        with open("stoplist.txt") as f:
            for w in f.read().split("\n"):
                sl.add(w)

        # count the words in the words list
        stem_con = Counter()
        word_to_stem = dict()
        porter = PorterStemmer()
        doc_count = 0
        for word in words:
            word = word.lower()
            if word:
                doc_count += 1
            if word and word not in sl:
                stem = porter.stem(word)
                word_to_stem[word] = stem
                stem_con[stem] += 1
        word_count = int((float(x[:-1])/100)*doc_count)

        # split the file into sentences
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        with open(tf) as f:
            sentences = tokenizer.tokenize(
                f.read().replace("\n\n", ". ").replace("\n", " "))

        # rank the sentences
        ranked_sentences = []
        for i, sentence in enumerate(sentences):
            s_to_w = re.split('\W+', sentence)
            ranked_sentences.append((sentence.replace("..", ".").replace("?.", "?"), i, sum(
                map(lambda x: stem_con[word_to_stem.get(x.lower())], s_to_w)), len(s_to_w)-1))
        ranked_sentences.sort(key=lambda x: -x[2])
        so_far = 0
        ranked_abstract = []
        for sentence in ranked_sentences:
            so_far += sentence[3]
            if so_far > word_count:
                break
            ranked_abstract.append(sentence)
        ranked_abstract.sort(key=lambda x: x[1])
        with open(OUTPUT_FILE, "w") as f:
            for sentence in ranked_abstract:
                f.write(sentence[0]+" ")
        if platform.system() == "Windows":
            os.system("start " + OUTPUT_FILE)
        else:
            os.system("xdg-open " + OUTPUT_FILE)


class BackgroundLabel(Label):
    def set_bgcolor(self, r, b, g, o):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(r, g, b, o)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect,
                  size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


DEFAULT_PADDING = 6


class AlignedTextInput(TextInput):

    def __init__(self, **kwargs):
        self.bind(on_text=self.on_text)
        super().__init__(**kwargs)

    def on_text(self, instance, value):
        self.redraw()

    def on_size(self, instance, value):
        self.redraw()

    def redraw(self):
        """ 
        Note: This methods depends on internal variables of its TextInput
        base class (_lines_rects and _refresh_text())
        """

        self._refresh_text(self.text)

        max_size = max(self._lines_rects, key=lambda r: r.size[0]).size
        num_lines = len(self._lines_rects)

        d = (self.width - max_size[0]) / 2.0 - DEFAULT_PADDING
        self.padding_x = [d, d]

        d = (self.height - max_size[1] * num_lines) / 2.0 - DEFAULT_PADDING
        self.padding_y = [d, d]


class IntInput(AlignedTextInput):

    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if (not self.text) and substring == "0":
            s = ""
        else:
            s = re.sub(pat, '', substring)
        return super(IntInput, self).insert_text(s, from_undo=from_undo)


class FloatInput(AlignedTextInput):

    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if (not self.text) and substring == "0":
            s = ""
        elif '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)


class AbstractionApp(App):

    def build(self):
        f = AbstractFloat()
        Window.bind(on_dropfile=f._on_file_drop)
        return f


if __name__ == "__main__":
    AbstractionApp().run()
