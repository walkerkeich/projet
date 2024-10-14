from django.shortcuts import redirect

class SlugRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Vérifier si le slug est 'administration-systeme'
        if request.path.endswith('administration-systeme/'):
            return redirect('app:Filieres')  # Rediriger vers la page des filières

        response = self.get_response(request)
        return response
