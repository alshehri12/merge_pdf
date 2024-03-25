# from django.shortcuts import render
# from django.http import HttpResponseBadRequest, HttpResponse
# from PyPDF2 import PdfMerger

# def upload_form(request):
#     if request.method == 'POST':
#         try:
#             file1 = request.FILES.get('file1')
#             file2 = request.FILES.get('file2')

#             if not file1 or not file2:
#                 return HttpResponseBadRequest("Please upload both files.")

#             # Validate file types if necessary
#             if not (file1.name.endswith('.pdf') and file2.name.endswith('.pdf')):
#                 return HttpResponseBadRequest("Please upload PDF files only.")

#             merger = PdfMerger()
#             merger.append(file1, import_outline=False)
#             merger.append(file2, import_outline=False)

#             output_filename = "merged.pdf"
#             with open(output_filename, 'wb') as merged_pdf:
#                 merger.write(merged_pdf)

#             # Serve the merged PDF as a response
#             with open(output_filename, 'rb') as merged_pdf:
#                 response = HttpResponse(merged_pdf, content_type='application/pdf')
#                 response['Content-Disposition'] = 'attachment; filename="merged.pdf"'
#                 return response
#         except Exception as e:
#             return HttpResponseBadRequest(f"Error: {str(e)}")
#     else:
#         return render(request, 'merge/form.html')

# def success(request):
#     # Optional success message template
#     return render(request, 'merge/success.html')

from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponse
from PyPDF2 import PdfMerger
from PIL import Image
import io


def upload_form(request):
    if request.method == 'POST':
        try:
            file1 = request.FILES.get('file1')
            file2 = request.FILES.get('file2')
            image = request.FILES.get('image')

            if not (file1 or file2 or image):
                return HttpResponseBadRequest("Please upload at least one file.")

            # Validate file types if necessary
            if file1 and not file1.name.endswith('.pdf'):
                return HttpResponseBadRequest("Please upload PDF files only.")
            if file2 and not file2.name.endswith('.pdf'):
                return HttpResponseBadRequest("Please upload PDF files only.")
            if image and not (image.name.endswith('.jpg') or image.name.endswith('.jpeg') or image.name.endswith('.png')):
                return HttpResponseBadRequest("Please upload JPG, JPEG, or PNG images only.")

            merger = PdfMerger()

            if file1:
                merger.append(file1, import_outline=False)
            if file2:
                merger.append(file2, import_outline=False)
            if image:
                # Convert image to PDF
                image_pdf = convert_image_to_pdf(image)
                merger.append(image_pdf, import_outline=False)

            output_filename = "merged.pdf"
            with open(output_filename, 'wb') as merged_pdf:
                merger.write(merged_pdf)

            # Serve the merged PDF as a response
            with open(output_filename, 'rb') as merged_pdf:
                response = HttpResponse(merged_pdf, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="merged.pdf"'
                return response
        except Exception as e:
            return HttpResponseBadRequest(f"Error: {str(e)}")
    else:
        return render(request, 'merge/form.html')

def convert_image_to_pdf(image):
    # Open the image using Pillow
    img = Image.open(image)

    # Convert the image to PDF
    img_byte_array = io.BytesIO()
    img.save(img_byte_array, format='PDF')
    img_byte_array.seek(0)

    return img_byte_array

def success(request):
    # Optional success message template
    return render(request, 'merge/success.html')