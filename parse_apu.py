import csv
import re


def convNum(x):
    if len(x.split(".")) == 4 and x.startswith("0"):
        return x

    if len(x.split(".")) == 1:
        return int(x)

    pInt = x.split(".")[0]
    pDec = "0." + x.split(".")[1]

    if len(pInt.split(",")) == 3:
        y = (
            int(pInt.split(",")[0]) * 1000000
            + int(pInt.split(",")[1]) * 1000
            + int(pInt.split(",")[2])
            + float(pDec)
        )
    elif len(pInt.split(",")) == 2:
        y = int(pInt.split(",")[0]) * 1000 + int(pInt.split(",")[1]) + float(pDec)

    else:
        y = int(pInt.split(",")[0]) + float(pDec)

    return round(y, 6)


lines_to_avoid = [
    "S10 ",
    "CHAPIHUAL,",
    "Análisis de precios unitarios",
    "Presupuesto",
    "Subpresupuesto",
    "CENTRO POBLADO CHAPIHUAL",
    "LIBERTAD”",
]

titles = ["Materiales", "Mano de Obra", "Equipos"]

with open("example/raw/3.csv", encoding="utf-8", mode="r") as csv_raw:
    with open("example/parsed/3.csv", encoding="utf-8", mode="w") as csv_parsed:
        csv_reader = csv.reader(csv_raw, delimiter=";")
        for row in csv_reader:
            if not any(line in row[0] for line in lines_to_avoid):
                raw_line = row[0]
                raw_line = re.split(r"\s{2,}", raw_line)

                for index, raw_item in enumerate(raw_line):
                    if raw_item != "":
                        parsed_item = raw_item.strip()
                        if index == 0 and len(raw_line) == 1:
                            if parsed_item in titles:
                                csv_parsed.write(f";{parsed_item}\n")
                                break
                            if not (any(c.isalpha() for c in parsed_item)) and any(
                                c.isdigit() for c in parsed_item
                            ):
                                csv_parsed.write(f";;;;;;{parsed_item}\n")
                                break

                        if any(c.isalpha() for c in parsed_item):
                            csv_parsed.write(f"{parsed_item}")
                        elif any(c.isdigit() for c in parsed_item):
                            parsed_item = convNum(parsed_item)
                            csv_parsed.write(f"{parsed_item}")
                        else:
                            break
                        if index < len(raw_line) - 1:
                            csv_parsed.write(";")

                csv_parsed.write("\n")
