from django.shortcuts import render, redirect, get_object_or_404
from . import models
from . import forms
from django.contrib import messages



def add_placement(request):
    if request.method == "POST":
        form = forms.PlacementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Placement added successfully")
            return redirect("list-of-placements")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error} in {field}")
    else:
        form = forms.placementForm()

    context = {
        "form": form,
    }
    return render(request, "add_placement.html", context)


def edit_placement(request, placement_id):
    placement = get_object_or_404(models.RecruitmentProcess, id=placement_id)
    print(placement)
    if request.method == "POST":
        form = forms.EditPlacementForm(request.POST, instance=placement)
        if form.is_valid():
            form.save()
            messages.success(request, "placement details updated successfully")
            return redirect("view_placement", placement_id=placement.id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error} in {field}")
    else:
        form = forms.EditPlacementForm(instance=placement)

    context = {
        "form": form,
        "placement": placement,
    }
    return render(request, "edit_placement.html", context)


def view_placement(request, placement_id):
    placement = get_object_or_404(models.RecruitmentProcess, id=placement_id)

    context = {
        "placement": placement,
    }
    return render(request, "view_placement.html", context)


def delete_placement(request, placement_id):
    placement = get_object_or_404(models.RecruitmentProcess, id=placement_id)
    if request.method == "POST":
        placement.delete()
        return redirect("list-of-placements")
    

def list_of_placements(request):
    placements = models.RecruitmentProcess.objects.all()

    context = {
        "placements": placements,
    }
    return render(request, "list_of_placements.html", context)
