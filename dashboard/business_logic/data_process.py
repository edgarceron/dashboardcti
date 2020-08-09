
def data_process(request):
    data = request.data
    id_agent = data['id_agent']
    id_campaign = data['id_campaign']
    start_date = data['start_date']
    end_date = data['end_date']

    