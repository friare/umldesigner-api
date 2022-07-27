AGREGATION_LIST = []
with open('./src/aggregation_keyword.txt') as file:
    for word in file:
        AGREGATION_LIST.append(word.strip())

print(AGREGATION_LIST)