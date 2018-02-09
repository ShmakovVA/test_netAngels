from django.http import HttpResponseRedirect
from django.shortcuts import render

from netAngels.models import Link
from .forms import LinkForm, HashLinkForm


def get_from_hash(request):
    if request.method == 'POST':
        form = HashLinkForm(request.POST)
        if form.is_valid():
            l = Link.objects.filter(hash=form.cleaned_data['hash'])
            if l:
                return HttpResponseRedirect(r'/new_link/{}/'.format(l[0].id))
            else:
                return render(request, 'from_hash.html', context={'form': form, 'mess': 'Not founded'})
        else:
            return render(request, 'from_hash.html', context={'form': form, 'mess': 'Invalid form'})
    else:
        hash_redirect = request.GET.get("hash", None)
        if hash_redirect:
            return HttpResponseRedirect(r'redirect/{}/'.format(hash_redirect))
        else:
            form = HashLinkForm(initial={'hash': '', })
            return render(request, 'from_hash.html', context={'form': form})


def home(request):
    if request.method == 'POST':

        form = LinkForm(request.POST)
        if form.is_valid():
            try:
                l = Link.objects.get(url=form.cleaned_data['url'])
            except Link.DoesNotExist:
                l = Link()
                l.url = form.cleaned_data['url']
                l.hash = hash(l.url)
                l.click_count = 0
                l.save()
            return HttpResponseRedirect(r'/new_link/{}/'.format(l.id))

    else:
        form = LinkForm(initial={'url': '', })

    top_20_links = Link.objects.all().order_by('click_count', 'datetime').reverse()[:20]
    return render(request, 'add_link_and_top_20.html', context={'form': form, 'top_20_links': top_20_links})


def all(request):
    if request.method == 'POST':
        id = request.POST.get("id", None)
        if id:
            l = Link.objects.get(id=id)
            if l:
                l.delete()

    links = Link.objects.all().order_by('click_count', 'datetime').reverse()
    return render(request, 'all_links.html', context={'all_links': links})


def new_link(request, id):
    try:
        link = Link.objects.get(id=id)
    except Link.DoesNotExist:
        return HttpResponseRedirect(r'/')
    return render(request, 'just_created_link.html', context={'link': link})


def redirect_from_short(request, hash):
    try:
        link = Link.objects.get(hash=hash)
    except Link.DoesNotExist:
        return HttpResponseRedirect(r'/')
    link.inc_clicks()
    return HttpResponseRedirect(link.url)
