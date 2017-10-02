from django.shortcuts import render
from sixerrapp.forms import available_select_options
from django.http import JsonResponse

# JSON service for ajax requests
def get_json_data_by_key(request):
    # Ajax handling
    if request.is_ajax() and 'selected_json_key' in request.POST:
        selected_json_key = request.POST['selected_json_key']
        if selected_json_key in forms.available_select_options:
            # Get the country regions from all regions only for the selected country
            r = next((item for item in forms.all_regions if item["code"] == selected_json_key), None)
            # Return country code, type and regions if available
            res = r if r else {}
        else:
            res = {}

        return JsonResponse(json.dumps(res), safe=False)

    return render(request, 'overview.html')
