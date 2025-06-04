#简单工厂模式通过一个工厂类直接创建对象，但工厂类本身不继承任何接口。

# 定义抽象产品类
class Shape:
    def draw(self):
        pass

# 定义具体产品类
class Circle(Shape):
    def draw(self):
        print("Inside Circle::draw() method.")

class Square(Shape):
    def draw(self):
        print("Inside Square::draw() method.")

# 定义工厂类
class ShapeFactory:
    @staticmethod
    def get_shape(shape_type):
        if shape_type == "CIRCLE":
            return Circle()
        elif shape_type == "SQUARE":
            return Square()
        else:
            return None

# 客户端代码
if __name__ == "__main__":
    shape_factory = ShapeFactory()

    shape1 = shape_factory.get_shape("CIRCLE")
    shape1.draw()

    shape2 = shape_factory.get_shape("SQUARE")
    shape2.draw()
