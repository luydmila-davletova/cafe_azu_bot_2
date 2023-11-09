from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Reservation, OrderSets


