from django.http import HttpResponseRedirect
from django.shortcuts import render

from netAngels.models import Link
from .forms import LinkForm, HashLinkForm


def get_from_hash(request):
    if request.method == 'POST':
        form = HashLinkForm(request.POST)
        if form.is_valid():
            link = Link.objects.filter(hash=form.cleaned_data['hash'])
            if link:
                return HttpResponseRedirect(r'/new_link/{}/'.format(link[0].id))
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
                link = Link.objects.get(url=form.cleaned_data['url'])
            except Link.DoesNotExist:
                url = form.cleaned_data['url']
                link = Link(url=url, hash=hash(url), click_count=0)
                link.save()
            return HttpResponseRedirect(r'/new_link/{}/'.format(link.id))

    else:
        form = LinkForm(initial={'url': '', })

    top_20_links = Link.objects.all().order_by('click_count', 'datetime').reverse()[:20]
    return render(request, 'add_link_and_top_20.html', context={'form': form, 'top_20_links': top_20_links})


def all_links(request):
    if request.method == 'POST':
        link_id = request.POST.get("id", None)
        if link_id:
            link = Link.objects.get(id=link_id)
            if link:
                link.delete()

    links = Link.objects.all().order_by('click_count', 'datetime').reverse()
    return render(request, 'all_links.html', context={'all_links': links})


def new_link(request, link_id):
    try:
        link = Link.objects.get(id=link_id)
    except Link.DoesNotExist:
        return HttpResponseRedirect(r'/')
    return render(request, 'just_created_link.html', context={'link': link})


def redirect_from_short(request, hash_value):
    try:
        link = Link.objects.get(hash=hash_value)
    except Link.DoesNotExist:
        return HttpResponseRedirect(r'/')
    link.inc_clicks()
    return HttpResponseRedirect(link.url)
