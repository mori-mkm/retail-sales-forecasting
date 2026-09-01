
def parameters():
    from itertools import product
    print("Definindo parametros")
    # setting initial values and some bounds for them
    ps = range(2, 6)
    d=1 
    qs = range(2, 6)
    Ps = range(0, 2)
    D=1 
    Qs = range(0, 2)
    s = 12 # season length is still 12

    parameters = product(ps, qs, Ps, Qs)
    parameters_list = list(parameters)
    
    return parameters_list;

def optimizeSARIMA(series,parameters_list, d, D, s):
    import statsmodels.api as sm
    import pandas as pd
    from tqdm import tqdm_notebook 

    results = []
    best_aic = float("inf")

    for param in tqdm_notebook(parameters_list):
        # we need try-except because on some combinations model fails to converge
        try:
            model=sm.tsa.statespace.SARIMAX(series, order=(param[0], d, param[1]), 
                                            seasonal_order=(param[2], D, param[3], s)).fit(disp=-1)
        except:
            continue
        aic = model.aic
        # saving best model, AIC and parameters
        if aic < best_aic:
            best_model = model
            best_aic = aic
            best_param = param
        results.append([param, model.aic])

    result_table = pd.DataFrame(results)
    result_table.columns = ['parameters', 'aic']
    # sorting in ascending order, the lower AIC is - the better
    result_table = result_table.sort_values(by='aic', ascending=True).reset_index(drop=True)
    
    return result_table;


def sarima_(val_orig, model, n_steps,d):
    import pandas as pd
    import numpy as np

    val_orig['arima_model'] = model.fittedvalues
    # making a shift on s+d steps, because these values were unobserved by the model
    # due to the differentiating
    val_orig['arima_model'][:n_steps+d] = np.NaN
    
    # forecasting on n_steps forward 
    forecast = model.predict(start = val_orig.shape[0], end = val_orig.shape[0]+n_steps)
    forecast = val_orig.arima_model.append(forecast)

    return forecast;

def forecast(treino_loja):
    import statsmodels.api as sm
    import pandas as pd
    from tqdm import tqdm_notebook 

    import warnings
    print("Realizando a predição")
    warnings.filterwarnings("ignore")
    d = 1
    D = 1
    s = 12
    parameters_list = parameters()

    result_table = optimizeSARIMA(treino_loja, parameters_list, d, D, s)

    # set the parameters that give the lowest AIC
    p, q, P, Q = result_table.parameters[0]

    best_model=sm.tsa.statespace.SARIMAX(treino_loja, order=(p, d, q), 
                                        seasonal_order=(P, D, Q, s)).fit(disp=-1)
    
    val_orig = pd.DataFrame()
    val_orig['atual'] = treino_loja

    forecast = sarima_(val_orig, best_model, 12,d)

    print("Os parametros utilizados foram p: {}, q: {}, P: {}, Q: {}.". format(p, q, P, Q))
    return forecast; 
    