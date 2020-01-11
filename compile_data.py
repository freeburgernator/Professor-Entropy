import json
import os

data_path = "C:\\Users\\freeb\\Documents\\GitHub\\Professor Entropy\\data"
filenames = os.listdir(data_path)

print(filenames[0])

all_classes = []

for filename in filenames:
    f = open(data_path + "\\" + filename, 'r')
    print("Adding " + filename)
    out = f.read()
    f.close()

    encoded = json.loads(out)
    all_classes = all_classes + encoded
    #all_classes.append(json.loads(f.read())

    print("Complete")

all_classes

with open('C:\\Users\\freeb\\Documents\\GitHub\\Professor Entropy' + '\\' + 'database.json', 'w', encoding='utf-8') as f:
    json.dump(all_classes, f, ensure_ascii=False, indent=4)

print("Process Complete")
