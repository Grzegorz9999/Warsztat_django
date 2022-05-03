import datetime
from django.shortcuts import render, redirect
from django.views import View

from .models import Room, RoomReservation

# Create your views here.

def main(request):
    return render(request, "exercise/main.html", {})

def add_room(request):
    if request.method == "GET":
        room = Room.objects.all()

        return render(
            request,
            'exercise/add_room.html',
            context={
                'room': room,
            }
        )

    elif request.method == "POST":
        name = request.POST.get("room-name")
        capacity = request.POST.get("capacity")
        capacity = int(capacity) if capacity else 0
        projector = request.POST.get("projector") == "on"

        if not name:
            return render(request, "exercise/add_room.html", context={"error": "Nie podano nawy sali"})
        if capacity <= 0:
            return render(request, "exercise/add_room.html", context={"error": "Pojemność sali musi być dodatnia"})
        if Room.objects.filter(name=name).first():
            return render(request, "exercise/add_room.html", context={"error": "Sala o podanej nazwie istnieje"})


        Room.objects.create(name=name, capacity=capacity, projector=projector)
        return redirect("/room/list")

#def show_room_list(request):
 #   rooms = Room.objects.all()

  #  return render(
   #     request,
    #    'exercise/show_room_list.html',
     #   context={
      #      'room': rooms,
       # }
   # )

class RoomListView(View):
    def get(self, request):
        rooms = Room.objects.all()
        return render(request, "exercise/show_room_list.html", context={"rooms": rooms})

class DeleteRoomView(View):
    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)
        room.delete()
        return redirect("/room/list")

class ModifyRoomView(View):
    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)
        return render(request, "exercise/modify_room.html", context={"room": room})

    def post(self, request, room_id):
        room = Room.objects.get(id=room_id)
        name = request.POST.get("room-name")
        capacity = request.POST.get("capacity")
        capacity = int(capacity) if capacity else 0
        projector = request.POST.get("projector") == "on"

        if not name:
            return render(request, "exercise/modify_room.html", context={"room": room,
                                                                "error": "Nie podano nawy sali"})
        if capacity <= 0:
            return render(request, "exercise/modify_room.html", context={"room": room,
                                                                "error": "Pojemność sali musi być dodatnia"})
        if name != room.name and Room.objects.filter(name=name).first():
            return render(request, "exercise/modify_room.html", context={"room": room,
                                                                "error": "Sala o podanej nazwie istnieje"})

        room.name = name
        room.capacity = capacity
        room.projector = projector
        room.save()
        return redirect("/room/list")

class ReservationView(View):
    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)
        return render(request, "exercise/reservation.html", context={"room": room})

    def post(self, request, room_id):
        room = Room.objects.get(id=room_id)
        date = request.POST.get("reservation-date")
        comment = request.POST.get("comment")

        if RoomReservation.objects.filter(room_id=room, date=date):
            return render(request, "exercise/reservation.html", context={"room": room, "error": "Sala jest już zarezerwowana!"})
        if date < str(datetime.date.today()):
            return render(request, "exercise/reservation.html", context={"room": room, "error": "Data jest z przeszłości!"})

        RoomReservation.objects.create(room=room, date=date, comment=comment)
        return redirect("/room/list")

class RoomDetailsView(View):
    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)
        reservations = room.roomreservation_set.filter(date__gte=str(datetime.date.today())).order_by('date')
        return render(request, "exercise/room_details.html", context={"room": room, "reservations": reservations})

    class RoomListView(View):
        def get(self, request):
            rooms = Room.objects.all()
            for room in rooms:
                reservation_dates = [reservation.date for reservation in room.roomreservation_set.all()]
                room.reserved = datetime.date.today() in reservation_dates
            return render(request, "exercise/rooms.html", context={"rooms": rooms})

class SearchView(View):
    def get(self, request):
        name = request.GET.get("room-name")
        capacity = request.GET.get("capacity")
        capacity = int(capacity) if capacity else 0
        projector = request.GET.get("projector") == "on"

        rooms = Room.objects.all()
        if projector:
            rooms = rooms.filter(projector=projector)
        if capacity:
            rooms = rooms.filter(capacity__gte=capacity)
        if name:
            rooms.filter(name__contains=name)

        for room in rooms:
            reservation_dates = [reservation.date for reservation in room.roomreservation_set.all()]
            room.reserved = str(datetime.date.today()) in reservation_dates

        return render(request, "exercise/rooms.html", context={"rooms": rooms, "date": datetime.date.today()})

class ReservationView(View):
    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)
        reservations = room.roomreservation_set.filter(date__gte=str(datetime.date.today())).order_by('date')
        return render(request, "exercise/reservation.html", context={"room": room, "reservations": reservations})

    def post(self, request, room_id):
        room = ConferenceRoom.objects.get(id=room_id)
        date = request.POST.get("reservation-date")
        comment = request.POST.get("comment")

        reservations = room.roomreservation_set.filter(date__gte=str(datetime.date.today())).order_by('date')

        if RoomReservation.objects.filter(room=room, date=date):
            return render(request, "exercise/reservation.html", context={"room": room,
                                                                "reservations": reservations,
                                                                "error": "Sala jest już zarezerwowana!"})
        if date < str(datetime.date.today()):
            return render(request, "exercise/reservation.html", context={"room": room,
                                                                "reservations": reservations,
                                                                "error": "Data jest z przeszłości!"})

        RoomReservation.objects.create(room=room, date=date, comment=comment)
        return redirect("/room/list")