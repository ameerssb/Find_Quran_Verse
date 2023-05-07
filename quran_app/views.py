from django.shortcuts import render
# from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import sys
# from pydub import AudioSegment
from .translate import Audio

def index(request):
    return render(request, 'quran_app/home.html')

class AudioTranslator(View):
    def post(self,request,audio=None):       
        try:
            audio = request.FILES['file']
        except ValueError:
            data = {'response': "This File is not uploaded correctly", 'status':500}
            return JsonResponse(data)
        if audio != None:
            try:
                media = Audio(audio=audio,filename=audio.name)
                media.Changin2Wav()
                media.Translating()
                response = media.Processing()
                data = {'response':list(response),'status':200}
                return JsonResponse(data)
            except:
                data = {'response': f"An Error occured while Processing Request {sys.exc_info()[1]}",'status':500}
                return JsonResponse(data)
        else:
            data = {'response': "This File is corrupted", 'status':500}
            return JsonResponse(data)

class TextTranslator(View):

    def post(self,request):
        try:
            arabic = request.POST['arabic']
        except ValueError:
            data = {'response': "This File is not uploaded correctly", 'status':500}
            return JsonResponse(data)
        if arabic != None:
            try:
                media = Audio(translate=arabic)
                response = media.Processing()
                print(response)
                data = {'response':response,'status':200}
                return JsonResponse(data)
            except :
                data = {'response': f"An Error occured while Processing Request {sys.exc_info()[1]}",'status':500}
                return JsonResponse(data)
        else:
            data = {'response': "This File is corrupted",'status':500}
            return JsonResponse(data)


@csrf_exempt
def AndroidAudio(request):
    if request.method == 'POST':
        try:
            audio = request.FILES['file']
        except ValueError:
            pass
        if audio != None:
            try:
                media = Audio(audio=audio,filename=audio.name)
                media.Changin2Wav()
                media.Translating()
                response = media.Processing()
                data = {'response':list(response),'status':200}
                return JsonResponse(data)
            except:
                data = {'response': f"An Error occured while Processing Request {sys.exc_info()[1]}",'status':500}
                return JsonResponse(data)
        else:
            data = {'response': "This File is corrupted", 'status':500}
            return JsonResponse(data)
    else:
        data = {'response': "No such page", 'status':404}
        return JsonResponse(data)
@csrf_exempt
def AndroidText(request):
    if request.method == 'POST':
        try:
            arabic = request.POST['arabic']
        except ValueError:
            pass
        if arabic != None:
            try:
                media = Audio(translate=arabic)
                response = media.Processing()
                data = {'response':list(response),'status':200}
                return JsonResponse(data)
            except:
                data = {'response': f"An Error occured while Processing Request {sys.exc_info()[1]}",'status':500}
                return JsonResponse(data)
        else:
            data = {'response': "This File is corrupted", 'status':500}
            return JsonResponse(data)
    else:
        data = {'response': "No such page", 'status':404}
        return JsonResponse(data)