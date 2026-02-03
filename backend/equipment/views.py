from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse

from .models import Dataset
from .utils import analyze_csv
from .pdf import  generate_pdf


from .models import Dataset
from .utils import analyze_csv, password_protect_pdf




class UploadCSV(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file uploaded"}, status=400)

        summary = analyze_csv(file)

        Dataset.objects.create(
            filename=file.name,
            summary=summary
        )

        if Dataset.objects.count() > 5:
            Dataset.objects.first().delete()

        return Response(summary)


class History(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = Dataset.objects.order_by("-uploaded_at")[:5]
        return Response([
            {
                "filename": d.filename,
                "uploaded_at": d.uploaded_at,
                "summary": d.summary
            } for d in data
        ])


class GeneratePDF(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        dataset = Dataset.objects.last()
        if not dataset:
            return Response({"error": "No data available"}, status=400)

        buffer = generate_pdf(dataset.summary)
        protected = password_protect_pdf(buffer, "1234")

        return FileResponse(
            protected,
            as_attachment=True,
            filename="equipment_report.pdf"
        )
