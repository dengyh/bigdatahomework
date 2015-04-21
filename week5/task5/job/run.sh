rm *.class *.jar
hadoop fs -rm -r stackoverflow/output/job
hadoop com.sun.tools.javac.Main BloomFilterJob.java
jar cf bf.jar BloomFilterJob*.class
hadoop jar bf.jar BloomFilterJob stackoverflow/input/job stackoverflow/output/job
