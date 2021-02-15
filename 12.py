from yandex_testing_lesson import is_correct_mobile_phone_number_ru

test_data = [('1234567890', False),
             ('+-123123123', False),
             ('791655555555', False),
             ('+7(916)555-55-5555', False),
             ('+7)916(555-55-55', False),
             ('+7((916))555-55-55', False),
             ('8(9165)55-55-55', False),
             ('8(916)555-55-55', True)]
yes = True
for in_data, correct_result in test_data:
    result = is_correct_mobile_phone_number_ru(in_data)
    if result != correct_result:
        print('NO')
        yes = False
        break
if yes:
    print('YES')
