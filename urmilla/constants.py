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