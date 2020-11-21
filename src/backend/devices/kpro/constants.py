# kpro device ids
KPRO23_ID_VENDOR = 0x403
KPRO23_ID_PRODUCT = 0xF5F8
KPRO4_ID_VENDOR = 0x1C40
KPRO4_ID_PRODUCT = 0x0434
KPRO23_ID = 23  # v2 and v3 works equally so I mixed both version numbers
KPRO4_ID = 4

# command 0x40
KPRO23_ECU_TYPE = 12
KPRO23_IGN = 17
KPRO23_SERIAL1 = 6
KPRO23_SERIAL2 = 7
KPRO23_FIRM1 = 8
KPRO23_FIRM2 = 9

KPRO4_ECU_TYPE = 10
KPRO4_IGN = 15
KPRO4_SERIAL1 = 4
KPRO4_SERIAL2 = 5
KPRO4_FIRM1 = 6
KPRO4_FIRM2 = 7

# command 0x60
KPRO23_TPS = 7
KPRO23_AFR1 = 18
KPRO23_AFR2 = 19
KPRO23_VSS = 6
KPRO23_RPM1 = 4
KPRO23_RPM2 = 5
KPRO23_MAP = 8
KPRO23_CAM = 10
KPRO23_GEAR = 37
KPRO23_EPS = 33
KPRO23_SCS = 33
KPRO23_RVSLCK = 33
KPRO23_BKSW = 33
KPRO23_ACSW = 33
KPRO23_ACCL = 33
KPRO23_FLR = 33
KPRO23_FANC = 33
KPRO23_MIL = 34

KPRO4_TPS = 5
KPRO4_AFR1 = 16
KPRO4_AFR2 = 17
KPRO4_VSS = 4
KPRO4_RPM1 = 2
KPRO4_RPM2 = 3
KPRO4_MAP = 6
KPRO4_CAM = 8
KPRO4_GEAR = 35
KPRO4_EPS = 31
KPRO4_SCS = 31
KPRO4_RVSLCK = 31
KPRO4_BKSW = 31
KPRO4_ACSW = 31
KPRO4_ACCL = 31
KPRO4_FLR = 31
KPRO4_FANC = 31

# command 0x61
KPRO23_ECT = 4
KPRO23_IAT = 5
KPRO23_BAT = 6

KPRO4_ECT = 2
KPRO4_IAT = 3
KPRO4_BAT = 4

# command 0x65
KPRO4_AN0_1 = 67
KPRO4_AN0_2 = 66
KPRO4_AN1_1 = 69
KPRO4_AN1_2 = 68
KPRO4_AN2_1 = 71
KPRO4_AN2_2 = 70
KPRO4_AN3_1 = 73
KPRO4_AN3_2 = 72
KPRO4_AN4_1 = 75
KPRO4_AN4_2 = 74
KPRO4_AN5_1 = 77
KPRO4_AN5_2 = 76
KPRO4_AN6_1 = 79
KPRO4_AN6_2 = 78
KPRO4_AN7_1 = 81
KPRO4_AN7_2 = 80
KPRO4_MIL = 30
KPRO4_ETH = 98
KPRO4_FLT = 99

# command 0xb0
KPRO3_AN0_1 = 5
KPRO3_AN0_2 = 4
KPRO3_AN1_1 = 7
KPRO3_AN1_2 = 6
KPRO3_AN2_1 = 9
KPRO3_AN2_2 = 8
KPRO3_AN3_1 = 11
KPRO3_AN3_2 = 10
KPRO3_AN4_1 = 13
KPRO3_AN4_2 = 12
KPRO3_AN5_1 = 15
KPRO3_AN5_2 = 14
KPRO3_AN6_1 = 17
KPRO3_AN6_2 = 16
KPRO3_AN7_1 = 19
KPRO3_AN7_2 = 18

# K-Pro return values to celsius
# first 5 positions are untested
TEMP = [
    123,
    123,
    123,
    123,
    123,
    123,
    123,
    123,
    123,
    123,
    123,
    123,
    123,
    123,
    121,
    118,
    117,
    114,
    112,
    110,
    108,
    106,
    103,
    101,
    100,
    97,
    96,
    95,
    93,
    92,
    91,
    90,
    88,
    87,
    86,
    85,
    83,
    82,
    82,
    81,
    80,
    79,
    78,
    77,
    76,
    76,
    75,
    74,
    73,
    72,
    71,
    70,
    70,
    69,
    68,
    68,
    67,
    67,
    66,
    65,
    65,
    64,
    63,
    63,
    62,
    62,
    61,
    61,
    60,
    59,
    58,
    58,
    57,
    57,
    56,
    56,
    55,
    55,
    54,
    53,
    54,
    52,
    52,
    52,
    51,
    51,
    52,
    50,
    50,
    49,
    49,
    48,
    49,
    47,
    47,
    47,
    46,
    46,
    46,
    45,
    45,
    44,
    44,
    43,
    43,
    42,
    42,
    42,
    41,
    41,
    40,
    40,
    40,
    39,
    38,
    38,
    38,
    37,
    37,
    37,
    36,
    36,
    35,
    35,
    35,
    34,
    33,
    33,
    33,
    32,
    32,
    32,
    32,
    31,
    31,
    30,
    30,
    29,
    28,
    28,
    28,
    27,
    27,
    26,
    26,
    26,
    25,
    25,
    25,
    24,
    23,
    23,
    23,
    22,
    22,
    22,
    22,
    21,
    21,
    20,
    19,
    19,
    18,
    18,
    17,
    17,
    17,
    16,
    16,
    16,
    15,
    15,
    14,
    14,
    13,
    13,
    12,
    12,
    12,
    11,
    11,
    11,
    10,
    10,
    9,
    8,
    8,
    8,
    7,
    7,
    7,
    6,
    6,
    5,
    5,
    5,
    4,
    3,
    3,
    3,
    2,
    2,
    2,
    1,
    1,
    0,
    0,
    0,
    -1,
    -1,
    -2,
    -2,
    -3,
    -3,
    -4,
    -5,
    -6,
    -6,
    -7,
    -7,
    -8,
    -8,
    -9,
    -10,
    -10,
    -11,
]
