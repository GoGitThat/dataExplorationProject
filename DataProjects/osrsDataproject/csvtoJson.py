import csv
import json
if __name__ == "__main__":
    outer = []
    inDict = {}
    data = []
    labels = []
    count=0
    with open('path_to_csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            t = {}
            if count==0:
                labels = row
            if count>0:
                if('date' in labels[0]):
                    t['date'] = row[0]
                else:
                    t[labels[0]] = row[0]
                t[labels[1]] = int(row[1])
                t[labels[2]] = float(row[2])
                data.append(t)
            count+=1
    with open('path_to_json', 'w') as f:
        json.dump(data, f)
