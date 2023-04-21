#!/usr/bin/env python3
# coding: utf-8
# File: answer_search.py
# Author: zlh<994182204@mail.dlut.edu.cn>
# Date: 23-4-21

class QuestionPaser:
    '''构建实体节点'''

    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict  # {'song':['红玫瑰']}

    '''解析主函数'''

    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']

        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []

            if question_type == 'song_desc':
                sql = self.sql_transfer(question_type, entity_dict.get('song'))

            elif question_type == 'artist_desc':
                sql = self.sql_transfer(question_type, entity_dict.get('artist'))

            elif question_type == 'artist_name':
                sql = self.sql_transfer(question_type, entity_dict.get('song'))

            elif question_type == 'artist_song':
                sql = self.sql_transfer(question_type, entity_dict.get('artist'))

            elif question_type == 'album_artist':
                sql = self.sql_transfer(question_type, entity_dict.get('artist'))

            elif question_type == 'album_song':
                sql = self.sql_transfer(question_type, entity_dict.get('album'))

            elif question_type == 'similar_songs':
                sql = self.sql_transfer(question_type, entity_dict.get('song'))

            elif question_type == 'playlist_song':
                sql = self.sql_transfer(question_type, entity_dict.get('song'))

            if sql:
                sql_['sql'] = sql
                sqls.append(sql_)

        return sqls

    '''针对不同的问题，分开进行处理'''

    def sql_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查询语句
        sql = []
        # 查询歌曲描述
        if question_type == 'song_desc':
            sql = ["MATCH (m:`歌曲`) where m.name = '{0}' return m.name, m.歌曲内容".format(i) for i in entities]
            # eg.MATCH (m:`歌曲`) where m.name = '红玫瑰' return m.name, m.歌曲内容
        # 查询歌曲的演唱者
        elif question_type == 'artist_name':
            sql = ["MATCH (m:`歌曲`) where m.name = '{0}' return m.name,m.歌手".format(i) for i in entities]

        # 查询歌手唱的歌
        elif question_type == 'artist_song':
            sql = ["MATCH (m:`歌曲`)-[r:`演唱`]->(n:`歌手`) where n.name = '{0}' return n.name, r.name,m.name LIMIT 10".format(i)
                   for i in entities]
            # MATCH (m:`歌曲`)-[r:`演唱`]->(n:`歌手`) where n.name = '陈奕迅' return n.name, r.name,m.name

        # 查询歌手信息
        elif question_type == 'artist_desc':
            sql1 = [
                "MATCH (m:`歌曲`)-[r1:`演唱`]->(n:`歌手`) where n.name = '{0}' return n.name, r1.name,m.name LIMIT 5".format(
                    i) for i in entities]
            sql2 = [
                "MATCH (n:`歌手`)-[r2:`歌手发布`]->(a:`专辑`) where n.name = '{0}' return n.name, r2.name,a.name LIMIT 5".format(
                    i) for i in entities]
            sql = sql1 + sql2

        # 查询专辑属于哪个歌手
        elif question_type == 'album_artist':
            sql = ["MATCH (m:`歌手`)-[r:`歌手发布`]->(n:`专辑`) where m.name = '{0}' return m.name, r.name,n.name LIMIT 10".format(i)
                   for i in entities]

        # 查询专辑下的歌
        elif question_type == 'album_song':
            sql = [
                "MATCH (m:`歌曲`)-[r:`归属专辑`]->(n:`专辑`) where n.name = '{0}' return m.name, r.name,n.name".format(i)
                for i in entities]

        # 推荐相似歌曲
        elif question_type == 'similar_songs':
            sql = ["MATCH (m:`歌曲`)-[r:`相似歌曲`]->(n:`歌曲`) where m.name = '{0}' return m.name, r.name, n.name".format(i)
                   for i in entities]

        # 查询歌单
        elif question_type == 'playlist_song':
            sql = [
                "MATCH (m:`歌曲`)-[r:`歌单`]->(n:`歌单`) where m.name = '{0}' return m.name, r.name, n.name".format(i)
                for i in entities]

        return sql


if __name__ == '__main__':
    handler = QuestionPaser()
