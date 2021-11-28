from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from property.models import Property, PropertyUser
from property.forms import PropertyForm, PropertyUserForm, PropertyUserFormset,property_update_formset
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def all_properties(request, id=None):
    queryset = Property.objects.all()
    context = {'res': queryset, 'active_page': 'Properties'}
    return render(request, 'properties.html', context)

@login_required
def add_property(request):
    form = PropertyForm(request.POST or None, request.FILES or None)
    formset = PropertyUserFormset(request.POST or None,  queryset=PropertyUser.objects.none())
    context = {
        "form": form,
        "formset": formset,
    }
    if all([form.is_valid(), formset.is_valid()]):
        property = form.save()
        for form in formset:
            property_user = form.save(commit=False)
            property_user.property = property
            property_user.save()
        return redirect('/property')
    return render(request, 'add_property.html', context=context)

@login_required
def property_search_view(request):
    query = request.GET.get('query')
    result =Property.objects.filter(area__icontains=query)
    context = {'res': result}
    return render(request, 'properties.html', context=context)

@login_required
def property_detail_view(request, id=None):
    try:
        article_obj = Property.objects.get(id=id)
    except Exception as e:
        article_obj = None
    context  = {
        "result": article_obj
    }
    return render(request, 'property_detail.html', context=context)

@login_required
def property_update_view(request, id=None):
    print(request.POST)
    obj = get_object_or_404(Property, id=id)
    form = PropertyForm(request.POST or None,  request.FILES or None, instance=obj)
    formset = property_update_formset(request.POST or None,  queryset=obj.property_users.all())
  
    if all([form.is_valid(), formset.is_valid()]):
        property = form.save(commit=False)
        property.save()
        for property_user_form in formset:
            # import pdb; pdb.set_trace()
            if property_user_form.cleaned_data['DELETE']:
                PropertyUser.objects.filter(id=property_user_form.instance.id).delete()
            elif property_user_form:
                property_user = property_user_form.save(commit=False)
                property_user.property = property
                property_user.save()
        formset = property_update_formset(queryset=obj.property_users.all())
    context = {
        "form": form,
        "object": obj,
        'formset': formset
    }
    return render(request, 'update.html', context=context)

@login_required
def property_delete_view(request, id=None):
    Property.objects.filter(id=id).delete()
    return redirect('/property')

# def delete_user_view(request, id=None):
#     PropertyUser.objects.filter(id=id).delete()

def ajax_create_form(request):
    form = PropertyForm(request.POST, request.FILES or None)
    context = { "form": form}
    if form.is_valid():
        ajax_object = form.save()
        context['form'] = PropertyForm()
    return render(request, 'ajax-form.html', context)