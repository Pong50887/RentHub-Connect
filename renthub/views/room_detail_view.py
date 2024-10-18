from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.views.generic import DetailView

from ..models import Room, Rental, RentalRequest, Renter
from ..utils import get_rental_progress_data


class RoomDetailView(DetailView):
    """
    Display the details of a specific room.
    """
    model = Room
    template_name = "renthub/rental.html"
    context_object_name = "room"

    def get_object(self, queryset=None):
        """Retrieve the room object based on the room number."""
        room_number = self.kwargs.get("room_number")
        room = get_object_or_404(Room, room_number=room_number)
        return room

    def get(self, request, *args, **kwargs):
        """Handle GET requests for room details."""
        try:
            room = self.get_object()
        except Http404:
            return HttpResponseRedirect(reverse("renthub:home"))

        if not room.availability:
            if Rental.objects.filter(room=room).exists():
                messages.info(request, "This room is taken.")
            else:
                messages.error(request, "This room is currently unavailable.")
            return HttpResponseRedirect(reverse("renthub:home"))

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Add extra context data to the template."""
        context = super().get_context_data(**kwargs)
        room = self.get_object()

        context['milestones'] = None
        try:
            renter = get_object_or_404(Renter, id=self.request.user.id)
            latest_request = RentalRequest.objects.filter(renter=renter, room=room).order_by('-id').first()

            if latest_request:
                context['milestones'] = get_rental_progress_data(latest_request.status)
        except Http404:
            pass
        return context