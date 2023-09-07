def parse(input_string: str) -> list:
    input_string = input_string[1:len(input_string)-1]                # Отбрасывает квадратные скобки, как нулевой и последний символ в вводимой строке 
    return list(map(int, input_string.split(",")))                    # Map применяет функцию int к каждому элементу генерируемого сплитом списка, а потом получившийся map_object превращается обратно в список

def find_irregularities(array: list) -> int | list | str:
    irregular_index = []
    for n in range(len(array)-1):
        if array[n+1] - array[n] != 1:                                # Если разность следующего члена массива и текущего члена массива не равна 1, то у функции встаёт вопросик
            irregular_index.append(array.index(array[n+1]))
    if len(irregular_index) == 1:                                     # Если после цикла в массиве всего 1 элемент
        return irregular_index[0]
    elif len(irregular_index) > 1:                                    # Если больше, чем 1
        return irregular_index
    else:                                                             # Если вообще нет элементов
        return "Не найдено"

print(find_irregularities(parse(input("Введите массив: \n"))))