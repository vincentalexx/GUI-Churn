from django.shortcuts import render, HttpResponse
from joblib import load

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

        if selected_model == 'logistic_regression':
            selected_model = 'Logistic Regression'
        elif selected_model == 'decision_tree':
            selected_model = 'Decision Tree'
        elif selected_model == 'random_forest':
            selected_model = 'Random Forest'
        elif selected_model == 'adaboost':
            selected_model = 'AdaBoost'
        elif selected_model == 'xgboost':
            selected_model = 'XGBoost'
        elif selected_model == 'catboost':
            selected_model = 'CatBoost'
        elif selected_model == 'linear_svm':
            selected_model = 'Linear SVM'
        elif selected_model == 'naive_bayes':
            selected_model = 'Naive Bayes'

        return render(request, 'existing_data.html', {'selected_model': selected_model, 'customer_id': customer_id})
    else:
        return render(request, 'existing_data.html')