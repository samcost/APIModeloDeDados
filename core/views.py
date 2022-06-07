from django.shortcuts import HttpResponse, Http404
import json
import pickle
import pandas as pd
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def API(request):

    if request.method == 'POST':
        try:
            body = request.body
            data = json.loads(body)

        except:
            raise Http404

        flag_cliente = data["flag_cliente"]
        del data["flag_cliente"]
        entradas = list(data.values())

        if flag_cliente:
            resposta = Clientes(entradas)

        else:
            resposta = NaoClientes(entradas)


        return HttpResponse(resposta)


def Clientes(array):

    modelo = pickle.load(open("dataset/seu_modelo.sav", 'rb'))
    pred = modelo.predict_proba([array])
    base_aplicacao = pd.DataFrame()
    base_aplicacao['prob'] = pred[:, 1]
    base_aplicacao['predito'] = 0
    base_aplicacao.loc[base_aplicacao.prob > 0.145, 'predito'] = 1

    corte1 = base_aplicacao[base_aplicacao.prob != 0]

    corte1.loc[(corte1['prob'] <= 1), 'faixa'] = '11'

    corte1.loc[(corte1['prob'] <= 0.3724508051418680), 'faixa'] = '10'

    corte1.loc[(corte1['prob'] <= 0.2235814987054040), 'faixa'] = '09'

    corte1.loc[(corte1['prob'] <= 0.1552882070556910), 'faixa'] = '08'

    corte1.loc[(corte1['prob'] <= 0.1236852619710550), 'faixa'] = '07'

    corte1.loc[(corte1['prob'] <= 0.0936522052286165), 'faixa'] = '06'

    corte1.loc[(corte1['prob'] <= 0.0672774704523527), 'faixa'] = '05'

    corte1.loc[(corte1['prob'] <= 0.0524730922594822), 'faixa'] = '04'

    corte1.loc[(corte1['prob'] <= 0.0447250377385042), 'faixa'] = '03'

    corte1.loc[(corte1['prob'] <= 0.0346986943543589), 'faixa'] = '02'

    corte1.loc[(corte1['prob'] <= 0.0199364873519738), 'faixa'] = '01'

    base_aplicacao = pd.concat([corte1])

    result = base_aplicacao[['prob', 'faixa']].copy()

    result = result.to_json(orient="records")
    parsed = json.loads(result)

    return HttpResponse(json.dumps(parsed, indent=4))


def NaoClientes(array):

    modelo = pickle.load(open("dataset/seu_modelo.sav", 'rb'))
    pred = modelo.predict_proba([array])
    base_aplicacao = pd.DataFrame()
    base_aplicacao['prob'] = pred[:, 1]

    base_aplicacao['predito'] = 0

    base_aplicacao.loc[base_aplicacao.prob > 0.151, 'predito'] = 1
    corte1 = base_aplicacao[base_aplicacao.prob != 0]

    corte1.loc[(corte1['prob'] <= 1), 'faixa'] = '10'

    corte1.loc[(corte1['prob'] <= 0.25463242), 'faixa'] = '09'

    corte1.loc[(corte1['prob'] <= 0.19554574), 'faixa'] = '08'

    corte1.loc[(corte1['prob'] <= 0.17829637), 'faixa'] = '07'

    corte1.loc[(corte1['prob'] <= 0.14547009), 'faixa'] = '06'

    corte1.loc[(corte1['prob'] <= 0.10539036), 'faixa'] = '05'

    corte1.loc[(corte1['prob'] <= 0.08947052), 'faixa'] = '04'

    corte1.loc[(corte1['prob'] <= 0.07821098), 'faixa'] = '03'

    corte1.loc[(corte1['prob'] <= 0.07074768), 'faixa'] = '02'

    corte1.loc[(corte1['prob'] <= 0.05496898), 'faixa'] = '01'

    base_aplicacao = pd.concat([corte1])

    result = base_aplicacao[['prob', 'faixa']].copy()

    result = result.to_json(orient="records")
    parsed = json.loads(result)

    return HttpResponse(json.dumps(parsed, indent=4))
