from django.shortcuts import render, redirect
from django.views import View

from .models import Room

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