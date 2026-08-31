"""
二叉树前序遍历（Preorder Traversal）
遍历顺序：根节点 -> 左子树 -> 右子树
"""


class TreeNode:
    """二叉树节点"""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def preorder_recursive(root):
    """递归实现前序遍历"""
    result = []

    def dfs(node):
        if node is None:
            return
        result.append(node.val)   # 先访问根节点
        dfs(node.left)            # 再遍历左子树
        dfs(node.right)           # 最后遍历右子树

    dfs(root)
    return result


def preorder_iterative(root):
    """迭代实现前序遍历（使用栈）"""
    if root is None:
        return []

    result = []
    stack = [root]

    while stack:
        node = stack.pop()
        result.append(node.val)

        # 栈是后进先出，所以先压右子树，再压左子树
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return result


if __name__ == "__main__":
    # 构建一棵测试二叉树：
    #        1
    #       / \
    #      2   3
    #     / \   \
    #    4   5   6
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.right = TreeNode(6)

    print("递归前序遍历:", preorder_recursive(root))
    print("迭代前序遍历:", preorder_iterative(root))

    # 边界测试
    print("空树递归结果:", preorder_recursive(None))
    print("空树迭代结果:", preorder_iterative(None))
