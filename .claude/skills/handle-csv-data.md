# Handle Fragrantica CSV Data

**When to apply:** Querying, filtering, normalizing, or extending the perfume dataset via `DataLoader`.

## Required Columns (validated on load, `src/data/loader.py:36`)
- `name` — normalized: lowercase + stripped
- `brand` — normalized: lowercase + stripped
- `id` — becomes the DataFrame index if present

## Columns used in tools and RAG (may vary by CSV version)
- `notes` — olfactory notes text; used in `search_perfumes` filter and RAG embeddings
- `season` — e.g. `"summer"`, `"winter"`, `"spring"`, `"fall"`, `"all-year"`
- `gender` — e.g. `"masculine"`, `"feminine"`, `"unisex"`
- `description` — free text; appended to RAG embedding input

## Filtering API (`src/data/loader.py:69`)
```python
# Scalar: exact match, case-insensitive
loader.filter_perfumes({"brand": "dior"})

# List: substring OR-match, case-insensitive (any item matches)
loader.filter_perfumes({"notes": ["citrus", "woody"]})

# Combined filters (AND logic between keys)
loader.filter_perfumes({
    "brand": "chanel",
    "notes": ["floral"],
    "season": "spring"
})
# Returns List[Dict[str, Any]]
```

## Full DataLoader API
```python
loader = DataLoader(csv_path=os.getenv("CSV_PATH"))

loader.get_all_perfumes()                     # List[Dict] — all rows, resets index
loader.get_perfume_by_id("dior-sauvage")      # Dict | None
loader.get_perfumes_by_ids(["id1", "id2"])    # List[Dict]
loader.filter_perfumes({"brand": "guerlain"}) # List[Dict]
```

## CSV normalization applied on load
1. `dropna(subset=['name', 'brand'])` — drops rows missing either required column
2. `drop_duplicates()` — removes exact duplicate rows
3. `name` and `brand` → `.str.strip().str.lower()`
4. `id` column → set as DataFrame index (lookup by `df.loc[id]`)

## Adding a new filterable column
1. Normalize it in `DataLoader.load_data()`:
```python
df['new_col'] = df['new_col'].str.strip().str.lower()
```
2. The generic loop in `filter_perfumes()` handles it automatically — no other changes needed.

## Don't
- Don't filter on columns not in the DataFrame — raises `KeyError`; check `loader.df.columns` first
- Don't mutate `self.df` directly after load — always work on `self.df.copy()`
- Don't expose raw DataFrames through API endpoints — always `.to_dict('records')`
- Don't assume `id` is always present — `get_perfume_by_id` checks `df.index` membership first
- [HUMAN APPROVAL REQUIRED] Never overwrite or delete the CSV source file
