from __future__ import annotations


def paginate(query, page: int, size: int):
    offset = (page - 1) * size
    return query.limit(size).offset(offset)
