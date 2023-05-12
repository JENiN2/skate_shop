from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth import login, logout
from skate_shop.settings import LOGIN_URL
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


from .models import Skate
from .forms import SkateForm, SkateUpdForm, RegistrationForm, LoginForm, ContactForm
from .serializers import SkateSerializer
from basket.forms import BasketAddProductForm


def index(request):
    return render(request, 'skates/index.html', {'title': 'Домашняя страница'})


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
    basket_form = BasketAddProductForm()
    context = {'title': 'Подробности',
               'skate_item': skate,
               'basket_form': basket_form
               }
    return render(
        request,
        'skates/skate_details.html',
        context
    )


@permission_required(perm='skate.add_skate', login_url=LOGIN_URL)
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
        context = {
            'title': 'Добавление скейтборда',
            'form': skate_form
        }
        return render(
            request=request,
            template_name='skates/skate_add.html',
            context=context
        )


@permission_required(perm='skate.change_skate', login_url=LOGIN_URL)
def skate_edit(request, skate_id):
    skate = get_object_or_404(Skate, pk=skate_id)
    if request.method == 'GET':
        form = SkateUpdForm(request.POST or None, instance=skate)
    else:
        form = SkateUpdForm(instance=skate, data=request.POST, files=request.FILES)
        if form.is_valid():
            print('-----------------------------------', form)
            form.save()
            return HttpResponseRedirect('/skates/list/' + str(skate_id))
    context = {
        'title': 'Редактирование товара',
        'skate_item': skate,
        'form': form,
               }
    return render(
        request,
        'skates/skate_edit.html',
        context
    )


@permission_required(perm='skate.delete_skate', login_url=LOGIN_URL)
def skate_delete(request, skate_id):
    print(skate_id)
    Skate.objects.filter(id=skate_id).delete()
    return HttpResponseRedirect('/skates/list')


def user_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = RegistrationForm()
    return render(request, 'skates/auth/registration.html', {'title': 'Регистрация',
                                                             'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'skates/auth/login.html', {'title': 'Авторизация',
                                                      'form': form})


def user_logout(request):
    logout(request)
    return redirect('log_in')


@login_required
def contact_email(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(
                form.cleaned_data['subject'],
                form.cleaned_data['content'],
                settings.EMAIL_HOST_USER,
                ['natali_jar@mail.ru'],
                fail_silently=False
            )
            if mail:
                return redirect('index')
    else:
        form = ContactForm()
    return render(request, "skates/email.html", {'title': 'Письмо',
                                                 'form': form})


@api_view(['GET', 'POST'])
def skates_api_list(request):
    if request.method == 'GET':
        skate_list = Skate.objects.all()
        serializer = SkateSerializer(skate_list, many=True)
        return Response({'skate_list': serializer.data})
    elif request.method == 'POST':
        serializer = SkateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def skates_api_detail(request, pk, format=None):
    skate_obj = get_object_or_404(Skate, pk=pk)
    if skate_obj.exist:
        if request.method == "GET":
            serializer = SkateSerializer(skate_obj)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = SkateSerializer(skate_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': 'Данные успешно обновлены',
                    'skate': serializer.data
                })
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            skate_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
