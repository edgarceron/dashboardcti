
def data_process(request):
    data = request.data
    id_agent = data['id_agent']
    id_queue_call_entry = data['id_queue_call_entry']
    start_date = data['start_date']
    end_date = data['end_date']

    