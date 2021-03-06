import  shapely
from shapely import geometry

x_points = [   -72.64313,
    -72.64329,
    -72.75134,
    -72.75203,
    -72.75707,
    -72.76486,
    -72.7591,
    -72.76177,
    -72.81703,
    -72.91628,
    -73.04828,
    -73.13059,
    -73.19781,
    -73.27508,
    -73.33687,
    -73.42605,
    -73.48731,
    -73.48739,
    -73.50775,
    -73.49467,
    -73.48011,
    -73.47025,
    -73.45443,
    -73.44827,
    -73.41917,
    -73.41386,
    -73.41175,
    -73.41088,
    -73.40134,
    -73.39798,
    -73.3926,
    -73.38202,
    -73.37519,
    -73.37174,
    -73.36905,
    -73.36341,
    -73.35709,
    -73.34314,
    -73.32907,
    -73.3227,
    -73.3147,
    -73.27876,
    -73.26553,
    -73.26496,
    -73.2606,
    -73.21493,
    -73.21043,
    -73.18186,
    -73.11981,
    -73.09759,
    -73.07151,
    -73.05437,
    -73.01864,
    -72.97955,
    -72.92862,
    -72.92356,
    -72.87454,
    -72.85487,
    -72.79108,
    -72.76225,
    -72.72136,
    -72.69266,
    -72.67645,
    -72.66115,
    -72.61349,
    -72.60156,
    -72.57333,
    -72.56587,
    -72.46457,
    -72.46194,
    -72.45844,
    -72.45819,
    -72.37299,
    -72.22286,
    -72.08588,
    -72.01069,
    -71.9618,
    -71.81162,
    -71.66491,
    -71.54741,
    -71.47433,
    -71.42354,
    -71.34818,
    -71.28879,
    -71.22616,
    -71.1977,
    -71.18521,
    -71.11392,
    -71.07206,
    -71.04967,
    -71.0044,
    -70.98147,
    -70.94388,
    -70.90277,
    -70.87102,
    -70.83079,
    -70.735,
    -70.73864,
    -70.74883,
    -70.74397,
    -70.73625,
    -70.7344,
    -70.73397,
    -70.73722,
    -70.73092,
    -70.72621,
    -70.71696,
    -70.62594,
    -70.50214,
    -70.56699,
    -70.64807,
    -70.68902,
    -70.66281,
    -70.64295,
    -70.4148,
    -70.24947,
    -70.17254,
    -70.12447,
    -70.01159,
    -69.94064,
    -69.8953,
    -69.87446,
    -69.86557,
    -69.86237,
    -69.85895,
    -69.87106,
    -69.88942,
    -69.9162,
    -69.92899,
    -69.96861,
    -69.99817,
    -70.02014,
    -70.0849,
    -70.12492,
    -70.12679,
    -70.09493,
    -70.06857,
    -70.06857,
    -70.09422,
    -70.13849,
    -70.1815,
    -70.21464,
    -70.24946,
    -70.29933,
    -70.34634,
    -70.38728,
    -70.4173,
    -70.45763,
    -70.48974,
    -70.5086,
    -70.49166,
    -70.47599,
    -70.40593,
    -70.38216,
    -70.35308,
    -70.29418,
    -70.24769,
    -70.22162,
    -70.18729,
    -70.13223,
    -70.09784,
    -70.11654,
    -70.06517,
    -69.99464,
    -69.96406,
    -69.93846,
    -69.91495,
    -69.89488,
    -69.89221,
    -69.89901,
    -69.93095,
    -69.98315,
    -70.05165,
    -70.13585,
    -70.228,
    -70.33509,
    -70.38667,
    -70.44476,
    -70.5122,
    -70.57185,
    -70.6312,
    -70.67168,
    -70.69287,
    -70.71106,
    -70.73406,
    -70.74431,
    -70.80595,
    -70.87733,
    -70.8942,
    -70.87447,
    -70.89136,
    -70.90374,
    -70.9026,
    -70.95575,
    -71.00631,
    -71.02903,
    -71.03811,
    -71.08504,
    -71.08857,
    -71.12533,
    -71.13851,
    -71.13334,
    -71.15105,
    -71.18591,
    -71.1976,
    -71.28991,
    -71.32896,
    -71.33039,
    -71.33102,
    -71.33372,
    -71.34127,
    -71.34629,
    -71.3421,
    -71.3396,
    -71.36469,
    -71.3816,
    -71.38152,
    -71.3815,
    -71.45,
    -71.50716,
    -71.5446,
    -71.60598,
    -71.70489,
    -71.79022,
    -71.79924,
    -71.82387,
    -71.87297,
    -71.95441,
    -72.02966,
    -72.10639,
    -72.17549,
    -72.32182,
    -72.45609,
    -72.57337,
    -72.60487
    ]
y_points = [
   42.0324,
    42.0324,
    42.0362,
    42.02907,
    42.02112,
    42.02174,
    42.01586,
    42.00898,
    42.03653,
    42.03799,
    42.03964,
    42.04217,
    42.04408,
    42.04633,
    42.04817,
    42.05048,
    42.04964,
    42.04964,
    42.08735,
    42.12309,
    42.1634,
    42.19023,
    42.23331,
    42.25009,
    42.32909,
    42.34353,
    42.34927,
    42.35163,
    42.37737,
    42.38641,
    42.4009,
    42.42949,
    42.44793,
    42.45756,
    42.46481,
    42.47967,
    42.49777,
    42.53522,
    42.57318,
    42.59021,
    42.61177,
    42.7086,
    42.74439,
    42.74594,
    42.74591,
    42.74495,
    42.74486,
    42.74433,
    42.74331,
    42.74263,
    42.74219,
    42.74163,
    42.74106,
    42.74022,
    42.73926,
    42.73916,
    42.73808,
    42.73765,
    42.73602,
    42.73532,
    42.7341,
    42.73336,
    42.73294,
    42.73254,
    42.73123,
    42.73098,
    42.73019,
    42.72999,
    42.72704,
    42.72696,
    42.72685,
    42.72684,
    42.72422,
    42.72004,
    42.71642,
    42.71415,
    42.71291,
    42.70909,
    42.7055,
    42.70279,
    42.70091,
    42.69979,
    42.69792,
    42.70239,
    42.74641,
    42.74096,
    42.79169,
    42.81722,
    42.80786,
    42.84025,
    42.86339,
    42.86657,
    42.87858,
    42.88653,
    42.87383,
    42.86892,
    42.87469,
    42.86926,
    42.85883,
    42.84317,
    42.82919,
    42.81243,
    42.80115,
    42.78796,
    42.7749,
    42.76126,
    42.74352,
    42.73972,
    42.63547,
    42.56078,
    42.40563,
    42.27239,
    42.24485,
    42.17819,
    42.1251,
    42.12693,
    42.13452,
    42.12604,
    42.07338,
    41.99235,
    41.90675,
    41.84237,
    41.80767,
    41.76632,
    41.70692,
    41.65257,
    41.62269,
    41.58429,
    41.53215,
    41.50012,
    41.4934,
    41.47393,
    41.46749,
    41.50012,
    41.53088,
    41.55925,
    41.58522,
    41.6107,
    41.60824,
    41.59869,
    41.59355,
    41.57775,
    41.56015,
    41.56592,
    41.56845,
    41.55768,
    41.53482,
    41.50934,
    41.50186,
    41.49897,
    41.47101,
    41.46614,
    41.45701,
    41.37512,
    41.38145,
    41.39145,
    41.38989,
    41.37177,
    41.35838,
    41.34873,
    41.35358,
    41.39513,
    41.44269,
    41.42502,
    41.39585,
    41.35765,
    41.32419,
    41.29037,
    41.27132,
    41.24554,
    41.21054,
    41.1914,
    41.19091,
    41.19465,
    41.22266,
    41.27278,
    41.27128,
    41.26551,
    41.29831,
    41.30009,
    41.29787,
    41.29453,
    41.28964,
    41.27486,
    41.25615,
    41.22603,
    41.19874,
    41.22414,
    41.25944,
    41.29497,
    41.31882,
    41.35508,
    41.36761,
    41.35016,
    41.35732,
    41.37558,
    41.40545,
    41.43347,
    41.43132,
    41.54358,
    41.60369,
    41.65399,
    41.66371,
    41.67337,
    41.67761,
    41.76434,
    41.78242,
    41.78542,
    41.78958,
    41.79375,
    41.80012,
    41.8251,
    41.8452,
    41.8912,
    41.89549,
    41.9123,
    41.95103,
    42.0102,
    42.0179,
    42.01662,
    42.0147,
    42.01338,
    42.01103,
    42.00874,
    42.00806,
    42.02371,
    42.02435,
    42.02605,
    42.0271,
    42.02907,
    42.03085,
    42.03198,
    42.03398,
    42.03006,
    42.025
    ]

polygon_points = []
for counter, i in enumerate(x_points):
    polygon_points.append([i, y_points[counter]])

massachusetts = geometry.Polygon(polygon_points)
boston = geometry.Point(-71.094575, 42.336094)
nashua = geometry.Point(-71.518855, 42.774483,)
manchester = geometry.Point(-71.543138, 43.031303)
worchester = geometry.Point(-71.820443, 42.260424)
assert massachusetts.contains(boston)
assert massachusetts.contains(worchester)
assert massachusetts.contains(nashua) == False
assert massachusetts.contains(manchester) == False
