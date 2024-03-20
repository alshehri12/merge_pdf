from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponse
from PyPDF2 import PdfMerger

def upload_form(request):
    if request.method == 'POST':
        try:
            file1 = request.FILES.get('file1')
            file2 = request.FILES.get('file2')

            if not file1 or not file2:
                return HttpResponseBadRequest("Please upload both files.")

            # Validate file types if necessary
            if not (file1.name.endswith('.pdf') and file2.name.endswith('.pdf')):
                return HttpResponseBadRequest("Please upload PDF files only.")

            merger = PdfMerger()
            merger.append(file1, import_outline=False)
            merger.append(file2, import_outline=False)

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

def success(request):
    # Optional success message template
    return render(request, 'merge/success.html')