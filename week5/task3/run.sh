rm -rf *.class *.jar
hadoop com.sun.tools.javac.Main Purchases.java
jar cf purchases.jar Purchases*.class
hadoop jar purchases.jar Purchases purchases/input purchaese/output/week5/
