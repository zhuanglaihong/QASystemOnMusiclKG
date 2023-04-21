#!/usr/bin/env python3
# coding: utf-8
# File: answer_search.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-5

from py2neo import Graph

class AnswerSearcher:
    def __init__(self):
        self.g = Graph('http://localhost:7474/', auth=("neo4j", "zlh123456"), name='neo4j')
        self.num_limit = 20

    '''执行cypher查询，并返回相应结果'''
    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.g.run(query).data()
                answers += ress
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return '回答失败，请重新输入'

        if question_type == 'song_desc':
            desc = [i['m.歌曲内容'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的歌曲介绍：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'artist_name':
            desc = [i['m.歌手'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '歌曲{0}的演唱者是：{1}'.format(subject, '；'.join(list(set(desc[0]))[:self.num_limit]))

        elif question_type == 'artist_song':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '歌手{0}的演唱曲目有：{1}等等'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'artist_desc':
            #print(answers[5])
            desc1 = [i['m.name'] for i in answers[0:5] ]  # 由于两条sql语句一起，这里需要过滤
            desc2 = [i['a.name'] for i in answers[5:10] ] # 注意修改条目数，各自五条
            subject = answers[0]['n.name']
            desc = [i for i in desc1 + desc2 if i != subject]
            final_answer = '歌手{0}的信息包括:\n1.歌曲：{1} 等等 \n 2.专辑《{2}》等等'.format(subject, '；'.join(list(set(desc1))[:self.num_limit]),'》；《'.join(list(set(desc2))[:self.num_limit]))

        elif question_type == 'album_artist':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '歌手{0}发布的专辑包括有：《{1}》等等'.format(subject, '》；《'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'similar_songs':
            do_desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '歌曲{0}推荐曲目有：{1} 等等'.format(subject, ';'.join(list(set(do_desc))[:self.num_limit]))

        elif question_type == 'album_song':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '专辑{0}包含有歌曲：{1}'.format(subject,'；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'playlist_song':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '包含歌曲{0}的歌单有：《{1}》等等'.format(subject,'》；《'.join(list(set(desc))[:self.num_limit]))

        return final_answer

if __name__ == '__main__':
    searcher = AnswerSearcher()