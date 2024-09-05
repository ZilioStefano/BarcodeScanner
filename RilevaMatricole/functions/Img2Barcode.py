from dbr import *
import pandas as pd


def scanPhoto():
    folder_path = r"media\RilevaMatricole_Images"
    files = os.listdir(folder_path)

    trovate = []
    file_list = []

    index_refuso = 0
    i = 0
    for file in files:

        try:
            # 1.Initialize license.
            # The string "DLS2eyJvcmdhbml6YXRpb25JRCI6IjIwMDAwMSJ9" here is a free public trial license. Note that network connection is required for this license to work.
            # You can also request a 30-day trial license in the customer portal: https://www.dynamsoft.com/customer/license/trialLicense?architecture=dcv&product=dbr&utm_source=samples&package=python
            error = BarcodeReader.init_license("t0070lQAAABtOhnVvDDFF78/0h+2FTcCgMpDA/rF6QSHbDxbAwVohB9CmAx4siyPd2bJpkfES0+jq1/v5YDKBO0uFDBJ+7lMg5w==;t0068lQAAACZgEYS0FcygP1AjMDCAtzfP1zHCZEMbQ25OqVl4PkT1ptmKcHjcqXd4bfzGgd7RWWoB8oXr4IE5I+QLuZfgdIY=")
            if error[0] != EnumErrorCode.DBR_OK:
                print("License error: " + error[1])

            # 2.Create an instance of Barcode Reader.
            reader = BarcodeReader.get_instance()
            if reader == None:
                raise BarcodeReaderError("Get instance failed")
            # There are two ways to configure runtime parameters. One is through PublicRuntimeSettings, the other is through parameters template.
            # 3. General settings (including barcode format, barcode count and scan region) through PublicRuntimeSettings
            # 3.1 Obtain current runtime settings of instance.
            settings = reader.get_runtime_settings()

            # 3.2 Set the expected barcode format you want to read.
            # The barcode format our library will search for is composed of BarcodeFormat group 1 and BarcodeFormat group 2.
            # So you need to specify the barcode format in group 1 and group 2 individually.
            settings.barcode_format_ids = EnumBarcodeFormat.BF_ALL
            settings.barcode_format_ids_2 = EnumBarcodeFormat_2.BF2_POSTALCODE | EnumBarcodeFormat_2.BF2_DOTCODE

            # 3.3 Set the expected barcode count you want to read.
            settings.expected_barcodes_count = 10
            # 3.4 Set the ROI(region of interest) to speed up the barcode reading process.
            # Note: DBR supports setting coordinates by pixels or percentages. The origin of the coordinate system is the upper left corner point.
            settings.region_measured_by_percentage = 1
            settings.region_left = 0
            settings.region_right = 100
            settings.region_top = 0
            settings.region_bottom = 100

            # 3.5 Apply the new settings to the instance
            reader.update_runtime_settings(settings)

            # 3. General settings (including barcode format, barcode count and scan region) through parameters template.
            # reader.init_runtime_settings_with_string("{\"ImageParameter\":{\"BarcodeFormatIds\":[\"BF_ONED\",\"BF_PDF417\",\"BF_QR_CODE\",\"BF_DATAMATRIX\"],\"BarcodeFormatIds_2\":null,\"ExpectedBarcodesCount\":10,\"Name\":\"sts\",\"RegionDefinitionNameArray\":[\"region0\"]},\"RegionDefinition\":{\"Bottom\":100,\"Left\":0,\"MeasuredByPercentage\":1,\"Name\":\"region0\",\"Right\":100,\"Top\":0}}")

            # Replace by your own image path
            try:

                image_path = os.path.join(folder_path, file)

                # 4.Decode barcodes from an image file.
                results = reader.decode_file(image_path)

                # 5.Output the barcode text.
                if results != None:
                    for text_result in results:
                        file_list.append(file)
                        print("Barcode " + str(i))
                        print("Barcode Format : " + text_result.barcode_format_string)
                        print("Barcode Text : " + text_result.barcode_text)

                        trovate.append(text_result.barcode_text)
                        i = i + 1
                else:
                    index_refuso = index_refuso + 1
                    trovate.append("Refuso "+str(index_refuso))
                    file_list.append(file)
                    print("No data detected.")

                # 6.Release resource
                reader.recycle_instance()

            except Exception as err:
                index_refuso = index_refuso + 1
                # trovate.append("Refuso "+index_refuso)
                print("Barcode " + str(i))
                i = i + 1
        except BarcodeReaderError as bre:
            print(bre)

    print(trovate)
    dict_df = {"Trovate": trovate, "File list": file_list}
    df = pd.DataFrame(dict_df)
    df.to_excel("Lista scansioni.xlsx", index=False)