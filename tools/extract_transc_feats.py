# coding=utf-8

from __future__ import print_function
import glob
import re
import string
import itertools

import nltk


VOCAB_FILE = "data/vocab.txt"
TRANSC_RAW_DIR = "data/raw/transc"
TRANSC_FEATS_FILE = "data/feats/transc.txt"
BLACKLIST = ["244623.txt", "243646.txt", "181504.txt", "221153.txt"]


with open(VOCAB_FILE) as vf:
    vocab = {line.strip(): i for (i, line) in enumerate(vf)}
max_feat_vec_len = 0
feat_vecs_written = 0

with open(TRANSC_FEATS_FILE, "w") as feats_file:
    for fname in glob.iglob(TRANSC_RAW_DIR + "/*"):
        if any(fname.endswith(s) for s in BLACKLIST):
            print("Ignoring '{}' (blacklisted)".format(fname))
            continue
        with open(fname) as f:
            transc_str = f.read()

        # Convert the transcription to lower case, but make
        # filler markers (like "umm", "uhh" etc.) upper case.
        transc_str = transc_str.lower()
        m = re.findall("[{(]([^\s]*?)[)}]", transc_str)
        for word in m:
            transc_str = re.sub("[({{]{}[)}}]".format(word),
                                word.upper(), transc_str)

        # Construct the feature vector.
        toks = nltk.word_tokenize(transc_str)
        feat_vec = []
        for tok in toks:
            if not tok in vocab:
                if not all(c in string.ascii_lowercase for c in tok):
                    # Learn the special words.
                    vocab[tok] = len(vocab)
            if tok in vocab:
                feat_vec.append(vocab[tok])
            else:
                feat_vec.append(-1)

        if len(feat_vec) > max_feat_vec_len:
            max_feat_vec_len = len(feat_vec)

        print(" ".join(itertools.imap(str, feat_vec)), file=feats_file)
        feat_vecs_written += 1

print("{} features written".format(feat_vecs_written))
print("Max feature vector length: {}".format(max_feat_vec_len))

