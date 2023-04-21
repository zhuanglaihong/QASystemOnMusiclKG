#!/usr/bin/env python3
# coding: utf-8


import os
import json
from py2neo import Graph, Node
import re


class MusicGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, 'data/163music.json')
        self.g = Graph('http://localhost:7474/', auth=("neo4j", "zlh123456"), name='neo4j') # 自己修改对应用户名和密码

    '''读取文件'''

    def read_nodes(self):
        # 共6类节点
        songs = []  # 歌名
        artist = []  # 歌手
        album = []  # 专辑
        lyric = []  # 歌曲内容
        playlist = []  # 歌单
        producer = []  # 制作人
        composer = []  # 作曲
        lyricist = []  # 作词
        accompany = []  # 伴奏

        song_infos = []  # 歌曲信息

        # 构建节点实体关系
        r_sing = []  # 演唱者
        r_song2album = []  # 歌曲属于专辑
        r_artists2album = []  # 歌手-专辑
        r_song2lyric = []  # 歌曲的作曲、作词、歌词信息
        r_song2similar = []  # 歌曲的相似歌曲
        r_song2playlist = []  # 歌曲属于歌单

        # 导入数据
        count = 0
        for data in open(self.data_path, encoding='utf-8'):
            music_dict = {}
            count += 1
            print('json_num=', count)
            data_json = json.loads(data)
            song_name = data_json['name']
            song_name = song_name.replace("'", "’")
            music_dict['name'] = song_name
            songs.append(song_name)
            music_dict['album_name'] = ''
            music_dict['artist_names'] = ''
            music_dict['similar_musics_names'] = ''
            music_dict['playlist'] = ''
            music_dict['lyric'] = ''

            # 添加字典
            if 'album_name' in data_json:
                music_dict['album_name'] = data_json['album_name']

            if 'artist_names' in data_json:
                music_dict['artist_names'] = data_json['artist_names']

            if 'lyric' in data_json:
                music_dict['lyric'] = data_json['lyric']
            if 'similar_musics_names' in data_json:
                music_dict['similar_musics_names'] = data_json['similar_musics_names']
            if 'playlist_names' in data_json:
                music_dict['playlist'] = data_json['playlist_names']

            # 实体节点
            if 'album_name' in data_json:
                data_json['album_name'] = data_json['album_name'].replace("'", "’")
                album.append(data_json['album_name'])
                r_song2album.append([song_name, data_json['album_name']])

            if 'artist_names' in data_json:
                # 给单人歌手是str， 多人是list
                # print(isinstance(data_json['artist_names'],str))
                if isinstance(data_json['artist_names'], str):
                    data_json['artist_names'] = data_json['artist_names'].replace("'", "’")
                    artist.append(data_json['artist_names'])
                    # print(data_json['artist_names'][0])
                    r_sing.append([song_name, data_json['artist_names']])
                    if 'album_name' in data_json:
                        r_artists2album.append([data_json['artist_names'], data_json['album_name']])
                else:
                    for artist_name in data_json['artist_names']:
                        # print(artist_name)
                        artist_name = artist_name.replace("'", "’")
                        artist.append(artist_name)
                        r_sing.append([song_name, artist_name])
                        if 'album_name' in data_json:
                            r_artists2album.append([artist_name, data_json['album_name']])

            if 'similar_musics_names' in data_json:
                similar_musics_names = data_json['similar_musics_names']
                for similar_musics_name in similar_musics_names:
                    similar_musics_name = similar_musics_name.replace("'", "’")
                    # print(similar_musics_name)
                    r_song2similar.append([song_name, similar_musics_name])

            if 'playlist_names' in data_json:
                playlist_names = data_json['playlist_names']
                for playlist_name in playlist_names:
                    playlist_name = playlist_name.replace("'", "’")
                    r_song2playlist.append([song_name, playlist_name])
                    playlist.append(playlist_name)
                # print(playlist)

            if 'lyric' in data_json:
                lyric_str = data_json['lyric']
                # print(lyric_str)
                lyric_str = lyric_str.replace("'", "’")
                lyric.append(lyric_str)
                # 字符串查找匹配其中内容

                r_song2lyric.append([song_name, lyric_str])

            song_infos.append(music_dict)
        print(r_artists2album)
        return set(songs), set(artist), set(album), set(lyric), set(
            playlist), song_infos, r_sing, r_song2album, r_artists2album, r_song2lyric, r_song2similar, r_song2playlist

    '''建立节点'''

    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
            count += 1
            # print('node+=', count, 'num_nodes=', len(nodes))
        return

    '''创建知识图谱中心歌曲的节点'''

    def create_song_nodes(self, song_infos):
        count = 0
        for music_dict in song_infos:
            node = Node("歌曲", name=music_dict['name'], 专辑=music_dict['album_name'],
                        歌手=music_dict['artist_names'],
                        相似歌曲=music_dict['similar_musics_names'],
                        歌单=music_dict['playlist'],
                        歌曲内容=music_dict['lyric'])  # 中心节点有6个属性键
            self.g.create(node)
            count += 1
            print('中心节点歌曲数=', count)
        return

    '''创建知识图谱实体节点类型schema'''

    def create_graphnodes(self):
        songs, artist, album, lyric, playlist, song_infos, r_sing, r_song2album, r_artists2album, r_song2lyric, r_song2similar, r_song2playlist = self.read_nodes()
        self.create_song_nodes(song_infos)
        self.create_node('歌手', artist)
        print('歌手数：', len(artist))
        self.create_node('专辑', album)
        print('专辑数：', len(album))
        self.create_node('歌曲内容', lyric)
        print('歌曲内容：', len(lyric))
        self.create_node('歌单', playlist)
        print('歌单数：', len(playlist))
        return

    '''创建实体关系边'''

    def create_graphrels(self):
        songs, artist, album, lyric, playlist, song_infos, r_sing, r_song2album, r_artists2album, r_song2lyric, r_song2similar, r_song2playlist = self.read_nodes()
        self.create_relationship('歌曲', '歌手', r_sing, '演唱', '演唱者')
        self.create_relationship('歌曲', '专辑', r_song2album, '归属', '归属专辑')
        self.create_relationship('歌手', '专辑', r_artists2album, '歌手发布', '发布专辑')
        self.create_relationship('歌曲', '歌曲内容', r_song2lyric, '歌曲内容', '歌曲信息')
        self.create_relationship('歌曲', '歌曲', r_song2similar, '相似歌曲', '相似风格')
        self.create_relationship('歌曲', '歌单', r_song2playlist, '歌单', '在此歌单')

    '''创建实体关联边'''

    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)  # 属性键name
            print(query)
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

    '''导出数据'''

    def export_data(self):
        songs, artist, album, lyric, playlist, song_infos, r_sing, r_song2album, r_artists2album, r_song2lyric, r_song2similar, r_song2playlist = self.read_nodes()
        f_song = open('./music/songs.txt', 'w+', encoding='utf-8')
        f_artist = open('./music/artist.txt', 'w+', encoding='utf-8')
        f_album = open('./music/album.txt', 'w+', encoding='utf-8')
        f_lyric = open('./music/lyric.txt', 'w+', encoding='utf-8')
        f_playlist = open('./music/playlist.txt', 'w+', encoding='utf-8')

        # 写入文件
        f_song.write('\n'.join(list(songs)))
        f_artist.write('\n'.join(list(artist)))
        f_album.write('\n'.join(list(album)))
        f_lyric.write('\n'.join(list(lyric)))
        f_playlist.write('\n'.join(list(playlist)))

        f_song.close()
        f_artist.close()
        f_album.close()
        f_lyric.close()
        f_playlist.close()

        return


if __name__ == '__main__':
    handler = MusicGraph()
    #handler.create_graphnodes()  # 建立节点
    #handler.create_graphrels()  # 建立实体关系边
    # handler.export_data() # 导出数据
