import json
import csv

file = open("analysis_results.json",'r')
data = json.loads(file.read())
file.close()

# print(data)

database = []

percentile_headers = ['GPA']

for percentile_row in data:
    percentile_headers.append(percentile_row[0])


gpa_column_left = []
for gpa_bin in data[0][1]:
    gpa_column_left.append([gpa_bin[0]])

for percentile_row in data:
    index = 0
    for gpa_bin in percentile_row[1]:
        gpa_column_left[index].append(gpa_bin[1])
        index = index + 1

database = gpa_column_left

with open('data_analysis_output.csv', mode='w', newline='') as output_file:
    writer = csv.writer(output_file, dialect='excel')

    writer.writerow(percentile_headers)
    for line in database:
        writer.writerow(line)

    output_file.close()
