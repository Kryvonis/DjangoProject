import csv

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views import View

from django.http.response import HttpResponse
from django.utils import timezone
from django.urls import reverse_lazy
from django.shortcuts import render_to_response

from src.user.models import MyUser
from src.user.templatetags.helpers import eligible, fizzbuzz


class UserDetailView(DetailView):
    model = MyUser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class UserListView(ListView):
    model = MyUser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class UserCreate(CreateView):
    model = MyUser
    fields = ['username', 'email', 'password', 'birthday']
    template_name_suffix = '_create'

    def form_valid(self, form):
        MyUser.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
        )
        return HttpResponse(status=204)


class UserUpdate(UpdateView):
    model = MyUser
    fields = ['username', 'email', 'birthday', 'random_number']
    success_url = reverse_lazy('user-list')
    template_name_suffix = '_update'


class UserDelete(DeleteView):
    model = MyUser
    success_url = reverse_lazy('user-list')


def handler404(request):
    response = render_to_response('common/404.html')
    response.status_code = 404
    return response


class DownloadView(View):
    def get(self, request, *args, **kwargs):
        users = MyUser.objects.all()
        if len(users) == 0:
            return render_to_response('common/404.html')
        filename = '{}.csv'.format(timezone.now().strftime('%c'))

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}'.format(
            filename
        )

        csvfile = csv.writer(
            response,
            delimiter=',',
            quotechar='|',
            quoting=csv.QUOTE_MINIMAL
        )
        csvfile.writerow([
            'Username',
            'Birthday',
            'Eligible',
            'Random Number',
            'BizzFuzz',

        ])
        for object in users:
            csvfile.writerow([
                object.username,
                object.birthday.strftime("%d/%m/%Y"),
                eligible(object.birthday),
                object.random_number,
                fizzbuzz(object.random_number),
            ])
        return response
