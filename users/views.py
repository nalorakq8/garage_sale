from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .models import User, Seller
from .forms import EditUserForm, EditSellerForm,BecomeSellerForm
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.http import Http404
from django.core.urlresolvers import reverse
from django.contrib import messages
# Create your views here.


@login_required
def profile_view(request, pk):
    profile_user = get_object_or_404(User, pk=pk)
    profile_seller = None
    if hasattr(request.user.user, 'seller') and request.user.user == profile_user:
        profile_seller = get_object_or_404(Seller, user=pk)

    return render(
        request,
        'profile_view.html',
        {
            'profile_user': profile_user,
            'profile_seller': profile_seller,
        })


def profile_edit(request, pk):
    if int(pk) == request.user.user.pk:
        profile_user = get_object_or_404(User, pk=pk)
        profile_seller = None
        if hasattr(request.user.user, 'seller'):
            profile_seller = get_object_or_404(Seller, user=pk)
        if hasattr(request.user.user, 'seller'):
            if request.method == 'POST':
                form_user = EditUserForm(
                    request.POST, request.FILES, instance=profile_user)
                form_seller = EditSellerForm(
                    request.POST, instance=profile_seller)
                if form_user.is_valid() and form_seller.is_valid():
                    obj_user = profile_user.save()
                    obj_seller = profile_seller.save()
                    messages.success(request, 'Profile was successfully updated.')
                    return redirect(reverse('profile_view', kwargs={
                        'pk': pk, }))
            else:
                form_user = EditUserForm(instance=profile_user)
                form_seller = EditSellerForm(instance=profile_seller)
        else:

            if request.method == 'POST':
                form_user = EditUserForm(
                    request.POST, request.FILES, instance=profile_user)
                form_seller = None
                if form_user.is_valid():
                    obj_user = profile_user.save()
                    messages.success(request, 'Profile was successfully updated.')
                    return redirect(reverse('profile_view', kwargs={
                        'pk': pk, }))
            else:
                form_user = EditUserForm(instance=profile_user)
                form_seller = None

        return render(
            request,
            'profile_edit.html',
            {
                "form_user": form_user,
                "form_seller": form_seller,
            }
        )
    else:
        raise Http404

@login_required
def become_seller(request):
    if hasattr(request.user.user, 'seller'):
        raise Http404
    if request.method == 'POST':
        form = BecomeSellerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulation, you can list auctions now!.')
            return redirect('/')
    else:

        form = BecomeSellerForm(initial={'user': request.user.user,
                                       })

    return render(
        request,
        'become_seller.html',
        {
            "form": form,
        }
    )
