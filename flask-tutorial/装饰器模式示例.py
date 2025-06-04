import time
import functools
'''
functools 是 Python 的标准库之一，主要用于操作和处理函数。
它提供了一系列工具，用于增强函数的功能、修改函数的行为或创建新的函数。
'''

# 1. 基础装饰器 - 打印函数执行时间
def timer_decorator(func):
    '''
    为什么需要两层函数：
    外层函数（timer_decorator）：
      接收被装饰的函数作为参数
      只执行一次（在定义时）
      返回内层函数
    内层函数（wrapper）：
      实现具体的装饰逻辑
      每次调用被装饰函数时都会执行
      可以访问外层函数的参数（闭包特性）
    '''
    @functools.wraps(func)  # 这行代码用于保留原函数的元信息，包括：函数名、文档字符串、参数列表等
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs) #用于调用传入的函数
        end_time = time.time()
        print(f"函数 {func.__name__} 执行时间: {end_time - start_time:.2f} 秒")
        return result
    return wrapper

# 2. 带参数的装饰器 - 重试机制
def retry_decorator(max_retries=3):
    '''
    为什么需要三层函数：
    第一层（retry_decorator）：接收装饰器的参数（如 max_retries）
    第二层（decorator）：接收被装饰的函数（func）
    第三层（wrapper）：实现具体的装饰逻辑
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == max_retries - 1:  # 最后一次重试
                        raise e
                    print(f"第 {i+1} 次尝试失败，正在重试...")
            return None
        return wrapper
    return decorator




# 使用装饰器的示例函数
@timer_decorator
def calculate_sum(n):
    """计算1到n的和"""
    return sum(range(1, n+1))

# 使用装饰器的示例函数
@retry_decorator(max_retries=3)
def risky_operation():
    """模拟可能失败的操作"""
    import random
    if random.random() < 0.7:  # 70%的概率失败
        raise Exception("操作失败")
    return "操作成功"



# 测试代码
if __name__ == "__main__":
    # 测试计时装饰器
    print("测试计时装饰器:")
    result = calculate_sum(10000000)
    print(f"计算结果: {result}\n")

    # 测试重试装饰器
    print("测试重试装饰器:")
    try:
        result = risky_operation()
        print(f"最终结果: {result}\n")
    except Exception as e:
        print(f"所有重试都失败了: {e}\n")

