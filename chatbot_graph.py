#!/usr/bin/env python3
# coding: utf-8
# File: answer_search.py
# Author: zlh<994182204@mail.dlut.edu.cn>
# Date: 23-4-21

from question_classifier import *
from question_parser import *
from answer_search import *

'''问答类'''


class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = '您好，我是在线音乐查询系统--小易，希望可以帮到您。目前支持华语歌曲，更多功能还在扩展中，有问题请联系994182204@mail.dlut.edu.cn'
        res_classify = self.classifier.classify(sent)
        #print(res_classify)
        if res_classify == {}:
            return '查找失败，请重新输入'
        if not res_classify:
            return answer
        res_sql = self.parser.parser_main(res_classify)
        #print(res_sql)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)


if __name__ == '__main__':
    handler = ChatBotGraph()
    while 1:
        question = input('用户:')
        answer = handler.chat_main(question)
        print('小易:', answer)
