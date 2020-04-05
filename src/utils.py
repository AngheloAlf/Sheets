def match_at(value: str, str_to_lookup: str, lookup_index: int=0) -> bool:
    return str_to_lookup[lookup_index:lookup_index+len(value)] == value
