import collections
from .models import Category
from .views import SubcategoryIndex


def menu_list(request):
    SubcategoryIndex.index = 0
    SubcategoryIndex.index1 = 0
    category_object = Category.objects.all()
    category_list = []
    subcategory_list = []
    category_dict = {}

    for category in category_object:
        if category.__str__().find('==') == -1:
            category_list.append(category.__str__())
            category_dict[category_list[-1]] = 0
        else:
            subcategory_list.append(category.__str__())

    subcategory_list = sorted(subcategory_list)
    category_list = sorted(category_list)
    category_dict = dict(collections.OrderedDict(
        sorted(category_dict.items())))

    count = 0
    for category in subcategory_list:
        subcategory_list[count] = str(subcategory_list[count]).split(' ==> ')
        category_dict[category.split(' ==> ')[0]] += 1
        count += 1

    context = {
        'categories': category_list,
        'category_dict': category_dict,
        'subcategory_list': list(subcategory_list),
    }

    return context
