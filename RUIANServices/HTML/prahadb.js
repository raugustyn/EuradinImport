// Číselníky pro Prahu vygenerované při importu do databáze.
var PRAHA_NAME = "praha";
var MOPDistricts = {
    "Praha 1": "Holešovice,Hradčany,Josefov,Malá Strana,Nové Město,Staré Město,Vinohrady",
    "Praha 3": "Strašnice,Vinohrady,Vysočany,Žižkov",
    "Praha 2": "Nové Město,Nusle,Vinohrady,Vyšehrad",
    "Praha 5": "Hlubočepy,Holyně,Jinonice,Košíře,Lahovice,Lipence,Lochkov,Malá Chuchle,Malá Strana,Motol,Radlice,Radotín,Řeporyje,Řepy,Slivenec,Smíchov,Sobín,Stodůlky,Třebonice,Velká Chuchle,Zadní Kopanina,Zbraslav,Zličín",
    "Praha 4": "Braník,Háje,Hodkovičky,Chodov,Cholupice,Kamýk,Komořany,Krč,Kunratice,Lhotka,Libuš,Michle,Modřany,Nusle,Písnice,Podolí,Šeberov,Točná,Újezd,Vinohrady,Záběhlice",
    "Praha 7": "Bubeneč,Holešovice,Troja",
    "Praha 6": "Břevnov,Bubeneč,Dejvice,Hradčany,Liboc,Lysolaje,Nebušice,Přední Kopanina,Ruzyně,Řepy,Sedlec,Střešovice,Suchdol,Veleslavín,Vokovice",
    "Praha 9": "Běchovice,Čakovice,Černý Most,Dolní Počernice,Hloubětín,Horní Počernice,Hostavice,Hrdlořezy,Kbely,Klánovice,Koloděje,Kyje,Letňany,Libeň,Malešice,Miškovice,Prosek,Satalice,Střížkov,Třeboradice,Újezd nad Lesy,Vinoř,Vysočany",
    "Praha 8": "Bohnice,Březiněves,Čimice,Ďáblice,Dolní Chabry,Karlín,Kobylisy,Libeň,Nové Město,Střížkov,Troja",
    "Praha 10": "Benice,Dolní Měcholupy,Dubeč,Hájek,Horní Měcholupy,Hostivař,Kolovraty,Královice,Křeslice,Lipany,Malešice,Michle,Nedvězí,Petrovice,Pitkovice,Strašnice,Štěrboholy,Uhříněves,Vinohrady,Vršovice,Záběhlice,Žižkov"
};

var PRAGUE_DISTRICTS = "Holešovice,Hradčany,Josefov,Malá Strana,Nové Město,Staré Město,Vinohrady,Strašnice,Vinohrady,Vysočany,Žižkov,Nové Město,Nusle,Vinohrady,Vyšehrad,Hlubočepy,Holyně,Jinonice,Košíře,Lahovice,Lipence,Lochkov,Malá Chuchle,Malá Strana,Motol,Radlice,Radotín,Řeporyje,Řepy,Slivenec,Smíchov,Sobín,Stodůlky,Třebonice,Velká Chuchle,Zadní Kopanina,Zbraslav,Zličín,Braník,Háje,Hodkovičky,Chodov,Cholupice,Kamýk,Komořany,Krč,Kunratice,Lhotka,Libuš,Michle,Modřany,Nusle,Písnice,Podolí,Šeberov,Točná,Újezd,Vinohrady,Záběhlice,Bubeneč,Holešovice,Troja,Břevnov,Bubeneč,Dejvice,Hradčany,Liboc,Lysolaje,Nebušice,Přední Kopanina,Ruzyně,Řepy,Sedlec,Střešovice,Suchdol,Veleslavín,Vokovice,Běchovice,Čakovice,Černý Most,Dolní Počernice,Hloubětín,Horní Počernice,Hostavice,Hrdlořezy,Kbely,Klánovice,Koloděje,Kyje,Letňany,Libeň,Malešice,Miškovice,Prosek,Satalice,Střížkov,Třeboradice,Újezd nad Lesy,Vinoř,Vysočany,Bohnice,Březiněves,Čimice,Ďáblice,Dolní Chabry,Karlín,Kobylisy,Libeň,Nové Město,Střížkov,Troja,Benice,Dolní Měcholupy,Dubeč,Hájek,Horní Měcholupy,Hostivař,Kolovraty,Královice,Křeslice,Lipany,Malešice,Michle,Nedvězí,Petrovice,Pitkovice,Strašnice,Štěrboholy,Uhříněves,Vinohrady,Vršovice,Záběhlice,Žižkov";

var DISTRICTMOPS = {
		"pitkovice" : "Praha 10",
		"hájek" : "Praha 10",
		"lahovice" : "Praha 5",
		"lysolaje" : "Praha 6",
		"nusle" : "Praha 2,Praha 4",
		"lochkov" : "Praha 5",
		"miškovice" : "Praha 9",
		"petrovice" : "Praha 10",
		"třebonice" : "Praha 5",
		"klánovice" : "Praha 9",
		"koloděje" : "Praha 9",
		"veleslavín" : "Praha 6",
		"yáběhlice" : "Praha 10,Praha 4",
		"krč" : "Praha 4",
		"žižkov" : "Praha 10,Praha 3",
		"troja" : "Praha 7,Praha 8",
		"písnice" : "Praha 4",
		"řepy" : "Praha 5,Praha 6",
		"nedvězí" : "Praha 10",
		"vršovice" : "Praha 10",
		"karlín" : "Praha 8",
		"letňany" : "Praha 9",
		"újezd" : "Praha 4",
		"malá Chuchle" : "Praha 5",
		"strašnice" : "Praha 10,Praha 3",
		"břevnov" : "Praha 6",
		"hostavice" : "Praha 9",
		"královice" : "Praha 10",
		"střešovice" : "Praha 6",
		"zadní Kopanina" : "Praha 5",
		"kbely" : "Praha 9",
		"liboc" : "Praha 6",
		"jinonice" : "Praha 5",
		"dolní Počernice" : "Praha 9",
		"zbraslav" : "Praha 5",
		"josefov" : "Praha 1",
		"háje" : "Praha 4",
		"dolní Měcholupy" : "Praha 10",
		"bohnice" : "Praha 8",
		"stodůlky" : "Praha 5",
		"hostivař" : "Praha 10",
		"točná" : "Praha 4",
		"braník" : "Praha 4",
		"velká Chuchle" : "Praha 5",
		"lipence" : "Praha 5",
		"radotín" : "Praha 5",
		"chodov" : "Praha 4",
		"kamýk" : "Praha 4",
		"čimice" : "Praha 8",
		"dejvice" : "Praha 6",
		"ruzyně" : "Praha 6",
		"dolní Chabry" : "Praha 8",
		"nebušice" : "Praha 6",
		"uhříněves" : "Praha 10",
		"přední Kopanina" : "Praha 6",
		"motol" : "Praha 5",
		"hlubočepy" : "Praha 5",
		"radlice" : "Praha 5",
		"kunratice" : "Praha 4",
		"košíře" : "Praha 5",
		"holešovice" : "Praha 1,Praha 7",
		"holyně" : "Praha 5",
		"staré Město" : "Praha 1",
		"horní Měcholupy" : "Praha 10",
		"hodkovičky" : "Praha 4",
		"vinohrady" : "Praha 1,Praha 10,Praha 2,Praha 3,Praha 4",
		"újezd nad Lesy" : "Praha 9",
		"michle" : "Praha 10,Praha 4",
		"modřany" : "Praha 4",
		"zličín" : "Praha 5",
		"řeporyje" : "Praha 5",
		"komořany" : "Praha 4",
		"satalice" : "Praha 9",
		"čakovice" : "Praha 9",
		"šeberov" : "Praha 4",
		"nové Město" : "Praha 1,Praha 2,Praha 8",
		"vyšehrad" : "Praha 2",
		"bubeneč" : "Praha 6,Praha 7",
		"ďáblice" : "Praha 8",
		"libeň" : "Praha 8,Praha 9",
		"hloubětín" : "Praha 9",
		"černý Most" : "Praha 9",
		"podolí" : "Praha 4",
		"kyje" : "Praha 9",
		"běchovice" : "Praha 9",
		"slivenec" : "Praha 5",
		"kolovraty" : "Praha 10",
		"hradčany" : "Praha 1,Praha 6",
		"třeboradice" : "Praha 9",
		"lhotka" : "Praha 4",
		"malá Strana" : "Praha 1,Praha 5",
		"sobín" : "Praha 5",
		"libuš" : "Praha 4",
		"suchdol" : "Praha 6",
		"smíchov" : "Praha 5",
		"křeslice" : "Praha 10",
		"hrdlořezy" : "Praha 9",
		"lipany" : "Praha 10",
		"horní Počernice" : "Praha 9",
		"vinoř" : "Praha 9",
		"vysočany" : "Praha 3,Praha 9",
		"kobylisy" : "Praha 8",
		"malešice" : "Praha 10,Praha 9",
		"sedlec" : "Praha 6",
		"prosek" : "Praha 9",
		"benice" : "Praha 10",
		"štěrboholy" : "Praha 10",
		"dubeč" : "Praha 10",
		"střížkov" : "Praha 8,Praha 9",
		"vokovice" : "Praha 6",
		"cholupice" : "Praha 4",
		"březiněves" : "Praha 8"
};

defaultDistrictNumberInnerHTML = '<option value=""></option>' +
    '<option value="1">Praha 1</option>' +
    '<option value="2">Praha 2</option>' +
    '<option value="3">Praha 3</option>' +
    '<option value="4">Praha 4</option>' +
    '<option value="5">Praha 5</option>' +
    '<option value="6">Praha 6</option>' +
    '<option value="7">Praha 7</option>' +
    '<option value="8">Praha 8</option>' +
    '<option value="9">Praha 9</option>' +
    '<option value="10">Praha 10</option>';
