def match_at(value, to_lookup, lookup_index: int=0) -> bool:
    return to_lookup[lookup_index:lookup_index+len(value)] == value

def remove_range(values_list: list, index: int, length: int) -> list:
    removed = []
    for i in range(length):
        removed.append(values_list[index])
        del values_list[index]
    return removed
