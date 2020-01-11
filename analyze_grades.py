import json

# Known TODOS
# Consolidate / eliminate duplicate values, ie, aggregate statisics

def get_headcount(teacher_class):
    return sum(teacher_class[6:])

def find_GPA_in_class(teacher_class, percentile):

    headcount = get_headcount(teacher_class)

    # get the rank. The rank ranges from 0 to class size - 1
    rank = round((headcount-1)-((headcount-1)*percentile/100), 0)

    grades = teacher_class[6:]
    # Determine what letter grade, as indicated by index, the student recieved

    index = 0
    count = -1
    length = len(teacher_class)
    while index < length and count < rank:
        count = count + grades[index]
        index = index + 1

    # Translate the index into a GPA
    gpa = 12 - (index-1)
    # account for the fact that there's no F+
    if gpa == 1:
        gpa = 0

    gpa = gpa / 3
    return gpa

def load_grades():

    # Load the json database into a data 2-D list
    f = open("database.json" , "r")
    data = json.loads(f.read())
    data = tuple(map(tuple,data))
    f.close()

    # Create the first layer of inforamtion
    database = dict()
    for line in data:
        if not line[0] in database.keys():
            database[line[0]] = dict()

    # Create the second layer of classes
    for line in data:
        if not line[4] in database[line[0]].keys():
            database[line[0]][line[4]] = dict()

    # Create the third layer of professors
    for line in data:
        if not line[2] in database[line[0]][line[4]].keys():
            database[line[0]][line[4]][line[1]] = line

    # print(database["Aggregate"]["TRANSPORT PHENOMENA"]['MULLINS, CHARLES B'])

    return database

def find_all_professor_varients(database, semester, class_name, minimum_headcount):
    professor_names = []

    professors = database[semester][class_name]
    for professor in professors.keys():
        if get_headcount(professors[professor]) >= minimum_headcount:
            professor_names.append(professor)

    return professor_names

def recusive_permutations(GPA_hist, GPA_list, index, value):
    if index >= len(GPA_list):
        average_GPA = round(round(value / index*2,1)/2,2)
        GPA_hist[average_GPA] = GPA_hist[average_GPA] + 1
    else:
        for grade in GPA_list[index]:
            recusive_permutations(GPA_hist, GPA_list, index+1, value + grade)

    return

def create_GPA_histogram(GPA_list):
    GPA_bin = 0
    GPA_hist = {0:0}
    while GPA_bin < 4.0:
        GPA_bin = round(GPA_bin + 0.05,2)
        GPA_hist[GPA_bin] = 0

    # print(GPA_hist)

    recusive_permutations(GPA_hist, GPA_list, 0, 0)
    # print(GPA_hist)

    unpacked_hist = []
    for key in GPA_hist.keys():
        unpacked_hist.append((key,GPA_hist[key]))

    # print(unpacked_hist)
    return unpacked_hist


def quick_results(GPA_hist):
    max = 0
    for item in GPA_hist:
        if item[1] > max:
            max = item[1]


    for item in GPA_hist:
        bars = " "
        number_bars = int(round(item[1]/max*80,0))
        for i in  range(0,number_bars):
            bars = bars + "|"
        print(str(item[0]) + " : " + bars)

def order_histogram(database, schedule, semester, minimum_headcount, percentile):
    GPA_list = []

    for class_name in schedule:
        GPAs = []
        professor_names = find_all_professor_varients(database,semester,class_name,minimum_headcount)
        for professor_name in professor_names:
            professor_class = database[semester][class_name][professor_name]
            GPAs.append(find_GPA_in_class(professor_class,percentile))

        GPA_list.append(GPAs)

    permutations = 1
    for GPAs in GPA_list:
        permutations = permutations * len(GPAs)

    print('Running ' + str(permutations) + ' permutations')

    #print(GPA_list)
    return create_GPA_histogram(GPA_list)


def main():

    database = load_grades()
    # print(database["Aggregate"]["TRANSPORT PHENOMENA"]['MULLINS, CHARLES B'])
    # print(find_GPA_in_class(database["Aggregate"]["TRANSPORT PHENOMENA"]['MULLINS, CHARLES B'], 70))
    # print(find_all_professor_varients(database,"Aggregate","TRANSPORT PHENOMENA",100))

    # get the class schedule

    # sample_list = [[0.3,0.4,3.5],[2.4,3.7,2.8],[1.6,2.5,3.9],[0.3,0.4,3.5],[2.4,3.7,2.8],[1.6,2.5,3.9]]
    # quick_results(create_GPA_histogram(sample_list))

    file = open('MechE_degreePlan.txt')

    schedule = []
    for line in file:
        schedule.append(line.strip('\n'))

    file.close()

    # for each class, find all professor find all possible professors
    semester = "Aggregate"
    minimum_headcount = 100
    minimum_percentile = 0
    maximum_percentile = 100
    interval = 5

    percentiles = []
    for i in range(minimum_percentile,maximum_percentile+interval,interval):
        percentiles.append(i)

    histograms = []

    for percentile in percentiles:
        print("Calculating percentile " + str(percentile))
        histograms.append( (percentile, order_histogram(database, schedule, semester, minimum_headcount,percentile) ) )

    for hist in histograms:
        print("----------------------------------------------")
        quick_results(hist[1])

    file = open("analysis_results.json","w")
    file.write(json.dumps(histograms))
    file.close()


    #print(GPA_list)

    # print("The selected number of permutations is: " + str(combinations))




    # print(combinations)

    # print(schedule)



main()
