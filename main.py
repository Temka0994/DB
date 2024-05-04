from mysql.connector import connect

action = 0

try:
    connection = connect(host='localhost',
                         user='root',
                         password='root',
                         database='phone_payments')
    print("Successful connection.\n")

    print(
        "Choose function number:\n"
        "1 - Вивести загальну суму внесену абонентом за певну дату.\n"
        "2 - Вивести інформацію про абонента та про його не сплачені хвилини.\n"
        "3 - Змінити тариф для категорії пенсіонерів.\n"
        "4 - Вивести несплачені хвилини та загальну кількість хвилин абоненту.\n"
        "5 - Вивести список абонентів, що мають найбільш оплачені міжкраїнні хвилини.\n"
        "6 - Замінити категорію абонентів.\n"
        "7 - Вивести прізвище, ім'я, по-батькові та категорію абонента.\n"
        "8 - Вивести користувачів у яких кількість несплачених міжкраїнних хвилин менша за 200 "
        "або кількість несплачених міських хвилин більша за 0 та кількість несплачених міжміських хвилин більше 100.\n"
        "9 - Вивести кількість сплачених хвилин між двома конкретними датами.\n"
        "10 - Вивести абонентів у яких кількість несплачених міських хвилин менше 100.\n"
        "11 - Зупинити програму.\n"
    )
    cursor = connection.cursor()
    while True:
        action = int(input())
        match action:
            case 1:
                print('Введіть дату формату YYYY-MM-DD')
                date = input()
                cursor.execute("SELECT s.last_name, s.first_name, s.surname, "
                               "SUM(p.payment_city + p.payment_intercity + p.payment_country) AS all_sum "
                               "FROM subscribers s "
                               "JOIN payments p ON s.telephone_id = p.telephone_id "
                               "WHERE p.payment_date = %s "
                               "GROUP BY s.last_name, s.first_name, s.surname", (date,))
                result = cursor.fetchall()
                print(*result)
            case 2:
                cursor.execute("SELECT s.last_name, s.first_name, s.surname, s.telephone_id as number, "
                               "s.tariff_id, t.privilege, s.unpaid_minutes_city "
                               "FROM subscribers s "
                               "JOIN payments p ON s.telephone_id = p.telephone_id "
                               "JOIN tariff t ON s.tariff_id = t.tariff_id")
                result = cursor.fetchall()
                print(*result)
            case 3:
                cursor.execute("UPDATE tariff "
                               "SET payment_amount = payment_amount * 0.9 "
                               "WHERE privilege = 'Пeнсiонер'")
                connection.commit()
            case 4:
                cursor.execute("SELECT s.last_name, s.first_name, s.surname, "
                               "SUM(s.unpaid_minutes_city), "
                               "SUM(s.unpaid_minutes_country), "
                               "SUM(s.unpaid_minutes_intercity), " 
                               "SUM(s.unpaid_minutes_city + s.unpaid_minutes_country + s.unpaid_minutes_intercity) "
                               "FROM subscribers s "
                               "GROUP BY s.last_name, s.first_name, s.surname ")
                result = cursor.fetchall()
                print(*result)
            case 5:
                cursor.execute("SELECT s.last_name, s.first_name, MAX(p.payment_country) AS max_payment_country "
                               "FROM subscribers s "
                               "INNER JOIN payments p ON s.telephone_id = p.telephone_id "
                               "GROUP BY s.last_name, s.first_name "
                               "ORDER BY max_payment_country DESC "
                               "LIMIT 2")
                result = cursor.fetchall()
                print(*result)
            case 6:
                cursor.execute("UPDATE tariff "
                               "SET privilege = 'Звичайний користувач' "
                               "WHERE privilege = 'Відсутня'")
                connection.commit()
            case 7:
                cursor.execute("SELECT s.last_name, s.first_name, s.surname, t.privilege "
                               "FROM subscribers s "
                               "JOIN tariff t ON s.tariff_id = t.tariff_id "
                               "WHERE t.privilege = 'Пенсіонер'")
                result = cursor.fetchall()
                print(*result)
            case 8:
                cursor.execute("SELECT last_name, first_name, surname "
                               "FROM subscribers "
                               "WHERE (unpaid_minutes_city > 0 and unpaid_minutes_intercity > 100) "
                               "OR unpaid_minutes_country < 200")
                result = cursor.fetchall()
                print(*result)
            case 9:
                print('1. Введіть дату формату YYYY-MM-DD')
                first_date = input()
                print('2. Введіть дату формату YYYY-MM-DD')
                second_date = input()
                cursor.execute("SELECT p.payment_date, "
                               "SUM(p.payment_city+ p.payment_intercity + p.payment_country) AS total_payment "
                               "FROM subscribers s "
                               "JOIN payments p ON s.telephone_id = p.telephone_id "
                               "WHERE p.payment_date BETWEEN %s AND %s "
                               "GROUP BY p.payment_date", (first_date, second_date))
                result = cursor.fetchall()
                print(*result)
            case 10:
                cursor.execute("SELECT last_name, first_name, surname, unpaid_minutes_city "
                               "FROM subscribers "
                               "WHERE unpaid_minutes_city < 100")
                result = cursor.fetchall()
                print(*result)
            case 11:
                cursor.close()
                print('Програму зупинено.')
                break
            case _:
                print('Непідходяще число.')

except Exception as ex:
    print("Something went wrong.")
    print(ex)
