import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import com.sun.org.apache.bcel.internal.generic.ArrayInstruction;

public class Purchases {
	public static class TokenizerMapper extends Mapper<Object, Text, Text, DoubleWritable> {
		private DoubleWritable cost = new DoubleWritable(); 
		private Text store = new Text();
		
		public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
			String[] tokens = value.toString().split("\t");
			if (tokens[2].compareTo("Las Vegas") == 0 || tokens[2].compareTo("Arlington") == 0) {
				context.getCounter(tokens[2], "count").increment((int)(Double.valueOf(tokens[4]).doubleValue() * 100));
			}
		}
	}
	
	public static void main(String[] args) throws Exception {
		Configuration conf = new Configuration();
		Job job = Job.getInstance(conf, "purchases count");
		job.setJarByClass(Purchases.class);
		job.setMapperClass(TokenizerMapper.class);
		FileInputFormat.addInputPath(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));
		int code = job.waitForCompletion(true) ? 0 : 1;
		if (code == 0) {
			System.out.println(job.getCounters().findCounter("Las Vegas", "count").getValue() / 100.0);
			System.out.println(job.getCounters().findCounter("Arlington", "count").getValue() / 100.0);
		}
		System.exit(code);
	}
}
