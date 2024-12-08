import csv
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404

from LMS_App.models.borrow_request import Borrow_Request
from LMS_App.models.library_user import Library_User
from django.views import View

class DownloadBorrowHistory(View):
    def get(self, request):
        library_user_id = request.session.get('id')
        if not library_user_id:
            return redirect('/login')

        library_user = get_object_or_404(Library_User, id=library_user_id)
        history = Borrow_Request.objects.filter(user=library_user).order_by('-requested_time')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="borrow_history.csv"'

        writer = csv.writer(response)
        writer.writerow(['Book Title', 'Status', 'Requested Time', 'Start Date', 'End Date'])
        for record in history:
            writer.writerow([
                record.book.title,
                record.status,
                record.requested_time.strftime('%Y-%m-%d %H:%M:%S'),
                record.start_date.strftime('%Y-%m-%d %H:%M:%S') if record.start_date else 'N/A',
                record.end_date.strftime('%Y-%m-%d %H:%M:%S') if record.end_date else 'N/A'
            ])

        return response
