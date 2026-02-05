# Recipe Management System

A full-stack web application for browsing and searching 8,451+ recipes with advanced filtering, pagination, and detailed recipe information.

## 🚀 Tech Stack

### Frontend
- **React 18** - UI framework
- **Vite 7** - Build tool and dev server
- **Tailwind CSS 3** - Styling
- **JavaScript (ES6+)** - Programming language

### Backend
- **Flask 3.1** - Python web framework
- **Flask-CORS 5.0** - Cross-origin resource sharing
- **SQLite 3** - Database
- **Python 3.14** - Programming language

### Testing
- **Pytest 8.3** - API testing framework

---

## 📁 Project Structure

```
recipes_test/
├── frontend/               # React application
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API service layer
│   │   └── index.css      # Global styles
│   ├── package.json       # Frontend dependencies
│   └── vite.config.js     # Vite configuration
│
├── backend/               # Flask API
│   ├── app/
│   │   ├── main.py       # Flask app & routes
│   │   └── database/
│   │       └── queries.py # Database queries
│   ├── tests/            # API test suite
│   ├── recipes.db        # SQLite database
│   ├── requirements.txt  # Python dependencies
│   └── venv/            # Python virtual environment
│
├── data/
│   └── US_recipes_null.json  # Source data (8,451 recipes)
│
└── import_recipes.py     # Data import script
```

---

## 🔧 Setup & Installation

### Prerequisites
- **Node.js 18+**
- **Python 3.14+**
- **Git**

### 1. Clone Repository
```bash
git clone https://github.com/Sathyanarayanaa-T/Recipies_assessment.git
cd Recipies_assessment
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Backend Dependencies:**
```
Flask==3.1.0
Flask-CORS==5.0.0
pytest==8.3.4
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install
```

**Frontend Dependencies:**
```json
{
  "react": "^18.3.1",
  "react-dom": "^18.3.1",
  "tailwindcss": "^3.4.17",
  "vite": "^7.3.1"
}
```

---

## 🏃 Running the Application

### Start Backend API
```bash
cd backend
PYTHONPATH=$(pwd) ./venv/bin/python app/main.py
```
**API runs on:** `http://localhost:8001`

### Start Frontend
```bash
cd frontend
npm run dev
```
**Frontend runs on:** `http://localhost:5174`

### Access Application
Open your browser and navigate to: **http://localhost:5174**

---

## 🗃️ Database Setup

The SQLite database (`recipes.db`) is already populated with 8,451 recipes. If you need to reimport data:

```bash
# From project root
python3 import_recipes.py
```

**What it does:**
- Reads `US_recipes_null.json`
- Cleans and validates data
- Handles null values
- Creates indexes for performance
- Imports all recipes into SQLite

---

## 📡 API Endpoints

### GET `/api/recipes`
Get paginated recipes sorted by rating.

**Query Parameters:**
- `page` (default: 1) - Page number
- `limit` (default: 10, max: 100) - Results per page

**Example:**
```bash
curl "http://localhost:8001/api/recipes?page=1&limit=15"
```

**Response:**
```json
{
  "page": 1,
  "limit": 15,
  "total_recipes": 8451,
  "total_pages": 564,
  "recipes": [...]
}
```

### GET `/api/recipes/search`
Search and filter recipes.

**Query Parameters:**
- `title` - Recipe name (case-insensitive)
- `cuisine` - Cuisine type
- `rating` - Minimum rating (0-5)
- `total_time` - Maximum time in minutes
- `calories` - Maximum calories
- `page`, `limit` - Pagination

**Example:**
```bash
curl "http://localhost:8001/api/recipes/search?title=pie&cuisine=Italian&rating=4.5"
```

---

## 🧪 Testing

### Run API Tests
```bash
cd backend
PYTHONPATH=$(pwd) ./venv/bin/pytest tests/ -v
```

**Test Coverage:**
- ✅ 26 automated tests
- ✅ All endpoints tested
- ✅ Edge cases covered
- ✅ Null value handling
- ✅ CORS validation

**Test Results:**
```
======================== 26 passed in 0.14s =========================
```

See [`backend/tests/README.md`](backend/tests/README.md) for detailed test documentation.

---

## ✨ Features

### 🔍 Search & Filter
- **Recipe Name** - Search by title (case-insensitive)
- **Cuisine Type** - Filter by cuisine
- **Rating** - Minimum star rating
- **Cooking Time** - Maximum total time
- **Calories** - Maximum calorie count
- **Combined Filters** - Use multiple filters together

### 📄 Pagination
- Customizable results per page (15-100)
- Navigate through 564 pages
- Shows total recipe count
- Smooth page transitions

### 📊 Recipe Details
- Click any recipe to view full details
- Nutrition information
- Prep, cook, and total time
- Serving size
- Recipe description

### 🎨 UI/UX
- Responsive design (mobile, tablet, desktop)
- Loading states
- Error handling
- Empty state fallbacks
- Star rating display
- Smooth animations

---

## 🏗️ How It Works

### Data Flow

```
1. User opens browser
   ↓
2. React app loads (Vite dev server)
   ↓
3. User searches/filters recipes
   ↓
4. Frontend calls Flask API
   ↓
5. Flask queries SQLite database
   ↓
6. Database returns filtered results
   ↓
7. Flask sends JSON response
   ↓
8. React displays recipes
```

### Frontend Architecture

```
RecipesPage (Main)
├── SearchFilters (Filter form)
├── RecipeTable (Data grid)
│   └── RecipeRow (Individual rows)
│       └── StarRating (Rating display)
├── PaginationControls
└── RecipeDetailDrawer (Side panel)
```

### API Service Layer

```javascript
// frontend/src/services/api.js
export const fetchRecipes = async (filters, page, limit) => {
  // Decides between getRecipes() or searchRecipes()
  // Returns: { recipes, total_recipes, total_pages, page, limit }
}
```

### Backend Query Flow

```python
# app/main.py → Flask routes
# app/database/queries.py → SQL queries
# recipes.db → Data storage
```

---

## 🔑 Key Technologies Explained

### Why Vite?
- **Fast HMR** - Instant hot module replacement
- **ES modules** - Native browser module support
- **Optimized builds** - Faster than Create React App

### Why Flask?
- **Lightweight** - Minimal overhead
- **Flexible** - Easy to customize
- **Python 3.14 compatible** - Unlike FastAPI (Pydantic issues)

### Why SQLite?
- **Zero configuration** - No server setup
- **File-based** - Easy to share and backup
- **Sufficient for 8,451 records** - Fast queries with indexes

### Why Tailwind CSS?
- **Utility-first** - Rapid UI development
- **Consistent design** - Predefined spacing, colors
- **No CSS bloat** - Only used classes included

---

## 📦 Package Versions

### Frontend (`package.json`)
```json
{
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.3.4",
    "autoprefixer": "^10.4.20",
    "postcss": "^8.4.49",
    "tailwindcss": "^3.4.17",
    "vite": "^7.3.1"
  }
}
```

### Backend (`requirements.txt`)
```
Flask==3.1.0
Flask-CORS==5.0.0
pytest==8.3.4
```

---

## 🐛 Common Issues & Solutions

### Issue: Port 8001 already in use
**Solution:**
```bash
# Find process using port 8001
lsof -i :8001
# Kill the process
kill -9 <PID>
```

### Issue: Database not found
**Solution:**
```bash
# Ensure you're in backend directory
cd backend
ls recipes.db  # Should exist

# If missing, reimport data
cd ..
python3 import_recipes.py
```

### Issue: Frontend can't connect to API
**Solution:**
1. Check backend is running on port 8001
2. Verify `PYTHONPATH` is set correctly
3. Check CORS is enabled (Flask-CORS installed)

### Issue: npm install fails
**Solution:**
```bash
# Clear npm cache
npm cache clean --force
# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json
# Reinstall
npm install
```

---

## 📈 Performance

- **Database:** Indexed on `rating`, `cuisine`, `total_time`
- **Frontend:** Lazy loading, debounced search (500ms)
- **API:** Pagination limits max 100 results per page
- **Load Time:** <1 second for typical queries

---

## 🎯 Development Tips

### Frontend Development
```bash
# Hot reload enabled - changes reflect instantly
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Backend Development
```bash
# Flask debug mode enabled
# Changes auto-reload the server

# Run specific tests
PYTHONPATH=$(pwd) ./venv/bin/pytest tests/test_api_endpoints.py::TestGetRecipesEndpoint -v
```

### Adding New Features

**New API Endpoint:**
1. Add route in `backend/app/main.py`
2. Add query function in `backend/app/database/queries.py`
3. Write tests in `backend/tests/test_api_endpoints.py`

**New Frontend Component:**
1. Create component in `frontend/src/components/`
2. Import and use in pages
3. Follow existing patterns (props, styling)

---

## 📝 License

This project was created as an assessment project.

---

## 👤 Author

**Sathyanarayana T**
- GitHub: [@Sathyanarayanaa-T](https://github.com/Sathyanarayanaa-T)
- Repository: [Recipies_assessment](https://github.com/Sathyanarayanaa-T/Recipies_assessment)

---

## 📚 Additional Documentation

- [API Tests Documentation](backend/tests/README.md) - Detailed test suite guide
- [Data Import Script](import_recipes.py) - Database setup documentation

---

**Built with ❤️ using React, Flask, and Tailwind CSS**
