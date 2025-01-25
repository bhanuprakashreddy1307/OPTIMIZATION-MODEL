from pulp import LpMinimize, LpProblem, LpVariable, lpSum

# Define the data: food items, cost, and nutrition values
foods = ['Chicken Breast', 'Eggs', 'Milk', 'Rice', 'Vegetables']

costs = {
    'Chicken Breast': 2.5,
    'Eggs': 0.5,
    'Milk': 1.0,
    'Rice': 0.8,
    'Vegetables': 0.6
}

nutrition = {
    'Calories': {
        'Chicken Breast': 165,
        'Eggs': 155,
        'Milk': 42,
        'Rice': 130,
        'Vegetables': 50
    },
    'Protein': {
        'Chicken Breast': 31,
        'Eggs': 13,
        'Milk': 3,
        'Rice': 2.7,
        'Vegetables': 2
    },
    'Fat': {
        'Chicken Breast': 3.6,
        'Eggs': 11,
        'Milk': 1,
        'Rice': 0.3,
        'Vegetables': 0.2
    },
    'Carbs': {
        'Chicken Breast': 0,
        'Eggs': 1.1,
        'Milk': 5,
        'Rice': 28,
        'Vegetables': 10
    }
}

# Nutritional requirements
requirements = {
    'Calories': 2000,
    'Protein': 100,
    'Fat': 70,
    'Carbs': 300
}

# Define the optimization problem
model = LpProblem("Diet Optimization", LpMinimize)

# Define decision variables: quantity of each food
food_vars = {food: LpVariable(food, lowBound=0, cat='Continuous') for food in foods}

# Objective Function: Minimize total cost
model += lpSum(costs[food] * food_vars[food] for food in foods), "Total Cost"

# Constraints: Meet the daily nutritional requirements
for nutrient, req in requirements.items():
    model += lpSum(nutrition[nutrient][food] * food_vars[food] for food in foods) >= req, f"Min_{nutrient}"

# Solve the optimization problem
model.solve()

# Display the results
print("Optimal Diet Plan:")
for food in foods:
    if food_vars[food].varValue > 0:
        print(f"{food}: {food_vars[food].varValue:.2f} units")

print(f"\nTotal Cost: ${model.objective.value():.2f}")
