from django.db import models

# Create your models here.
from dataclasses import dataclass, field, asdict
from itertools import count

_id_counter = count(1)

@dataclass
class Ticket:
    subject: str
    description: str = ""
    status: str = "open"
    id: int = field(default_factory=lambda: next(_id_counter))

    def to_dict(self):
        return asdict(self)


class TicketStore:
    def __init__(self):
        self._items = {}

    def all(self):
        return list(self._items.values())

    def get(self, ticket_id):
        return self._items.get(ticket_id)

    def add(self, ticket):
        self._items[ticket.id] = ticket
        return ticket

    def delete(self, ticket_id):
        return self._items.pop(ticket_id, None)

store = TicketStore()