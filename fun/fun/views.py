from django.shortcuts import render

def home(request):
    return render(request, "index.html")


def chatting(request):
    return render(request, "chat.html")