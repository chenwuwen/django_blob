# -*-coding:utf-8-*-
from django.shortcuts import render
from django.views import View


class Index(View):
    def get(self, request):
        user = request.session['user']
        return render(request, "index.html", {'user': user})


