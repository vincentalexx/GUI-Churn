from django.shortcuts import render, HttpResponse
from joblib import load
from .models import Customer

logistic_regression_model = load('./models/logistic_regression_model.pkl')
decision_tree_model = load('./models/decision_tree_model.pkl')
random_forest_model = load('./models/random_forest_model.pkl')
adaboost_model = load('./models/adaboost_model.pkl')
adaboost_model = load('./models/xgboost_model.pkl')
xgboost_model = load('./models/xgboost_model.pkl')
catboost_model = load('./models/catboost_model.pkl')
linear_svm_model = load('./models/linear_svm_model.pkl')
naive_bayes_model = load('./models/naive_bayes_model.pkl')

lr_scaler = load('./scaler/logistic_regression_scaler.pkl')
dt_scaler = load('./scaler/decision_tree_scaler.pkl')
rf_scaler = load('./scaler/random_forest_scaler.pkl')
ada_scaler = load('./scaler/adaboost_scaler.pkl')
xg_scaler = load('./scaler/xgboost_scaler.pkl')
# cat_scaler = load('./scaler/catboost_scaler.pkl')
svm_scaler = load('./scaler/linear_svm_scaler.pkl')
nb_scaler = load('./scaler/naive_bayes_scaler.pkl')

# Create your views here.
def new_data(request):
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

        if selected_model == 'logistic_regression':
            scaler = lr_scaler
            input_scaled = scaler.transform(data)
            predict = logistic_regression_model.predict(input_scaled)
            selected_model = 'Logistic Regression'
            probability = logistic_regression_model.predict_proba(input_scaled)[0][1]

        elif selected_model == 'decision_tree':
            scaler = dt_scaler
            input_scaled = scaler.transform(data)
            predict = decision_tree_model.predict(input_scaled)
            selected_model = 'Decision Tree'
            probability = decision_tree_model.predict_proba(input_scaled)[0][1]

        elif selected_model == 'random_forest':
            scaler = rf_scaler
            input_scaled = scaler.transform(data)
            predict = random_forest_model.predict(input_scaled)
            selected_model = 'Random Forest'
            probability = random_forest_model.predict_proba(input_scaled)[0][1]

        elif selected_model == 'adaboost':
            scaler = ada_scaler
            input_scaled = scaler.transform(data)
            predict = adaboost_model.predict(input_scaled)
            selected_model = 'AdaBoost'
            probability = adaboost_model.predict_proba(input_scaled)[0][1]

        elif selected_model == 'xgboost':
            scaler = xg_scaler
            input_scaled = scaler.transform(data)
            predict = xgboost_model.predict(input_scaled)
            selected_model = 'XGBoost'
            probability = xgboost_model.predict_proba(input_scaled)[0][1]

        elif selected_model == 'catboost':
            # scaler = cat_scaler
            # input_scaled = scaler.transform(data)
            predict = catboost_model.predict(data)
            selected_model = 'CatBoost'
            probability = catboost_model.predict_proba(data)[0][1]

        elif selected_model == 'linear_svm':
            scaler = svm_scaler
            input_scaled = scaler.transform(data)
            predict = linear_svm_model.predict(input_scaled)
            selected_model = 'Linear SVM'
            probability = linear_svm_model.predict_proba(input_scaled)[0][1]

        elif selected_model == 'naive_bayes':
            scaler = nb_scaler
            input_scaled = scaler.transform(data)
            predict = naive_bayes_model.predict(input_scaled)
            selected_model = 'Naive Bayes'
            probability = naive_bayes_model.predict_proba(input_scaled)[0][1]

        if predict == 1:
            predict = "Churn"
            result = "High Churn Risk."
        else:
            predict = "Not Churn"
            result = "Low Churn Risk."

        probability = round(probability * 100, 2)

        return render(request, 'new_data.html', {'result' : result, 'predict': predict, 'selected_model': selected_model, 'probability' : probability})

    else:
        return render(request, 'new_data.html')

def existing_data(request):
    if request.method == 'POST':
        selected_model = request.POST['select_model']
        customer_id = request.POST['customer_id']
        
        customer_data = Customer.objects.get(id=customer_id)

        if customer_data.remaining_contract == 0:
            customer_data_contract = 0
        else:
            customer_data_contract = 1

        # data = [[float(customer_data.is_tv_subscriber), float(customer_data.is_movie_package_subscriber), float(customer_data.subscription_age), float(customer_data.bill_avg), float(customer_data.remaining_contract), float(customer_data.service_failure_count), float(customer_data.download_avg), float(customer_data.upload_avg), float(customer_data.download_over_limit)]]
        data = [[float(customer_data.is_tv_subscriber), float(customer_data.is_movie_package_subscriber), customer_data.subscription_age, customer_data.bill_avg, customer_data.remaining_contract, customer_data.service_failure_count, customer_data.download_avg, customer_data.upload_avg, customer_data.download_over_limit, float(customer_data_contract)]]

        if selected_model == 'logistic_regression':
            scaler = lr_scaler
            input_scaled = scaler.transform(data)
            predict = logistic_regression_model.predict(input_scaled)
            selected_model = 'Logistic Regression'
            probability = logistic_regression_model.predict_proba(input_scaled)[0][1]

        elif selected_model == 'decision_tree':
            scaler = dt_scaler
            input_scaled = scaler.transform(data)
            predict = decision_tree_model.predict(input_scaled)
            selected_model = 'Decision Tree'
            probability = decision_tree_model.predict_proba(input_scaled)[0][1]

        elif selected_model == 'random_forest':
            scaler = rf_scaler
            input_scaled = scaler.transform(data)
            predict = random_forest_model.predict(input_scaled)
            selected_model = 'Random Forest'
            probability = random_forest_model.predict_proba(input_scaled)[0][1]

        elif selected_model == 'adaboost':
            scaler = ada_scaler
            input_scaled = scaler.transform(data)
            predict = adaboost_model.predict(input_scaled)
            selected_model = 'AdaBoost'
            probability = adaboost_model.predict_proba(input_scaled)[0][1]

        elif selected_model == 'xgboost':
            scaler = xg_scaler
            input_scaled = scaler.transform(data)
            predict = xgboost_model.predict(input_scaled)
            selected_model = 'XGBoost'
            probability = xgboost_model.predict_proba(input_scaled)[0][1]

        elif selected_model == 'catboost':
            # scaler = cat_scaler
            # input_scaled = scaler.transform(data)
            predict = catboost_model.predict(data)
            selected_model = 'CatBoost'
            probability = catboost_model.predict_proba(data)[0][1]

        elif selected_model == 'linear_svm':
            scaler = svm_scaler
            input_scaled = scaler.transform(data)
            predict = linear_svm_model.predict(input_scaled)
            selected_model = 'Linear SVM'
            probability = linear_svm_model.predict_proba(input_scaled)[0][1]

        elif selected_model == 'naive_bayes':
            scaler = nb_scaler
            input_scaled = scaler.transform(data)
            predict = naive_bayes_model.predict(input_scaled)
            selected_model = 'Naive Bayes'
            probability = naive_bayes_model.predict_proba(input_scaled)[0][1]

        if predict == 1:
            predict = "Churn"
            result = "High Churn Risk."
        else:
            predict = "Not Churn"
            result = "Low Churn Risk."

        probability = round(probability * 100, 2)

        return render(request, 'existing_data.html', {'result' : result, 'predict': predict, 'selected_model': selected_model, 'probability' : probability, 'customer_data': customer_data})
    else:
        return render(request, 'existing_data.html')