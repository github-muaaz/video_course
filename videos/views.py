from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, FileResponse
from .models import Video, UserProfile, Payment
from django.conf import settings
import os
import re

@login_required
def index(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    can_watch = request.user.is_superuser or user_profile.is_subscribed
    videos = Video.objects.all() if can_watch else []

    return render(request, "index.html", {"videos": videos, "can_watch": can_watch})


def protected_media(request, file_path):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You are not allowed to access this file.")

    video = get_object_or_404(Video, video=f"videos/{file_path}")
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if not request.user.is_superuser and not user_profile.is_subscribed:
        return HttpResponseForbidden("You must be subscribed to access this video.")

    file_path = os.path.join(settings.MEDIA_ROOT, "videos", file_path)
    return FileResponse(open(file_path, "rb"))


def is_valid_card(card_number):
    return re.fullmatch(r"\d{16}", card_number) is not None


def is_valid_expiry(expiry_date):
    return re.fullmatch(r"(0[1-9]|1[0-2])\/\d{2}", expiry_date) is not None


def is_valid_cvv(cvv):
    return re.fullmatch(r"\d{3}", cvv) is not None


@login_required
def subscribe(request):
    if request.method == "POST":
        card_number = request.POST.get("card_number")
        expiry_date = request.POST.get("expiry_date")
        cvv = request.POST.get("cvv")

        if not (card_number and expiry_date and cvv):
            return render(request, "subscribe.html", {"error": "All fields are required."})

        if not is_valid_card(card_number):
            return render(request, "subscribe.html", {"error": "Invalid card number. It must be 16 digits."})

        if not is_valid_expiry(expiry_date):
            return render(request, "subscribe.html", {"error": "Invalid expiry date. Use MM/YY format."})

        if not is_valid_cvv(cvv):
            return render(request, "subscribe.html", {"error": "Invalid CVV. It must be 3 digits."})

        Payment.objects.update_or_create(
            user=request.user,
            defaults={
                "card_number": card_number,
                "expiry_date": expiry_date,
                "cvv": cvv
            }
        )

        user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
        user_profile.is_subscribed = True
        user_profile.save()

        return redirect("videos")

    return render(request, "subscribe.html")


@login_required
def unsubscribe(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        user_profile.is_subscribed = False
        user_profile.save()

        Payment.objects.filter(user=request.user).delete()

        return redirect("videos")

    return render(request, "unsubscribe.html")
