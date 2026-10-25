"""
GreenLoop AI - SQLite Database Manager
Stores user-entered activities and computes record counts and gamification points.
"""

import os
import sqlite3
from datetime import datetime, timedelta
from contextlib import contextmanager

DB_PATH = os.environ.get(
    "GREENLOOP_DB_PATH",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "greenloop.db"),
)
DB_DIR = os.path.dirname(os.path.abspath(DB_PATH))

@contextmanager
def get_connection():
    """Yield a row-enabled SQLite connection and always close it."""
    db_path = os.path.abspath(DB_PATH)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path, timeout=10)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    """Initializes the database schema and performs safe, non-destructive schema migrations."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                item_name TEXT NOT NULL,
                project_name TEXT NOT NULL,
                image_path TEXT,
                notes TEXT,
                impact_points INTEGER DEFAULT 50,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Non-destructive migration for existing tables: add impact_points if missing
        cursor.execute("PRAGMA table_info(activities)")
        existing_cols = [row["name"] for row in cursor.fetchall()]
        if "impact_points" not in existing_cols:
            cursor.execute("ALTER TABLE activities ADD COLUMN impact_points INTEGER DEFAULT 50")
            cursor.execute("UPDATE activities SET impact_points = 50 WHERE impact_points IS NULL")

        conn.commit()

def is_duplicate_activity(category, item_name, project_name, window_seconds=300):
    """
    Prevents accidental duplicate submissions from awarding points twice.
    Returns True if an identical (category, item_name, project_name) was recorded
    within window_seconds (default 5 minutes).
    """
    if not item_name or not project_name:
        return False
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, created_at FROM activities
            WHERE LOWER(category) = LOWER(?)
              AND LOWER(TRIM(item_name)) = LOWER(TRIM(?))
              AND LOWER(TRIM(project_name)) = LOWER(TRIM(?))
            ORDER BY id DESC LIMIT 1
        """, (category.strip(), item_name.strip(), project_name.strip()))
        row = cursor.fetchone()
        if not row:
            return False

        created_str = row["created_at"]
        if not created_str:
            return False

        try:
            clean_time_str = str(created_str).split(".")[0]
            created_dt = datetime.strptime(clean_time_str, "%Y-%m-%d %H:%M:%S")
            diff = (datetime.now() - created_dt).total_seconds()
            if 0 <= diff <= window_seconds:
                return True
        except Exception:
            pass
        return False

def log_activity(category, item_name, project_name, image_path="", notes="", impact_points=50):
    """Inserts one activity with a validated positive gamification score."""
    pts = int(impact_points)
    if pts <= 0 or pts > 500:
        raise ValueError("Impact points must be between 1 and 500.")

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO activities (category, item_name, project_name, image_path, notes, impact_points, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (category, item_name, project_name, image_path, notes, pts, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        return cursor.lastrowid

def log_activity_once(category, item_name, project_name, image_path="", notes="", impact_points=50, window_seconds=300):
    """Atomically reject a recent duplicate and insert one valid activity."""
    pts = int(impact_points)
    if pts <= 0 or pts > 500:
        raise ValueError("Impact points must be between 1 and 500.")
    now = datetime.now()
    cutoff = (now - timedelta(seconds=window_seconds)).strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        conn.execute("BEGIN IMMEDIATE")
        duplicate = conn.execute("""
            SELECT 1 FROM activities
            WHERE LOWER(category)=LOWER(?)
              AND LOWER(TRIM(item_name))=LOWER(TRIM(?))
              AND LOWER(TRIM(project_name))=LOWER(TRIM(?))
              AND created_at >= ? LIMIT 1
        """, (category, item_name, project_name, cutoff)).fetchone()
        if duplicate:
            return None
        cursor = conn.execute("""
            INSERT INTO activities (category, item_name, project_name, image_path, notes, impact_points, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (category, item_name, project_name, image_path, notes, pts, now.strftime("%Y-%m-%d %H:%M:%S")))
        return cursor.lastrowid

def get_all_activities(limit=50):
    """Retrieves recorded activities in reverse chronological order."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, category, item_name, project_name, image_path, notes, COALESCE(impact_points, 50) AS impact_points, created_at
            FROM activities
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
        return [dict(row) for row in cursor.fetchall()]

def delete_activity(activity_id):
    """Deletes a specific activity record."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM activities WHERE id = ?", (activity_id,))
        conn.commit()
        return cursor.rowcount > 0

def get_sustainability_stats():
    """
    Computes saved-record totals, gamification points, and category breakdowns.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Total items
        cursor.execute("SELECT COUNT(*) AS total FROM activities")
        total_diverted = cursor.fetchone()["total"] or 0

        # Total points earned
        cursor.execute("SELECT SUM(COALESCE(impact_points, 50)) AS total_points FROM activities")
        total_points = cursor.fetchone()["total_points"] or 0
        
        # Breakdown by category (items)
        cursor.execute("""
            SELECT category, COUNT(*) AS count
            FROM activities
            GROUP BY category
            ORDER BY count DESC
        """)
        raw_counts = cursor.fetchall()
        
        category_counts = {
            "plastic": 0,
            "paper": 0,
            "glass": 0,
            "metal": 0,
            "organic": 0
        }
        for row in raw_counts:
            cat = (row["category"] or "").lower()
            if cat in category_counts:
                category_counts[cat] = row["count"]
            else:
                category_counts["other"] = category_counts.get("other", 0) + row["count"]

        # Breakdown by category (points)
        cursor.execute("""
            SELECT category, SUM(COALESCE(impact_points, 50)) AS points
            FROM activities
            GROUP BY category
        """)
        raw_points = cursor.fetchall()
        category_points = {
            "plastic": 0,
            "paper": 0,
            "glass": 0,
            "metal": 0,
            "organic": 0
        }
        for row in raw_points:
            cat = (row["category"] or "").lower()
            if cat in category_points:
                category_points[cat] = row["points"]
            else:
                category_points["other"] = category_points.get("other", 0) + (row["points"] or 0)

        # Category breakdown percentages
        category_percentages = {}
        for cat, cnt in category_counts.items():
            pct = round((cnt / total_diverted * 100), 1) if total_diverted > 0 else 0
            category_percentages[cat] = pct

        total_activities = total_diverted
        achievements = [
            {"name": "First Loop", "threshold": 1},
            {"name": "Reuse Regular", "threshold": 5},
            {"name": "Circular Champion", "threshold": 10},
        ]
        earned = [a["name"] for a in achievements if total_activities >= a["threshold"]]
        next_achievement = next((a for a in achievements if total_activities < a["threshold"]), None)
        return {
            "total_diverted": total_diverted,
            "total_activities": total_activities,
            "total_points": total_points,
            "category_counts": category_counts,
            "category_points": category_points,
            "category_percentages": category_percentages,
            "most_active_category": max(category_counts, key=category_counts.get) if total_diverted > 0 else "None yet",
            "achievements": earned,
            "next_achievement": next_achievement,
            "next_achievement_progress": min(100, round(total_activities / next_achievement["threshold"] * 100)) if next_achievement else 100
        }

