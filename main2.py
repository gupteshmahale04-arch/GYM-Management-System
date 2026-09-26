from pathlib import Path
import json
import random
import string
import datetime
import matplotlib.pyplot as plt
import seaborn  as sns
class GYM:
    database = "database.json"
    data = []

    # Load existing data if file exists
    if Path(database).exists():
        with open(database) as fs:
            data = json.loads(fs.read())

    @classmethod
    def __update(cls):
        with open(cls.database, "w") as fs:
            fs.write(json.dumps(cls.data, indent=4))

    @classmethod
    def __GYM_id(cls):
        alpha = random.choices(string.ascii_lowercase, k=2)
        num = random.choices(string.digits, k=4)
        GYM_id = alpha + num
        random.shuffle(GYM_id)
        return "".join(GYM_id)

    # ------------------- Account Creation -------------------
    def user_data(self):
        Name = input("Enter The Name >")
        Roll_No = "0156MG2610" + str(len(GYM.data) + 1)

        G_Mail = input("Enter G Mail id >")
        while "@" not in G_Mail:
            print("Reenter e_mail ")
            G_Mail = input("Enter G Mail id >")

        Mobile = input("Enter the Mobile Number >")
        while len(Mobile) != 10 or not Mobile.isdigit():
            print("Please reenter mobile no (must be 10 digits)")
            Mobile = input("Enter the Mobile Number >")

        Age = int(input("Enter The Age >"))
        if Age <= 16:
            print("You are not eligible for gym")
            return

        Weight = input("Enter The Weight (Kg) >")
        Height = input("Enter The Height (in Cm) >")
        Gender = input("Enter The Gender >")

        P_Contact = input("Enter the Parent's Mobile Number >")
        while len(P_Contact) != 10 or not P_Contact.isdigit():
            print("Parent contact must be 10 digits")
            P_Contact = input("Enter the Parent's Mobile Number >")

        Password = input("Enter the Password >")
        while len(Password) < 8:
            print("Password must be at least 8 characters")
            Password = input("Enter the Password >")

        GYM_id = GYM.__GYM_id()
        print("Your Roll No. is", Roll_No)
        print("Your GYM id is", GYM_id)

        user = {
            "Name": Name,
            "G_Mail": G_Mail,
            "Mobile": Mobile,
            "Age": Age,
            "Weight": Weight,
            "Height": Height,
            "Gender": Gender,
            "P_Contact": P_Contact,
            "GYM_id": GYM_id,
            "Roll_No": Roll_No,
            "Password": Password,
            "Step": [],
            "Exercises": [],
            "Diet": []
        }

        GYM.data.append(user)
        GYM.__update()

    # ------------------- View Profile -------------------
    def view_profile(self):
        Roll_No = input("Enter The Roll No >")
        Password = input("Enter the Password >")
        user_data = [i for i in GYM.data if i.get("Roll_No") == Roll_No and i.get("Password") == Password]

        if not user_data:
            print("You are not Member of Gym")
        else:
            for key, value in user_data[0].items():
                print(f"{key}: {value}")

    # ------------------- Daily Steps -------------------
    def daily_update(self):
        Roll_No = input("Enter The Roll No >")
        Password = input("Enter the Password >")
        user_data = [i for i in GYM.data if i.get("Roll_No") == Roll_No and i.get("Password") == Password]

        if not user_data:
            print("You are not Member of Gym")
            return

        day = int(input("Enter today's step count: >> "))
        user_data[0]["Step"].append({"date": datetime.date.today().isoformat(), "steps": day})
        GYM.__update()
        print("Steps updated successfully!")

        # Visualization
        steps = [entry["steps"] for entry in user_data[0]["Step"]]
        dates = [entry["date"] for entry in user_data[0]["Step"]]

        plt.figure(figsize=(8, 4))
        plt.plot(dates, steps, marker="o", linestyle="-", color="blue")
        plt.title(f"Step Progress for {user_data[0]['Name']}")
        plt.xlabel("Date")
        plt.ylabel("Steps")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    # ------------------- Exercise Tracking -------------------
    def add_exercise(self):
        Roll_No = input("Enter Roll No >")
        Password = input("Enter Password >")
        user_data = [i for i in GYM.data if i.get("Roll_No") == Roll_No and i.get("Password") == Password]

        if not user_data:
            print("You are not Member of Gym")
            return

        exercise = input("Enter exercise name > ")
        duration = int(input("Enter duration (minutes) > "))
        calories = int(input("Enter calories burned > "))

        user_data[0]["Exercises"].append({
            "date": datetime.date.today().isoformat(),
            "exercise": exercise,
            "duration": duration,
            "calories": calories
        })

        GYM.__update()
        print("Exercise added successfully!")

    # ------------------- Diet Tracking -------------------
    def add_diet(self):
        Roll_No = input("Enter Roll No >")
        Password = input("Enter Password >")
        user_data = [i for i in GYM.data if i.get("Roll_No") == Roll_No and i.get("Password") == Password]

        if not user_data:
            print("You are not Member of Gym")
            return

        meal = input("Enter meal name > ")
        calories = int(input("Enter calories > "))
        protein = int(input("Enter protein (g) > "))
        carbs = int(input("Enter carbs (g) > "))
        fat = int(input("Enter fat (g) > "))

        user_data[0]["Diet"].append({
            "date": datetime.date.today().isoformat(),
            "meal": meal,
            "calories": calories,
            "protein": protein,
            "carbs": carbs,
            "fat": fat
        })

        GYM.__update()
        print("Diet logged successfully!")

    # ------------------- Visualization -------------------
    # def visualize_progress(self):
    #     Roll_No = input("Enter Roll No >")
    #     Password = input("Enter Password >")
    #     user_data = [i for i in GYM.data if i.get("Roll_No") == Roll_No and i.get("Password") == Password]

    #     if not user_data:
    #         print("You are not Member of Gym")
    #         return

    #     steps = [s["steps"] for s in user_data[0].get("Step", [])]
    #     exercises = [e["calories"] for e in user_data[0].get("Exercises", [])]
    #     diet = [d["calories"] for d in user_data[0].get("Diet", [])]

    #     plt.figure(figsize=(10, 6))
    #     if steps: plt.boxplot(steps,bin=30, label="Steps")
    #     if exercises: plt.boxplot(exercises,bin=30, label="Calories Burned (Exercise)")
    #     if diet: plt.boxplot(diet,bin=30, label="Calories Consumed (Diet)")
    #     plt.legend()
    #     plt.title(f"Health Progress for {user_data[0]['Name']}")
    #     plt.show()

    def visualize_progress(self):
        
        Roll_No = input("Enter Roll No >")
        Password = input("Enter Password >")
        user_data = [i for i in GYM.data if i.get("Roll_No") == Roll_No and i.get("Password") == Password]

        if not user_data:
            print("You are not Member of Gym")
            return

        # Extract daily data
        steps = [s["steps"] for s in user_data[0].get("Step", [])]
        step_dates = [s["date"] for s in user_data[0].get("Step", [])]

        exercises = [e["calories"] for e in user_data[0].get("Exercises", [])]
        exercise_dates = [e["date"] for e in user_data[0].get("Exercises", [])]

        diet = [d["calories"] for d in user_data[0].get("Diet", [])]
        diet_dates = [d["date"] for d in user_data[0].get("Diet", [])]

        plt.figure(figsize=(12, 6))

        # Daily steps bar plot
        if steps:
            plt.bar(step_dates, steps, color="skyblue", label="Steps")

        # Daily exercise calories bar plot
        if exercises:
            plt.bar(exercise_dates, exercises, color="orange", label="Calories Burned (Exercise)")

        # Daily diet calories bar plot
        if diet:
            plt.bar(diet_dates, diet, color="green", label="Calories Consumed (Diet)")

        plt.xticks(rotation=45)
        plt.xlabel("Date")
        plt.ylabel("Count")
        plt.title(f"Daily Health Progress for {user_data[0]['Name']}")
        plt.legend()
        plt.tight_layout()
        plt.show()


# ------------------- Main Menu -------------------
gym = GYM()

while True:
    print("\n--- Gym Management System ---")
    print("1. Create Account")
    print("2. View Profile")
    print("3. Daily Steps Update")
    print("4. Add Exercise")
    print("5. Add Diet")
    print("6. Visualize Progress")
    print("0. Exit")

    n = int(input("Enter your choice >> "))
    if n == 1: gym.user_data()
    elif n == 2: gym.view_profile()
    elif n == 3: gym.daily_update()
    elif n == 4: gym.add_exercise()
    elif n == 5: gym.add_diet()
    elif n == 6: gym.visualize_progress()
    elif n == 0:
        print("Thank you! Stay fit 💪")
    else:
        print("Invalid choice, try again")
