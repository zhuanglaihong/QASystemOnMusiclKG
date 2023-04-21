#!/usr/bin/env python3
# coding: utf-8
# File: answer_search.py
# Author: zlh<994182204@mail.dlut.edu.cn>
# Date: 23-4-21

import os
import ahocorasick
import jieba
import jieba.posseg as pseg

class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        # 　特征词路径
        self.songs_path = os.path.join(cur_dir, 'music/songs.txt')
        self.artist_path = os.path.join(cur_dir, 'music/artist.txt')
        self.album_path = os.path.join(cur_dir, 'music/album.txt')
        self.playlist_path = os.path.join(cur_dir, 'music/playlist.txt')

        # 加载特征词
        self.songs_wds = [i.strip() for i in open(self.songs_path, encoding='utf-8') if i.strip()]
        self.artist_wds = [i.strip() for i in open(self.artist_path, encoding='utf-8') if i.strip()]
        self.album_wds = [i.strip() for i in open(self.album_path, encoding='utf-8') if i.strip()]
        self.playlist_wds = [i.strip() for i in open(self.playlist_path, encoding='utf-8') if i.strip()]

        self.region_words = set(self.songs_wds + self.artist_wds + self.album_wds + self.playlist_wds)
        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()

        # 问句疑问词
        self.songs_qwds = ['什么歌曲', '什么歌名', '歌曲名为什么', '音乐名', '歌名为', '曲目','歌词']

        self.artist_qwds = ['演唱', '唱', '谁唱', '他的歌', '她的歌', '唱的歌', '唱哪些歌', '歌手','唱什么歌','谁唱的']

        self.album_qwds = ['专辑', '发布', '唱片','包含' ,'发行','《','》']

        self.similar_qwds = ['和','根据','推荐','和类似','相似','风格','喜欢']

        self.playlist_qwds = ['歌单','列表','推荐列表']

        print('model init finished ......')
        return

    '''分类主函数'''

    def classify(self, question):
        data = {}
        # seg_list = jieba.cut(question)  # 默认是精确模式和启用HMM

        music_dict = self.check_music(question)
        if not music_dict:
            return {}
        data['args'] = music_dict
        # 收集问句当中所涉及到的实体类型
        types = []
        for type_ in music_dict.values():
            types += type_
        # question_type = 'others'

        question_types = []

        # 歌名
        if self.check_words(self.songs_qwds, question) and ('song' in types):
            question_type = 'song_desc'
            question_types.append(question_type)

        # 歌手
        if self.check_words(self.artist_qwds, question) and ('song' in types):
            question_type = 'artist_name'
            question_types.append(question_type)
        if self.check_words(self.artist_qwds, question) and ('artist' in types):
            question_type = 'artist_song'
            question_types.append(question_type)

        # 专辑
        if self.check_words(self.album_qwds, question) and ('album' in types):
            question_type = 'album_song'
            question_types.append(question_type)
        if self.check_words(self.album_qwds, question) and ('artist' in types):
            question_type = 'album_artist'
            question_types.append(question_type)

        # 推荐
        if self.check_words(self.similar_qwds, question) and 'song' in types:
            question_type = 'similar_songs'
            question_types.append(question_type)

        # 歌单
        if self.check_words(self.playlist_qwds, question) and 'song' in types:
            question_type = 'playlist_song'
            question_types.append(question_type)

        # 若没有查到相关的外部查询信息，那么则将该歌曲的描述信息返回
        if question_types == [] and 'song' in types:
            question_types = ['song_desc']
        if question_types == [] and 'artist' in types:
            question_types = ['artist_desc']

        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types

        return data

    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.songs_wds:
                wd_dict[wd].append('song')
            if wd in self.artist_wds:
                wd_dict[wd].append('artist')
            if wd in self.album_wds:
                wd_dict[wd].append('album')
            if wd in self.playlist_wds:
                wd_dict[wd].append('playlist')
        return wd_dict

    '''构造actree，加速过滤'''

    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''问句过滤'''

    def check_music(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i: self.wdtype_dict.get(i) for i in final_wds}

        return final_dict

    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)
