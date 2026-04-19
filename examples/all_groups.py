"""
List all groups available in the Akademiks API.
"""

from akademiks import fetch_groups

groups = fetch_groups()
print(f"{'ID':<25} Название")
print("-" * 50)
for g in sorted(groups, key=lambda x: x["id"]):
    print(f"{g['id']:<25} {g.get('title', '')}")
print(f"\nВсего: {len(groups)} групп")
