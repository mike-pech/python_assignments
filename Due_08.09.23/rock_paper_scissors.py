options = ["камень", "ножницы", "бумага"]
results = ["ничья", "игрок 2 выиграл", "игрок 1 выиграл"]

player_1, player_2 = input("Ввод: \n").split()
                                                            # Очень элегантное решение использующее индексацию списков. 
case = options.index(player_1) - options.index(player_2)    # Здесь вычисляется индекс результата в диапозоне от -2 до 2
print(results[case])