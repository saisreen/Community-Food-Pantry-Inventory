# Community Food Pantry Inventory — Phase 1

This Python prototype demonstrates three complementary data structures for food pantry inventory: a dictionary for item ID lookup, sets for category membership, and a min-heap for expiration priority.

## Run

```bash
python pantry_inventory.py
```

The program uses Python 3 and no third-party packages. It prints a PASS message when the included demonstration assertions succeed.

## Supported operations

- Add an item and reject duplicate IDs or negative stock.
- Look up an item by its ID.
- Change inventory quantity without allowing negative stock.
- List the records belonging to one category.
- Change an expiration date and identify the next item expiring.
- Remove an item and keep the category index consistent.

## Limitations

The prototype is in-memory, single-process, and does not persist data. Expiration updates use lazy heap cleanup, so old heap entries may remain temporarily. Later phases can add benchmarking, persistence, and heap rebuilding.

## Project report

See `Phase1_Pantry_Inventory_Report.docx` for the design rationale, asymptotic analysis, pseudocode, limitations, and references.
