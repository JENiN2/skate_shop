from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator

from .models import Skate
from .forms import SkateForm


def index(request):
    return render(request, 'skates/index.html')


def skates_list(request):
    context = {'title': 'Скейтборды'}
    skate = Skate.objects.all()
    paginator = Paginator(skate, 4)
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


def skate_detail(request, skate_id):
    skate = get_object_or_404(Skate, pk=skate_id)
    context = {'skate_item': skate}
    print(context)
    return render(
        request,
        'skates/skate_details.html',
        context
    )


def skate_add(request):
    if request.method == 'POST':
        context = dict()
        context['name'] = request.POST.get('name')
        context['description'] = request.POST.get('description')
        context['price'] = request.POST.get('price')
        context['article_number'] = request.POST.get('article_number')
        context['color'] = request.POST.get('color')
        context['photo'] = request.POST.get('photo')

        Skate.objects.create(
            name=context['name'],
            description=context['description'],
            price=context['price'],
            article_number=context['article_number'],
            color=context['color'],
            photo='image/skates/'+context['photo']
        )

        return HttpResponseRedirect('/skates/list')
    else:
        skate_form = SkateForm()
        context = {'form': skate_form}
        return render(
            request=request,
            template_name='skates/skate_add.html',
            context=context
        )
