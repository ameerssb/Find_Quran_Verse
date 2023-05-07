import pandas as pd
import numpy as np
import mysql.connector
from django.http import JsonResponse
from django.db import connection
import sys
import speech_recognition as sr
from pydub import AudioSegment
import re
from .models import Quran_Suras,Quran_text_all,Quran_text_simple
pd.options.mode.chained_assignment = None



class Audio():
    def __init__(self,audio=None,filename=None,translate=None):
        self.audio = audio
        self.filename = filename
        self.translate = translate
        self.result = []
    
    def Translating(self):
        AUDIO_FILE = self.audio
        r = sr.Recognizer()
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source)  # read the entire audio file
        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY", show_all=True)`
            # instead of `r.recognize_google(audio, show_all=True)`
            print("Translation in Progress")
            s_result = r.recognize_google(audio, language="ar-SA", show_all=True)
            print('Done Translating... Finding The Verse')
            data = {'data':s_result['alternative'][0]['transcript'],'status':200}
            self.translate = data
            return self.translate
        except sr.UnknownValueError:
            data = {'response':"Google Speech Recognition could not understand audio",'status':500}
            return JsonResponse(data)
        except sr.RequestError as e:
            data = {'response':"Could not request results from Google Speech Recognition service; {0}".format(e),'status':500}        
            return JsonResponse(data)
    
    def Processing(self):
        s_result = self.translate
        # connection = connect()
        Speech_Text = s_result
        Speech_Text = re.sub(' +', ' ', Speech_Text)
        answer = ''
        # ans = {}
        # sani = ''
        with connection.cursor() as cursor:
            query = 'SELECT qs.sura_name,qt.sura,qt.aya,qt.text FROM quran_app_quran_text_simple qt LEFT JOIN quran_app_quran_suras qs ON sura = qs.id'
            cursor.execute(query)
            table = cursor.fetchall()
        quran = pd.DataFrame(table,columns=['Chapter Name','Chapter','Verse','text'])
        # print(quran.head())
        # quran_full = Quran_text_all.objects.raw('SELECT qs.sura_name,qt.sura,qt.aya,qt.text FROM quran_app_quran_text_full qt LEFT JOIN quran_app_quran_suras qs ON sura = qs.id')
        div = {}
        string = []
        one = Speech_Text
        em = quran
        em['text'] = em['text'].str.replace('إ|أ', 'ا', regex = True)
        em['text'] = em['text'].str.replace('إ|أ', 'ا', regex = True)
        for i in range(len(quran['text'])):
            div[i] = quran['text'][i].split()
            quran['text'][i] = ' '.join(item for item in div[i] if item.isalnum())
        if one in 'الف|1,000|1000|الفلاش|الفلافل|الفلا|الفل|على فلان لم|علي فلا لم|على فلاش لم|على لنا|علي لم|علي لما|علي|علي لم':
            string.append(em[em['text'].str.contains('بسم الله الرحمن الرحيم الم')])
            strin = pd.DataFrame(string[0])
            answer = strin.sort_values(['text'], ascending = True)
            self.result = answer
            return self.result.to_dict()
        else:
            if not em[em['text'].str.contains(Speech_Text)].empty:
                string.append(em[em['text'].str.contains(Speech_Text)])
            if 'ه' in Speech_Text:
                qs = Speech_Text
                qss = qs.replace('ه','ة')
                if not em[em['text'].str.contains(qss)].empty:
                    string.append(em[em['text'].str.contains(qss)])
            if not string == []:
                string[0].index= np.arange(1, len(string[0]) + 1)
                answer = pd.DataFrame(string[0])
                self.result = answer.to_dict()
                return self.result
            else:
                with connection.cursor() as cursor:
                    query = Quran_text_all.objects.raw('SELECT qs.sura_name,qt.sura,qt.aya,qt.text FROM quran_app_quran_text_all qt LEFT JOIN quran_app_quran_suras qs ON sura = qs.id')
                    cursor.execute(query)
                    table = cursor.fetchall()
                quran_full = pd.DataFrame(table,columns=['Chapter Name','Chapter','Verse','text'])
                print(quran_full.head())
                if not quran_full[quran_full['text'].str.contains(Speech_Text)].empty:
                    string.append(quran_full[quran_full['text'].str.contains(Speech_Text)])
                if not string == []:
                    string[0].index= np.arange(1, len(string[0]) + 1)
            #        string[0].reset_index(inplace = True)
                    answer = pd.DataFrame(string[0])
                    self.result = answer.to_dict()
                    return self.result
                else:
                    try:
                        verse_find = {}
                        for i in range(len(Speech_Text)):
                            Store = Speech_Text
                            statement = """
                            SELECT MATCH (text) AGAINST (%s IN NATURAL LANGUAGE MODE) score,text,sura,aya,quran_suras.sura_name
                            FROM quran_app_quran_text_simple LEFT JOIN quran_app_quran_suras ON sura = id
                            WHERE MATCH (text) AGAINST (%s IN NATURAL LANGUAGE MODE)
                            ORDER BY MATCH (text) AGAINST (%s IN NATURAL LANGUAGE MODE) DESC
                            """
                            with connection.cursor() as cursor:
                                query = Quran_text_simple.objects.raw(statement, params=(Store,Store,Store,))
                                cursor.execute(query)
                                table = cursor.fetchall()
                            verse_find[i] = pd.DataFrame(table,columns=['score','text','Chapter','Verse','Chapter Name'])
                            # connection.commit()
                            # print(verse_find[i].head())
                        answer = verse_find[0]
                        score = answer['score'].iloc[0]
                        add = 1
                        for i in range(len(answer)-1):
                            if score * 0.85 < answer['score'].iloc[i+1] and score >= 5.0:
                                add = i
                        answer = verse_find[0]
                        answer = answer[["Chapter Name","Chapter","Verse","text"]]
                        answer.index= np.arange(1, len(answer) + 1)
                        answer = answer.iloc[:add]
                        self.result = answer
                        return self.result.to_dict()
                    except KeyError:
                        content = "Cant Find, Make sure you are reciting correctly"
                        data = {'response':content,'status':500}
                        return JsonResponse(data)                    

    def Changin2Wav(self):
        point = 0
        aud = ''
        if self.filename.lower().endswith('wav'):
            point = 1
        elif self.filename.lower().endswith('mp3'):
            point = 2
        elif self.filename.lower().endswith('mp4'):
            point = 3
        elif self.filename.lower().endswith('m4a'):
            point = 4
        elif self.filename.lower().endswith('wma'):
            point = 5
        elif self.filename.lower().endswith('flac'):
            point = 6
        elif self.filename.lower().endswith('aac'):
            point = 7
        elif self.filename.lower().endswith('ogg'):
            point = 8
        elif self.filename.lower().endswith('raw'):
            point = 9
        elif self.filename.lower().endswith('3gp'):
            point = 10
        else:
            point = 0
        if point == 0:
            data = {'respnse':"Can't Process this type of file",'status':500}
            return JsonResponse(data)
        try:
            if point == 1:
                sound = AudioSegment.from_file(self.audio, 'wav')
                aud = self.audio
            if point == 2:
                sound = AudioSegment.from_file(self.audio, 'mp3')
                sound.export(aud, format='wav')
            elif point == 3:
                sound = AudioSegment.from_file(self.audio, 'mp4')
                sound.export(aud, format='wav')
            elif point == 4:
                sound = AudioSegment.from_file(self.audio, 'm4a')
                sound.export(aud, format='wav')
            elif point == 5:
                sound = AudioSegment.from_file(self.audio, 'wma')
                sound.export(aud, format='wav')
            elif point == 6:
                sound = AudioSegment.from_file(self.audio, 'flac')
                sound.export(aud, format='wav')
            elif point == 7:
                sound = AudioSegment.from_file(self.audio, 'aac')
                sound.export(aud, format='wav')
            elif point == 8:
                sound = AudioSegment.from_file(self.audio, 'ogg')
                sound.export(aud, format='wav')
            elif point == 9:
                sound = AudioSegment.from_file(self.audio, 'raw')
                sound.export(aud, format='wav')
            elif point == 10:
                sound = AudioSegment.from_file(self.audio, '3gp')
                sound.export(aud, format='wav')
            self.audio = aud
            return self.audio
        except:
            content = f"An error occured while reading this file, please check this file or upload another{sys.exc_info()[0]}"
            data = {'response':content,'status':500}
            return JsonResponse(data)

    def Count(query):
        add = 0
        for inc in query:
            add +=1
        return add



    # def connect():
    #     try:
    #         connection = mysql.connector.connect(
    #             # host="quran-verse-server.mysql.database.azure.com",
    #             # user="quranverserequestuser@quran-verse-server",
    #             # password="Sanisbature17@",
    #         host="localhost",
    #         user="root",
    #         password="",
    #             database="quran",
    #         )
    #     except Exception as e:
    #         error = "An Error Occured while connecting to database"
    #         print(error)
    #         return error
    #     return connection


    # def JsonToString(response):
    #     data = ""
    #     json_object = json.dumps(response, ensure_ascii=False)
    #     x = json.loads(response)
    #     length = len(x)
    #     for i in range(length):
    #         i += 1
    #         i = str(i) 
    #         data += "Sura Chapter: " + str(x[i]["sura"]) + "\nSura Name: " + str(x[i]["sura_name"]) + "\nVerse Number: " + str(x[i]["aya"]) + "\nArabic Text: " + str(x[i]["text"]) +"\n\n"
    #     data += str(length) + " Results Found"
    #     return data
