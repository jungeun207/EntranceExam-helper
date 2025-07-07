from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import FeedbackForm
from .models import Feedback

def feedback_form(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '피드백이 성공적으로 전송되었습니다! 소중한 의견 감사합니다.')
            return redirect('feedback:success')
    else:
        form = FeedbackForm()
    
    return render(request, 'feedback/form.html', {'form': form})

def feedback_success(request):
    return render(request, 'feedback/success.html')

class FeedbackCreateView(CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'feedback/form.html'
    success_url = reverse_lazy('feedback:success')
    
    def form_valid(self, form):
        messages.success(self.request, '피드백이 성공적으로 전송되었습니다!')
        return super().form_valid(form)