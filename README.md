# 🥗 MealPlanner

> ⚠️ This project is **Paused**  further development is not guaranteed


MealPlanner will combine **recipe management, nutritional overview, shopping list generation**, and **LLM-powered recipe modification** into one app.  
The long-term vision is to make it easy for households to plan meals together, manage grocery shopping, and adapt recipes to everyone’s needs.

<br/>

## 🌟 Planned Features
- 🧮 **Nutritional overview**: Built on Livsmedelsverket (Swedish Food Agency) nutritional database
- 🍲 **Recipe management**: Store, create, and adapt recipes
- 👨‍👩‍👧‍👦 **Family/household support**: Different diets, allergies, and member preferences
- 🛒 **Shopping lists**: Auto-generated from recipes & meal plans
- 🤖 **LLM integration**: AI-powered recipe generation and substitutions

<br/>

## 🛠️ Planned Tech Stack
- **Frontend**: Streamlit (prototype), future React/Lovable app
- **Backend**: FastAPI + Pydantic
- **Database**: DuckDB (local dev, cloud later)
- **Data Pipeline**: dlt (ingestion) + dbt (transformations)
- **ETL Flow**: Structured into `raw → staging → dim → fct`

<br/>

## 📂 Repository Structure
- `backend/` → FastAPI app (API, models, database access)
- `frontend/` → Streamlit prototype UI
- `ingestion/` → dlt ingestion pipelines (e.g., Livsmedelsverket API)
- `mealplanner_dbt/` → dbt transformations & models
- `data/` → Local DuckDB database (not version controlled)

<br/>

## 👩‍💻 Contributors

<a href="https://github.com/Remmold"><img src="https://avatars.githubusercontent.com/u/181938310?v=4" width="60px;" alt="Remmold"/></a>
<a href="https://github.com/vegetablecloud"><img src="https://avatars.githubusercontent.com/u/94803419?v=4" width="60px;" alt="Vegetablecloud"/></a>
<a href="https://github.com/wahdanz1"><img src="https://avatars.githubusercontent.com/u/97974748?v=4" width="60px;" alt="wahdanz1"/></a>
