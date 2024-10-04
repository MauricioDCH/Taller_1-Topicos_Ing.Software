from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse

from .models import Menu, Review
from .forms import ReviewForm, ContactoForm
from django.core.mail import send_mail
import markdown2
import time
import google.generativeai as genai
from django.contrib import messages


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        # Check if user exists
        user = User.objects.filter(username=username).first()
        if user is None:
            # If not, create a new user
            user = User.objects.create_user(username=username, password=password)

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('form')

        return render(request, 'login.html')


class HomeView(View):
    def get(self, request):
        if 'siguiente_btn' in request.GET:
            return redirect('portal_view')
        return render(request, 'home.html')


class PortalView(ListView):
    model = Menu
    template_name = 'portal.html'
    context_object_name = 'menus'

    def get_queryset(self):
        busqueda = self.request.GET.get('busqueda')
        if busqueda:
            return Menu.objects.filter(title__icontains=busqueda)
        return Menu.objects.all()


class InicioView(TemplateView):
    template_name = 'inicio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mensaje_bienvenida'] = "¡Bienvenido a nuestra aplicación!"
        return context


class ContactoView(TemplateView):
    template_name = 'contacto.html'

    def get(self, request, *args, **kwargs):
        form = ContactoForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ContactoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            telefono = request.POST.get('telefono')
            email = form.cleaned_data['email']
            mensaje = form.cleaned_data['mensaje']

            # Envía el correo
            send_mail(
                subject=f'{nombre} requiere información, contactate con él/ella',
                message=f'Nombre: {nombre}\nTeléfono: {telefono}\nEmail: {email}\nMensaje: {mensaje}',
                from_email=email,
                recipient_list=['estudio.mauricio.correa@gmail.com'],  # Cambia esto por el correo que recibirá el mensaje
                fail_silently=False,
            )
            return render(request, 'gracias.html')  # Puedes redirigir a una página de agradecimiento
        return render(request, self.template_name, {'form': form})

class GenerarView(View):
    def get(self, request):
        genai.configure(api_key="AIzaSyAWOVQpKOtCnjGq22aXznUPJdyn2Upk7iE")
        generation_config = {
            "temperature": 0.9,
            "top_p": 0.95,
            "top_k": 32,
            "max_output_tokens": 10240,
        }

        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            safety_settings=safety_settings
        )

        mensaje = ""
        generateMenu = ""
        response = ""
        generateMenu0 = "Vas a actuar como un experto en recetas de todo tipo. Debes preguntar por cosas como la cantidad de personas, alergias, tipo de situación, posibles ingredientes a disposición, entre otros. Generame un menú con sus ingredientes, información nutricional y pasos de preparación a partir del siguiente mensaje: "

        # Check if there is a message in the GET request
        if request.GET.get('generateMenu'):
            mensaje = request.GET.get('generateMenu')
            generateMenu = "Vas a actuar como un experto en recetas de todo tipo. Generame un menú con sus ingredientes, información nutricional y pasos de preparación a partir del siguiente mensaje: " + mensaje

        if generateMenu != "":
            try:
                # Send the message and get the response
                retorno = model.generate_content(generateMenu)
                retorno_text = retorno.candidates[0].content.parts[0].text

                # Process the response using markdown2
                response = markdown2.markdown(retorno_text)

                time.sleep(2)

                # Request the dish title
                titulo = model.generate_content("Ahora limítate a decirme el título del platillo basado en lo que me acabas de decir, sin utilizar letra en negrilla:" + response)
                titulo_text = titulo.candidates[0].content.parts[0].text

                # Save title and description to the database
                Menu.objects.create(
                    title=titulo_text,
                    descripcion=retorno_text,
                    imagen="menu/images/vaca_marina.png"
                )

            except TypeError as e:
                response = f"Error al procesar el menú: {e}"
            except AttributeError as e:
                response = f"Error en la estructura de la respuesta: {e}"
            except Exception as e:
                response = f"Se produjo un error inesperado: {e}"

        return render(request, 'generar.html', {'generateMenu': generateMenu, 'respuesta': response, 'mensaje': mensaje})


class MenuDetailView(DetailView):
    model = Menu
    template_name = 'detail.html'
    context_object_name = 'menu'  # Usar 'menu' en la plantilla para acceder al objeto

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtiene el objeto del menú usando el `menu_id` de la URL
        menu = self.object  
        
        # Procesa la descripción como markdown
        menu.descripcion = markdown2.markdown(menu.descripcion)  
        
        # Obtiene las reseñas relacionadas con el menú
        context['reviews'] = Review.objects.filter(menu=menu)  
        
        return context


@method_decorator(login_required, name='dispatch')
class CreateReviewView(View):
    def get(self, request, menu_id):
        menu = get_object_or_404(Menu, pk=menu_id)
        form = ReviewForm()
        return render(request, 'createreview.html', {'form': form, 'menu': menu})

    def post(self, request, menu_id):
        menu = get_object_or_404(Menu, pk=menu_id)
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.menu = menu
            review.save()
            return redirect('detail', menu_id)

        return render(request, 'create_review.html', {'form': form, 'menu': menu})

    def get_success_url(self):
        return reverse('detail', args=[self.object.menu.id])


@method_decorator(login_required, name='dispatch')
class UpdateReviewView(UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'updatereview.html'

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.object.menu.id})

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form, 'error': 'Bad data in form'})


@method_decorator(login_required, name='dispatch')
class DeleteReviewView(View):
    def post(self, request, review_id):
        review = get_object_or_404(Review, pk=review_id, user=request.user)
        review.delete()
        return redirect('detail', review.menu.id)

class BuscarView(View):
    def get(self, request):
        busqueda = request.GET.get('busqueda')
        resultados = Menu.objects.filter(title__icontains=busqueda)  # Cambia 'nombre' por 'title'
        return render(request, 'busqueda.html', {'resultados': resultados})