from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator

from .models import Skate


def index(request):
    return render(request, 'skates/index.html')


def skates_list(request):
    context = {'title': 'Скейтборды'}
    skate = Skate.objects.all()
    paginator = Paginator(skate, 2)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)
    context['page_obj'] = page_objects

    if request.method == 'GET':
        skate_id = request.GET.get('id', 1)
        try:
            skate_one = Skate.objects.get(pk=skate_id)
        except:
            pass
        else:
            context['skate_one'] = skate_one
        context['name'] = request.GET.get('name')
    elif request.method == 'POST':
        skate_id = request.POST.get('id', 1)
        try:
            skate_one = Skate.objects.get(pk=skate_id)
        except:
            pass
        else:
            context['skate_one'] = skate_one
        context['name'] = request.POST.get('name')

    return render(
        request=request,
        template_name='skates/skates_list.html',
        context=context
    )
