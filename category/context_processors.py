from .models import Category

def menu_links(request):
    links=Category.objects.all()
    return dict(links=links)


# menu_links is used to fetch all the cate from the db
# inside links we are storing all cate as we need all cate
# dict()used to bring all the cate lists and store them in the ljnks variable