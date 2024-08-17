from django.shortcuts import render

def custom_404(request, exception):
    return render(request, 'page_not_found.html', status=404)