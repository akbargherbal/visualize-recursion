def remove_covered_optimized(intervals):
    """
    Remove intervals that are completely covered by other intervals.
    Optimized with sorting: O(n log n) time.

    Args:
        intervals: List of (start, end) tuples

    Returns:
        List of intervals with covered ones removed
    """
    # Sort by start time (ascending), then by end time (descending)
    # This ensures that if two intervals have the same start,
    # the longer one comes first
    sorted_intervals = sorted(intervals, key=lambda x: (x[0], -x[1]))

    def filter_covered(intervals, max_end_so_far):
        """
        Filter covered intervals recursively.

        Args:
            intervals: Remaining intervals to process (sorted)
            max_end_so_far: Maximum end time seen so far

        Returns:
            List of non-covered intervals
        """
        if not intervals:
            return []

        first = intervals[0]
        rest = intervals[1:]

        # If first's end is <= max_end_so_far, it's covered
        if first[1] <= max_end_so_far:
            # Skip this interval
            return filter_covered(rest, max_end_so_far)
        else:
            # Keep this interval and update max_end
            new_max_end = max(max_end_so_far, first[1])
            return [first] + filter_covered(rest, new_max_end)

    return filter_covered(sorted_intervals, float("-inf"))


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
