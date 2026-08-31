class TreeNode:
    """二叉树节点"""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def preorder_recursive(root):
    """前序遍历（递归）：根 -> 左 -> 右"""
    result = []

    def dfs(node):
        if node is None:
            return
        result.append(node.val)      # 访问根节点
        dfs(node.left)               # 遍历左子树
        dfs(node.right)              # 遍历右子树

    dfs(root)
    return result


def preorder_iterative(root):
    """前序遍历（迭代）：使用栈实现 根 -> 左 -> 右"""
    if root is None:
        return []

    result = []
    stack = [root]

    while stack:
        node = stack.pop()
        result.append(node.val)      # 访问根节点
        # 先压右孩子，再压左孩子（栈是后进先出，保证左孩子先出栈）
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
    root.left = TreeNode(2, TreeNode(4), TreeNode(5))
    root.right = TreeNode(3, None, TreeNode(6))

    print("递归前序遍历:", preorder_recursive(root))
    print("迭代前序遍历:", preorder_iterative(root))
