 #input need from user
#total rent
#total food ordered
#electricity bill
#charge per unit
#nymber of person 


rent = int(input("enter your flat rent :"))
food = int(input("enter amount of food :"))
electricity_spend = int(input("enter the amount of electricy :"))
charje_per_unit = int(input("enter charje pper unit :"))
persons = int(input("number of person :"))

total_bill = electricity_spend * charje_per_unit

output = (rent + food + total_bill)

print ("each person will pay = ",output)

