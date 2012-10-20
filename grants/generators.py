from models import Grantee
import random
import pickle
a = Grantee()

dicName={
'part1':['Ollanius','Solar','Marnius','Garvial',],
'part2':['Pius','Marcharius','Calgar','Loken',],
}
f=open('syllables','w')
pickle.dump(dicName,f)
f.close()
f1=open('syllables','r')
sd=pickle.load(f1)
f1.close()
first_part=sd['part1'][random.randint(0,len(sd['part1'])-1)]
second_part=sd['part2'][random.randint(0,len(sd['part2'])-1)]
a.name = first_part + " " + second_part

dicEmail={
'part1':['clanOf','awesome','floating','123',],
'part2':['Ryan','','Sauce','Nachos','Cadians'],
}
f=open('syllables','w')
pickle.dump(dicEmail,f)
f.close()
f1=open('syllables','r')
sd=pickle.load(f1)
f1.close()
first_part=sd['part1'][random.randint(0,len(sd['part1'])-1)]
second_part=sd['part2'][random.randint(0,len(sd['part2'])-1)]
a.email = first_part + second_part + "@gmail.com"

a.address = str(random.randrange(1000, 9999)) + " " + str(random.randrange(10, 99)) + "th PL NW"

arrayCity = ["Seattle", "Portland", "Kent", "Othello", "Bainbridge"]
a.city = arrayCity[random.randrange(0,5)]

stateTemp = random.choice(a.STATE_CHOICES)
a.state = stateTemp[0]

a.zip = str(random.randrange(10000, 99999))

a.telephone_number = "(" + str(random.randrange(100,1000)) + ")" + str(random.randrange(100, 1000)) + "-" + str(random.randrange(1000,10000))

a.fax_number = "(" + str(random.randrange(100,1000)) + ")" + str(random.randrange(100, 1000)) + "-" + str(random.randrange(1000,10000))

dicOrgEmail={
'part1':['NorthWest','Achieving','AllianceFor','PeopleFor',],
'part2':['Change','Achievement','Action','Progress'],
}
f=open('syllables','w')
pickle.dump(dicOrgEmail,f)
f.close()
f1=open('syllables','r')
sd=pickle.load(f1)
f1.close()
first_part=sd['part1'][random.randint(0,len(sd['part1'])-1)]
second_part=sd['part2'][random.randint(0,len(sd['part2'])-1)]
a.email_address = first_part + second_part + "@gmail.com"

a.website = first_part + second_part + ".org"

statusTemp = random.choice(a.STATUS_CHOICES)
a.status = statusTemp[0]

a.ein = str(random.randrange(10,100)) + "-" + str(random.randrange(1000000,100000000))

a.founded = random.randrange(1800, 2013)

a.mission_statement = "Lorem ipsum dolor sit amet."

a.fiscal_org = str(random.randrange(1000000,10000000))

a.fiscal_person = str(random.randrange(1000000,10000000))

a.fiscal_telephone = "(" + str(random.randrange(100,1000)) + ")" + str(random.randrange(100, 1000)) + "-" + str(random.randrange(1000,10000))

a.fiscal_email = str(random.randrange(1000000,10000000)) + "@yahoo.com"

tempAddress = str(random.randrange(1000, 9999)) + " " + str(random.randrange(10, 99)) + "th ST "
tempCityStateZip = arrayCity[random.randrange(0,5)] + " " + random.choice(a.STATE_CHOICES)[0] + " " + str(random.randrange(10000, 99999))
a.fiscal_address =  tempAddress + tempCityStateZip

a.fiscal_letter = str(random.randrange(10,100))

a.fiscal_letterName = str(random.randrange(10,100))

a.fiscal_letter_type = str(random.randrange(0, 4))

a.save()






