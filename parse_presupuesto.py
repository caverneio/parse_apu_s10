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
    "Presupuesto",
    "DISTRITO",
    "Cliente",
    "Lugar",
    "Item"
]


with open("example/raw_presupuesto.csv", encoding="utf-8", mode="r") as csv_raw:
    with open("example/parsed_presupuesto.csv", encoding="utf-8", mode="w") as csv_parsed:
        csv_reader = csv.reader(csv_raw, delimiter="|")
        csv_reader = list(csv_reader)
        for idx, row in enumerate(csv_reader):
            if not any(line in row[0] for line in lines_to_avoid) and row[0] != "":
                raw_line = row[0]
                raw_line = re.split(r"\s{2,}", raw_line)

                # if len(raw_line) == 1 pass # skip this line
                if len(raw_line) == 1:
                    continue


                # next line
                raw_next_line = csv_reader[(idx + 1)%len(csv_reader)][0]
                raw_next_line = re.split(r"\s{2,}", raw_next_line)

                if len(raw_line) == 3:
                    description = raw_line[1]
                    if len(raw_next_line) == 1:
                        description += " " + raw_next_line[0]

                    csv_parsed.write(
                        f"{raw_line[0]};{description};;;;{convNum(raw_line[2])}"
                    )

                elif len(raw_line) == 6:
                    description = raw_line[1]
                    if len(raw_next_line) == 1:
                        description += " " + raw_next_line[0]

                    csv_parsed.write(
                        f"{raw_line[0]};{description};{raw_line[2]};{convNum(raw_line[3])};{convNum(raw_line[4])};{convNum(raw_line[5])}"
                    )

                else:
                    for index,parsed_item in enumerate(raw_line):
                        if any(c.isalpha() for c in parsed_item):
                            csv_parsed.write(f"{parsed_item}")
                        elif any(c.isdigit() for c in parsed_item):
                            parsed_item = convNum(parsed_item)
                            csv_parsed.write(f"{parsed_item}")
                        if index != 5:
                            csv_parsed.write(";")
               
                csv_parsed.write("\n")
