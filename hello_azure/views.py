from os import stat
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import numpy as np
import mysql.connector
import speech_recognition as sr
from pydub import AudioSegment
import requests
import json
import re
pd.options.mode.chained_assignment = None

def index(request):
    print('Request for index page received')
    return render(request, 'hello_azure/home.html')


@csrf_exempt
def hello(req):
    Aud = None
    if req.method == 'POST':
        try:
            Aud = req.FILES['file']
        except ValueError:
            pass
        if Aud != None:
            filename = Aud.name
            point = Changin2Wav(filename)
            if point == 0:
                return HttpResponse("Can't Process this type of file")
            try:
                if point == 2:
                    sound = AudioSegment.from_file(Aud, 'mp3')
                    sound.export(Aud, format='wav')
                elif point == 3:
                    sound = AudioSegment.from_file(Aud, 'mp4')
                    sound.export(Aud, format='wav')
                elif point == 4:
                    sound = AudioSegment.from_file(Aud, 'm4a')
                    sound.export(Aud, format='wav')
                elif point == 5:
                    sound = AudioSegment.from_file(Aud, 'wma')
                    sound.export(Aud, format='wav')
                elif point == 6:
                    sound = AudioSegment.from_file(Aud, 'flac')
                    sound.export(Aud, format='wav')
                elif point == 7:
                    sound = AudioSegment.from_file(Aud, 'aac')
                    sound.export(Aud, format='wav')
                elif point == 8:
                    sound = AudioSegment.from_file(Aud, 'ogg')
                    sound.export(Aud, format='wav')
                elif point == 9:
                    sound = AudioSegment.from_file(Aud, 'raw')
                    sound.export(Aud, format='wav')
                elif point == 10:
                    sound = AudioSegment.from_file(Aud, '3gp')
                    sound.export(Aud, format='wav')
            except:
                content = {"An error occured while reading this file, please check this file or upload another"}
                return HttpResponse(content, status=500)
#            fs = FileSystemStorage()
#            filename = fs.save(img_file.name, img_file)
#            path = fs.path(filename)
            url = "https://quranfind.azurewebsites.net/api/quran"
            files=[
            ('file',(filename,Aud.open(),'audio/wav'))
            ]
            headers = {}
            try:
                file = Translating(Aud)
                response = Processing(file)
                #response = requests.request("POST", url, headers=headers, files=files, timeout=50)
                #if response.status_code == 200:
                json_object = json.dumps(response, ensure_ascii=False)
                return HttpResponse(json_object, status = 200)
                if response.status_code == 500:
                    return HttpResponse( "An Error occured while Processing Request", status=500)
                else:
                    return HttpResponse("an error occured", status=400)
            except :
                return HttpResponse( "An Error occured while Processing Request", status=500)
#            except requests.Timeout:
#                    return HttpResponse( "An Error occured while Processing Request", status=500)
        else:
            return HttpResponse("This File is corrupted", status=500)
    else:
        return HttpResponse(
         "No Such WebPage",
         status=404
    )

@csrf_exempt
def translator(req):
    if req.method == 'POST':
        try:
            arabic = req.POST['arabic']
        except ValueError:
            pass
        if arabic != None:
    #            file = Translating(Aud)
            url = "https://quranfind.azurewebsites.net/api/quran"
            payload={'arabic_text': arabic}
            try:
                response = Processing(arabic)
                #response = requests.request("GET", url, params=payload, timeout=50)
                #if response.status_code == 200:
                json_object = json.dumps(response, ensure_ascii=False)
                return HttpResponse(json_object, status = 200)
                if response.status_code == 500:
                    return HttpResponse( "An Error occured while Processing Request", status=500)
                else:
                    return HttpResponse("an error occured", status=400)
            except :
                return HttpResponse( "An Error occured while Processing Request", status=500)
#            except requests.Timeout:
#                    return HttpResponse( "An Error occured while Processing Request", status=500)
        else:
            return HttpResponse("This File is corrupted", status=500)
    else:
        return HttpResponse(
         "No Such WebPage",
         status=404
    )



@csrf_exempt
def AndroidAudio(req):
    Aud = None
    if req.method == 'POST':
        try:
            Aud = req.FILES['file']
        except ValueError:
            pass
        if Aud != None:
            filename = Aud.name
            point = Changin2Wav(filename)
            if point == 0:
                return HttpResponse("Can't Process this type of file")
            try:
                if point == 2:
                    sound = AudioSegment.from_file(Aud, 'mp3')
                    sound.export(Aud, format='wav')
                elif point == 3:
                    sound = AudioSegment.from_file(Aud, 'mp4')
                    sound.export(Aud, format='wav')
                elif point == 4:
                    sound = AudioSegment.from_file(Aud, 'm4a')
                    sound.export(Aud, format='wav')
                elif point == 5:
                    sound = AudioSegment.from_file(Aud, 'wma')
                    sound.export(Aud, format='wav')
                elif point == 6:
                    sound = AudioSegment.from_file(Aud, 'flac')
                    sound.export(Aud, format='wav')
                elif point == 7:
                    sound = AudioSegment.from_file(Aud, 'aac')
                    sound.export(Aud, format='wav')
                elif point == 8:
                    sound = AudioSegment.from_file(Aud, 'ogg')
                    sound.export(Aud, format='wav')
                elif point == 9:
                    sound = AudioSegment.from_file(Aud, 'raw')
                    sound.export(Aud, format='wav')
                elif point == 10:
                    sound = AudioSegment.from_file(Aud, '3gp')
                    sound.export(Aud, format='wav')
            except:
                content = {"An error occured while reading this file, please check this file or upload another"}
                return HttpResponse(content, status=500)
#            fs = FileSystemStorage()
#            filename = fs.save(img_file.name, img_file)
#            path = fs.path(filename)
            url = "https://quranfind.azurewebsites.net/api/quran"
            files=[
            ('file',(filename,Aud.open(),'audio/wav'))
            ]
            headers = {}
            try:
                file = Translating(Aud)
                response = Processing(file)
                #response = requests.request("POST", url, headers=headers, files=files, timeout=50)
                #if response.status_code == 200:
#                json_object = json.dumps(response, ensure_ascii=False)
                json_object = JsonToString(response)
                return HttpResponse(json_object, status = 200)
                if response.status_code == 500:
                    return HttpResponse( "An Error occured while Processing Request", status=500)
                else:
                    return HttpResponse("an error occured", status=400)
            except :
                return HttpResponse( "An Error occured while Processing Request", status=500)
#            except requests.Timeout:
#                    return HttpResponse( "An Error occured while Processing Request", status=500)
        else:
            return HttpResponse("This File is corrupted", status=500)
    else:
        return HttpResponse(
         "No Such WebPage",
         status=404
    )

@csrf_exempt
def AndroidText(req):
    if req.method == 'POST':
        try:
            arabic = req.POST['arabic']
        except ValueError:
            pass
        if arabic != None:
    #            file = Translating(Aud)
            url = "https://quranfind.azurewebsites.net/api/quran"
            payload={'arabic_text': arabic}
            try:
                response = Processing(arabic)
                #response = requests.request("GET", url, params=payload, timeout=50)
                #if response.status_code == 200:
                json_object = JsonToString(response)
                return HttpResponse(json_object, status = 200)
                if response.status_code == 500:
                    return HttpResponse( "An Error occured while Processing Request", status=500)
                else:
                    return HttpResponse("an error occured", status=400)
            except :
                return HttpResponse( "An Error occured while Processing Request", status=500)
#            except requests.Timeout:
#                    return HttpResponse( "An Error occured while Processing Request", status=500)
        else:
            return HttpResponse("This File is corrupted", status=500)
    else:
        return HttpResponse(
         "No Such WebPage",
         status=404
    )

def JsonToString(response):
    data = ""
    json_object = json.dumps(response, ensure_ascii=False)
    x = json.loads(response)
    length = len(x)
    for i in range(length):
        i += 1
        i = str(i) 
        data += "Sura Chapter: " + str(x[i]["sura"]) + "\nSura Name: " + str(x[i]["Sura_Name"]) + "\nVerse Number: " + str(x[i]["aya"]) + "\nArabic Text: " + str(x[i]["text"]) +"\n\n"
    data += str(length) + " Results Found"
    return data

def Changin2Wav(filename):
    point = 0
    if filename.lower().endswith('wav'):
        point = 1
        return point
    elif filename.lower().endswith('mp3'):
        point = 2
        return point
    elif filename.lower().endswith('mp4'):
        point = 3
        return point
    elif filename.lower().endswith('m4a'):
        point = 4
        return point
    elif filename.lower().endswith('wma'):
        point = 5
        return point
    elif filename.lower().endswith('flac'):
        point = 6
        return point
    elif filename.lower().endswith('aac'):
        point = 7
        return point
    elif filename.lower().endswith('ogg'):
        point = 8
        return point
    elif filename.lower().endswith('raw'):
        point = 9
        return point
    elif filename.lower().endswith('3gp'):
        point = 10
        return point
    else:
        return point

def Translating(AUDIO_FILE):
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
        return s_result['alternative'][0]['transcript']
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    


def connect():
    try:
        connection = mysql.connector.connect(
            host="quran-verse-server.mysql.database.azure.com",
            user="quranverserequestuser@quran-verse-server",
            password="Sanisbature17@",
#            host="localhost",
#            user="access",
#            password="88890573",
            database="quran",
        )
    except Exception as e:
        error = "An Error Occured while connecting to database"
        print(error)
        return error
    return connection

def Processing(s_result):
    connection = connect()
    Speech_Text = s_result
    Speech_Text = re.sub(' +', ' ', Speech_Text)
    answer = ''
    ans = {}
    sani = ''
    quran = pd.read_sql('SELECT qs.Sura_Name,qt.sura,qt.aya,qt.text FROM quran_text_simple qt LEFT JOIN quran_suras qs ON sura = qs.Sura_Chapter', connection)
#    quran_full = pd.read_sql('SELECT qs.Sura_Name,qt.sura,qt.aya,qt.text FROM quran_text_full qt LEFT JOIN quran_suras qs ON sura = qs.Sura_Chapter', connection)
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
        string.append(quran[quran['text'].str.contains('بسم الله الرحمن الرحيم الم')])
        strin = pd.DataFrame(string[0])
        answer = strin.sort_values(['text'], ascending = True)
    else:
        if not quran[quran['text'].str.contains(Speech_Text)].empty:
            string.append(quran[quran['text'].str.contains(Speech_Text)])
        if 'ه' in Speech_Text:
            qs = Speech_Text
            qss = qs.replace('ه','ة')
            if not quran[quran['text'].str.contains(qss)].empty:
                string.append(quran[quran['text'].str.contains(qss)])
        if not string == []:
            string[0].index= np.arange(1, len(string[0]) + 1)
            answer = pd.DataFrame(string[0])
            verses = answer.to_json(force_ascii=False, orient="index")
            return verses
        else:
            quran_full = pd.read_sql('SELECT qs.Sura_Name,qt.sura,qt.aya,qt.text FROM quran_text_all qt LEFT JOIN quran_suras qs ON sura = qs.Sura_Chapter', connection)
            if not quran_full[quran_full['text'].str.contains(Speech_Text)].empty:
                string.append(quran_full[quran_full['text'].str.contains(Speech_Text)])
            if not string == []:
                string[0].index= np.arange(1, len(string[0]) + 1)
        #        string[0].reset_index(inplace = True)
                answer = pd.DataFrame(string[0])
                verses = answer.to_json(force_ascii=False, orient="index")
                return verses
            else:    
                try:
                    verse_find = {}
                    for i in range(len(Speech_Text)):
                        Store = Speech_Text
                        statement = """
                        SELECT MATCH (text) AGAINST (%s IN NATURAL LANGUAGE MODE) score,text,sura,aya,quran_suras.Sura_Name
                        FROM quran_text_simple LEFT JOIN quran_suras ON sura = Sura_Chapter
                        WHERE MATCH (text) AGAINST (%s IN NATURAL LANGUAGE MODE)
                        ORDER BY MATCH (text) AGAINST (%s IN NATURAL LANGUAGE MODE) DESC
                        """
                        verse_find[i] = pd.read_sql(statement, connection, params=(Store,Store,Store,))
                        connection.commit()
                    answer = verse_find[0]
                    score = answer['score'].iloc[0]
                    add = 1
                    for i in range(len(answer)-1):
                        if score * 0.85 < answer['score'].iloc[i+1] and score >= 5.0:
                            add = i
                    answer = verse_find[0]
                    answer = answer[["Sura_Name","sura","aya","text"]]
                    answer.index= np.arange(1, len(answer) + 1)
                    answer = answer.iloc[:add]
                    verses = answer.to_json(force_ascii=False, orient="index")
                    return verses
                except KeyError:
                    return "Cant Find, Make sure you are reciting correctly"
