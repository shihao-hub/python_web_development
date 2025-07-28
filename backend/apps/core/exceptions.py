from typing import Annotated, Any, Type


class TypeCheckError(Exception):
    """类型检查出错"""

    def __init__(self, value: Any, expected_type: Type["object"]):
        super().__init__(f"期待 {expected_type} 类型，但是实际 {type(value)} 类型。")


class NotAllowedMethodError(Exception):
    """不允许调用的请求方法"""

    def __init__(self, method_name: str):
        super().__init__(f"不允许调用 {method_name} 方法。")
