import pandas as pd
import requests

newIDs = [24, 25, 5, 6, 27, 23, 26, 7, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 8, 9, 10, 1, 3, 2, 4]



def cleanup(data: str):
    start = data.find("<pre>") + 5
    end = data.find("</pre>")
    data = data[start:end]
    data = data.replace(" ", "")
    data = data.replace("\\n", "\n")
    return data


def downloadData(ID):
    for id in ID:
        url = f"https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={newIDs[id - 1]}&year1=1981&year2=2020&type=Mean"
        filename = f"{id}"
        with requests.get(url, headers={"Accept": "text/plain"}) as plain:
            data = str(plain.content)
            data = cleanup(data)
        with open(f"Data/{filename}.csv", "w+") as output:
            output.write(f"Year,Week,SMN,SMT,VCI,TCI,VHI\n")
            output.write(data)


def createFrame(ID):
    tempframes = []
    for id in ID:
        try:
            with open(f'Data/{id}.csv') as f:
                pass
        except IOError:
            downloadData([id])
        temp = pd.read_csv(f"Data/{id}.csv", header=0, index_col=False)
        temp["Province"] = id
        tempframes.append(temp)

    df = pd.concat(tempframes)
    df = (df.where(df["VHI"] != -1)
          .dropna())
    return df