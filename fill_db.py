from netAngels.models import Link

URL = 'http://very_long_link/for_tets/{}'


def fill():
    if Link.objects.count() < 50:
        for i in range(0, 100):
            link = Link(url=URL.format(i), click_count=0, hash=hash(URL.format(i)))
            link.save()
