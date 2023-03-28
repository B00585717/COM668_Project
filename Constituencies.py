import json

constituencies = {}
i = 1
value = 1

while i < 100:
    match value:
        case 1:
            key = i
            if key < 10:
                constituencies.update({'BT' + str(key): value})
                i += 1
            else:
                value = 2
        case 2:
            key = i
            if key < 20:
                constituencies.update({'BT' + str(key): value})
                i += 1
            else:
                value = 3
        case 3:
            key = i
            if key < 30:
                constituencies.update({'BT' + str(key): value})
                i += 1
            else:
                value = 4
        case 4:
            key = i
            if key < 40:
                constituencies.update({'BT' + str(key): value})
                i += 1
            else:
                value = 5
        case 5:
            key = i
            if key < 50:
                constituencies.update({'BT' + str(key): value})
                i += 1
            else:
                value = 6
        case 6:
            key = i
            if key < 60:
                constituencies.update({'BT' + str(key): value})
                i += 1
            else:
                value = 7
        case 7:
            key = i
            if key < 70:
                constituencies.update({'BT' + str(key): value})
                i += 1
            else:
                value = 8
        case 8:
            key = i
            if key < 80:
                constituencies.update({'BT' + str(key): value})
                i += 1
            else:
                value = 9
        case 9:
            key = i
            if key < 90:
                constituencies.update({'BT' + str(key): value})
                i += 1
            else:
                value = 10
        case 10:
            key = i
            if key <= 100:
                constituencies.update({'BT' + str(key): value})
                i += 1


with open('constituencies.json', 'w') as f:
    json.dump(constituencies, f)


