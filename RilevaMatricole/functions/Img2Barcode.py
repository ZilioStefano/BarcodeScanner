from dbr import *
import pandas as pd
from datetime import datetime
import json
# import re
import easyocr


def text_method(url, n_refuso):
    # Create an OCR reader object

    try:
        reader = easyocr.Reader(['en'])

        # Read text from an image
        result = reader.readtext(url)
        results = ""
        # Print the extracted text
        for detection in result:
            results = results + detection[1] + " - "

    except Exception as err:
        n_refuso += 1
        results = "Refuso "+str(n_refuso)
        print(err)

    return results, n_refuso


def barcode_method(image_path, n_refuso):

    risultato = []

    with open('casi/template-9.json', 'r') as file:
        data = json.load(file)

    data = json.dumps(data)

    try:
        error = BarcodeReader.init_license("t0070lQAAABtOhnVvDDFF78/0h+2FTcCgMpDA/rF6QSHbDxbAwVohB9CmAx4siyPd2bJpkfES0+"
                                           "jq1/v5YDKBO0uFDBJ+7lMg5w==;t0068lQAAACZgEYS0FcygP1AjMDCAtzfP1zHCZEMbQ25OqVl"
                                           "4PkT1ptmKcHjcqXd4bfzGgd7RWWoB8oXr4IE5I+QLuZfgdIY=")

        if error[0] != EnumErrorCode.DBR_OK:
            print(error[1])
        dbr = BarcodeReader()
        dbr.init_runtime_settings_with_string(data)

        try:

            # prova con il metodo principale
            results = dbr.decode_file(image_path)

            if results is not None:  # and results.barcode_text.isdigit == True:
                for text_result in results:

                    if text_result.barcode_text.isnumeric():

                        print("Barcode Format : " + text_result.barcode_format_string)
                        print("Barcode Text : " + text_result.barcode_text)
                        risultato = text_result.barcode_text

                    else:
                        n_refuso += 1
                        risultato = "Refuso " + str(n_refuso)

            else:
                n_refuso += 1
                risultato = "Refuso " + str(n_refuso)

            # 6.Release resource
            dbr.recycle_instance()

        except Exception as err:
            n_refuso += 1
            risultato = "Refuso " + str(n_refuso)
            # trovate.append("Refuso "+index_refuso)
            print(err)

    except Exception as err:
        n_refuso += 1
        risultato = "Refuso " + str(n_refuso)
        print(err)

    return risultato, n_refuso


def scan(method, folder_path, files):

    i = 0

    n_refuso = 0

    df = pd.DataFrame()
    refusi = []

    for file in files:
        i = i + 1
        print("Barcode " + str(i))
        image_path = os.path.join(folder_path, file)

        if method[0] == "barcode":

            print("---------BARCODE method---------")

            results, n_refuso = barcode_method(image_path, n_refuso)

            if results[0:6] == "Refuso":
                refusi.append(file)

        elif method[0] == "testo":
            print("---------TEXT method---------")
            results, n_refuso = text_method(image_path, n_refuso)

        else:
            print("---------MIXED method---------")
            results, n_refuso = barcode_method(image_path, n_refuso)

            if results[0:6] == "Refuso":
                results, n_refuso = text_method(image_path, n_refuso)

        dict_df = {"Trovate": results, "File list": file}
        df = pd.concat([df, pd.DataFrame(dict_df, index=[0])])

    Now = datetime.now()
    file_name = "static/results/"+Now.strftime("%Y%m%d_%H%M%S")+".xlsx"
    df.to_excel(file_name, index=False)

    dict_refusi = {"Refusi": refusi}
    df_refusi = pd.DataFrame(dict_refusi)
    # file_name_refusi = "Refusi_"+Now.strftime("%Y%m%d_%H%M%S")+".xlsx"
    # df_refusi.to_excel(file_name_refusi, index=False)

    with pd.ExcelWriter(file_name) as writer:

        # use to_excel function and specify the sheet_name and index
        # to store the dataframe in specified sheet
        df.to_excel(writer, sheet_name="Rilievo", index=False)
        df_refusi.to_excel(writer, sheet_name="Refusi", index=False)

    return file_name
