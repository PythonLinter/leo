# from nanohttp import RestController, json
# from leo.models import NineToTen, TenToNine
#
# flags = "12345"
# print(flags)
#
# query = NineToTen.query
# query = query.filter(NineToTen.nine == '8064')
# print(query.count)

#
# def find_scenario():
# select flags from nine_to_ten where nine = '8064';
recognize = ['10112', '10122', '10132', '10142', '10152', '10162', '10121', '10131', '10132', '10141', '10151',
             '10161',
             '10111', '10121', '10131', '10141', '10151', '10161', '10111', '10121', '10131', '10141', '10151',
             '10151',
             '10161', '10111']
for flag in recognize:
    combination = flag[2]
    scenario = flag[3]
    choice_list = flag[4]
    # if combination == 1:
    print("Combination are %r" % combination)
    print("Scenario are %r" % scenario)
    print("Choice list are %r" % choice_list)
    print("...............................")

    # FLAGS = X1X2X3X4X5
    # X1:Map
    # X2:Approximate,
    # X3:Combination,
    # X4:Scenario,
    # X5:Choice List
    # Combination = 0 or 1 / Scenario = if 0 scenario not exist, if >= 1 has conversions
