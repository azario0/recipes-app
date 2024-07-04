import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

# Function to add a new recipe to the CSV file
def add_recipe(recipe_name, ingredients):
    file_exists = os.path.isfile('recipes.csv')
    with open('recipes.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Recipe', 'Ingredients'])  # Add header if file does not exist
        writer.writerow([recipe_name] + ingredients)

# Function to fetch recipes based on available ingredients
def fetch_recipes(available_ingredients):
    matched_recipes = []
    if os.path.exists('recipes.csv'):
        with open('recipes.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                recipe_name = row[0]
                recipe_ingredients = row[1:]
                if any(item in recipe_ingredients for item in available_ingredients):
                    matched_recipes.append(recipe_name)
    return matched_recipes

# Function to get all recipes
def get_all_recipes():
    recipes = []
    if os.path.exists('recipes.csv'):
        with open('recipes.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                recipe_name = row[0]
                recipe_ingredients = row[1:]
                recipes.append((recipe_name, recipe_ingredients))
    return recipes

# Function to update a recipe in the CSV file
def update_recipe(old_name, new_name, new_ingredients):
    recipes = get_all_recipes()
    with open('recipes.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Recipe', 'Ingredients'])  # Write header
        for recipe_name, ingredients in recipes:
            if recipe_name == old_name:
                writer.writerow([new_name] + new_ingredients)
            else:
                writer.writerow([recipe_name] + ingredients)

                
class RecipeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Recipe Recommendation App")
        self.geometry("600x500")
        
        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Title
        ttk.Label(self, text="Recipe Recommendation", font=("Helvetica", 16)).pack(pady=10)
        
        # Entry for available ingredients
        self.ingredients_entry = ttk.Entry(self, width=50)
        self.ingredients_entry.pack(pady=10)
        self.ingredients_entry.insert(0, "Enter ingredients separated by commas")
        
        # Button to fetch recipes
        ttk.Button(self, text="Fetch Recipes", command=self.fetch_recipes_action).pack(pady=10)
        
        # Button to add new recipe
        ttk.Button(self, text="Add New Recipe", command=self.new_recipe_window).pack(pady=10)
        
        # Button to view all recipes
        ttk.Button(self, text="View All Recipes", command=self.view_all_recipes_window).pack(pady=10)
        
        # Listbox to display matched recipes
        self.recipe_listbox = tk.Listbox(self, width=50, height=10)
        self.recipe_listbox.pack(pady=10)

    def fetch_recipes_action(self):
        ingredients = self.ingredients_entry.get().split(",")
        ingredients = [ingredient.strip().lower() for ingredient in ingredients]
        matched_recipes = fetch_recipes(ingredients)
        self.recipe_listbox.delete(0, tk.END)
        if matched_recipes:
            for recipe in matched_recipes:
                self.recipe_listbox.insert(tk.END, recipe)
        else:
            self.recipe_listbox.insert(tk.END, "No recipes found")

    def new_recipe_window(self):
        new_window = tk.Toplevel(self)
        new_window.title("Add New Recipe")
        new_window.geometry("400x300")
        
        # Recipe name entry
        ttk.Label(new_window, text="Recipe Name:").pack(pady=5)
        recipe_name_entry = ttk.Entry(new_window, width=40)
        recipe_name_entry.pack(pady=5)
        
        # Ingredients entry
        ttk.Label(new_window, text="Ingredients (comma separated):").pack(pady=5)
        ingredients_entry = ttk.Entry(new_window, width=40)
        ingredients_entry.pack(pady=5)
        
        # Save button
        ttk.Button(new_window, text="Save Recipe", command=lambda: self.save_recipe_action(new_window, recipe_name_entry, ingredients_entry)).pack(pady=20)
        
    def save_recipe_action(self, window, name_entry, ingredients_entry):
        recipe_name = name_entry.get()
        ingredients = ingredients_entry.get().split(",")
        ingredients = [ingredient.strip().lower() for ingredient in ingredients]
        if recipe_name and ingredients:
            add_recipe(recipe_name, ingredients)
            messagebox.showinfo("Success", "Recipe added successfully!")
            window.destroy()
        else:
            messagebox.showerror("Error", "Please enter a recipe name and ingredients.")
    
    def view_all_recipes_window(self):
        new_window = tk.Toplevel(self)
        new_window.title("All Recipes")
        new_window.geometry("600x400")
        
        recipes = get_all_recipes()
        for recipe_name, ingredients in recipes:
            frame = tk.Frame(new_window)
            frame.pack(pady=5, fill='x')
            
            # Recipe name entry
            name_entry = ttk.Entry(frame, width=20)
            name_entry.pack(side='left', padx=5)
            name_entry.insert(0, recipe_name)
            
            # Ingredients entry
            ingredients_entry = ttk.Entry(frame, width=40)
            ingredients_entry.pack(side='left', padx=5)
            ingredients_entry.insert(0, ", ".join(ingredients))
            
            # Update button
            ttk.Button(frame, text="Update", command=lambda n=name_entry, i=ingredients_entry, old_name=recipe_name: self.update_recipe_action(old_name, n, i)).pack(side='left', padx=5)
    
    def update_recipe_action(self, old_name, name_entry, ingredients_entry):
        new_name = name_entry.get()
        new_ingredients = ingredients_entry.get().split(",")
        new_ingredients = [ingredient.strip().lower() for ingredient in new_ingredients]
        if new_name and new_ingredients:
            update_recipe(old_name, new_name, new_ingredients)
            messagebox.showinfo("Success", "Recipe updated successfully!")
        else:
            messagebox.showerror("Error", "Please enter a recipe name and ingredients.")

if __name__ == "__main__":
    app = RecipeApp()
    app.mainloop()
