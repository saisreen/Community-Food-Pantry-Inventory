"""Community food pantry inventory: Phase 1 data structure prototype."""
from dataclasses import dataclass
from datetime import date
import heapq


@dataclass
class FoodItem:
    item_id: str
    name: str
    category: str
    quantity: int
    expires: date


class PantryInventory:
    """Dictionary lookup, set-based category index, and expiration min-heap."""

    def __init__(self):
        self.items = {}           # item_id -> FoodItem; expected O(1) lookup
        self.categories = {}      # category -> set of item IDs
        self.expiry_heap = []     # (expiration, item_id); old entries are checked

    def add_item(self, item):
        if not isinstance(item, FoodItem):
            raise TypeError('Expected a FoodItem')
        if not item.item_id or not item.name or not item.category:
            raise ValueError('ID, name, and category are required')
        if item.quantity < 0:
            raise ValueError('Quantity cannot be negative')
        if item.item_id in self.items:
            raise ValueError('Duplicate item ID')
        self.items[item.item_id] = item
        self.categories.setdefault(item.category, set()).add(item.item_id)
        heapq.heappush(self.expiry_heap, (item.expires, item.item_id))

    def get_item(self, item_id):
        return self.items.get(item_id)

    def change_quantity(self, item_id, difference):
        item = self.items[item_id]
        if item.quantity + difference < 0:
            raise ValueError('Insufficient stock')
        item.quantity += difference
        return item.quantity

    def list_category(self, category):
        return [self.items[item_id] for item_id in sorted(self.categories.get(category, set()))]

    def change_expiration(self, item_id, new_date):
        item = self.items[item_id]
        item.expires = new_date
        heapq.heappush(self.expiry_heap, (new_date, item_id))

    def remove_item(self, item_id):
        item = self.items.pop(item_id)
        group = self.categories[item.category]
        group.remove(item_id)
        if not group:
            del self.categories[item.category]
        # Stale heap records are discarded when checking upcoming expirations.
        return item

    def next_expiring(self):
        while self.expiry_heap:
            expiry, item_id = self.expiry_heap[0]
            current = self.items.get(item_id)
            if current is None or current.expires != expiry:
                heapq.heappop(self.expiry_heap)
                continue
            return current
        return None


def demo():
    pantry = PantryInventory()
    pantry.add_item(FoodItem('F101', 'Rice', 'Grains', 25, date(2027, 5, 10)))
    pantry.add_item(FoodItem('F102', 'Milk', 'Dairy', 12, date(2026, 11, 8)))
    pantry.add_item(FoodItem('F103', 'Oats', 'Grains', 18, date(2027, 2, 3)))
    assert pantry.get_item('F101').name == 'Rice'
    assert len(pantry.list_category('Grains')) == 2
    assert pantry.change_quantity('F101', -5) == 20
    assert pantry.next_expiring().item_id == 'F102'
    pantry.change_expiration('F102', date(2027, 8, 1))
    assert pantry.next_expiring().item_id == 'F103'
    pantry.remove_item('F103')
    assert pantry.next_expiring().item_id == 'F101'
    try:
        pantry.change_quantity('F101', -100)
        raise AssertionError('Negative stock should fail')
    except ValueError:
        pass
    print('PASS: lookup, category search, stock update, expiration, removal, invalid stock')
    print('Remaining items:', [(x.item_id, x.quantity) for x in pantry.items.values()])


if __name__ == '__main__':
    demo()
