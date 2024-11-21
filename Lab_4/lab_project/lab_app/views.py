import pandas as pd
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Avg, Min, Max, Count
from .models import Client, Device, Worker, RepairApplication, SparePart, EquipmentForSale
import plotly.express as px
from bokeh.io import output_notebook, save, show
from bokeh.embed import components
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, Slider
from bokeh.layouts import column
from django.http import HttpResponse
import numpy as np

def index(request):
    return render(request, 'index.html')

def clients(request):
    clients = Client.objects.all()
    return render(request, 'client.html', {'clients': clients})

def add_client(request):
    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        address = request.POST['address']
        client = Client(name=name, surname=surname, phone_number=phone_number, email=email, address=address)
        client.save()
        messages.success(request, 'Client added successfully!')
        return redirect('clients')
    return render(request, 'add_client.html')

def delete_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    client.delete()
    messages.success(request, 'Client deleted successfully!')
    return redirect('clients')

def edit_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        client.name = request.POST['name']
        client.surname = request.POST['surname']
        client.phone_number = request.POST['phone_number']
        client.email = request.POST['email']
        client.address = request.POST['address']
        client.save()
        messages.success(request, 'Client updated successfully!')
        return redirect('clients')
    return render(request, 'edit_client.html', {'client': client})

def devices(request):
    devices = Device.objects.all()
    return render(request, 'devices.html', {'devices': devices})

def add_device(request):
    if request.method == 'POST':
        type = request.POST['type']
        model = request.POST['model']
        brand = request.POST['brand']
        serial_number = request.POST['serial_number']
        device = Device(type=type, model=model, brand=brand, serial_number=serial_number)
        device.save()
        messages.success(request, 'Device added successfully!')
        return redirect('devices')
    return render(request, 'add_device.html')

def delete_device(request, serial_number):
    device = get_object_or_404(Device, serial_number=serial_number)
    device.delete()
    messages.success(request, 'Device deleted successfully!')
    return redirect('devices')

def edit_device(request, serial_number):
    device = get_object_or_404(Device, serial_number=serial_number)
    if request.method == 'POST':
        device.type = request.POST['type']
        device.model = request.POST['model']
        device.brand = request.POST['brand']
        device.serial_number = request.POST['serial_number']
        device.save()
        messages.success(request, 'Device updated successfully!')
        return redirect('devices')
    return render(request, 'edit_device.html', {'device': device})

def workers(request):
    workers = Worker.objects.all()
    return render(request, 'workers.html', {'workers': workers})

def add_worker(request):
    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        position = request.POST['position']
        phone_number = request.POST['phone_number']
        city_of_residence = request.POST['city_of_residence']
        street = request.POST['street']
        worker = Worker(name=name, surname=surname, position=position, phone_number=phone_number, 
                        city_of_residence=city_of_residence, street=street)
        worker.save()
        messages.success(request, 'Worker added successfully!')
        return redirect('workers')
    return render(request, 'add_worker.html')

def delete_worker(request, worker_id):
    worker = get_object_or_404(Worker, id=worker_id)
    worker.delete()
    messages.success(request, 'Worker deleted successfully!')
    return redirect('workers')

def edit_worker(request, worker_id):
    worker = get_object_or_404(Worker, id=worker_id)
    if request.method == 'POST':
        worker.name = request.POST['name']
        worker.surname = request.POST['surname']
        worker.position = request.POST['position']
        worker.phone_number = request.POST['phone_number']
        worker.city_of_residence = request.POST['city_of_residence']
        worker.street = request.POST['street']
        worker.save()
        messages.success(request, 'Worker updated successfully!')
        return redirect('workers')
    return render(request, 'edit_worker.html', {'worker': worker})

def repairs_count_by_client(request):
    repairs = RepairApplication.objects.values('client_id') \
        .annotate(repairs_count=Count('id')) \
        .filter(repairs_count__gt=1)
    
    df = pd.DataFrame(list(repairs))

    return JsonResponse(df.to_dict(orient="records"), safe=False)

def in_progress_repair_applications(request):
    repairs = RepairApplication.objects.filter(status='in_progress').select_related('device')
    
    df = pd.DataFrame(list(repairs.values('client_id', 'device_serial_number', 'description', 'planned_price')))
    
    return JsonResponse(df.to_dict(orient="records"), safe=False)

def spare_parts_count(request):
    spare_parts = SparePart.objects.values('model') \
        .annotate(count=Count('id')) \
        .order_by('-count')
    
    df = pd.DataFrame(list(spare_parts))

    return JsonResponse(df.to_dict(orient="records"), safe=False)

def clients_with_multiple_repairs(request):
    clients = RepairApplication.objects.values('client_id') \
        .annotate(repair_count=Count('id')) \
        .filter(repair_count__gt=1)

    df = pd.DataFrame(list(clients))

    return JsonResponse(df.to_dict(orient="records"), safe=False)

def spare_parts_sorted_by_price(request):
    spare_parts = SparePart.objects.order_by('price')
    
    df = pd.DataFrame(list(spare_parts.values()))

    return JsonResponse(df.to_dict(orient="records"), safe=False)

def devices_in_repair(request):
    devices_in_repair_data = RepairApplication.objects.filter(status='In Progress') \
        .values('device_serial_number', 'status', 'planned_price')
    
    df = pd.DataFrame(list(devices_in_repair_data))

    return JsonResponse(df.to_dict(orient="records"), safe=False)

def repair_application_statistics_pandas(request):
    repairs = RepairApplication.objects.all()
    df = pd.DataFrame(list(repairs.values('planned_price')))
    
    statistics = {
        'avg_price': df['planned_price'].mean(),
        'min_price': df['planned_price'].min(),
        'max_price': df['planned_price'].max(),
        'median_price': df['planned_price'].median(),
    }
    
    return JsonResponse(statistics)

def repairs_count_by_client_plotly(request):
    repairs = RepairApplication.objects.values('client_id', 'client__name') \
        .annotate(repairs_count=Count('id')) \
        .filter(repairs_count__gt=0)
    
    df = pd.DataFrame(list(repairs))
    
    fig = px.bar(
        df,
        x='client__name',
        y='repairs_count',
        labels={'client__name': 'Client Name', 'repairs_count': 'Number of Repairs'},
        title='Repairs Count by Client'
    )

    graph_html = fig.to_html(full_html=False)
    return graph_html

def repairs_count_by_client_bokeh(request):
    repairs = RepairApplication.objects.values('client_id') \
        .annotate(repairs_count=Count('id')) \
        .filter(repairs_count__gt=0)
    
    df = pd.DataFrame(list(repairs))
    
    source = ColumnDataSource(df)
    p = figure(title="Repairs Count by Client", 
               x_axis_label="Client ID", 
               y_axis_label="Number of Repairs", 
               height=350, width=800)
    p.line(x='client_id', y='repairs_count', source=source, line_width=2)

    script, div = components(p)
    
    return render(request, 'bokeh_dashboard.html', {'script': script, 'div': div})

def interactive_bokeh_plot(request):
    repairs = RepairApplication.objects.values('client_id') \
        .annotate(repairs_count=Count('id')) \
        .filter(repairs_count__gt=1)
    
    df = pd.DataFrame(list(repairs))
    
    source = ColumnDataSource(df)
    
    p = figure(title="Repairs Count by Client", x_axis_label="Client ID", y_axis_label="Number of Repairs")
    p.line(x='client_id', y='repairs_count', source=source, line_width=2)
    
    slider = Slider(start=0, end=10, value=1, step=1, title="Client ID Filter")
    slider.on_change('value', update_plot)
    
    layout = column(p, slider)
    
    output_file("interactive_dashboard.html")
    save(layout)
    
    with open("interactive_dashboard.html", "r") as f:
        html = f.read()
        
    return HttpResponse(html)

def update_plot(request, slider_value):
    repairs = RepairApplication.objects.values('client_id', 'client__name') \
        .annotate(repairs_count=Count('id')) \
        .filter(repairs_count__gte=int(slider_value))

    if not repairs:
        return JsonResponse({'graph': '<p>No data found for the selected filter.</p>'})

    df = pd.DataFrame(list(repairs))

    fig = px.bar(
        df,
        x='client__name',
        y='repairs_count',
        labels={'client__name': 'Client Name', 'repairs_count': 'Number of Repairs'},
        title=f'Repairs Count by Client (Threshold: {slider_value})'
    )

    graph_data = fig.to_dict()

    def serialize_graph_data(data):
        if isinstance(data, np.ndarray):
            return data.tolist()  
        elif isinstance(data, dict):
            return {key: serialize_graph_data(value) for key, value in data.items()}  
        elif isinstance(data, list):
            return [serialize_graph_data(item) for item in data]  
        else:
            return data  

    serializable_graph_data = serialize_graph_data(graph_data)

    return JsonResponse({'graph': serializable_graph_data})

def repairs_count_by_client_view(request):
    repairs = RepairApplication.objects.values('client_id') \
        .annotate(repairs_count=Count('id')) \
        .filter(repairs_count__gt=0)

    total_repairs = repairs.aggregate(total_repairs=Count('id'))['total_repairs']

    return render(request, 'repairs_count_by_client.html', {'repairs': repairs, 'total_repairs': total_repairs})

def in_progress_repair_applications_view(request):
    in_progress_repairs = RepairApplication.objects.filter(status='In Progress') \
        .values('client_id', 'device_serial_number', 'description', 'planned_price')
    return render(request, 'in_progress_repair_applications.html', {'in_progress_repairs': in_progress_repairs})

def spare_parts_count_view(request):
    spare_parts = SparePart.objects.values('model') \
        .annotate(count=Count('id')) \
        .order_by('-count')
    return render(request, 'spare_parts_count.html', {'spare_parts': spare_parts})

def clients_with_multiple_repairs_view(request):
    clients = RepairApplication.objects.values('client_id') \
        .annotate(repair_count=Count('id')) \
        .filter(repair_count__gt=1)
    return render(request, 'clients_with_multiple_repairs.html', {'clients': clients})

def spare_parts_sorted_by_price_view(request):
    spare_parts = SparePart.objects.order_by('price')
    return render(request, 'spare_parts_sorted_by_price.html', {'spare_parts': spare_parts})

def devices_in_repair_view(request):
    devices_in_repair_data = RepairApplication.objects.filter(status='In Progress') \
        .values('device_serial_number', 'status', 'planned_price')
    return render(request, 'devices_in_repair.html', {'devices_in_repair': devices_in_repair_data})

def repair_application_statistics_pandas_view(request):
    repairs = RepairApplication.objects.all()
    df = pd.DataFrame(list(repairs.values('planned_price')))
    
    statistics = {
        'avg_price': df['planned_price'].mean(),
        'min_price': df['planned_price'].min(),
        'max_price': df['planned_price'].max(),
        'median_price': df['planned_price'].median(),
    }

    return render(request, 'repair_application_statistics.html', {'statistics': statistics})

def plotly_dashboard(request):
    graph = repairs_count_by_client_plotly(request)
    return render(request, 'plotly_dashboard.html', {'graph': graph})

def bokeh_dashboard(request):
    return repairs_count_by_client_bokeh(request)






