import random


def quick_sort(arr):
    """快速排序（原地实现，随机基准，Lomuto 分区）

    参数:
        arr: 待排序的列表

    返回:
        排序后的列表（原列表会被修改）
    """
    def _sort(low, high):
        if low >= high:
            return
        pivot_index = _partition(low, high)
        _sort(low, pivot_index - 1)
        _sort(pivot_index + 1, high)

    def _partition(low, high):
        # 随机选基准并与最后一个元素交换，避免最坏情况 O(n^2)
        rand = random.randint(low, high)
        arr[rand], arr[high] = arr[high], arr[rand]

        pivot = arr[high]
        i = low  # i 指向小于基准区域的右边界
        for j in range(low, high):
            if arr[j] < pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
        # 将基准放到正确位置
        arr[i], arr[high] = arr[high], arr[i]
        return i

    if len(arr) <= 1:
        return arr
    _sort(0, len(arr) - 1)
    return arr


if __name__ == "__main__":
    # 测试用例
    test_cases = [
        [3, 6, 8, 10, 1, 2, 1],
        [5, 2, 9, 1, 7, 6, 3],
        [9, 8, 7, 6, 5, 4, 3, 2, 1],  # 逆序（最容易触发最坏情况）
        [1, 2, 3, 4, 5],              # 已有序
        [42],
        [],
        [7, 7, 7, 7, 7],
        [random.randint(0, 100) for _ in range(20)],  # 随机数组
    ]

    all_passed = True
    for case in test_cases:
        original = case.copy()
        sorted_case = quick_sort(case)
        passed = sorted_case == sorted(original)
        all_passed &= passed
        print(f"[{'PASS' if passed else 'FAIL'}] 原始: {original}")
        print(f"      排序: {sorted_case}")

    print("-" * 50)
    print("全部测试通过！" if all_passed else "存在失败用例！")
