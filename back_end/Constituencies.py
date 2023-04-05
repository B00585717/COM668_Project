import json

constituencies = {}
i = 1
value = 1

east_belfast = [3, 4, 5, 6, 16]
south_belfast = [2, 7, 8, 9, 10]
west_belfast = [11, 12, 13, 17]
north_belfast = [1, 14, 15, 37]
north_down = [18, 19, 20, 21, 23]
strangford = [22, 24]
lagan_valley = [25, 26, 27, 28]
crumlin = [29]
south_down = [30, 31, 33]
upper_bann = [32, 58, 63, 64, 65, 66, 67]
newry_and_armagh = [34, 35, 60, 61, 62]
south_antrim = [36, 39, ]
east_antrim = [38, 40]
north_antrim = [41, 42, 43, 44, 53, 54]
mid_ulster = [45, 46, 80]
east_londonderry = [47, 49, 51, 52, 55, 56, 57]
foyle = [48]
fermanagh_and_south_tyrone = [68, 69, 71, 74, 75, 76, 77, 92, 93, 94]
west_tyrone = [78, 79, 81, 82]

NUM_OF_POSTCODES = 94

while i <= NUM_OF_POSTCODES:
    match value:
        case 1:

            if i in east_belfast:
                constituencies.update({'BT' + str(i): 1})
                i += 1
                value = 1
            else:
                value = 2
        case 2:

            if i in south_belfast:
                constituencies.update({'BT' + str(i): 2})
                i += 1
                value = 1
            else:
                value = 3
        case 3:

            if i in west_belfast:
                constituencies.update({'BT' + str(i): 3})
                i += 1
                value = 1
            else:
                value = 4
        case 4:

            if i in north_belfast:
                constituencies.update({'BT' + str(i): 4})
                i += 1
                value = 1
            else:
                value = 5
        case 5:

            if i in north_down:
                constituencies.update({'BT' + str(i): 5})
                i += 1
                value = 1
            else:
                value = 6
        case 6:

            if i in strangford:
                constituencies.update({'BT' + str(i): 6})
                i += 1
                value = 1
            else:
                value = 7
        case 7:

            if i in lagan_valley:
                constituencies.update({'BT' + str(i): 7})
                i += 1
                value = 1
            else:
                value = 8
        case 8:

            if i in crumlin:
                constituencies.update({'BT' + str(i): 8})
                i += 1
                value = 1
            else:
                value = 9
        case 9:

            if i in south_down:
                constituencies.update({'BT' + str(i): 9})
                i += 1
                value = 1
            else:
                value = 10
        case 10:

            if i in upper_bann:
                constituencies.update({'BT' + str(i): 10})
                i += 1
                value = 1
            else:
                value = 11
        case 11:

            if i in newry_and_armagh:
                constituencies.update({'BT' + str(i): 11})
                i += 1
                value = 1
            else:
                value = 12
        case 12:

            if i in south_antrim:
                constituencies.update({'BT' + str(i): 12})
                i += 1
                value = 1
            else:
                value = 13
        case 13:

            if i in east_antrim:
                constituencies.update({'BT' + str(i): 13})
                i += 1
                value = 1
            else:
                value = 14
        case 14:

            if i in north_antrim:
                constituencies.update({'BT' + str(i): 14})
                i += 1
                value = 1
            else:
                value = 15
        case 15:

            if i in mid_ulster:
                constituencies.update({'BT' + str(i): 15})
                i += 1
                value = 1
            else:
                value = 16
        case 16:

            if i in east_londonderry:
                constituencies.update({'BT' + str(i): 16})
                i += 1
                value = 1
            else:
                value = 17
        case 17:

            if i in foyle:
                constituencies.update({'BT' + str(i): 17})
                i += 1
                value = 1
            else:
                value = 18
        case 18:

            if i in fermanagh_and_south_tyrone:
                constituencies.update({'BT' + str(i): 18})
                i += 1
                value = 1
            else:
                value = 19
        case 19:

            if i in west_tyrone:
                constituencies.update({'BT' + str(i): 19})
                i += 1
                value = 1
            else:
                value = 1
                i += 1


with open('constituencies.json', 'w') as f:
    json.dump(constituencies, f)


