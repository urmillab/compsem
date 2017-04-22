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

EVENT_TYPES = {
	"life" : 0,
	"movement" : 1,
	"transaction" : 2,
	"business" : 3,
	"conflict": 4,
	"contact" : 5,
	"personnel" : 6,
	"justice" : 7
	
}

EVENT_TYPES_TO_SUBTYPES = {
	"life" : ["be-born", "marry", "divorce", "injure", "die"],
	"movement" : ["transport"],
	"transaction" : ["transfer-ownership", "transfer-money"],
	"business" : ["start-org", "merge-org", "declare-bankruptcy", "end-org"],
	"conflict": ["attack", "demonstrate"],
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

CHAINS = ['1, 1', '1, 2', '2, 1', '3, 1', '3, 2', '3, 3', '4, 1', '5, 1', '5, 2', '5, 3', '6, 1', '7, 1', '8, 1', '9, 1', '9, 2', '10, 1', '12, 1', '12, 2', '13, 1', '15, 1', '17, 1', '18, 1', '18, 2', '19, 1', '19, 2', '20, 1', '21, 1', '22, 1', '23, 1', '24, 1', '26, 1', '27, 1', '28, 1', '29, 1', '30, 1', '31, 1', '32, 1', '33, 1', '34, 1', '34, 2', '35, 1', '36, 1', '36, 2', '37, 1', '37, 2', '37, 3', '38, 1', '38, 2', '38, 3', '38, 4', '39, 1', '39, 2', '39, 3', '40, 1', '40, 2', '40, 3', '41, 1', '42, 1', '42, 2', '42, 3', '42, 4', '43, 1', '44, 1', '45, 1', '45, 2', '47, 1', '48, 1', '49, 1', '50, 1', '51, 1', '52, 1', '52, 2', '53, 1', '55, 1']