from django.shortcuts import render, redirect
from django.http import HttpResponse, QueryDict
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .forms import *
from .models import *
import numpy as np


def finish(request):
    if request.method == 'POST':
        if request.POST['action'] == 'Анализировать иерархию':
            answers_criteria_list = request.POST.getlist('select', [])
            answers_variants_list = request.POST.getlist('select2', [])
            len_criteria = request.POST.getlist('len_criteria', [])
            len_variants = request.POST.getlist('len_variants', [])
            print(answers_variants_list)
            print(answers_variants_list)
            user = request.user.username
            outvariants = request.POST.get('outvariantslala')
            outcriteria = request.POST.get('outcriterialala')
            print(outvariants, 'django')
            if len(answers_variants_list) == 0 or len(answers_criteria_list) == 0 or len_criteria[0]=='' or len_variants[0] == '':
                error2 = 'Для начала добавьте критерии и варианты!'
                return render(request, 'main/index.html', context={'error2': error2} )
            print(outvariants, "this is outvariants from def finish")
            print(outcriteria, "this is outcriteria from def finish")

            
            for i, elem in enumerate(answers_criteria_list):
                answers_criteria_list[i] = float(elem)
            
            for i, elem in enumerate(len_criteria):
                len_criteria[i] = int(elem)
            len_criteria = len_criteria[0]

            criterias_koef = np.zeros((len_criteria, len_criteria))
            k = 0
            for i in range(len_criteria):
                for j in range(len_criteria):
                    if i == j:

                        criterias_koef[i][j] = 1
                    elif j > i:
                        criterias_koef[i][j] = answers_criteria_list[k]
                        criterias_koef[j][i] = round(1 / round(answers_criteria_list[k], 4), 4)
                        k += 1
            k = 0
            answers_variants_list = request.POST.getlist('select2', [])
            for i, elem in enumerate(answers_variants_list):
                answers_variants_list[i] = float(elem)
            len_variants = request.POST.getlist('len_variants', [])
            for i, elem in enumerate(len_variants):
                len_variants[i] = int(elem)
            len_variants = len_variants[0]
            criteria_x_variants_list = []
            for i in range(len_criteria):
                i = np.zeros((len_variants, len_variants))
                criteria_x_variants_list.append(i)

            for i in range(len_criteria):
                for j in range(len_variants):
                    for n in range(len_variants):
                        if j == n:
                            criteria_x_variants_list[i][j][n] = 1
                        elif n > j:
                            criteria_x_variants_list[i][j][n] = answers_variants_list[k]
                            criteria_x_variants_list[i][n][j] = round(1 / round(answers_variants_list[k], 4), 4)
                            k += 1
            k = 0

            print(criterias_koef, "this")

            print(len_criteria, "len_criteria")
            for i in range(len(criteria_x_variants_list)):
                print(criteria_x_variants_list[i], "this is variants", i)
            print(k, "k")
            lslist = []
            summa_list = []
            # Создание финальной матрицы критерииХварианты , а так же рейтинг критериев , и результат.
            big_matrix = np.zeros((len_variants, len_criteria))
            for matrix in range(len(criteria_x_variants_list)):
                print(matrix, 'matrix')
                # here must being fuction normirovka
                lslist.clear()
                for j in range(criteria_x_variants_list[matrix].shape[1]):
                    summa = 0
                    for n in range(criteria_x_variants_list[matrix].shape[0]):
                        summa += criteria_x_variants_list[matrix][n][j]
                    summa_list.append(summa)
                    print(summa_list, 'summa list to big')
                # делим столбцы на сумму их элементов
                for i in range(criteria_x_variants_list[matrix].shape[0]):

                    for j in range(criteria_x_variants_list[matrix].shape[1]):
                        criteria_x_variants_list[matrix][j][i] = round(
                            criteria_x_variants_list[matrix][j][i] / summa_list[i],
                            4)
                # находим сумму строк и добавляем в список списки из сум ....
                for i in range(criteria_x_variants_list[matrix].shape[0]):
                    summa = 0
                    for j in range(criteria_x_variants_list[matrix].shape[1]):
                        summa += criteria_x_variants_list[matrix][i][j]
                    summa = round(summa / criteria_x_variants_list[matrix].shape[1], 4)
                    lslist.append(summa)
                    print(lslist, 'lsllist to big')
                for s in range(len_variants):
                    big_matrix[s][matrix] = lslist[s]
                    print(big_matrix[s][matrix], 'append', lslist[s])
                summa_list.clear()

            # here must be called function secondly
            lslist.clear()
            for j in range(criterias_koef.shape[1]):
                summa = 0
                for n in range(criterias_koef.shape[0]):
                    summa += criterias_koef[n][j]
                summa_list.append(summa)
                print(summa_list, 'summa_list second')
            # делим столбцы на сумму их элементов
            for i in range(criterias_koef.shape[0]):
                for j in range(criterias_koef.shape[1]):
                    criterias_koef[j][i] = round(criterias_koef[j][i] / summa_list[i], 4)
            # находим сумму строк и добавляем в список списки из сум ....
            for i in range(criterias_koef.shape[0]):
                summa = 0
                for j in range(criterias_koef.shape[1]):
                    summa += criterias_koef[i][j]
                summa = round(summa / criterias_koef.shape[1], 4)
                lslist.append(summa)
                print(lslist, 'lslist second')
            res = (big_matrix.dot(lslist)).tolist()
            for i in range(len(res)):
            	res[i] = round(res[i], 3)*100
            request.session['res']= res	
            print(request.session['res'], "res")
            print(big_matrix, "big_matrix")
            print(lslist, "raiting")
            print(request.POST)
            message_out = "Анализ успешно выполнен"

            return render(request, 'main/index.html',
                          context={'criteria_matrix': criterias_koef, 'big_matrix': big_matrix,
                                   'res': request.session['res'], 'raiting': lslist,
                                   'outvariants': request.session['variants'],
                                   'outcriterian': request.session['criterian'],
                                   "user": user , "message_out":message_out})

        elif request.POST['action'] == "Сохранить":
            chek = request.POST.getlist("res", [])
            chek2 = request.POST.getlist("selection_name", [])
            if chek[0] == '':
                a = "Получите результат для того что бы сохранить!"
                return render(request, "main/index.html", context={"message":a})
            
            elif chek2[0] == '':
                request.session['selection_name'] = request.POST.get('selection_name')
                form = History.objects.create(user=request.user.username, criterian = request.session['criterian'],variants=request.session['variants'], selection_result=request.session['res'])
                form.save()
                a="Успешно сохранено!"
                return render(request, "main/index.html", context={"message":a})
            else:
	            request.session['selection_name'] = request.POST.get('selection_name')
	            form = History.objects.create(name = request.session['selection_name'] ,user=request.user.username, criterian = request.session['criterian'],variants=request.session['variants'], selection_result=request.session['res'])
	            form.save()
	            a="Успешно сохранено!"
	            del request.session['selection_name']
	            del request.session['res']
	            del request.session['variants']
	            del request.session['criterian']
	            return render(request, "main/index.html", context={"message":a})
    return render(request, "main/index.html")


def index(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            criterian = request.POST.getlist('firstlist', [])
            b = request.POST.getlist('tags', [])
            criterian.extend(b)
            variants = request.POST.getlist('tags2', [])
            if len(criterian) != len(set(criterian)) and len(variants) == len(set(variants)):
                error = 'Поля не должны быть одинаковыми!'
                return render(request, 'main/index.html', context = {'error': error})
            elif len(criterian) != len(set(criterian)):
                error = 'Критерии не должны быть одинаковыми!'
                return render(request, 'main/index.html', context = {'error': error})
            elif len(variants) != len(set(variants)):
                error = 'Варианты не должны быть одинаковыми!'
                return render(request, 'main/index.html', context = {'error': error})   
            request.session['criterian'] = criterian
            request.session['variants'] = variants

            len_criteria = len(criterian)
            len_variants = len(variants)
            iterablecomponent = 0
            print(request.POST)
            print(request.session['variants'], "this is variants session")
            print(request.session['criterian'], "this is criterian sessi")
            print("criterian", criterian, len_criteria)
            print("variants", variants, len_variants)
            return render(request, 'main/index.html',
                          context={'outcriterian': criterian, 'outvariants': variants,
                                   'len_variants': len_variants,
                                   'len_criteria': len_criteria, })
    
        else:
            return render(request, 'main/index.html')
    else:
        return render(request, 'main/base.html')

def base(request):
    return render(request, 'main/base.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {

        'form': form

    })


def history(request):
    if request.user.is_authenticated:
        qeurylist = History.objects.filter(user__contains = request.user.username)
        user = History.objects.all()
        print(qeurylist)
        return render(request , 'main/history.html' , context={"lis":qeurylist})
    else:
        return render(request, 'main/base.html')
