from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from . import ddpm_2,ddpm_conditional_2
import json
from .models import Image_Binary
from django.core.serializers import serialize
import base64

def display_image(request):
    image_instances = Image_Binary.objects.all()

    if image_instances:
        # Serialize the queryset to JSON
        images_data = serialize('json', image_instances)

        # Return JSON response with images data
        return JsonResponse({'images': images_data}, content_type='application/json')
    else:
        # Handle case when no image found
        return JsonResponse({'error': 'No images found'}, status=404)

# Create your views here.

def index(request):
    return render(request,template_name='index4.html')

def previous_image(request):
    return render(request,template_name='database.html')

def generate_img(request):
    ddpm_2.generate_image()
    image_instance = Image_Binary.objects.latest('created_at')  # Assuming you want to retrieve the first image, adjust as needed

    if image_instance:
        # Retrieve the binary data from the database
        image_binary = image_instance.image_data
        # Create an HttpResponse with the binary data
        response = HttpResponse(image_binary, content_type="image/jpeg")  # Adjust content type as needed
        response['Content-Disposition'] = 'inline; filename="image.jpg"'  # Specify filename if necessary
        return response
    else:
        # Handle case when no image found
        return HttpResponse("No image found", status=404)
    
def generate_img_2(request):
    ddpm_conditional_2.generate_image()
    image_instance = Image_Binary.objects.latest('created_at')  # Assuming you want to retrieve the first image, adjust as needed

    if image_instance:
        # Retrieve the binary data from the database
        image_binary = image_instance.image_data
        # Create an HttpResponse with the binary data
        response = HttpResponse(image_binary, content_type="image/jpeg")  # Adjust content type as needed
        response['Content-Disposition'] = 'inline; filename="image.jpg"'  # Specify filename if necessary
        return response
    else:
        # Handle case when no image found
        return HttpResponse("No image found", status=404)
    
#def display_image(request):
#    image_instances = Image_Binary.objects.all()
#
#    if image_instances:
#        # List to hold image data
#        images_data = []
#
#        # Loop through each image instance
#        for image_instance in image_instances:
#            # Retrieve the binary data from the database
#            image_binary = image_instance.image_data
#
#            # Append image data to the list
#            images_data.append({
#                'image': image_binary,  # Assuming you have a field for filename in your model
#            })
#
#        # Return JSON response with images data
#        return JsonResponse({'images':images_data,}, content_type='application/json')
#    else:
#        # Handle case when no image found
#        return JsonResponse({'error': 'No images found'}, status=404)

def display_image(request):
    image_instances = Image_Binary.objects.all().order_by('-created_at')
    images_binary = []
    if image_instances:
        for i in range(len(image_instances)):
            images_binary.append(base64.b64encode(image_instances[i].image_data).decode('utf-8'))
        # Serialize the queryset to JSON
        image_json = json.dumps(images_binary)
        # Return JSON response with images data
        return JsonResponse({'images': image_json}, content_type='application/json')
    else:
        # Handle case when no image found
        return JsonResponse({'error': 'No images found'}, status=404)
