from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Note
from notes.forms import NoteForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class NoteList(LoginRequiredMixin, ListView):
  model = Note
  template_name = 'notes/list.html'
  

class NoteCreate(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/create.html'
    success_url = reverse_lazy('note_list')


class NoteUpdate(LoginRequiredMixin, UpdateView):
  model = Note
  form_class = NoteForm
  template_name = 'notes/update.html'
  success_url = reverse_lazy('note_list')

class NoteDelete(LoginRequiredMixin, DeleteView):
  model = Note
  
  template_name = 'notes/delete.html'
  success_url = reverse_lazy('note_list')