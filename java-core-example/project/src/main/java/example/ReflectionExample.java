package example;

import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class ReflectionExample {
    public static void main(String[] args) throws ClassNotFoundException, NoSuchMethodException, InvocationTargetException, IllegalAccessException, InstantiationException {

        // 方式一：forName()—— JVM 查找并加载指定的类，也就是说JVM会执行该类的静态代码段
        Class myClass = Class.forName("example.PeopleImpl");

        // 方式二：getClass()
//        Class myClass = new PeopleImpl().getClass();

        // 方式三：.class直接获取
//        Class myClass = PeopleImpl.class;

        // 调用普通方法
        Object object = myClass.newInstance();
        Method method = myClass.getDeclaredMethod("sayHi",String.class);
//        method.invoke(object,"老王");

        // 调用静态（static）方法
//        Method getSex = myClass.getMethod("getSex");
//        getSex.invoke(myClass);

        // 调用私有方法
//        Class myClass = Class.forName("example.PeopleImpl");
//        Object object = myClass.newInstance();
//        Method privSayHi = myClass.getDeclaredMethod("privSayHi");
//        privSayHi.setAccessible(true); // 修改访问限制
//        privSayHi.invoke(object);

        // 获取所有方法
//        for (Method method : myClass.getDeclaredMethods()) {
//            System.out.println(method);
//        }

//        // 获取所有字段
//        for (Field field : myClass.getDeclaredFields()) {
//            System.out.println(field);
//        }

        // Declared 获取当前类的变量或方法，private和public都可以获取到，但不能获取到父类任何信息
        // 非 Declared 的只能获取到 public 的变量或方法，并且可以获取到父类的


    }
}

interface People {
    int parentAge = 18;
    public void sayHi(String name);
}

class PeopleImpl implements People {
    private String privSex = "男";
    public String race = "汉族";
    @Override
    public void sayHi(String name) {
        System.out.println("hello," + name);
    }

    private void prvSayHi() {
        System.out.println("prvSayHi~");
    }
    public static void getSex() {
        System.out.println("18岁");
    }
}
