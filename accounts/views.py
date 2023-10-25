from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render, redirect
from .decorators import validate_registration_data
from .models import Account
from django.contrib import messages
# for email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.utils import http, encoding, html
# END IMPORTS


@api_view(['POST'])
@validate_registration_data
def register(request):
    data = request.data
    user = Account.objects.create(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        username=data['email']
    )
    user.set_password(data['password'])
    user.save()
    account_verification_link(request, user)
    return Response("User created, verification email has been sent to your email.")


@api_view(['POST'])
def forgot_password(request):
    email = request.data['email']
    if Account.objects.filter(email=email).exists():
        user = Account.objects.get(email__exact=email)
        # reset password email
        current_site = get_current_site(request)
        context = {
            'user': user,
            'domain': current_site,
            'uid': http.urlsafe_base64_encode(encoding.force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        }
        html_message = render_to_string(
            'reset_password_email.html', context, request)
        plain_message = html.strip_tags(html_message)
        email = EmailMultiAlternatives(
            "Password Reset Email", plain_message, to=[user.email])
        email.attach_alternative(html_message, "text/html")
        email.send()
        return Response({'message': 'Password reset link has been sent to your email.'})
    else:
        return Response({'error': 'Email does not exist.'})


def reset_password(request, uidb64, token):
    try:
        uid = http.urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password.')
        return render(request, 'reset_password.html')
    else:
        messages.error(request, 'This link has been expired!')
        return render(request, 'reset_failed.html')


def reset_password_data(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            return render(request, 'reset_password_success.html')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('reset_password_data')


def account_verification_link(request, user):
    current_site = get_current_site(request)
    context = {
        'user': user,
        'domain': current_site,
        'uid': http.urlsafe_base64_encode(encoding.force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    }
    html_message = render_to_string(
        'account_verification.html', context, request)
    plain_message = html.strip_tags(html_message)
    email = EmailMultiAlternatives(
        "Verify Account", plain_message, to=[user.email])
    email.attach_alternative(html_message, "text/html")
    email.send()


def activate(request, uidb64, token):
    try:
        uid = http.urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'account_activated.html')
    else:
        return render(request, 'activation_failed.html')
