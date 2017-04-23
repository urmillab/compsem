# Event roles
EVENT_ROLES = {
	"person" : 0,
	"place" : 1,
	"buyer" : 2,
	"seller" : 3,
	"beneficiary" : 4,
	"price" : 5,
	"artifact" : 6, 
	"origin" : 7,
	"destination" : 8,
	"giver" : 9,
	"recipient" : 10,
	"money" : 11,
	"org" : 12,
	"agent" : 13,
	"victim" : 14,
	"instrument" : 15,
	"entity" : 16,
	"attacker" : 17,
	"target" : 18,
	"defendant" : 19,
	"adjudicator" : 20,
	"prosecutor" : 21,
	"plaintiff" : 22,
	"crime" : 23,
	"position" : 24,
	"sentence" : 25,
	"vehicle" : 26,
	"time-after" : 27,
	"time-before" : 28,
	"time-at-beginning" : 29,
	"time-at-end" : 30,
	"time-starting" : 31,
	"time-ending" : 32,
	"time-holds" : 33,
	"time-within" : 34,
}

EVENT_TYPES_TO_SUBTYPES = {
	"life": ["be-born", "marry", "divorce", "injure", "die"],
	"movement" : ["transport"],
	"transaction" : ["transfer-ownership", "transfer-money"],
	"business" : ["start-org", "merge-org", "declare-bankruptcy", "end-org"],
	"conflict":  ["attack", "demonstrate"],
	"contact" : ["meet", "phone-write"],
	"personnel" : ["start-position", "end-position", "nominate", "elect"],
	"justice" : ["arrest-jail", "release-parole", "trial-hearing", "charge-indict", \
	 "sue", "convict", "sentence", "fine", "execute", "extradite", "acquit", "appeal",
	 "pardon"]
}

DOCUMENT_TYPES = {
	"weblog",
	"broadcast news",
	"usenet",
	"broadcast conversation",
	"newswire",
	"telephone"
}

EVENT_TYPES = {
	"life": 0, 
	"movement": 1, 
	"transaction": 2, 
	"business": 3, 
	"conflict": 4, 
	"contact": 5, 
	"personnel": 6, 
	"justice": 7
}


CHAINS = ['1, 1', '1, 2', '2, 1', '3, 1', '3, 2', '3, 3', '4, 1', '5, 1', '5, 2', '5, 3', '6, 1', '7, 1', '8, 1', '9, 1', '9, 2', '10, 1', '12, 1', '12, 2', '13, 1', '15, 1', '17, 1', '18, 1', '18, 2', '19, 1', '19, 2', '20, 1', '21, 1', '22, 1', '23, 1', '24, 1', '26, 1', '27, 1', '28, 1', '29, 1', '30, 1', '31, 1', '32, 1', '33, 1', '34, 1', '34, 2', '35, 1', '36, 1', '36, 2', '37, 1', '37, 2', '37, 3', '38, 1', '38, 2', '38, 3', '38, 4', '39, 1', '39, 2', '39, 3', '40, 1', '40, 2', '40, 3', '41, 1', '42, 1', '42, 2', '42, 3', '42, 4', '43, 1', '44, 1', '45, 1', '45, 2', '47, 1', '48, 1', '49, 1', '50, 1', '51, 1', '52, 1', '52, 2', '53, 1', '55, 1']

INDEX_TO_CHAIN = {
	0: "1_1.xml",
	1: "1_2.xml",
	2: "2_1.xml",
	3: "3_1.xml",
	4: "3_2.xml",
	5: "3_3.xml",
	6: "4_1.xml",
	7: "5_1.xml",
	8: "5_2.xml",
	9: "5_3.xml",
	10: "6_1.xml",
	11: "7_1.xml",
	12: "8_1.xml",
	13: "9_1.xml",
	14: "9_2.xml",
	15: "10_1.xml",
	16: "12_1.xml",
	17: "12_2.xml",
	18: "13_1.xml",
	19: "15_1.xml",
	20: "17_1.xml",
	21: "18_1.xml",
	22: "18_2.xml",
	23: "19_1.xml",
	24: "19_2.xml",
	25: "20_1.xml",
	26: "21_1.xml",
	27: "22_1.xml",
	28: "23_1.xml",
	29: "24_1.xml",
	30: "26_1.xml",
	31: "27_1.xml",
	32: "28_1.xml",
	33: "29_1.xml",
	34: "30_1.xml",
	35: "31_1.xml",
	36: "32_1.xml",
	37: "33_1.xml",
	38: "34_1.xml",
	39: "34_2.xml",
	40: "35_1.xml",
	41: "36_1.xml",
	42: "36_2.xml",
	43: "37_1.xml",
	44: "37_2.xml",
	45: "37_3.xml",
	46: "38_1.xml",
	47: "38_2.xml",
	48: "38_3.xml",
	49: "38_4.xml",
	50: "39_1.xml",
	51: "39_2.xml",
	52: "39_3.xml",
	53: "40_1.xml",
	54: "40_2.xml",
	55: "40_3.xml",
	56: "41_1.xml",
	57: "42_1.xml",
	58: "42_2.xml",
	59: "42_3.xml",
	60: "42_4.xml",
	61: "43_1.xml",
	62: "44_1.xml",
	63: "45_1.xml",
	64: "45_2.xml",
	65: "47_1.xml",
	66: "48_1.xml",
	67: "49_1.xml",
	68: "50_1.xml",
	69: "51_1.xml",
	70: "52_1.xml",
	71: "52_2.xml",
	72: "53_1.xml",
	73: "55_1.xml"
}

"""mapping from doc name to its id number in gold standard corpus. 
   Docs with less than 2 events per each event group have a key of -1 because they weren't used
   6 docs of original 55 were removed: 11, 14, 16, 25, 46, 54"""
   
GS_DOC_TO_MATRIX_INDEX = {
	"CNN_IP_20030402.1600.00-2": 1,
	"CNN_IP_20030402.1600.02-1": 2,
	"CNN_IP_20030404.1600.00-2": 3,
	"CNN_IP_20030405.1600.01-3": 4, 
	"CNN_IP_20030408.1600.03": 5, 
	"CNN_IP_20030412.1600.05": 6, 
	"CNN_ENG_20030305_170125.1": 7,
	"CNN_ENG_20030312_083725.3": 8, 
	"CNN_ENG_20030402_190500.11": 9, 
	"CNN_ENG_20030403_183513.1": 10, 
	"CNN_ENG_20030415_103039.0": -1, 
	"CNN_ENG_20030415_173752.0": 12, 
	"CNN_ENG_20030421_090007.11": 13, 
	"CNN_ENG_20030421_120508.13": -1, 
	"CNN_ENG_20030424_173553.8": 15, 
	"CNN_ENG_20030506_053020.14": -1, 
	"CNN_ENG_20030507_170539.0": 17, 
	"CNN_ENG_20030508_170552.18": 18, 
	"CNN_ENG_20030513_160506.16": 19, 
	"CNN_ENG_20030529_085826.10": 20, 
	"CNN_ENG_20030604_092828.7": 21, 
	"CNN_ENG_20030612_173004.2": 22, 
	"CNN_ENG_20030617_105836.4": 23, 
	"CNN_ENG_20030618_150128.6": 24, 
	"CNNHL_ENG_20030416_193742.26": -1, 
	"CNNHL_ENG_20030425_183518.12": 26, 
	"CNNHL_ENG_20030428_123600.14": 27, 
	"CNNHL_ENG_20030523_221118.14": 28, 
	"CNNHL_ENG_20030616_230155.7": 29, 
	"fsh_29195": 30, 
	"fsh_29361": 31, 
	"fsh_29395": 32, 
	"AFP_ENG_20030327.0022": 33, 
	"AFP_ENG_20030519.0372": 34, 
	"APW_ENG_20030325.0786": 35, 
	"APW_ENG_20030411.0304": 36, 
	"APW_ENG_20030412.0531": 37, 
	"APW_ENG_20030422.0469": 38, 
	"APW_ENG_20030502.0686": 39, 
	"APW_ENG_20030520.0757": 40, 
		"NYT_ENG_20030403.0008": 41, 
	"alt.atheism_20041104.2428": 42, 
	"misc.invest.marketplace_20050208.2406": 43, 
	"rec.boats_20050130.1006": 44, 
	"rec.games.chess.politics_20041216.1047": 45, 
	"AGGRESSIVEVOICEDAILY_20041101.1144": -1, 
	"AGGRESSIVEVOICEDAILY_20041223.1449": 47, 
	"AGGRESSIVEVOICEDAILY_20041226.1712": 48, 
	"AGGRESSIVEVOICEDAILY_20050205.1954": 49, 
	"AGGRESSIVEVOICEDAILY_20050224.1207": 50, 
	"FLOPPINGACES_20041114.1240.039": 51, 
	"FLOPPINGACES_20041228.0927.010": 52, 
	"MARKBACKER_20041117.1107": 53, 
	"MARKETVIEW_20050120.1641": -1, 
	"MARKETVIEW_20050206.2009": 55 
}
