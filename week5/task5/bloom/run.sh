rm *.class *.jar
hadoop com.sun.tools.javac.Main BloomFilterMR.java
jar cf bf.jar BloomFilterMR.class
hadoop jar bf.jar BloomFilterMR stackoverflow/input/forum_users.tsv 10 0.1 stackoverflow/input/bloom.bin
