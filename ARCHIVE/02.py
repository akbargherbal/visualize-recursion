def remove_covered_optimized(intervals):
    """
    Remove intervals that are completely covered by other intervals.
    Optimized with sorting: O(n log n) time.

    Args:
        intervals: List of (start, end) tuples

    Returns:
        List of intervals with covered ones removed
    """
    print(f"\n{'='*60}")
    print(f"STARTING remove_covered_optimized")
    print(f"  Input intervals: {intervals}")
    
    # Sort by start time (ascending), then by end time (descending)
    # This ensures that if two intervals have the same start,
    # the longer one comes first
    sorted_intervals = sorted(intervals, key=lambda x: (x[0], -x[1]))
    print(f"  Sorted (start ASC, end DESC): {sorted_intervals}")
    print(f"  Sorting logic: Longer intervals with same start come first")
    print(f"{'='*60}\n")

    def filter_covered(intervals, max_end_so_far, depth=0):
        """
        Filter covered intervals recursively.

        Args:
            intervals: Remaining intervals to process (sorted)
            max_end_so_far: Maximum end time seen so far

        Returns:
            List of non-covered intervals
        """
        indent = "  " * depth
        print(f"{indent}[RECURSION DEPTH {depth}]")
        print(f"{indent}  Remaining intervals: {intervals}")
        print(f"{indent}  Max end seen so far: {max_end_so_far}")
        
        if not intervals:
            print(f"{indent}  -> BASE CASE: No more intervals to process")
            print(f"{indent}  -> Returning []")
            return []

        first = intervals[0]
        rest = intervals[1:]
        print(f"{indent}  Current interval: {first}")
        print(f"{indent}  Start: {first[0]}, End: {first[1]}")
        print(f"{indent}  Remaining after current: {rest}")

        # If first's end is <= max_end_so_far, it's covered
        if first[1] <= max_end_so_far:
            print(f"{indent}  -> COVERED: end ({first[1]}) <= max_end ({max_end_so_far})")
            print(f"{indent}  -> SKIPPING this interval (it's covered by a previous one)")
            print(f"{indent}  -> Continuing with max_end = {max_end_so_far}")
            return filter_covered(rest, max_end_so_far, depth + 1)
        else:
            print(f"{indent}  -> NOT COVERED: end ({first[1]}) > max_end ({max_end_so_far})")
            new_max_end = max(max_end_so_far, first[1])
            print(f"{indent}  -> KEEPING this interval")
            print(f"{indent}  -> Updating max_end: max({max_end_so_far}, {first[1]}) = {new_max_end}")
            print(f"{indent}  -> Adding {first} to result and recursing...")
            return [first] + filter_covered(rest, new_max_end, depth + 1)

    result = filter_covered(sorted_intervals, float('-inf'))
    print(f"\n{'='*60}")
    print(f"FINAL RESULT: {result}")
    print(f"Removed {len(intervals) - len(result)} covered interval(s)")
    print(f"{'='*60}\n")
    return result

# Test all cases
print("Test 1 - Original case:")
bookings = [(540, 660), (600, 720), (540, 720), (900, 960)]
print("Input:", bookings)
print("Output:", remove_covered_optimized(bookings))

print("\nTest 2 - Covering interval first:")
test1 = [(540, 720), (540, 660), (600, 720), (900, 960)]
print("Input:", test1)
print("Output:", remove_covered_optimized(test1))

print("\nTest 3 - Multiple covering relationships:")
test2 = [(540, 600), (540, 900), (600, 660), (780, 840)]
print("Input:", test2)
print("Output:", remove_covered_optimized(test2))

print("\nTest 4 - No covered intervals:")
test3 = [(540, 600), (660, 720), (780, 840)]
print("Input:", test3)
print("Output:", remove_covered_optimized(test3))

print("\nTest 5 - All covered by one:")
test4 = [(540, 1020), (600, 660), (720, 780), (900, 960)]
print("Input:", test4)
print("Output:", remove_covered_optimized(test4))