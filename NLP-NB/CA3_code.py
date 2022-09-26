from __future__ import unicode_literals
from hazm import *
import pandas as pd
import time
import math

ALPHA = 1
TITLE_WEIGHT = 2
NOT_A_WORD = [",", ".", "/", "؟", "!", "(", ")", "ـ", "-", "*", "**", "،"]


def count_in_class(word, recommend):
    # prev_count = rec_count[word]
    if recommend == 'recommended':
        if word in rec_word_count:
            rec_word_count[word] += 1
        else:
            rec_word_count[word] = 1
    elif recommend == 'not_recommended':
        if word in not_rec_word_count:
            not_rec_word_count[word] += 1
        else:
            not_rec_word_count[word] = 1
    return


def parse(title, comment, recommend, is_train):
    opinion = ""
    for i in range(TITLE_WEIGHT):
        opinion += title
        opinion += " "

    opinion = opinion + " " + comment
    opinion = norm.normalize(opinion)
    words = word_tokenize(opinion)
    accepted_words = []
    for i in range(len(words)):
        # if words[i] not in stopwords_list():
        if words[i] not in NOT_A_WORD:
            words[i] = lem.lemmatize(words[i])
            # words[i] = stemmer.stem(words[i])
            if is_train:
                count_in_class(words[i], recommend)
            accepted_words.append(words[i])

    return accepted_words


def calc_conditional_prob(word):
    if word in rec_word_count:
        rec_count = rec_word_count[word]
    else:
        rec_count = 0
    if word in not_rec_word_count:
        not_rec_count = not_rec_word_count[word]
    else:
        not_rec_count = 0
    if ALPHA > 0:
        rec_cond = (rec_count + ALPHA) / (total_rec_words + len(rec_word_count) * ALPHA)
        not_rec_cond = (not_rec_count + ALPHA) / (total_not_rec_words + len(not_rec_word_count) * ALPHA)
        return math.log2(rec_cond), math.log2(not_rec_cond)
    else:
        return (rec_count / total_rec_words), (not_rec_count / total_not_rec_words)


def guess_recommendation(title, comment):
    rec_prob_log = math.log2(rec_prob)
    not_rec_prob_log = math.log2(not_rec_prob)
    words = parse(title, comment, "", False)
    for i in range(len(words)):
        words[i] = lem.lemmatize(words[i])
        rec_cond, not_rec_cond = calc_conditional_prob(words[i])
        rec_prob_log += rec_cond
        not_rec_prob_log += not_rec_cond

    if not_rec_prob_log > rec_prob_log:
        return "not_recommended"
    else:
        return "recommended"


def guess_without_additive(title, comment):
    words = parse(title, comment, "", False)
    rec_prob_comm = rec_prob
    not_rec_prob_comm = not_rec_prob
    for i in range(len(words)):
        if not_rec_prob_comm == 0 or rec_prob_comm == 0:
            break
        words[i] = lem.lemmatize(words[i])
        rec_cond, not_rec_cond = calc_conditional_prob(words[i])
        rec_prob_comm *= rec_cond
        not_rec_prob_comm *= not_rec_cond

    if not_rec_prob_comm > rec_prob_comm:
        return "not_recommended"
    else:
        return "recommended"


def calc_total_words():
    total_rec = 0
    total_not_rec = 0
    for key in rec_word_count:
        total_rec += rec_word_count[key]
    for key in not_rec_word_count:
        total_not_rec += not_rec_word_count[key]

    return total_rec, total_not_rec


st = time.time()
lem = Lemmatizer()
norm = Normalizer()
stemmer = Stemmer()
rec_word_count = {}
not_rec_word_count = {}
stopwords = stopwords_list()
TrainDF = pd.read_csv('CA3_dataset/comment_train.csv')
TrainDF['words'] = TrainDF.apply(lambda row: parse(row['title'], row['comment'], row['recommend'], True), axis=1)
classes_count = TrainDF['recommend'].value_counts()
rec_prob = classes_count['recommended'] / len(TrainDF)
not_rec_prob = classes_count['not_recommended'] / len(TrainDF)
total_rec_words, total_not_rec_words = calc_total_words()
TestDF = pd.read_csv('CA3_dataset/comment_test.csv')

# For removing Additive smoothing, comment the below line out AND SET THE ALPHA TO 0 !!!!

TestDF['guessed_recommendation'] = TestDF.apply(lambda row: guess_recommendation(row['title'], row['comment']), axis=1)

# TestDF['guessed_recommendation'] = TestDF.apply(lambda row: guess_without_additive(row['title'], row['comment']), axis=1)

correct_detected_recommendation = len(TestDF[(TestDF["recommend"] == "recommended") & (TestDF["guessed_recommendation"] == "recommended")])
accuracy = len(TestDF[(TestDF["recommend"] == TestDF["guessed_recommendation"])]) / len(TestDF)
precision = correct_detected_recommendation / len(TestDF[(TestDF["guessed_recommendation"] == "recommended")])
recall = correct_detected_recommendation / len(TestDF[(TestDF["recommend"] == "recommended")])
f1 = 2 * precision * recall / (precision + recall)
end = time.time()
print("time was %f seconds!" % (end - st))
print("Accuracy: ", accuracy)
print("Precision: ", precision)
print("Recall: ", recall)
print("F1: ", f1)
