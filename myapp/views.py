from django.shortcuts import render
from django.http import HttpResponse
import spacy

def home(request):
    if request.method == 'POST' and request.FILES['file']:
        # Load the spaCy English model
        # import spacy

        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            # If the model is not found, download it
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            nlp = spacy.load("en_core_web_sm")

        # nlp = spacy.load("en_core_web_sm")

        # Read the uploaded files
        uploaded_file = request.FILES['file']
        file_contents = uploaded_file.read().decode('utf-8')

        # Process the file contents with spaCy NER
        doc = nlp(file_contents)

        # Replace identified entities with placeholders
        masked_text = file_contents
        for ent in doc.ents:
            masked_text = masked_text.replace(ent.text, "[MASK]")

        # Create an HTTP response with the masked text file
        response = HttpResponse(masked_text, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="masked_text.txt"'
        return response
    return render(request, 'home.html')
