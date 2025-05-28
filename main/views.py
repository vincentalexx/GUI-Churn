from django.shortcuts import render, HttpResponse
from joblib import load

logistic_regression_model = load('./models/logistic_regression_model.pkl')
scaler = load('./scaler/scaler.pkl')

# Create your views here.
def main(request):
    if request.method == 'POST':
        selected_model = request.POST['select_model']
        tv_subscriber = request.POST['tv_subscriber']
        movie_subscriber = request.POST['movie_subscriber']
        subscription_age = request.POST['subscription_age']
        bill_avg = request.POST['bill_avg']
        remaining_contract = request.POST['remaining_contract']
        service_failure_count = request.POST['service_failure_count']
        download_avg = request.POST['download_avg']
        upload_avg = request.POST['upload_avg']
        download_over_limit = request.POST['download_over_limit']
        contract = request.POST['contract']

        data = [[float(tv_subscriber), float(movie_subscriber), float(subscription_age), float(bill_avg), float(remaining_contract), float(service_failure_count), float(download_avg), float(upload_avg), float(download_over_limit), float(contract)]]

        input_scaled = scaler.transform(data)

        if selected_model == 'logistic_regression':
            predict = logistic_regression_model.predict(input_scaled)
            selected_model = 'Logistic Regression'


        if predict == 1:
            predict = "Customer will churn"
        else:
            predict = "Customer will not churn"

        return render(request, 'main.html', {'result' : predict, 'selected_model': selected_model})

        # return render(request, 'main.html', {'result': result, 'tv_subscriber': tv_subscriber, 'movie_subscriber': movie_subscriber, 'subscription_age': subscription_age, 'bill_avg': bill_avg, 'remaining_contract': remaining_contract, 'service_failure_count': service_failure_count, 'download_avg': download_avg, 'upload_avg': upload_avg, 'download_over_limit': download_over_limit, 'contract': contract})
    else:
        return render(request, 'main.html')