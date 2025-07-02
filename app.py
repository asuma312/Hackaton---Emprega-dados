import uuid

from flask import Flask, jsonify, Blueprint, request, current_app
from flask_cors import CORS
import pandas as pd
import os
import re
from sheets import GoogleSheetsSDK
from config import sheet_id, sharepoint_url, sharepoint_file

from cloudscraper import create_scraper
from sheets_cleaner import SheetsCleaner
from base64 import b64decode
from uuid import uuid4

import requests

app = Flask(__name__)
CORS(app)


def get_excel()->str:
    session = create_scraper()
    response = session.get(sharepoint_url)
    with open(sharepoint_file, 'wb') as f:
        f.write(response.content)
    return sharepoint_file

def clean_data(row):
    row['Valor parcela'] = float(row['Valor parcela'].split(" ")[-1].replace(".", "").replace(",", "."))
    only_numbers_pattern = r'[^0-9.]'
    row['WhatsApp'] = re.sub(only_numbers_pattern, '', str(row['WhatsApp']))
    return row

@app.route('/hackaton/get_excel')
def get_excel_route():
    sharepoint_file = get_excel()
    df = pd.read_excel(sharepoint_file)
    df = df.apply(clean_data, axis=1)
    os.remove(sharepoint_file)
    return jsonify({'data':df.to_json(orient='records')})


@app.route('/hackaton/get_sheets')
def get_sheets():
    receita_name = f"{uuid4().hex}.csv"
    despesas_name = f"{uuid4().hex}.csv"
    plr_name = f"{uuid4().hex}.csv"


    sheet_obj = GoogleSheetsSDK()
    sheets_cleaner_obj = SheetsCleaner()
    receita_sheet = sheet_obj.baixar_sheet(
        sheet_id,
        'Receita',
        receita_name
    )

    df_receita = sheets_cleaner_obj.clean_receita_csv(receita_sheet)

    despesas_sheet = sheet_obj.baixar_sheet(
        sheet_id,
        'Despesas',
        despesas_name,
        skiprows=1
    )

    df_despesas = sheets_cleaner_obj.clean_despesas_csv(despesas_sheet)
    alfabeto = [chr(i) for i in range(ord('a'), ord('u') + 1)]

    PLR_sheet = sheet_obj.baixar_sheet(
        sheet_id,
        'PLR',
        plr_name,
        hard_coded_columns=alfabeto
    )

    df_plr, df_metas = sheets_cleaner_obj.clean_plr_csv(PLR_sheet)

    if os.path.exists('metas_historico.csv'):
        df_metas_historico = pd.read_csv('metas_historico.csv')
        df_metas = pd.concat([df_metas, df_metas_historico], ignore_index=True)
    else:
        df_metas_historico = pd.DataFrame(columns=["meta", "data_1", "data_2"])




    os.remove(receita_name)
    os.remove(despesas_name)
    os.remove(plr_name)

    return jsonify({
        'receita':df_receita.to_json(orient='records'),
        'despesa': df_despesas.to_json(orient='records'),
        'plr':df_plr.to_json(orient='records'),
        'metas':df_metas.to_json(orient='records'),
        'metas_historico': df_metas_historico.to_json(orient='records')
    }), 200

@app.route("/hackaton/read_screenshot", methods=['POST'])
def read_screenshot():
    ocr_apikey = 'TODO'
    data = request.get_json()
    base64img = data.get("screenshot")
    endpoint = 'https://api.ocr.space/parse/image'
    payload = {
        "apikey": ocr_apikey,
        'base64Image': base64img,
        'filetype': 'PNG',
        'OCREngine':2
    }

    response = requests.post(endpoint, data=payload)
    print(f"Response: {response.status_code}, {response.text}")
    data = response.json()
    text = data['ParsedResults'][0]['ParsedText'].split("\n")

    is_next_meta = False
    value_meta = None

    is_next_data = False
    is_next_data_2 = False
    data_1 = None
    data_2 = None

    for line in text:
        if is_next_meta:
            value_meta = line
            is_next_meta = False
        elif is_next_data:
            data_1 = line.split(" ")[0]
            is_next_data = False
            is_next_data_2 = True
        elif is_next_data_2:
            data_2 = line.split(" ")[0]
            is_next_data_2 = False

        if line == 'Insira a meta da campanha aqui':
            is_next_meta = True
        elif line == "Período em dias":
            is_next_data = True
    if not value_meta:
        return jsonify(success=False, message="Meta not found in screenshot"), 400
    if not data_1 or not data_2:
        return jsonify(success=False, message="Data not found in screenshot"), 400
    _dict = {
        "meta": value_meta,
        "data_inicio": data_1,
        "data_fim": data_2
    }
    csv_name = 'metas_historico.csv'
    if os.path.exists(csv_name):
        df = pd.read_csv(csv_name)
    else:
        df = pd.DataFrame(columns=["meta", "data_inicio", "data_fim"])
    #verifica se ja tem data_inicio e data fim inputadas agora no csv, se tiver só substitui ao inves de adicionar
    if not df.empty:
        existing_row = df[(df['data_inicio'] == _dict['data_inicio']) & (df['data_fim'] == _dict['data_fim'])]
        if not existing_row.empty:
            df.loc[existing_row.index, 'meta'] = _dict['meta']
            df.to_csv(csv_name, index=False)
            print(f"Updated existing data: {_dict}")
            return jsonify(success=True, message="Meta updated successfully"), 200

    df = df.append(_dict, ignore_index=True)
    df.to_csv(csv_name, index=False)
    print(f"Parsed data: {_dict}")
    return jsonify(success=True, message="Screenshot saved as temp.png"), 200


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)