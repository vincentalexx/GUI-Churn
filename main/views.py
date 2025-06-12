from django.shortcuts import render, HttpResponse
from joblib import load
from .models import Customer
import locale

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

logistic_regression_model = load('./models/logistic_regression_model.pkl')
decision_tree_model = load('./models/decision_tree_model.pkl')
random_forest_model = load('./models/random_forest_model.pkl')
adaboost_model = load('./models/adaboost_model.pkl')
xgboost_model = load('./models/xgboost_model.pkl')
catboost_model = load('./models/catboost_model.pkl')
linear_svm_model = load('./models/linear_svm_model.pkl')
naive_bayes_model = load('./models/naive_bayes_model.pkl')

scaler = load('./scaler/standard_scaler.pkl')

# Create your views here.
def new_data(request):
    if request.method == 'POST':
        selected_model = request.POST['select_model']
        customer_data = {
            'is_tv_subscriber': request.POST['tv_subscriber'],
            'is_movie_package_subscriber': request.POST['movie_subscriber'],
            'subscription_age': request.POST['subscription_age'],
            'bill_avg': request.POST['bill_avg'],
            'remaining_contract': request.POST['remaining_contract'],
            'download_avg': request.POST['download_avg'],
            'upload_avg': request.POST['upload_avg'],
            'download_over_limit': request.POST['download_over_limit'],
            'contract': request.POST['contract']
        }

        subscription_age = float(customer_data['subscription_age'])
        subscription_age = subscription_age / 12
        bill_avg = float(customer_data['bill_avg'])
        bill_avg = bill_avg / 10000
        remaining_contract = float(customer_data['remaining_contract'])
        remaining_contract = remaining_contract / 12

        # data = [[float(customer_data['is_tv_subscriber']), float(customer_data['is_movie_package_subscriber']), float(subscription_age), float(bill_avg), float(remaining_contract), float(customer_data['service_failure_count']), float(customer_data['download_avg']), float(customer_data['upload_avg']), float(customer_data['download_over_limit']), float(customer_data['contract'])]]
        data = [[float(customer_data['is_tv_subscriber']), float(customer_data['is_movie_package_subscriber']), float(subscription_age), float(bill_avg), float(remaining_contract), float(customer_data['download_avg']), float(customer_data['upload_avg']), float(customer_data['download_over_limit']), float(customer_data['contract'])]]

        if selected_model == 'logistic_regression':
            input_scaled = scaler.transform(data)
            predict = logistic_regression_model.predict(input_scaled)
            selected_model = 'Logistic Regression'
            probability = logistic_regression_model.predict_proba(input_scaled)[0][1]

        elif selected_model == 'decision_tree':
            predict = decision_tree_model.predict(data)
            selected_model = 'Decision Tree'
            probability = decision_tree_model.predict_proba(data)[0][1]

        elif selected_model == 'random_forest':
            predict = random_forest_model.predict(data)
            selected_model = 'Random Forest'
            probability = random_forest_model.predict_proba(data)[0][1]

        elif selected_model == 'adaboost':
            predict = adaboost_model.predict(data)
            selected_model = 'AdaBoost'
            probability = adaboost_model.predict_proba(data)[0][1]

        elif selected_model == 'xgboost':
            predict = xgboost_model.predict(data)
            selected_model = 'XGBoost'
            probability = xgboost_model.predict_proba(data)[0][1]

        elif selected_model == 'catboost':
            predict = catboost_model.predict(data)
            selected_model = 'CatBoost'
            probability = catboost_model.predict_proba(data)[0][1]

        elif selected_model == 'linear_svm':
            input_scaled = scaler.transform(data)
            predict = linear_svm_model.predict(input_scaled)
            selected_model = 'Linear SVM'
            probability = linear_svm_model.predict_proba(input_scaled)[0][1]

        elif selected_model == 'naive_bayes':
            predict = naive_bayes_model.predict(data)
            selected_model = 'Naive Bayes'
            probability = naive_bayes_model.predict_proba(data)[0][1]

        if predict == 1:
            actions = ['Tawarkan layanan tambahan seperti paket hiburan untuk meningkatkan nilai langganan.', 'Dorong perpanjangan kontrak dengan insentif menarik seperti diskon atau bonus.', 'Berikan penghargaan loyalitas seperti cashback, poin, atau hadiah eksklusif.']
        else:
            actions = ['Lakukan intervensi proaktif dengan menghubungi pelanggan yang berisiko tinggi untuk mendengar dan menyelesaikan keluhan mereka.', 'Tawarkan paket atau harga yang lebih fleksibel agar sesuai dengan kebutuhan dan kemampuan pelanggan.', 'Luncurkan kampanye retensi personalisasi berisi penawaran khusus untuk menarik pelanggan agar tetap bertahan.']
        
        if predict == 1:
            predict = "Churn"
            result = "High Churn Risk."
        else:
            predict = "Not Churn"
            result = "Low Churn Risk."

        probability = round(probability * 100, 2)

        customer_data['bill_avg'] = int(customer_data['bill_avg'])
        customer_data['bill_avg'] = locale.format_string('%d', customer_data['bill_avg'], grouping=True)
        customer_data['subscription_age'] = int(customer_data['subscription_age'])
        customer_data['remaining_contract'] = int(customer_data['remaining_contract'])
        customer_data['download_over_limit'] = int(customer_data['download_over_limit'])

        return render(request, 'new_data.html', {'result' : result, 'predict': predict, 'selected_model': selected_model, 'probability' : probability, 'customer_data': customer_data, 'actions': actions})

    else:
        return render(request, 'new_data.html')

def existing_data(request):
    if request.method == 'POST':
        selected_model = request.POST['select_model']
        customer_id = request.POST['customer_id']
        
        customer_data = Customer.objects.get(id=customer_id)

        # data = [[float(customer_data.is_tv_subscriber), float(customer_data.is_movie_package_subscriber), float(customer_data.subscription_age), float(customer_data.bill_avg), float(customer_data.remaining_contract), float(customer_data.service_failure_count), float(customer_data.download_avg), float(customer_data.upload_avg), float(customer_data.download_over_limit)]]
        data = [[float(customer_data.is_tv_subscriber), float(customer_data.is_movie_package_subscriber), customer_data.subscription_age, customer_data.bill_avg, customer_data.reamining_contract, customer_data.download_avg, customer_data.upload_avg, customer_data.download_over_limit, float(customer_data.is_contract)]]

        if selected_model == 'logistic_regression':
            input_scaled = scaler.transform(data)
            predict = logistic_regression_model.predict(input_scaled)
            selected_model = 'Logistic Regression'
            probability = logistic_regression_model.predict_proba(input_scaled)[0][1]

        elif selected_model == 'decision_tree':
            predict = decision_tree_model.predict(data)
            selected_model = 'Decision Tree'
            probability = decision_tree_model.predict_proba(data)[0][1]

        elif selected_model == 'random_forest':
            predict = random_forest_model.predict(data)
            selected_model = 'Random Forest'
            probability = random_forest_model.predict_proba(data)[0][1]

        elif selected_model == 'adaboost':
            predict = adaboost_model.predict(data)
            selected_model = 'AdaBoost'
            probability = adaboost_model.predict_proba(data)[0][1]

        elif selected_model == 'xgboost':
            predict = xgboost_model.predict(data)
            selected_model = 'XGBoost'
            probability = xgboost_model.predict_proba(data)[0][1]

        elif selected_model == 'catboost':
            predict = catboost_model.predict(data)
            selected_model = 'CatBoost'
            probability = catboost_model.predict_proba(data)[0][1]

        elif selected_model == 'linear_svm':
            input_scaled = scaler.transform(data)
            predict = linear_svm_model.predict(input_scaled)
            selected_model = 'Linear SVM'
            probability = linear_svm_model.predict_proba(input_scaled)[0][1]

        elif selected_model == 'naive_bayes':
            predict = naive_bayes_model.predict(data)
            selected_model = 'Naive Bayes'
            probability = naive_bayes_model.predict_proba(data)[0][1]

        if predict == 1:
            actions = ['Tawarkan layanan tambahan seperti paket hiburan untuk meningkatkan nilai langganan.', 'Dorong perpanjangan kontrak dengan insentif menarik seperti diskon atau bonus.', 'Berikan penghargaan loyalitas seperti cashback, poin, atau hadiah eksklusif.']
        else:
            actions = ['Lakukan intervensi proaktif dengan menghubungi pelanggan yang berisiko tinggi untuk mendengar dan menyelesaikan keluhan mereka.', 'Tawarkan paket atau harga yang lebih fleksibel agar sesuai dengan kebutuhan dan kemampuan pelanggan.', 'Luncurkan kampanye retensi personalisasi berisi penawaran khusus untuk menarik pelanggan agar tetap bertahan.']

        if predict == 1:
            predict = "Churn"
            result = "High Churn Risk."
        else:
            predict = "Not Churn"
            result = "Low Churn Risk."

        probability = round(probability * 100, 2)

        customer_data.bill_avg = customer_data.bill_avg * 10000
        customer_data.bill_avg = int(customer_data.bill_avg)
        customer_data.bill_avg = locale.format_string('%d', customer_data.bill_avg, grouping=True)
        customer_data.subscription_age = customer_data.subscription_age * 12
        customer_data.subscription_age = int(customer_data.subscription_age)
        customer_data.reamining_contract = customer_data.reamining_contract * 12
        customer_data.reamining_contract = int(customer_data.reamining_contract)
        customer_data.download_over_limit = int(customer_data.download_over_limit)

        return render(request, 'existing_data.html', {'result' : result, 'predict': predict, 'selected_model': selected_model, 'probability' : probability, 'customer_data': customer_data, 'actions': actions})
    else:
        return render(request, 'existing_data.html')