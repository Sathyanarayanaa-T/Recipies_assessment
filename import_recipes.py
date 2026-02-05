#!/usr/bin/env python3
"""
Recipe Import Script
Imports recipe data from US_recipes_null.json into SQLite database.
Handles NaN values, validates data, and creates proper indexes.
"""

import json
import sqlite3
import math
import sys
from pathlib import Path


def create_database(db_path='recipes.db'):
    """Create SQLite database with proper schema and indexes."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create recipes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cuisine VARCHAR(255),
            title VARCHAR(500),
            rating REAL,
            prep_time INTEGER,
            cook_time INTEGER,
            total_time INTEGER,
            description TEXT,
            nutrients TEXT,
            serves VARCHAR(50)
        )
    ''')
    
    # Create indexes for performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_rating ON recipes(rating DESC)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_cuisine ON recipes(cuisine)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_total_time ON recipes(total_time)')
    
    conn.commit()
    return conn


def is_nan_value(value):
    """Check if a value is NaN (handles various representations)."""
    if value is None:
        return True
    if isinstance(value, float) and math.isnan(value):
        return True
    if isinstance(value, str) and value.lower() in ['nan', 'null', '']:
        return True
    return False


def clean_numeric_value(value):
    """Convert value to number or None if NaN."""
    if is_nan_value(value):
        return None
    try:
        # Try to convert to float first
        num = float(value)
        if math.isnan(num):
            return None
        # Return as int if it's a whole number
        if num.is_integer():
            return int(num)
        return num
    except (ValueError, TypeError):
        return None


def import_recipes(json_file_path, db_path='recipes.db'):
    """
    Import recipes from JSON file into SQLite database.
    
    Args:
        json_file_path: Path to the JSON file containing recipes
        db_path: Path to SQLite database file
    
    Returns:
        tuple: (success_count, error_count, errors_list)
    """
    # Read JSON file
    print(f"Reading JSON file: {json_file_path}")
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Found {len(data)} recipes to import")
    
    # Create/connect to database
    print(f"Creating database: {db_path}")
    conn = create_database(db_path)
    cursor = conn.cursor()
    
    # Clear existing data (optional - remove if you want to append)
    cursor.execute('DELETE FROM recipes')
    print("Cleared existing data")
    
    success_count = 0
    error_count = 0
    errors = []
    
    try:
        # Start transaction
        for recipe_id, recipe in data.items():
            try:
                # Extract and clean fields
                cuisine = recipe.get('cuisine')
                title = recipe.get('title')
                rating = clean_numeric_value(recipe.get('rating'))
                prep_time = clean_numeric_value(recipe.get('prep_time'))
                cook_time = clean_numeric_value(recipe.get('cook_time'))
                total_time = clean_numeric_value(recipe.get('total_time'))
                description = recipe.get('description')
                serves = recipe.get('serves')
                
                # Convert nutrients to JSON string
                nutrients = recipe.get('nutrients', {})
                if nutrients:
                    # Clean nutrients values
                    cleaned_nutrients = {}
                    for key, value in nutrients.items():
                        if not is_nan_value(value):
                            cleaned_nutrients[key] = value
                    nutrients_json = json.dumps(cleaned_nutrients)
                else:
                    nutrients_json = json.dumps({})
                
                # Insert into database
                cursor.execute('''
                    INSERT INTO recipes (
                        cuisine, title, rating, prep_time, cook_time,
                        total_time, description, nutrients, serves
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    cuisine, title, rating, prep_time, cook_time,
                    total_time, description, nutrients_json, serves
                ))
                
                success_count += 1
                
                # Progress indicator
                if success_count % 1000 == 0:
                    print(f"  Imported {success_count} recipes...")
                    
            except Exception as e:
                error_count += 1
                error_msg = f"Error importing recipe {recipe_id} ({recipe.get('title', 'Unknown')}): {str(e)}"
                errors.append(error_msg)
                if error_count <= 10:  # Only print first 10 errors
                    print(f"  ⚠️  {error_msg}")
        
        # Commit transaction
        conn.commit()
        print(f"\n✅ Import completed successfully!")
        print(f"   Total imported: {success_count}")
        print(f"   Errors: {error_count}")
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Import failed: {str(e)}")
        raise
    finally:
        conn.close()
    
    return success_count, error_count, errors


def verify_import(db_path='recipes.db'):
    """Verify the imported data."""
    print(f"\n🔍 Verifying import...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Count total recipes
    cursor.execute('SELECT COUNT(*) FROM recipes')
    total = cursor.fetchone()[0]
    print(f"   Total recipes in database: {total}")
    
    # Count recipes with rating
    cursor.execute('SELECT COUNT(*) FROM recipes WHERE rating IS NOT NULL')
    with_rating = cursor.fetchone()[0]
    print(f"   Recipes with rating: {with_rating}")
    
    # Count recipes with NULL rating
    cursor.execute('SELECT COUNT(*) FROM recipes WHERE rating IS NULL')
    null_rating = cursor.fetchone()[0]
    print(f"   Recipes with NULL rating: {null_rating}")
    
    # Check highest rated recipes
    cursor.execute('SELECT title, rating FROM recipes WHERE rating IS NOT NULL ORDER BY rating DESC LIMIT 5')
    top_recipes = cursor.fetchall()
    print(f"\n   Top 5 highest rated recipes:")
    for title, rating in top_recipes:
        print(f"      - {title}: {rating}")
    
    # Check cuisine distribution
    cursor.execute('SELECT cuisine, COUNT(*) as count FROM recipes GROUP BY cuisine ORDER BY count DESC LIMIT 5')
    cuisines = cursor.fetchall()
    print(f"\n   Top 5 cuisines:")
    for cuisine, count in cuisines:
        print(f"      - {cuisine}: {count} recipes")
    
    # Verify nutrients JSON
    cursor.execute('SELECT nutrients FROM recipes LIMIT 1')
    sample_nutrients = cursor.fetchone()[0]
    try:
        json.loads(sample_nutrients)
        print(f"\n   ✅ Nutrients JSON is valid")
    except:
        print(f"\n   ❌ Nutrients JSON is invalid")
    
    conn.close()
    print(f"\n✅ Verification complete!\n")


def main():
    """Main entry point."""
    json_file = 'US_recipes_null.json'
    db_file = 'recipes.db'
    
    # Check if JSON file exists
    if not Path(json_file).exists():
        print(f"❌ Error: {json_file} not found!")
        print(f"   Please make sure the file is in the current directory.")
        sys.exit(1)
    
    print("=" * 60)
    print("Recipe Import Script")
    print("=" * 60)
    
    # Import recipes
    success, errors, error_list = import_recipes(json_file, db_file)
    
    # Verify import
    verify_import(db_file)
    
    # Save errors to file if any
    if error_list:
        error_file = 'import_errors.log'
        with open(error_file, 'w') as f:
            for error in error_list:
                f.write(error + '\n')
        print(f"⚠️  Errors saved to {error_file}")
    
    print("=" * 60)
    print("Import complete! Database ready to use.")
    print("=" * 60)


if __name__ == '__main__':
    main()
