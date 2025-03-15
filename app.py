from flask import Flask, render_template, request
from datetime import datetime, timedelta

app = Flask(__name__)

def calcular_multa(num_linhas, valor_por_linha, inicio, fim, cancelamento):
    # Converter datas
    data_inicio = datetime.strptime(inicio, "%Y-%m-%d")
    data_fim = datetime.strptime(fim, "%Y-%m-%d")
    data_cancelamento = datetime.strptime(cancelamento, "%Y-%m-%d")
    
    # Valor diário da linha
    valor_diario = valor_por_linha / 30  # Considerando cada mês com 30 dias fixos
    
    # Calcular os dias restantes no mês do cancelamento
    ultimo_dia_mes_cancelamento = 30
    dias_restantes_cancelamento = ultimo_dia_mes_cancelamento - data_cancelamento.day
    
    # Calcular os dias restantes no último mês do contrato
    dias_restantes_final = data_fim.day  # Considera os dias do mês final
    
    # Calcular a quantidade de meses completos restantes no contrato
    meses_restantes = ((data_fim.year - data_cancelamento.year) * 12 + (data_fim.month - data_cancelamento.month)) - 1
    if meses_restantes < 0:
        meses_restantes = 0
    
    # Calcular o valor da multa para os dias restantes
    valor_multa_dias = (dias_restantes_cancelamento + dias_restantes_final) * valor_diario * num_linhas * 0.30
    
    # Calcular o valor da multa para os meses completos restantes
    valor_multa_meses = meses_restantes * valor_por_linha * num_linhas * 0.30
    
    # Valor total da multa
    multa_total = round(valor_multa_dias + valor_multa_meses, 2)
    
    return {
        "dias_restantes_cancelamento": dias_restantes_cancelamento,
        "dias_restantes_final": dias_restantes_final,
        "meses_restantes": meses_restantes,
        "valor_multa_dias": round(valor_multa_dias, 2),
        "valor_multa_meses": round(valor_multa_meses, 2),
        "multa": multa_total,
        "data_cancelamento": cancelamento
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    if request.method == 'POST':
        try:
            num_linhas = int(request.form['num_linhas'])
            valor_por_linha = float(request.form['valor_por_linha'])
            inicio = request.form['inicio']
            fim = request.form['fim']
            cancelamento = request.form['cancelamento']
            resultado = calcular_multa(num_linhas, valor_por_linha, inicio, fim, cancelamento)
        except ValueError:
            resultado = {"error": "Por favor, insira valores válidos."}
    return render_template('index.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)