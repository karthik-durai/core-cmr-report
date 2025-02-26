import os
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import xml.etree.ElementTree as ET
from xml_parser import get_data
from django.views.decorators.csrf import csrf_exempt


UPLOAD_DIR = 'uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def upload_page(request):
    return render(request, 'upload.html')

@csrf_exempt  # Disable CSRF for simplicity
def upload_xml(request):
    if request.method == 'POST' and request.FILES.get('xml_file'):
        xml_file = request.FILES['xml_file']
        
        if not xml_file.name.endswith('.xml'):
            return JsonResponse({'error': 'Only XML files are allowed'}, status=400)
        
        fs = FileSystemStorage(location=UPLOAD_DIR)
        filename = fs.save(xml_file.name, xml_file)
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        try:
            data = get_data(file_path)
        except ET.ParseError:
            return JsonResponse({'error': 'Invalid XML format'}, status=400)
        
        fs.delete(filename)
        
        return HttpResponse(data)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)