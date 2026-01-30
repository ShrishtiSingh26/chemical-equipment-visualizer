# equipment/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Dataset
from .utils import analyze_csv

class UploadCSV(APIView):
    def post(self, request):
        file = request.FILES['file']
        summary = analyze_csv(file)

        Dataset.objects.create(
            filename=file.name,
            summary=summary
        )

        if Dataset.objects.count() > 5:
            Dataset.objects.first().delete()

        return Response(summary)

class History(APIView):
    def get(self, request):
        data = Dataset.objects.order_by('-uploaded_at')[:5]
        return Response([
            {
                "filename": d.filename,
                "uploaded_at": d.uploaded_at,
                "summary": d.summary
            } for d in data
        ])
